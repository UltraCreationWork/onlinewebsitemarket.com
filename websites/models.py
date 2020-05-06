from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class UserProfile(models.Model):
    user                    =       models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id      =       models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing    =       models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



class Product(models.Model):
    title           = models.CharField(max_length=255)
    category        = models.CharField(max_length=255)
    img             = models.ImageField(upload_to="media")
    url             = models.URLField()
    disc            = models.TextField()
    slug            = models.SlugField()
    price           = models.FloatField()
    discount_price  = models.FloatField(blank=True, null=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })

    
    
    
class OrderItem(models.Model):
    user        =       models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered     =       models.BooleanField(default=False)
    item        =       models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity    =       models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
    
class Order(models.Model):
    user                =       models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ref_code            =       models.CharField(max_length=20, blank=True, null=True)
    items               =       models.ManyToManyField(OrderItem)
    start_date          =       models.DateTimeField(auto_now_add=True)
    ordered_date        =       models.DateTimeField()
    ordered             =       models.BooleanField(default=False)
    shipping_address    =       models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address     =       models.ForeignKey('Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment             =       models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon              =       models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered     =       models.BooleanField(default=False)
    received            =       models.BooleanField(default=False)
    refund_requested    =       models.BooleanField(default=False)
    refund_granted      =       models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Address(models.Model):
    user                    =       models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    street_address          =       models.CharField(max_length=100)
    apartment_address       =       models.CharField(max_length=100)
    country                 =       CountryField(multiple=False)
    zip                     =       models.CharField(max_length=100)
    address_type            =       models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default                 =       models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id        =       models.CharField(max_length=50)
    user                    =       models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, blank=True, null=True)
    amount                  =       models.FloatField()
    timestamp               =       models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code        =       models.CharField(max_length=15)
    amount      =       models.FloatField()

    def __str__(self):
        return self.code

class Refund(models.Model):
    order       =       models.ForeignKey(Order, on_delete=models.CASCADE)
    reason      =       models.TextField()
    accepted    =       models.BooleanField(default=False)
    email       =       models.EmailField()

    def __str__(self):
        return f"{self.pk}"



class Testimonial(models.Model):
    name = models.CharField(max_length=30)
    img  = models.ImageField(upload_to="media")
    disc = models.TextField()
    prof = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class clint(models.Model):
    company_name    =   models.CharField(max_length=50)
    logo            =   models.ImageField(upload_to="media")
    website         =   models.URLField()

    def __str__(self):
        return self.company_name


class Team(models.Model):
    name                =   models.CharField(max_length=30)
    prof                =   models.CharField(max_length=20)
    img                 =   models.ImageField(upload_to="media")
    social_link_one     =   models.URLField(blank=True,default="twitter.com")
    social_link_two     =   models.URLField(blank=True,default="facebook.com")
    social_link_three   =   models.URLField(blank=True,default="instagram.com")
    social_link_four    =   models.URLField(blank=True,default="linkedin.com")
    social_link_five    =   models.URLField(blank=True,default="youtube.com")

    def __str__(self):
        return self.name


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)