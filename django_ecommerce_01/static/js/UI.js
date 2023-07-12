class UI {
    // Constructor (if needed)
    constructor() {
      // Initialize any properties
    }
  
    // Methods!!


    // hide / show sections
    showDiv(id) {
      var divs = document.getElementsByClassName("section");
      for (var i = 0; i < divs.length; i++) {
        if (divs[i].id === id) {
          divs[i].style.display = "block";
        } else {
          divs[i].style.display = "none";
        }
      }
    }

    // show loader-spiner
    showLoader(){
        const spiner = document.querySelector('.spinner-wrapper')
        spiner.style.display = 'block'
    }
    // hide loader-spiner
    hideLoader(){
        const spiner = document.querySelector('.spinner-wrapper')
        spiner.style.display = 'none'
    }

    showAlert(type, message) {
      var alertContainer = document.getElementById("message-alert");
      
      // Create the alert div element
      var alertDiv = document.createElement("div");
      alertDiv.classList.add("alert", "alert-" + type);
      
      // Create the close button
      var closeButton = document.createElement("button");
      closeButton.setAttribute("type", "button");
      closeButton.classList.add("close");
      closeButton.setAttribute("data-dismiss", "alert");
      closeButton.setAttribute("aria-hidden", "true");
      closeButton.innerHTML = "&times;";
      
      // Create the strong element for the message
      var strongElement = document.createElement("strong");
      strongElement.textContent = message;
      
      // Append the close button and the strong element to the alert div
      alertDiv.appendChild(closeButton);
      alertDiv.appendChild(strongElement);
      
      // Clear any existing content in the alert container
      alertContainer.innerHTML = "";
      
      // Append the alert div to the alert container
      alertContainer.appendChild(alertDiv);
    }
    

}



