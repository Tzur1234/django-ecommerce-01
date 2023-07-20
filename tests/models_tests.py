from django.test import TestCase
from django.contrib.auth import get_user_model
from django_ecommerce_01.models import Product, ColorVariation, SizeVariation, Address, OrderItem, Order, Payment

User = get_user_model()


class ProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.color_variation = ColorVariation.objects.create(name='Red')
        self.size_variation = SizeVariation.objects.create(name='Small')
        self.product = Product.objects.create(
            title='Test Product',
            slug='test-product',
            description='This is a test product',
            active=True,
            image='product-image/test-image.jpg',
            price=100
        )
        self.product.color_variation.add(self.color_variation)
        self.product.size_variation.add(self.size_variation)

    def test_product_creation(self):
        """Test if the Product model is created correctly"""
        self.assertEqual(self.product.title, 'Test Product')
        self.assertEqual(self.product.slug, 'test-product')
        self.assertEqual(self.product.description, 'This is a test product')
        self.assertTrue(self.product.active)
        self.assertEqual(str(self.product.image), 'product-image/test-image.jpg')
        self.assertEqual(self.product.price, 100)
        self.assertIn(self.color_variation, self.product.color_variation.all())
        self.assertIn(self.size_variation, self.product.size_variation.all())

    def test_get_total_price(self):
        """Test if the get_total_price method returns the correct formatted price"""
        self.assertEqual(self.product.get_total_price(), '1.0')

    def test_get_absolute_url(self):
        """Test if the get_absolute_url method returns the correct URL"""
        self.assertEqual(self.product.get_absolute_url(), '/cart/product-details/test-product/')

    def test_get_absolute_url_add_to_cart(self):
        """Test if the get_absolute_url_add_to_cart method returns the correct URL"""
        self.assertEqual(self.product.get_absolute_url_add_to_cart(), '/cart/add-to-cart/test-product/')


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.color_variation = ColorVariation.objects.create(name='Red')
        self.size_variation = SizeVariation.objects.create(name='Small')
        self.product = Product.objects.create(
            title='Test Product',
            slug='test-product',
            description='This is a test product',
            active=True,
            image='product-image/test-image.jpg',
            price=100
        )
        self.order = Order.objects.create(user=self.user)
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            color=self.color_variation,
            size=self.size_variation
        )

    def test_order_item_creation(self):
        """Test if the OrderItem model is created correctly"""
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.color, self.color_variation)
        self.assertEqual(self.order_item.size, self.size_variation)

    def test_get_raw_amount_price(self):
        """Test if the get_raw_amount_price method returns the correct raw price"""
        self.assertEqual(self.order_item.get_raw_amount_price(), 200)

    def test_get_absolute_price(self):
        """Test if the get_absolute_price method returns the correct formatted price"""
        self.assertEqual(self.order_item.get_absolute_price(), 2.0)

    def test_get_absolute_delete_url(self):
        """Test if the get_absolute_delete_url method returns the correct URL"""
        self.assertEqual(self.order_item.get_absolute_delete_url(), '/cart/delete-order-item/1/')

    def test_update_quantity_url(self):
        """Test if the update_quantity_url method returns the correct URL"""
        self.assertEqual(self.order_item.update_quantity_url(), '/cart/update_order_item/1/')


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.address = Address.objects.create(
            user=self.user,
            address_line_1='123 Test St',
            address_line_2='Apt 4',
            city='Test City',
            zip_code='12345',
            default=True
        )
        self.order = Order.objects.create(user=self.user, address=self.address)

    def test_order_creation(self):
        """Test if the Order model is created correctly"""
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.address, self.address)
        self.assertFalse(self.order.ordered)

    def test_reference_number(self):
        """Test if the reference_number property returns the correct reference number"""
        self.assertEqual(self.order.reference_number, 'ORDER-1')

    def test_get_subtotal(self):
        """Test if the get_subtotal method returns the correct subtotal"""
        product = Product.objects.create(
            title='Test Product',
            slug='test-product',
            description='This is a test product',
            active=True,
            image='product-image/test-image.jpg',
            price=100
        )
        OrderItem.objects.create(
            order=self.order,
            product=product,
            quantity=2,
            color=ColorVariation.objects.create(name='Red'),
            size=SizeVariation.objects.create(name='Small')
        )
        self.assertEqual(self.order.get_subtotal(), 2.0)

    def test_get_total(self):
        """Test if the get_total method returns the correct total"""
        product = Product.objects.create(
            title='Test Product',
            slug='test-product',
            description='This is a test product',
            active=True,
            image='product-image/test-image.jpg',
            price=100
        )
        OrderItem.objects.create(
            order=self.order,
            product=product,
            quantity=2,
            color=ColorVariation.objects.create(name='Red'),
            size=SizeVariation.objects.create(name='Small')
        )
        self.assertEqual(self.order.get_total(), 2.0)


class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.address = Address.objects.create(
            user=self.user,
            address_line_1='123 Test St',
            address_line_2='Apt 4',
            city='Test City',
            zip_code='12345',
            default=True
        )
        self.order = Order.objects.create(user=self.user, address=self.address)
        self.payment = Payment.objects.create(
            order=self.order,
            payment_method='PayPal',
            amount=10.0,
            raw_response='Payment successful'
        )

    def test_payment_creation(self):
        """Test if the Payment model is created correctly"""
        self.assertEqual(self.payment.order, self.order)
        self.assertEqual(self.payment.payment_method, 'PayPal')
        self.assertEqual(self.payment.amount, 10.0)
        self.assertEqual(self.payment.raw_response, 'Payment successful')

    def test_reference_number(self):
        """Test if the reference_number property returns the correct reference number"""
        self.assertEqual(self.payment.reference_number, 'PAYMENT-1-1')
