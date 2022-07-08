---
layout: post
title: How to enable colab for longer runtimes by keeping it active
date: 2022-07-08
---


This [post](https://stackoverflow.com/questions/54057011/google-colab-session-timeout) is of help:

**Steps:**

1. Open the inspector view by typing Ctrl+ Shift + i and then clicking on console tab at top.
2. Paste the below code snippet at bottom of console and hit enter

```
function ClickConnect(){
console.log("Working"); 
document.querySelector("#top-toolbar > colab-connect-button").shadowRoot.querySelector("#connect").click();
}
setInterval(ClickConnect,60000)
```

Above code would keep on clicking the page and prevent it from disconnecting.

