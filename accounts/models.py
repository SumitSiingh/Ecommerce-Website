from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
	user = models.OneToOneField(User, primary_key = True, unique = True, on_delete=models.CASCADE)
	phone = models.CharField(max_length=200, null=True)
	pic = models.ImageField(default = 'noimage.png', null = True, blank = True)

	def __str__(self):
		return self.user.first_name + ' ' + self.user.last_name


class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name


class Product(models.Model):
	CATEGORY = (
			('Indoor', 'Indoor'),
			('Out Door', 'Out Door'),
			)

	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name


class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)

	customer = models.ForeignKey(Customer, null = True, on_delete = models.CASCADE)
	product = models.ForeignKey(Product, null = True, on_delete = models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	note = models.CharField(max_length=100, null = True, blank = True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)

	def __str__(self):
		return self.product.name + ' by ' + self.customer.user.first_name
