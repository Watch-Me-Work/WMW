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
	console.log('data is')
	console.log(e.data)
	textToSend = {"document_html": e.data};
	summarize()
    
}, false);

function summarize() {
	fetch(api_url, {
		method: 'POST',
		body: JSON.stringify(textToSend),
		headers:{
		  'Content-Type': 'application/json'
		} })
	  .then(data => { 
	  		data.json().then(jsonData => {
	  			console.log('got a data response')
	  			console.log(jsonData)
	  		})	
		  })
	  .then(res => { 
		  console.log(res)
	   })
	  .catch(error => console.error('Error:', error));
}

document.getElementById('searchButton').addEventListener('click', summarize);


},{"node-fetch":1}]},{},[2]);
