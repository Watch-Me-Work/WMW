(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
(function (global){
"use strict";

// ref: https://github.com/tc39/proposal-global
var getGlobal = function () {
	// the only reliable means to get the global object is
	// `Function('return this')()`
	// However, this causes CSP violations in Chrome apps.
	if (typeof self !== 'undefined') { return self; }
	if (typeof window !== 'undefined') { return window; }
	if (typeof global !== 'undefined') { return global; }
	throw new Error('unable to locate global object');
}

var global = getGlobal();

module.exports = exports = global.fetch;

// Needed for TypeScript and Webpack.
exports.default = global.fetch.bind(global);

exports.Headers = global.Headers;
exports.Request = global.Request;
exports.Response = global.Response;
}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
},{}],2:[function(require,module,exports){

const fetch = require("node-fetch");
const api_url = 'http://localhost:3380/find_related';

var last_results = null;
window.addEventListener('load', (e) => {
    let topic_switch = document.getElementById('showTopicSwitch');
    if ('topic_checked' in localStorage) {
        topic_switch.checked = JSON.parse(localStorage['topic_checked']);
    }
    if (topic_switch !== null) {
        topic_switch.addEventListener('change', (e) => {
            localStorage['topic_checked'] = JSON.stringify(e.target.checked);
            updateResultSidebar(last_results);
        })
    }

    let ner_switch = document.getElementById('showNerSwitch');
    if ('ner_checked' in localStorage) {
        ner_switch.checked = JSON.parse(localStorage['ner_checked']);
    }
    if (ner_switch !== null) {
        ner_switch.addEventListener('change', (e) => {
            localStorage['ner_checked'] = JSON.stringify(e.target.checked);
            updateResultSidebar(last_results);
        })
    }
});

window.addEventListener("message", function(e){
	console.log(e)
	if (e.data.window_message !== "summarizeTab") { return }
	// get url off active tab, call summarize
	chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
    	textBody = {
			"document_html": e.data.txt,
			"url": tabs[0].url
		};
		summarize(textBody)
	});
}, false);

function summarize(textBody) {
	console.log(textBody)
	const htmlTagCheck = textBody.document_html.slice(0, 30);
	if (!htmlTagCheck.includes('html')){
		return;
	} else {
		// todo: maybe pass the text into the function instead of having it as a global?
		fetch(api_url, {
			method: 'POST',
			body: JSON.stringify(textBody),
			headers:{
			  'Content-Type': 'application/json'
			} })
		  .then(data => { 
		  		data.json().then(jsonData => {
		  			updateResultSidebar(jsonData['results'])
                    last_results = jsonData['results'];
		  		})	
			  })
		  .then(res => { 
			  console.log(res)
		   })
		  .catch(error => console.error('Error:', error));
	}
}

// todo: move to sidebar.js
function updateResultSidebar(resultsData) {
    if (resultsData === null) {
        return;
    }
	let resultsList = makeResultList(resultsData);
	document.getElementById('resultsList').innerHTML = resultsList;
	// document.getElementById('resultsList').text = resultsList;

}


function makeResultList(results) {
    // Create the list element:
    let mainDiv = document.createElement('div');

    let divHtml = '';
    if (results.length === 0) {
        divHtml = '<p>No results were found for this page</p>';
    }
    for (let result of results) {
    	const pageLink = result.url
    	const pageTitle = result.title
        let pageSnippet = result.snippet;
        let source_html = '';

        if ('source' in result) {
            let pretty_name = 'Unknown'
            let checkbox = null;
            if (result.source === 'topic') {
                checkbox = document.getElementById('showTopicSwitch');
                pretty_name = 'Topic';
            } else if (result.source === 'ner') {
                checkbox = document.getElementById('showNerSwitch');
                pretty_name = 'Entity';
            }

            if (!(checkbox === null || checkbox.checked)) {
                // Skip and don't display the result
                continue;
            }

            
            source_html = `<small>Recommended because: ${pretty_name}</small>`
        }

        if (pageSnippet === null) {
            pageSnippet = '';
        }

        pageSnippet += '...';


    	// hacky but cbf to implement bootstrap elements manually
    	const newDivContent = `
                
    	        <div class="list-group-item list-group-item-action" id="result-item">
                <div class="d-flex w-100 justify-content-between">
                  <a href="${result.url}" target="_blank"><h5 class="mb-1">${result.title}</h5></a>
                  ${source_html}
                </div>
                <p class="mb-1">${pageSnippet}</p>
              </div>

        `
        divHtml += newDivContent
    }

    mainDiv.innerHtml = divHtml;

    // Finally, return the constructed list:
    return divHtml;
}

// todo: add search button again! figure out how functions will be passed in
// maybe emit event as "message"
// document.getElementById('searchButton').addEventListener('click', function() {
// 		window.postMessage(window.documentElement.outerHTML)
// 	    // chrome.tabs.sendMessage(tab.id, "message");
// });


},{"node-fetch":1}]},{},[2]);
