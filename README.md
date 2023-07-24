# django-ecommerce

an e-commerce platform built with django rest framework.



## User Guide

To use the application as a user, follow these steps:

1. Perform a structured registration process. Enter your email address (it is recommended to enter a valid email address as you will need to verify it later through your email account).

2. After registration and logging into the application, you will be able to browse the available items for sale.

3. For each item, you can click on it and a window will immediately open where you can view the item details, add it to the cart, and specify the desired size and color.

4. At the end of the process, click on "Shopping Cart" where you can view all the items you have added to the cart, along with the price for each individual item. The final price will be the total price of the multiplied item price by the number of items requested. You can also remove an item from the list and update the desired number of items for each item. After each update, you can see the real-time update of the final price you need to pay for all the items. 

5. After reviewing all the items you want to purchase, click on "Proceed To CheckOut" and you will immediately see the payment window. Click on the appropriate payment method for you. In the current system, there is a secure connection to a payment system - Paypal. 

6. At the end of the registration process, you will receive a pop-up message confirming that the payment for the order has been successfully received.




### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy django_ecommerce_01

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).


License: MIT