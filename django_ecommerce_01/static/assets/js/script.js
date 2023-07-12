// UI


// show only the given section id & hide others
function showDiv(id) {
    var divs = document.getElementsByClassName("section");
    for (var i = 0; i < divs.length; i++) {
      if (divs[i].id === id) {
        divs[i].style.display = "block";
      } else {
        divs[i].style.display = "none";
      }
    }
  }
// aa



// Buttons
contactBtn = document.getElementById('contact-button')



// Event Listener:

contactBtn.addEventListener('click', () => {

    showDiv('contact')

})




