window.addEventListener('DOMContentLoaded', function() {
     // document.getElementById("response").innerText = window.response
     document.getElementById("textArea").value = window.response
});

window.onblur = function() {
    window.close();
}
