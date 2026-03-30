import re
import subprocess

with open('index.html', 'r') as f:
    js = re.search(r'<script>([\s\S]*?)</script>', f.read(), re.DOTALL).group(1)

mock_js = """
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
var console = { log: print, error: print };
"""

with open('test_mock.js', 'w') as f:
    f.write(mock_js + "\n" + js)

res = subprocess.run(['/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Resources/jsc', 'test_mock.js'], capture_output=True, text=True)
print("OUT:", res.stdout)
print("ERR:", res.stderr)
