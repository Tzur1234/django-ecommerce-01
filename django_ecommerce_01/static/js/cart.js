
// window.addEventListener('load', getOrderItem)





function getOrderItem(){
// The function send request for all OrderItem instances related to the user

        const UIinstance = new UI();

        UIinstance.viewLoader('cart', 'block') // show loader
        UIinstance.showDiv('cart') // show section
        
       // Send the POST request
       fetch('/api/cart/cart-view/', {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': UIinstance.getCookie('csrftoken')
        }   
    })
    .then(response => {
        if (!response.ok) {
        throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data.data);
        insertOrderItemsUI(data.data)
        
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    })
    .finally(() => {
      UIinstance.viewLoader('cart', 'none') // hide loader
  });


}

function insertOrderItemsUI(orderItems){

        // Get the container element for the products
        const tableBody = document.querySelector('#cart .container-fluid .row .table .align-middle');

        // clear all remaining data
        tableBody.innerHTML = ''

        if (orderItems.length === 0) {
          // Create a table row for displaying the message
          const emptyRow = document.createElement('tr');
          const emptyCell = document.createElement('td');
          emptyCell.setAttribute('colspan', '5');
          emptyCell.textContent = 'No order items found.';
          emptyRow.appendChild(emptyCell);
          tableBody.appendChild(emptyRow);
        } else {

        orderItems.forEach((orderItem) => {
            // Create table row
            const row = document.createElement('tr');
        
            // Create table cells
            const productCell = document.createElement('td');
            const priceCell = document.createElement('td');
            const quantityCell = document.createElement('td');
            const totaPricelCell = document.createElement('td');
            const deleteCell = document.createElement('td');
        
            // Set cell content
            productCell.innerHTML = `<img src="${orderItem.product.image}" alt="" style="width: 50px;"> ${orderItem.product.title}`;
            priceCell.textContent = `$${orderItem.product.price}`;
            quantityCell.innerHTML = `
              <div class="input-group quantity mx-auto" style="width: 100px;">
                <div class="input-group-btn">
                  <button class="btn btn-sm btn-primary btn-minus" href="${orderItem.orderitem_update_link}">
                    <i class="fa fa-minus" href="${orderItem.orderitem_update_link}"></i>
                  </button>
                </div>
                <input type="text" class="form-control form-control-sm bg-secondary text-center" value="${orderItem.quantity}">
                <div class="input-group-btn">
                  <button class="btn btn-sm btn-primary btn-plus" href="${orderItem.orderitem_update_link}">
                    <i class="fa fa-plus" href="${orderItem.orderitem_update_link}"></i>
                  </button>
                </div>
              </div>
            `;
            quantityCell.addEventListener('click', addRemoveQuantity)
            totaPricelCell.textContent = `$${orderItem.total_price}`;
            deleteCell.innerHTML = `<button onclick="deleteOrderItem(event)" href="${orderItem.orderitem_delete_link}" class="btn btn-sm btn-primary"><i href="${orderItem.orderitem_delete_link}" class="fa fa-times"></i></button>`;
            // deleteCell.addEventListener('click', deleteOrderItem)


        
            // Append cells to row
            row.appendChild(productCell);
            row.appendChild(priceCell);
            row.appendChild(quantityCell);
            row.appendChild(totaPricelCell);
            row.appendChild(deleteCell);

        
            // Append row to table body
            tableBody.appendChild(row);
          });
          
        }

}


function deleteOrderItem(e){
  e.preventDefault()

  delete_url = e.target.getAttribute('href')

  console.log(e.target)


  const UIinstance = new UI();

  // Send the DELETE request
    fetch(delete_url, {
    method: 'DELETE',
    headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': UIinstance.getCookie('csrftoken')
    }   
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('The response from the server was not successful.');
    }
    return response.json();
  })
  .then(data => {
    console.log(data);
    // Show message
    UIinstance.showAlert(data.alert, data.message)
    // remove orderItem from the table
    const tdElement = moveUpToTR(e.target);
    tdElement.remove()
    
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
    // Handle error appropriately (e.g., display an error message to the user)
  });

  
}


function moveUpToTR(element) {
  let currentNode = element;
  while (currentNode !== null && currentNode.tagName !== 'TR') {
    currentNode = currentNode.parentNode;
  }
  return currentNode;
}


function addRemoveQuantity(e){

  update_url = e.target.getAttribute('href')

  console.log(update_url)


  if (e.target.className === 'fa fa-plus' || e.target.className === 'btn btn-sm btn-primary btn-plus'){
      console.log('Add')
      add = "True"
    }
    else if(e.target.className === 'fa fa-minus' || e.target.className === 'btn btn-sm btn-primary btn-minus'){
      console.log('Minus')
      add = "False"
  }
  else {
    return
  }

  sendUpdateOrderItemRquest(add, update_url, e)




}


function sendUpdateOrderItemRquest(add, update_url, e){
  
  const UIinstance = new UI();

    // Send the PUT request
    fetch(update_url, {
      method: 'PUT',
      headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': UIinstance.getCookie('csrftoken')
      },
      body: JSON.stringify({'add': add})    
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('The response from the server was not successful.');
      }
      return response.json();
    })
    .then(data => {
      console.log(data);
      console.log(data.total);

      // Update iNPUT TAG
      const trTag = moveUpToTR(e.target)
      const inputTag = trTag.querySelector('input');
      if (add === "True") {
        inputTag.value = parseInt(inputTag.value) + 1;
      } else {
        inputTag.value = parseInt(inputTag.value) - 1;
      }

      // Update total Order price
      document.querySelector('#sub_total').innerHTML = `$${data.sub_total}`
      document.querySelector('#total').innerHTML = `$${data.total + 10}`

      // Send Message
      UIinstance.showAlert(data.alert, data.message)

    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
      // Handle error appropriately (e.g., display an error message to the user)
    });
  

}