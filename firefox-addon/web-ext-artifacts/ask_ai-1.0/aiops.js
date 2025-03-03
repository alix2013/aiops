//Description: 
//  AIOps main code for chrome extension, created by An Lixue
//

// AISERVER_URL="http://localhost:5001"
// DEFAULT_AISERVER_URL="http://aiserver:5001"
DEFAULT_AISERVER_URL="http://aiserver:5001"
DEFAULT_CHATSERVER_URL="http://aiserver:5006"

function getStorage(key) {
    return new Promise((resolve, reject) => {
      browser.storage.sync.get(key, (result) => {
          if (browser.runtime.lastError) {
              reject(browser.runtime.lastError);
          } else {
              resolve(result[key]);
          }
      });
    });
}

browser.runtime.onInstalled.addListener(function() {
  browser.storage.sync.set({"AISERVER_URL": DEFAULT_AISERVER_URL,"CHATSERVER_URL": DEFAULT_CHATSERVER_URL}, function() {
    console.log('The key have been saved.', DEFAULT_AISERVER_URL);
  });
});

//addListener for context menu
browser.runtime.onInstalled.addListener(function() {
  browser.contextMenus.create({
    "id": "askai4pd",
    "title": "Ask AI for troubleshooting",
    "contexts": ["selection"]
  });

  browser.contextMenus.create({
    "id": "askai",
    "title": "Ask AI",
    "contexts": ["selection"]
  });

  var menuItem = {
    "id": "askai4sum",
    "title": "Ask AI to summarize text",
    "contexts": ["selection"]
  };
  browser.contextMenus.create(menuItem);

  browser.contextMenus.create({
    title: "Ask more",
    contexts: ["selection"],
    id: "askMoreContextMenu"
  });


});

// ask  without prompt
async function askai(inputText) {
  // var url = "http://aiserver:5001/ask"
  // url = AISERVER_URL+"/ask"
  var url = await getStorage("AISERVER_URL") 
  if (!url) url = DEFAULT_AISERVER_URL
  url = url +"/ask"
  console.log("url:",url);
  console.log("input",inputText)
  var reqbody = JSON.stringify({
     request: inputText
  })
  console.log("reqbody", reqbody)
  try {
    const response = await fetch(url,
      { 
        method: 'POST',
        body: reqbody,
        headers: {
          'Content-Type': 'application/json',
        }
      });
    console.log("response", response)
    const data = await response.json();
    return data.response
    
  } catch (error) {
    console.log(error);
    return error+",please contact system adminstrator";
  }
}

// askai for troubleshooting
async function askai4pd(inputText) {
  // var url = AISERVER_URL + "/ask4pd"
  var url = await getStorage("AISERVER_URL") 
  if (!url) url = DEFAULT_AISERVER_URL
  url = url + "/ask4pd"
  console.log("url:",url);
  console.log("input",inputText)
  var reqbody = JSON.stringify({
     request: inputText
  })
  console.log("reqbody", reqbody)
  try {
    const response = await fetch(url,
      { 
        method: 'POST',
        body: reqbody,
        headers: {
          'Content-Type': 'application/json',
        }
      });
    console.log("response", response)
    const data = await response.json();
    return data.response
    
  } catch (error) {
    console.log(error);
    return error+",please contact system adminstrator";

  }
}

// askai for summary text
async function askai4sum(inputText) {
  // var url = AISERVER_URL + "/ask4pd"
  var url = await getStorage("AISERVER_URL") 
  if (!url) url = DEFAULT_AISERVER_URL
  url = url + "/sum"
  console.log("url:",url);
  console.log("input",inputText)
  var reqbody = JSON.stringify({
     request: inputText
  })
  console.log("reqbody", reqbody)
  try {
    const response = await fetch(url,
      { 
        method: 'POST',
        body: reqbody,
        headers: {
          'Content-Type': 'application/json',
        }
      });
    console.log("response", response)
    const data = await response.json();
    return data.response
    
  } catch (error) {
    console.log(error);
    return error+",please contact system adminstrator";
  }
}
//addListener for askai
// browser.contextMenus.onClicked.addListener( async function(info) {
browser.contextMenus.onClicked.addListener( async function(info,tab) {
  if (info.menuItemId === "askai") {
    var response = await askai(info.selectionText)
    console.log("response---", response)
    browser.tabs.sendMessage(tab.id, { action: "showInformation", selectedText: response });
  //   let left = screen.width - 600
  //   let top = 0
  //   var popup = window.open("popup.html", "", 'width=600,height=400,left=' + left + ',top=' + top); 
  //   popup.response = response
  //   popup.onblur = function() {
  //     popup.close();
  //   }
  }
});

//addListener for troubleshooting
browser.contextMenus.onClicked.addListener( async function(info,tab ) {
  if (info.menuItemId === "askai4pd") {
    var response = await askai4pd(info.selectionText)
    console.log("response4pd", response)
    browser.tabs.sendMessage(tab.id, { action: "showInformation", selectedText: response });
    // let left = screen.width - 600 
    // let top = 0
    // var popup = window.open("popup.html", "", 'width=600,height=400,left=' + left + ',top=' + top); 
    // popup.response = response
  }
});

//addListener for summarize
browser.contextMenus.onClicked.addListener( async function(info,tab ) {
  if (info.menuItemId === "askai4sum") {
    var response = await askai4sum(info.selectionText)
    console.log("response summary:", response)
    browser.tabs.sendMessage(tab.id, { action: "showInformation", selectedText: response });
    // let left = screen.width - 600 
    // let top = 0
    // var popup = window.open("popup.html", "", 'width=600,height=400,left=' + left + ',top=' + top); 
    // popup.response = response
  }
});

browser.contextMenus.onClicked.addListener(async function (info, tab) {
  if (info.menuItemId === "askMoreContextMenu") {
    var response = await askai4sum(info.selectionText)
    console.log("response summary:", response)
    // browser.tabs.sendMessage(tab.id, { action: "showInformation", selectedText: info.selectionText });
    browser.tabs.sendMessage(tab.id, { action: "showInformation", selectedText: response });
  }
});

// browser.runtime.onMessage.addListener(function (message) {
//   if (message.action === "copyToClipboard") {
//     copyToClipboard(message.text);
//   }
// });

// function copyToClipboard(text) {
//   console.log("copyToClipboard called")
//   // Create a temporary textarea element to copy text to clipboard
//   const textarea = document.createElement("textarea");
//   textarea.value = text;
//   document.body.appendChild(textarea);
//   textarea.select();
//   document.execCommand("copy");
//   document.body.removeChild(textarea);
// }


browser.contextMenus.create({
  id: "open-options",
  title: "Extension Options",
  contexts: ["browser_action"],
});

browser.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "open-options") {
    browser.runtime.openOptionsPage();
  }
});

