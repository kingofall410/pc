//called when the user opens a new tab or loads a new page in a tab
chrome.tabs.onUpdated.addListener( function (tabId, changeInfo, tab) {
  if (changeInfo.status == 'complete' && tab.active) {
    //switchPage(tab.url);
	  onPageSwitch(tab.url);
  }
})

//called when a user switches into an inactive tab
chrome.tabs.onActivated.addListener( function (activeInfo) {
  chrome.tabs.get(activeInfo.tabId, function(tab) {
	  onPageSwitch(tab.url);
  })

})

//need a chrome.window.onFocusChanged here to check if the user has multiple windows open and track only the active window 
//https://developer.chrome.com/extensions/windows#event-onFocusChanged
//also need to add onmousemove and on page scroll


const coreapi = window.coreapi;
const schema = window.schema;

var client = new coreapi.Client();
var currentDomain = "";
var startTime;

function onPageSwitch(url) {
	//log stop time immediately
	stopTime = new Date();
	
	if (currentDomain != "") {
		//send previous viewing data
		duration = (stopTime-startTime)/1000;
		logPageSwitch(currentDomain, startTime, duration);	
	}
	
	//update globals
	startTime = stopTime;
	currentDomain = getDomain(url);
}

function logPageSwitch(domain, startTime, duration) {

	let action = ["visits", "create"];
	let params = {domain: domain, startTime: startTime.toJSON(), duration: duration};
	client.action(schema, action, params).then(function(result) {
	    console.log(result);
	})
}

function getDomain(url) {
  let startIndex;
  if (url.startsWith("http://")) {
    startIndex = 7;
  } else {
    startIndex = 8;
  }
  let noproto = url.slice(startIndex, url.length+1);
  let domain = noproto.slice(0, noproto.indexOf("/"));
  return domain;
}
