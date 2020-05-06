from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from websites.views import home,ItemDetailView,CheckoutView,OrderSummaryView,add_to_cart,remove_from_cart,remove_single_item_from_cart,AddCouponView,RequestRefundView,PaymentView,t_p,Contact_view
from websites.sitemaps import Prodsitemaps,Staticsitemaps
from django.contrib.sitemaps.views import sitemap
def trigger_error(request):
    division_by_zero = 1 / 0

sitemaps = {
    'prod': Prodsitemaps,
    'static':Staticsitemaps
}

urlpatterns = [
    path('online/', admin.site.urls),
    path("",home,name="home"),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path("accounts/",include('allauth.urls')),
    path("term/",t_p,name="term"),
    path('sitemap.xml',sitemap,{'sitemaps':sitemaps}),
    path('contact/',Contact_view,name="contact"),
    path('sentry-debug/', trigger_error)

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)


