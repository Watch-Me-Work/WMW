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
var textToSend = null

window.addEventListener("message", function(e){
	textToSend = {"document_html": e.data};
	summarize()
}, false);

function summarize() {
	// todo: maybe pass the text into the function instead of having it as a global?
	fetch(api_url, {
		method: 'POST',
		body: JSON.stringify(textToSend),
		headers:{
		  'Content-Type': 'application/json'
		} })
	  .then(data => { 
	  		data.json().then(jsonData => {
	  			console.log(jsonData)
	  			updateResultSidebar(jsonData['results'])
	  		})	
		  })
	  .then(res => { 
		  console.log(res)
	   })
	  .catch(error => console.error('Error:', error));
}

// todo: move to sidebar.js
function updateResultSidebar(resultsData) {
	let resultsList = makeResultList(resultsData)
	console.log(document.getElementById('resultsList'))
	document.getElementById('resultsList').innerHTML = resultsList;
	// document.getElementById('resultsList').text = resultsList;

}


function makeResultList(results) {
    // Create the list element:
    let mainDiv = document.createElement('div');

    let divHtml = '';
    console.log(results)
    for (let result of results) {
    	const pageLink = 'https:'
    	const pageTitle = result.title

    	// hacky but cbf to implement bootstrap elements manually
    	const newDivContent = `
    	        <div class="list-group-item list-group-item-action" id="result-item">
                <div class="d-flex w-100 justify-content-between">
                  <h5 class="mb-1">${pageTitle}</h5>
                  <small>Match Score?</small>
                </div>
                <p class="mb-1">A short description about the article/content of the page.</p>
                <a href="${pageLink}" target="_blank"><button type="button" class="btn btn-info btn-lg btn-block">Go to ${pageTitle.slice(0, 30)}</button></a>
              </div>

        `
        divHtml += newDivContent
    }

    mainDiv.innerHtml = divHtml;

    // Finally, return the constructed list:
    return divHtml;
}

document.getElementById('searchButton').addEventListener('click', summarize);


},{"node-fetch":1}]},{},[2]);
