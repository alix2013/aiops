DEFAULT_AISERVER_URL = "http://aiserver:5001"
DEFAULT_CHATSERVER_URL = "http://aiserver:5001"
document.addEventListener('DOMContentLoaded', function () {
    var input = document.getElementById('inputField');
    chrome.storage.sync.get(['AISERVER_URL'], function(storage){
       if (!storage.AISERVER_URL) {
        input.value= DEFAULT_AISERVER_URL
       }else {
         input.value = storage.AISERVER_URL
       }
    })

    var chatInput = document.getElementById('chatInputField');
    chrome.storage.sync.get(['CHATSERVER_URL'], function(storage){
       if (!storage.CHATSERVER_URL) {
        chatInput.value= DEFAULT_CHATSERVER_URL
       }else {
         chatInput.value = storage.CHATSERVER_URL
       }
    })


    input.focus();
    var submitButton = document.getElementById('submitButton');

    input.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            submitButton.click();
        }
    });
    submitButton.addEventListener("click", submitForm);
});

function submitForm() {
  var inputValue = document.getElementById("inputField").value;
  var chatInputValue = document.getElementById("chatInputField").value;

  console.log("server url:"+ inputValue)
  chrome.storage.sync.set({'AISERVER_URL':inputValue, 'CHATSERVER_URL':chatInputValue}, function(){
     // close();
     alert("Saved AISERVER_URL:"+inputValue+" CHATSERVER_URL:"+chatInputValue)
     close();
  })
}

