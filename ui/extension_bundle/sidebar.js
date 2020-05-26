// close button message sender code
document.getElementById("closeButton").onclick = function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
		  chrome.tabs.sendMessage(tabs[0].id, "toggle");
	});
}

