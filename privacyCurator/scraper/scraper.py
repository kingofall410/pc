'''
Created on Jul 6, 2017

@author: Dan
'''
import requests
import re
from bs4 import BeautifulSoup
from api.models import BiasSetDefinition, BiasDefinition, Source
from django.db import connection

class Scraper:
    def __init__(self, domain, *args):
        self.domain = domain
        self.urlList = args
     
    @staticmethod
    def makeSoup(url):
        r = requests.get(url)
        
        if (r.status_code == 200):
            soup = BeautifulSoup(r.content, "html.parser")
            return soup
        else:
            print("Could not connect to "+url)           



class SourceScraper(Scraper):
    def getSites(self):
        pass
    
class AllSidesSourceScraper(Scraper):        
    
    def getSiteTagList(self, soup):
        return soup.find_all(href=re.compile("^/news-source/"))
    
    def getBiasTag(self, site):
        bias = site.find_next(href=re.compile("^/bias/"))
        return bias
    
    def getSourceUrl(self, site):
        sourcePageUrl = self.domain+site["href"][1:]
        littleSoup = Scraper.makeSoup(sourcePageUrl)       
        
        div = littleSoup.find("div", {"class" : "source-image"})
        sourceUrl = div.a["href"].strip()
        return sourceUrl     

    def getSourceDomain(self, url):
        
        root = re.match("https*://[^/]*/?", url)
        print("root", root)
        if (root):            
            lru = root.group(0)[::-1]
            print("lru", lru)
            m = re.match('/*\w*\.\w*', lru)           
            print("m", m)
            domain = m.group(0)[::-1] if m else ""
            print("domain", domain)
            if (domain.endswith("/")):
                domain = domain[:-1]
            
        ''' 
        header = re.match('https?://', url)
        print("header", header)
        trailer = re.match('/*', url[::-1])
        print("trailer", trailer)
        domain = url[header.end()+1:-trailer.end()]
        print("domain", header.end()+1, trailer.end(), domain)'''
        return domain
        
    
    def getSiteBiasDomain(self, maxNrSources=None):
        sites = []
        for url in self.urlList:
            bigSoup = Scraper.makeSoup(self.domain+url)
            if (bigSoup):
                sites.extend(self.getSiteTagList(bigSoup))
                
        sitebiasurl = [(site.text, 
                           self.getBiasTag(site)["href"], 
                           self.getSourceUrl(site)) for site in sites[:maxNrSources]]
        
        sbud = [(site, bias, url, self.getSourceDomain(url)) for (site, bias, url) in sitebiasurl]                     
        return sbud


class AllSidesSetDefinitionScraper(Scraper):
   
    NR_LEVELS = 5
    
    def parse(self):
        bsd, _ = BiasSetDefinition.objects.update_or_create(domain=self.domain,
                                                         defaults={"nrLevels" : self.NR_LEVELS},)
        BiasDefinition.objects.update_or_create(set=bsd, 
                                                level=-2,
                                                defaults={"textDesc" : "Left",
                                                          "levelLabel" : "L",
                                                          "tag" : "/bias/left"},)
        BiasDefinition.objects.update_or_create(set=bsd, 
                                                level=-1,
                                                defaults={"textDesc" : "Lean Left",
                                                          "levelLabel" : "LL",
                                                          "tag" : "/bias/left-center"},)
        BiasDefinition.objects.update_or_create(set=bsd, 
                                                level=0,
                                                defaults={"textDesc" : "Center",
                                                          "levelLabel" : "C",
                                                          "tag" : "/bias/center"},)
        BiasDefinition.objects.update_or_create(set=bsd, 
                                                level=1,
                                                defaults={"textDesc" : "Lean Right",
                                                          "levelLabel" : "LR",
                                                          "tag" : "/bias/right-center"},)
        BiasDefinition.objects.update_or_create(set=bsd, 
                                                level=2,
                                                defaults={"textDesc" : "Right",
                                                          "levelLabel" : "R",
                                                          "tag" : "/bias/right"},)
        return bsd.biases.all()
        
def saveSiteBiasDomain(biases, sbud):
    
    biasList = list(biases)

    for site, bias, url, domain in sbud:
        #must create before using many to many
        source, _ = Source.objects.update_or_create(url=url)
        source.sitename=site
        source.domain=domain
        
        if ("allsides" not in bias):
            b = next(b for b in biasList if b.tag == bias)
            source.bias.add(b)
        else:            
            source.bias.add(*biasList)
        
        source.save()
        
def load():
    
    setDefScraper = AllSidesSetDefinitionScraper("allsides.com")     
    biases = setDefScraper.parse()
    
    sourceScraper = AllSidesSourceScraper("https://www.allsides.com/", "bias/bias-ratings", 
                                          "bias/bias-ratings?field_news_source_type_tid=2&field_news_bias_nid=1&field_featured_bias_rating_value=All&title=&page=1",
                                          "bias/bias-ratings?field_news_source_type_tid=2&field_news_bias_nid=1&field_featured_bias_rating_value=All&title=&page=2")
    sbud = sourceScraper.getSiteBiasDomain()
    
    saveSiteBiasDomain(biases, sbud)

    