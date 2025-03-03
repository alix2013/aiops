//Description: 
//  AIOps main code for chrome extension, created by An Lixue
//

// AISERVER_URL="http://localhost:5001"
// DEFAULT_AISERVER_URL="http://aiserver:5001"
DEFAULT_AISERVER_URL="http://aiserver:5001"
DEFAULT_CHATSERVER_URL="http://aiserver:5006"

function getStorage(key) {
    return new Promise((resolve, reject) => {
      chrome.storage.sync.get(key, (result) => {
          if (chrome.runtime.lastError) {
              reject(chrome.runtime.lastError);
          } else {
              resolve(result[key]);
          }
      });
    });
}

chrome.runtime.onInstalled.addListener(function() {
  chrome.storage.sync.set({"AISERVER_URL": DEFAULT_AISERVER_URL,"CHATSERVER_URL": DEFAULT_CHATSERVER_URL}, function() {
    console.log('The key have been saved.', DEFAULT_AISERVER_URL);
  });
});

//addListener for context menu
chrome.runtime.onInstalled.addListener(function() {
  chrome.contextMenus.create({
    "id": "askai4pd",
    "title": "Ask AI for troubleshooting",
    "contexts": ["selection"]
  });

  chrome.contextMenus.create({
    "id": "askai",
    "title": "Ask AI in Knowledge Base",
    "contexts": ["selection"]
  });

  chrome.contextMenus.create({
    "id": "askai4any",
    "title": "Ask AI any",
    "contexts": ["selection"]
  });


  var menuItem = {
    "id": "askai4sum",
    "title": "Ask AI for summary",
    "contexts": ["selection"]
  };
  chrome.contextMenus.create(menuItem);

  chrome.contextMenus.create({
    title: "Ask AI for translation",
    contexts: ["selection"],
    id: "askai4translate"
  });

  chrome.contextMenus.create({
    title: "Ask AI for translation in stream way",
    contexts: ["selection"],
    id: "askai4translatestream"
  });

});


async function restAPI(url,method, body) {
    try {
    const response = await fetch(url,
      { 
        method: method,
        body: body,
        headers: {
          'Content-Type': 'application/json',
        }
      });
    console.log(url, "response", response)
    const data = await response.json();
    return data.response
    
  } catch (error) {
    console.log(error);
    return error+",please contact system adminstrator";
  }

} 

async function restAPI_stream(url,method, body, callback) {
    try {
    const response = await fetch(url,
      { 
        method: method,
        body: body,
        headers: {
          'Content-Type': 'application/json',
        }
      });

    // var source = new EventSource(response.url);

    // source.onmessage = function(event) {
    //     var data = JSON.parse(event.data);
    //     callback(data);
    // };

    const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
    // let result;
    // while (result = await reader.read()) {
    //     if (result.done) break;
    //     let value = result.value;
    //     console.log("readed value from stream:", value)
    //     let data = JSON.parse(value);
    //     callback(data);
    // }

    let result;
    while (result = await reader.read()) {
        if (result.done) break;
        let values = result.value.split('\n');
        for (let value of values) {
            if (value.trim() !== '') {
                console.log("readed value from stream:", value)
                let data = JSON.parse(value);
                callback(data);
            }
        }
    }
    
  } catch (error) {
    console.log(error);
    return error+",please contact system adminstrator";
  }

} 
// ask any question without prompt, no RAG 
async function askaiany(inputText) {
  // var url = "http://aiserver:5001/ask"
  // url = AISERVER_URL+"/ask"
  var url = await getStorage("AISERVER_URL") 
  if (!url) url = DEFAULT_AISERVER_URL
  url = url +"/askany"
  console.log("url:",url);
  console.log("input",inputText)
  var reqbody = JSON.stringify({
     request: inputText
  })
  console.log("reqbody", reqbody)
  return restAPI(url, "POST", reqbody)
}



//stream askai
async function askaiany_stream(inputText, callback) {
  // var url = "http://aiserver:5001/ask"
  // url = AISERVER_URL+"/ask"
  var url = await getStorage("AISERVER_URL") 
  if (!url) url = DEFAULT_AISERVER_URL
  url = url +"/stream/askany"
  console.log("url:",url);
  console.log("input",inputText)
  var reqbody = JSON.stringify({
     request: inputText
  })
  console.log("reqbody", reqbody)
  // return restAPI(url, "POST", reqbody)
  // restAPI(url, "POST", reqbody)
  restAPI_stream(url,"POST",reqbody,callback)
}

