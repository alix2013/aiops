// AISERVER_URL="http://localhost:5001"
DEFAULT_AISERVER_URL="http://aiserver:5001"

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

document.addEventListener('DOMContentLoaded', function () {
    var input = document.getElementById('inputField');
    input.focus();
    var submitButton = document.getElementById('submitButton');
    var chatButton = document.getElementById('chatButton');

    input.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            submitButton.click();
        }
    });
    submitButton.addEventListener("click", submitForm);
    chatButton.addEventListener("click", openChat);
});

async function openChat(){
  chatServerUrl = await getStorage("CHATSERVER_URL")
  // browser.tabs.create({ url: "http://localhost:5006" });
  browser.tabs.create({ url: chatServerUrl });
}

async function submitForm() {
  // Disable the submit button and show loader spinner
  var submitButton = document.getElementById("submitButton");
  // Disable the submit button and show the spinner
  submitButton.disabled = true;
  submitButton.innerHTML = '<i class="fa fa-spinner fa-spin"></i>';
  // Get the input value
  var inputValue = document.getElementById("inputField").value;
 
  responseTextArea.value = "";
  // Make the API request using fetch()
  // fetch("http://aiserver:5001/ask", {
  //fetch(AISERVER_URL + "/ask", {
  serverUrl = await getStorage("AISERVER_URL")
  if (!serverUrl) serverUrl = DEFAULT_AISERVER_URL
  console.log(serverUrl, serverUrl)
  fetch(serverUrl + "/ask", {
    method: "POST",
    headers: {
    "Content-Type": "application/json",
    },
    body: JSON.stringify({ request: inputValue }),
    })
    .then(function(response) {
      if (response.ok) {
      // Log the response for debugging
        console.log(response);
      // Parse the response JSON data
        return response.json();
      } else {
        throw new Error("Error occurred while making the API request.");
      }
    })
    .then(function(responseData) {
  // Show the response text in the textarea
      var responseTextArea = document.getElementById("responseTextArea");
      responseTextArea.value = responseData.response;
     })
    .catch(function(error) {
  // Handle the error case
  //alert(error.message);
      responseTextArea.value = error.message
    })
    .finally(function() {
    // Enable the submit button and reset its text
      submitButton.disabled = false;
      submitButton.innerHTML = "Submit";

    });
}
    

