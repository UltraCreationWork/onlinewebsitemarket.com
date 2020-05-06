from django.contrib.sitemaps import Sitemap
from .models import Product
from django.urls import reverse

class Prodsitemaps(Sitemap):
    
    def post(self):
        return Product.objects.all()
    
class Staticsitemaps(Sitemap):
    
    def item(self):
        return ['product']

    def location(self,item):
        return reverse(item)