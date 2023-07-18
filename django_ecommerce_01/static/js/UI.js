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


 
    viewLoader(section_id, display){
      // The function receives section_id and display mode (none / block)
      //  according to the parameters, the function hide / display the spinner loader in the relevant section

      const choosedSection = document.getElementById(section_id);     
      const spinnerLoader = choosedSection.querySelector('#spinner-loader');
      spinnerLoader.style.display = display;

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
    
    // get csrf token
    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }

  


}






