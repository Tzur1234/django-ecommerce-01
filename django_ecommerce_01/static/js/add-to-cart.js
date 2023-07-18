
// ADD-TO-CART-EVENT
function addToCart(e){
    const UIinstance = new UI();

    
    UIinstance.viewLoader('product-detail', 'block') // show loader

    e.preventDefault();

    // Retrieve the href attribute of the button
    const url = e.target.getAttribute('href');
    
    // Get the selected size and color
    const size_id = document.querySelector('input[name="size"]:checked').value;
    const color_id = document.querySelector('input[name="color"]:checked').value;
    const quantity = document.querySelector('#quantity').value

      // Send the POST request
        fetch(url, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': UIinstance.getCookie('csrftoken')
            },
            body: JSON.stringify({
                'quantity': quantity,
                'color_id': color_id,
                'size_id': size_id,
            })     
        })
        .then(response => {
            if (!response.ok) {
            throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);

            // show message
            UIinstance.showAlert(data.alert, data.message)


        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        })
        .finally(() => {
            UIinstance.viewLoader('product-detail', 'none') // show loader
        });

}