// ask  without prompt for RAQ
async function askai(inputText) {
  var url = await getStorage("AISERVER_URL") 
  if (!url) url = DEFAULT_AISERVER_URL
  url = url +"/ask"
  console.log("url:",url);
  console.log("input",inputText)
  var reqbody = JSON.stringify({
     request: inputText
  })
  console.log("reqbody", reqbody)
  return restAPI(url, "POST", reqbody)
  // try {
  //   const response = await fetch(url,
  //     { 
  //       method: 'POST',
  //       body: reqbody,
  //       headers: {
  //         'Content-Type': 'application/json',
  //       }
  //     });
  //   console.log("response", response)
  //   const data = await response.json();
  //   return data.response
  //   
  // } catch (error) {
  //   console.log(error);
  //   return error+",please contact system adminstrator";
  // }
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
  return restAPI(url, "POST", reqbody)

  // try {
  //   const response = await fetch(url,
  //     { 
  //       method: 'POST',
  //       body: reqbody,
  //       headers: {
  //         'Content-Type': 'application/json',
  //       }
  //     });
  //   console.log("response", response)
  //   const data = await response.json();
  //   return data.response
  //   
  // } catch (error) {
  //   console.log(error);
  //   return error+",please contact system adminstrator";

  // }
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
 
  return restAPI(url, "POST", reqbody)

  // try {
  //   const response = await fetch(url,
  //     { 
  //       method: 'POST',
  //       body: reqbody,
  //       headers: {
  //         'Content-Type': 'application/json',
  //       }
  //     });
  //   console.log("response", response)
  //   const data = await response.json();
  //   return data.response
  //   
  // } catch (error) {
  //   console.log(error);
  //   return error+",please contact system adminstrator";
  // }
}
//addListener for askai
// chrome.contextMenus.onClicked.addListener( async function(info) {
chrome.contextMenus.onClicked.addListener( async function(info,tab) {
  if (info.menuItemId === "askai") {
    var response = await askai(info.selectionText)
    console.log("response---", response)
    chrome.tabs.sendMessage(tab.id, { action: "showInformation", selectedText: response });
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
chrome.contextMenus.onClicked.addListener( async function(info,tab ) {
  if (info.menuItemId === "askai4pd") {
    var response = await askai4pd(info.selectionText)
    console.log("response4pd", response)
    chrome.tabs.sendMessage(tab.id, { action: "showInformation", selectedText: response });
    // let left = screen.width - 600 
    // let top = 0
    // var popup = window.open("popup.html", "", 'width=600,height=400,left=' + left + ',top=' + top); 
    // popup.response = response
  }
});

//addListener for any questions
chrome.contextMenus.onClicked.addListener( async function(info,tab ) {
  if (info.menuItemId === "askai4any") {
    var response = await askaiany(info.selectionText)
    console.log("response4askany", response)
    chrome.tabs.sendMessage(tab.id, { action: "showInformation", selectedText: response });
    // let left = screen.width - 600 
    // let top = 0
    // var popup = window.open("popup.html", "", 'width=600,height=400,left=' + left + ',top=' + top); 
    // popup.response = response
  }
});
//addListener for summarize
chrome.contextMenus.onClicked.addListener( async function(info,tab ) {
  if (info.menuItemId === "askai4sum") {
    var response = await askai4sum(info.selectionText)
    console.log("response summary:", response)
    chrome.tabs.sendMessage(tab.id, { action: "showInformation", selectedText: response });
    // let left = screen.width - 600 
    // let top = 0
    // var popup = window.open("popup.html", "", 'width=600,height=400,left=' + left + ',top=' + top); 
    // popup.response = response
  }
});

chrome.contextMenus.onClicked.addListener(async function (info, tab) {
  if (info.menuItemId === "askai4translate") {
    var question = "please translate the following to Simplified Chinese: " +  info.selectionText
    var response = await askaiany(question)
    console.log("ask any response:", response)
    // chrome.tabs.sendMessage(tab.id, { action: "showInformation", selectedText: info.selectionText });
    chrome.tabs.sendMessage(tab.id, { action: "showInformation", selectedText: response });
  }
});

chrome.contextMenus.onClicked.addListener(async function (info, tab) {
  if (info.menuItemId === "askai4translatestream") {
    var question = "please translate the following to Simplified Chinese: " +  info.selectionText
    askaiany_stream(question, function(data){
        console.log("ask any stream response:", data)
        // chrome.tabs.sendMessage(tab.id, { action: "showInformation", selectedText: info.selectionText });
        chrome.tabs.sendMessage(tab.id, { action: "showInformation", selectedText: data.answer });
    })
  }
});
// chrome.runtime.onMessage.addListener(function (message) {
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


