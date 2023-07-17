function getCookie(name) {
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
const csrf_token = getCookie('csrftoken')


paypal.Buttons({
createOrder() {
  return fetch("/api/cart/create-paypal-order/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': getCookie('csrftoken'), 

    },
    body: JSON.stringify({
      cart: [
        {
          sku: "YOUR_PRODUCT_STOCK_KEEPING_UNIT",
          quantity: "YOUR_PRODUCT_QUANTITY",
        },
      ]
    })
  })
  .then((response) => response.json())
  .then((order) => {
        return order.id
});
},
onApprove(data) {
// This function captures the funds from the transaction.
return fetch("/api/cart/confirm-paypal-order/", {
method: "POST",
headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': getCookie('csrftoken'), 
},
body: JSON.stringify({
    orderID: data.orderID
})
})
.then((response) => response.json())
.then((details) => {
// This function shows a transaction success message to your buyer.
alert('Transaction completed by ' + details.payer.name.given_name);
console.log(details);


});
}

}).render('#paypal-button-container');