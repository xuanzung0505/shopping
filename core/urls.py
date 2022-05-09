from django.urls import path, include
from . import views

app_name = 'shopping'

urlpatterns = [
    path('index/', views.indexPage.as_view(), name='index'),

    path('login/', views.loginPage.as_view(), name='login'),

    path('catalog/', views.catalogPage.as_view(), name='catalog'),
    path('catalog/search/<str:search_query>/', views.catalogSearch.as_view(), name='catalogsearch'),
    # path('catalog/search/All/', views.catalogSearchAll.as_view(), name='catalogsearchall'),
    path('catalog/filter/<str:category_id>/', views.catalogFilter.as_view(), name='catalogfilter'),

    path('detail/<int:product_id>/', views.detailPage.as_view(), name='productdetail'),

    path('cart/', views.cartPage.as_view(), name='cart'),
    path('cart/delete/<str:id>/', views.cartItemDelete.as_view(), name='cartitemdelete'),
    path('cart/quantityChange/<str:id>/<str:quantity>/', views.cartItemQuantityChange.as_view(), name='cartitemquantitychange'),
    
    path('checkout/',views.checkoutPage.as_view(), name='checkout'),
    # path('success/', views.successPage.as_view(), name='success'),
    path('order/', views.orderPage.as_view(), name='order'),
    path('order/<int:order_id>/', views.orderDetailPage.as_view(), name='orderdetail'),
    
    #rest framework
    path('api/product/', views.getAllProductAPIView.as_view()),
    path('api/category/', views.getAllCategoryAPIView.as_view()),
    path('api/user/', views.getAllUserAPIView.as_view()),
    path('api/cart/', views.getAllCartAPIView.as_view()),
    path('api/cartitem/<str:cart_id>/', views.getAllCartItemAPIView.as_view()),
    path('api/order/', views.getAllOrderAPIView.as_view()),
]