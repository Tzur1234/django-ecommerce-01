
window.addEventListener('load', () => {
  
  document.querySelector('#checkout-btn1').addEventListener('click', showCheckout)
  document.querySelector('#checkout-btn2').addEventListener('click', showCheckout)
  
})

function showCheckout(){
  const UIinstance = new UI();
  UIinstance.showDiv('checkout') // show the write div element


   // Send the POST request
   fetch('/api/cart/cart-view/', {
    method: 'GET',
    headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': UIinstance.getCookie('csrftoken')
    }   
  })
  .then(response => response.json())
  .then(data => {
      console.log(data.extra_content);

      // Insert total price data
      document.querySelector('#total-checkout').innerHTML = `$${data.extra_content.total}`
      
  })
  .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
  })


}