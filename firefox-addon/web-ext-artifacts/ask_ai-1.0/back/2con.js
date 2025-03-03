
// content.js
chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
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
    infoDiv.style.fontSize = "26px";
    infoDiv.style.color = "darkblue";
    infoDiv.style.border = "1px solid #ccc";
    infoDiv.style.borderRadius = "5px";

    // Use createElement for each HTML element
    const heading = document.createElement("h1");
    heading.innerText = "AI comments:";

    const paragraph = document.createElement("p");
    paragraph.innerText = selectedText;

    // Append the elements to the div
    infoDiv.appendChild(heading);
    infoDiv.appendChild(paragraph);

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
    heading.innerText = selectedText;

    const paragraph = infoDiv.querySelector("p");
    paragraph.innerText = "Additional information goes here.";
  }
}


// function showInformation(selectedText) {
//   // Check if the information div already exists.
//   let infoDiv = document.getElementById("askMoreInfo");
//   if (!infoDiv) {
//     // Create a div to display additional information.
//     infoDiv = document.createElement("div");
//     infoDiv.id = "askMoreInfo";
//     infoDiv.style.position = "fixed";
//     infoDiv.style.top = "50px"; // Adjust this value to avoid the toolbar
//     infoDiv.style.right = "0";
//     infoDiv.style.width = "30%";
//     infoDiv.style.height = "calc(100% - 50px)"; // Adjust for the height of the toolbar
//     infoDiv.style.backgroundColor = "#f5f5f5";
//     infoDiv.style.overflowY = "auto";
//     infoDiv.style.padding = "10px";
//     
//     // Additional styling
//     infoDiv.style.fontSize = "16px";
//     infoDiv.style.color = "darkblue";
//     infoDiv.style.border = "1px solid #ccc";
//     infoDiv.style.borderRadius = "5px";

//     // Use HTML tags for formatting
//     infoDiv.innerHTML = `<h1>${selectedText}</h1><p>Additional information goes here.</p>`;

//     // Append the div to the body.
//     document.body.appendChild(infoDiv);

//     // Listen for text deselection and remove the displayed information.
//     document.addEventListener("mouseup", function () {
//       if (!document.getSelection().toString()) {
//         infoDiv.remove();
//       }
//     });
//   } else {
//     // Update the content if the div already exists.
//     infoDiv.innerHTML = `<h1>${selectedText}</h1><p>Additional information goes here.</p>`;
//   }
// }


// function showInformation(selectedText) {
//   // Check if the information div already exists.
//   let infoDiv = document.getElementById("askMoreInfo");
//   if (!infoDiv) {
//     // Create a div to display additional information.
//     infoDiv = document.createElement("div");
//     infoDiv.id = "askMoreInfo";
//     infoDiv.style.position = "fixed";
//     infoDiv.style.top = "50px"; // Adjust this value to avoid the toolbar
//     infoDiv.style.right = "0";
//     infoDiv.style.width = "30%";
//     infoDiv.style.height = "calc(100% - 50px)"; // Adjust for the height of the toolbar
//     infoDiv.style.backgroundColor = "#f5f5f5";
//     infoDiv.style.overflowY = "auto";
//     infoDiv.style.padding = "10px";
//     // infoDiv.innerText = `Additional information about: ${selectedText}`;
//     infoDiv.innerHTML = `<h1>AI Comments:</h1> <p>${selectedText}`;
//     // Append the div to the body.
//     document.body.appendChild(infoDiv);

//     // Listen for text deselection and remove the displayed information.
//     document.addEventListener("mouseup", function () {
//       if (!document.getSelection().toString()) {
//         infoDiv.remove();
//       }
//     });
//   } else {
//     // Update the content if the div already exists.
//     // infoDiv.innerText = `Additional information about: ${selectedText}`;
//     infoDiv.innerHTML = `<h1>AI Comments:</h1> <p> ${selectedText}`;
//   }
// }

