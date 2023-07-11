from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import reverse


User = get_user_model()


class ColorVariation(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SizeVariation(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Address(models.Model):
    ADDRESS_CHOICES = (
        ('B', 'Billing'),
        ('S', 'Shipping'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_line_1}, {self.address_line_2}, {self.city}, {self.zip_code}"

    class Meta:
        verbose_name_plural = 'Addresses'

class Product(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product-image/')
    color_variation = models.ManyToManyField(ColorVariation)
    size_variation = models.ManyToManyField(SizeVariation)
    price = models.IntegerField(default=0)

    def get_total_price(self):
        return "{}".format(self.price / 100)

    """
    The function returns the url for the specific product
    """
    def get_absolute_url(self):
        return reverse("cart:product-details", kwargs={'slug': self.slug})
    
    def get_absolute_url_add_to_cart(self):
        return reverse("cart:add-to-cart", kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

class OrderItem(models.Model):
    order = models.ForeignKey(
        "Order", related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    color = models.ForeignKey(ColorVariation, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeVariation, on_delete=models.CASCADE)

    def get_raw_amount_price(self):
        return self.quantity * self.product.price

    def get_absolute_price(self):
        raw_price = self.get_raw_amount_price()
        return raw_price / 100

    
    def get_absolute_delete_url(self):
        return reverse("cart:delete-order-item", kwargs={'id': self.pk})

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)

    billing_address = models.ForeignKey(
        Address, related_name='billing_address', blank=True, null=True, on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', blank=True, null=True, on_delete=models.SET_NULL)

    @property
    def reference_number(self):
        return f"ORDER-{self.pk}"

    def __str__(self):
        return self.reference_number

class Payment(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=20, choices=(
        ('PayPal', 'PayPal'),
    ))
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    amount = models.FloatField()
    raw_response = models.TextField()

    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"PAYMENT-{self.order}-{self.pk}"
    

"""
The singals complete the slug field based on the title field
"""
def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(pre_save_product_receiver, sender=Product)