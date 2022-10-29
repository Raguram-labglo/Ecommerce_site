from django.urls import URLPattern, path
from sympy import cancel
from . import views

urlpatterns = [path('show/', views.Product_list, name = 'show'),
               path('search/', views.Search, name = 'search'),
               path('', views.Form_in, name = 'login'),
               path('logout/', views.Form_out, name = 'logout'),
               path('add_to_cart/<int:id>', views.add_to_cart, name = 'add_to_cart'),
               path('cart/',views.Show_cart, name = 'cart'),
               path('del_cart/<int:id>',views.Remove_cart, name = 'del_cart'),
               path('orders/', views.Order_details, name = 'orders'),
               path('cancel_order/<int:id>',views.Cancel_order, name = 'cancel_order'),
               path('update_cart/<int:id>', views.Update_cart, name = 'update_cart'),
               path('create_order/', views.Create_order, name = 'create_order'),
               path('wish/<int:id>', views.Wish_list_products, name = 'wish'),
               path('wish_list/', views.Show_wish, name = 'wish_list'),
               path('remove_wish/<int:id>', views.Remove_wish, name = 'remove_wish')
               ]