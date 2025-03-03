
// content.js
browser.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === "showInformation") {
    showInformation(message.selectedText);
  }
});

function showInformation(selectedText) {
  // Check if the information div already exists.
  let infoDiv = document.getElementById("askMoreInfo");
  if (!infoDiv) {
    // Create a div to display additional information.
    infoDiv = document.createElement("div");
    infoDiv.id = "askMoreInfo";
    infoDiv.style.position = "fixed";
    infoDiv.style.top = "50px"; // Adjust this value to avoid the toolbar
    infoDiv.style.right = "0";
    infoDiv.style.width = "30%";
    infoDiv.style.height = "calc(100% - 50px)"; // Adjust for the height of the toolbar
    infoDiv.style.backgroundColor = "#f5f5f5";
    infoDiv.style.overflowY = "auto";
    infoDiv.style.padding = "10px";
    
    // Additional styling
    // infoDiv.style.fontSize = "16px !important";
    infoDiv.style.zIndex = "9999";  //on top 
    infoDiv.style.color = "darkblue";
    infoDiv.style.border = "1px solid #ccc";
    infoDiv.style.borderRadius = "5px";

    // infoDiv.style.cssText = `
    //   font-size: 16px !important; 
    //   z-index: 9999 !important;
    //   color: darkblue !important; 
    //   border: 1px solid #ccc !important; 
    //   border-radius: 5px !important; 
    // `;

    // Use createElement for each HTML element
    const heading = document.createElement("div");
    // heading.innerHTML = `<h1>${selectedText}</h1>`;
    // heading.innerHTML = `<h1>AI:</h1>`;
    heading.innerHTML = `<h1 style="font-size: 20px !important; font-weight: bold !important;">AI:</h1>`;
    // const paragraph = document.createElement("p");
    // paragraph.innerText = "Additional information goes here.";

    const paragraph = document.createElement("div");
    // paragraph.innerHTML = `<h4>${selectedText}</h4>`;
    paragraph.innerHTML = `<p style="font-size: 18px !important;">${selectedText.replace(/\n/g, "<br>")}</p>`;

    // Append the elements to the div
    // infoDiv.appendChild(heading);
    // infoDiv.appendChild(paragraph);
    // Append the div to the body.
    // document.body.appendChild(infoDiv);

    // Create a copy icon element
    const copyIcon = document.createElement("div");
    copyIcon.innerHTML = "&#128203;"; // Unicode character for copy icon
    copyIcon.style.cursor = "pointer";
    copyIcon.style.marginTop = "5px";
    // copyIcon.addEventListener("click", function () {
    //   copyToClipboard(selectedText);
    // });
    //
    copyIcon.addEventListener("mousedown", function () {
      console.log("copy icon mousedown called");
      copyToClipboard(selectedText);
    });

    // copyIcon.addEventListener("click", function () {
    //   // const backgroundPage = browser.extension.getBackgroundPage();
    //   // backgroundPage.copyToClipboard(selectedText);
    //   console.log("copy clicked")
    //   // browser.runtime.sendMessage({ action: "copyToClipboard", text: selectedText });
    //   copyToClipboard(selectedText);
    // });

    // Append the elements to the div
    infoDiv.appendChild(heading);
    infoDiv.appendChild(paragraph);
    infoDiv.appendChild(copyIcon);

    // Append the div to the body.
    document.body.appendChild(infoDiv);

    // Listen for text deselection and remove the displayed information.
    document.addEventListener("mouseup", function () {
      if (!document.getSelection().toString()) {
        infoDiv.remove();
      }
    });
  } else {
    // Update the content if the div already exists.
    const heading = infoDiv.querySelector("h1");
    heading.innerHTML = `<h1 style="font-size: 20px !important; font-weight: bold !important;">AI:</h1>`;

    const paragraph = infoDiv.querySelector("p");
    // paragraph.innerHTML = `<h4>${selectedText}</h4>`;
    // paragraph.innerHTML = `<p style="font-size: 18px !important;">${selectedText}</p>`;
    paragraph.innerHTML = `<p style="font-size: 18px !important;">${selectedText.replace(/\n/g, "<br>")}</p>`;

    // paragraph.innerText = "Additional information goes here.";
  }
}

function copyToClipboard(text) {
  // Create a temporary textarea element to copy text to clipboard
  const textarea = document.createElement("textarea");
  textarea.value = text;
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  document.body.removeChild(textarea);
}

