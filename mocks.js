
var document = {
  getElementById: function() { return { style: {}, classList: { toggle: function(){}, add: function(){}, remove: function(){} }, addEventListener: function(){} }; },
  documentElement: { clientWidth: 1000, clientHeight: 1000 },
  querySelectorAll: function() { return []; },
  body: { appendChild: function(){} },
  createElement: function() { return { style: {}, classList: { toggle: function(){}, add: function(){}, remove: function(){} }, appendChild: function(){}, setAttribute: function(){} }; }
};
var window = { addEventListener: function(){}, devicePixelRatio: 1, prompt: function(){}, confirm: function(){}, location: { reload: function(){} } };
var navigator = { userAgent: "mock", clipboard: { writeText: function(){} } };
var localStorage = { getItem: function(){ return null; }, setItem: function(){}, removeItem: function(){} };
var Math = globalThis.Math;
var Date = globalThis.Date;
var setTimeout = function(){};
var clearTimeout = function(){};
var requestAnimationFrame = function(cb) { };
var btoa = function() { return ""; };
var atob = function() { return ""; };
var decodeURIComponent = function() {};
var encodeURIComponent = function() {};

