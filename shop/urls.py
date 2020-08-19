from django.urls import path
from .views import *
from .import views

app_name = "shop"

urlpatterns = [
    path('',HomeListView.as_view(),name="home"),
    path('detail/<int:pk>',ProductDetail.as_view(),name='product_detail'),
    path('addtocart/<int:pk>',AddToCart.as_view(),name='add_to_cart'),
    path('ordersummary/',OrderSummary.as_view(),name="order_summary"),
    path('checkout/',Checkout.as_view(),name='checkout'),
    path('payment/',PaymentView.as_view(),name="payment"),
    path('myorder/',MyOrder.as_view(),name="my_order"),
    path('removeformcart/<int:pk>/',RemoveFormCart.as_view(),name="removefromcart"),
    path('removeitem/<int:pk>/',RemoveCart.as_view(),name="removeitem"),
    #path('search',SearchProduct.as_view(),name = "search"),
    path('search',views.search,name='search')

]