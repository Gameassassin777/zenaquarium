const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const match = html.match(/<script>([\s\S]*?)<\/script>/);
const jsCode = match[1];

const { JSDOM } = require('jsdom');
const dom = new JSDOM(html, { runScripts: "dangerously", resources: "usable" });

dom.window.addEventListener('error', event => {
  console.error('JS Error:', event.error);
});

setTimeout(() => {
  console.log("Simulating loop manually...");
  if (dom.window.loop) {
    try {
      dom.window.loop();
      console.log("Loop ran successfully.");
    } catch(e) {
      console.error("Loop crashed:", e);
    }
  } else {
    console.log("Loop function not found!");
  }
}, 500);
