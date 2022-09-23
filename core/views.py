from dataclasses import fields
from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View

# from product.models import Product, Category
# from cart.models import Cart, CartItem
# from order.models import Order

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.forms.models import model_to_dict
from django.core import serializers

#json
import json
from django.core.serializers.json import DjangoJSONEncoder

#DAO
from businesslogic.productDAO.ProductDAO import ProductDAO
from businesslogic.categoryDAO.CategoryDAO import CategoryDAO
from businesslogic.cartDAO.CartDAO import CartDAO
from businesslogic.orderDAO.OrderDAO import OrderDAO
from businesslogic.userDAO.UserDAO import UserDAO

#REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product.serializers import GetAllProductSerializer, GetAllCategorySerializer, ProductSerializer
from user.serializers import GetAllUserSerializer
from cart.serializers import GetAllCartSerializer, GetAllCartItemSerializer
from order.serializers import GetAllOrderSerializer
# Create your views here.

class indexPage(View):
    def get(self,request):
        return render(request,'indexpage/index.html')

class loginPage(View):
    def get(self,request):
        return render(request,'loginpage/login.html')
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        myuser = authenticate(username=username, password=password)
        if myuser is None:
            return HttpResponse('user does not exist')
        
        login(request, myuser) #sign in
        return render(request, 'indexpage/index.html')


class catalogPage(LoginRequiredMixin, View):
    login_url='../login/'
    def get(self,request):
        # productList = Product.objects.filter(active=True)
        productList = ProductDAO.getActiveProduct()
        categoryList = CategoryDAO.getActiveCategory()
        # print(productList.count())
        # data = serializers.serialize('json', list(productList),fields="__all__")

        data = GetAllProductSerializer(productList, many=True)
        # return Response(data=mydata.data, status=status.HTTP_200_OK)
        # data = json.dumps(list(productList), cls=DjangoJSONEncoder)
        res = data.data
        # print(list(res))
        # print("json dumps:" + json.dumps(list(res)))
        context = {"productlist":data.data, "categoryList": categoryList}
        return render(request,'catalogpage/catalog.html',context)

class catalogSearch(LoginRequiredMixin, View):
    login_url='../login/'
    def post(self, request, search_query):
        
        # product_qset = Product.objects.filter(title__icontains = search_query, active=True)
        product_qset = ProductDAO.searchActiveProductByName(search_query)

        qset_json = serializers.serialize('json', product_qset)

        # size = int(product_qset.count())

        return JsonResponse(qset_json, status=200, safe=False)

class catalogFilter(LoginRequiredMixin, View):
    login_url='../login/'
    def post(self, request, category_id):
        
        if(int(category_id) != 0):
            category = CategoryDAO.getCategoryByID(category_id)
            product_qset = ProductDAO.searchActiveProductByCategory(category)
            
            qset_json = serializers.serialize('json', product_qset)
        else:
            product_qset = ProductDAO.getActiveProduct()            
            qset_json = serializers.serialize('json', product_qset)
        
        # size = int(product_qset.count())

        return JsonResponse(qset_json, status=200, safe=False)

# class catalogSearchAll(LoginRequiredMixin, View):
#     login_url='../login/'
#     def post(self, request):

#         product_qset = Product.objects.all()
        
#         qset_json = serializers.serialize('json', product_qset)

#         # size = int(product_qset.count())

#         return JsonResponse(qset_json, status=200, safe=False)

class detailPage(LoginRequiredMixin, View):
    login_url='../login/'
    def get(self, request, product_id):
        # product = Product.objects.get(pk=product_id)
        product = ProductDAO.getProductByID(product_id)
        context = {"product":product}
        return render(request,'productdetailpage/productdetail.html',context)

    def post(self, request, product_id):
        # product = Product.objects.get(pk=product_id)
        product = ProductDAO.getProductByID(product_id)

        quantity = int(request.POST.get('quantity'))
       

        #add a cart item to cart

        #get the cart from user credentials
        user = request.user
        
        cart_qset = CartDAO.getFreeCartByUser(user) #get the ONLY cart
        #if none then create new cart
        cart = CartDAO.createCartByUser(user)
        
        for item in cart_qset:
            cart = item
        CartDAO.saveCart(cart)

        cartTotalPrice = float(cart.totalPrice)

        #change the cartitem matched with the selected product
        cartitem_qset = CartDAO.getACartItemByProduct(cart, product)
        # cartitem_qset = CartItem.objects.filter(cart = cart, item = product) #cartitem query set ONLY 1
          
        totalPrice = float(product.price) * quantity
        if cartitem_qset.count() == 0: #does not exist
            cartitem = CartDAO.createCartItem(cart, product, quantity, totalPrice)
            CartDAO.saveCartItem(cartitem)

        else: #exists so add more
            for cartitem in cartitem_qset:
                #save the new quantity
                cartitemquantity = int(cartitem.quantity)
                cartitemquantity += quantity
                cartitem.quantity = cartitemquantity

                #save the new totalPrice
                cartitem.totalPrice = cartitem.price * cartitem.quantity
                CartDAO.saveCartItem(cartitem)

        #add totalprice to carttotal
        cartTotalPrice += totalPrice
        cart.totalPrice = cartTotalPrice
        CartDAO.saveCart(cart)

        context = {"product":product}
        return render(request,'productdetailpage/productdetail.html',context)
 
class cartPage(LoginRequiredMixin, View):
    login_url='../login/'
    def get(self, request):
        user = request.user

        cart_qset = CartDAO.getFreeCartByUser(user) #get the ONLY cart
        #if none then create new cart
        cart = CartDAO.createCartByUser(user)
        
        for item in cart_qset:
            cart = item
        CartDAO.saveCart(cart)
        
        cartitem_qset = CartDAO.getAllCartItem(cart)
        
        context = { "cart":cart
            ,"cartitem_set":cartitem_qset}

        return render(request,'cartpage/cart.html',context)

    # def delete(self, request, cartitem_id):
    #     return HttpResponse(cartitem_id)

class cartItemDelete(LoginRequiredMixin, View):
    login_url='../login/'
    def post(self, request, id):
        user = request.user
        
        cartItem = CartDAO.getACartItemByID(id)
        cart_qset = CartDAO.getFreeCartByUser(user)
        for item in cart_qset:
            cart = item

        cartItemTotalPrice = float(cartItem.totalPrice)
        cartTotalPrice = float(cart.totalPrice) 
        cartTotalPrice -= cartItemTotalPrice
        
        cart.totalPrice = cartTotalPrice
        CartDAO.saveCart(cart)

        CartDAO.deleteCartItem(cartItem)
        return JsonResponse({'result' : 'ok', 'cartTotal' : str(cartTotalPrice)}, status=200)

class cartItemQuantityChange(LoginRequiredMixin, View):
    login_url = '../login'
    def post(self,request,id, quantity):
        user = request.user
            
        cartItem = CartDAO.getACartItemByID(id)
        cart_qset = CartDAO.getFreeCartByUser(user)

        for item in cart_qset:
            cart = item

        #save new cartitem quantity AND totalprice
        cartItemTotalPriceNew = float(cartItem.price) * int(quantity)
        cartItem.quantity = int(quantity)
        cartItem.totalPrice = cartItemTotalPriceNew
        CartDAO.saveCartItem(cartItem)

        #also update the cart
        cartTotalPrice = 0.0
        cartItem_qset = CartDAO.getAllCartItem(cart)
        for cartItem in cartItem_qset:
            cartTotalPrice += float(cartItem.totalPrice)

        cart.totalPrice = cartTotalPrice
        CartDAO.saveCart(cart)

        return JsonResponse({'result':'ok', 'cartItemTotal': str(cartItemTotalPriceNew),
        'cartTotal': str(cartTotalPrice)}, status=200)
        

class checkoutPage(LoginRequiredMixin, View):
    login_url='../login/'
    def get(self,request):
        user = request.user

        cart_qset = CartDAO.getFreeCartByUser(user)
        #if none then create new cart
        cart = CartDAO.createCartByUser(user)
        for item in cart_qset:
            cart = item
        CartDAO.saveCart(cart)

        cartitem_qset = CartDAO.getAllCartItem(cart)
        
        context = { "cart":cart
            ,"cartitem_set":cartitem_qset}

        return render(request,'checkoutpage/checkout.html', context)
    
    def post(self,request):
        user = request.user

        cart_qset = CartDAO.getFreeCartByUser(user)
        for item in cart_qset:
            cart = item

        cardHolder = "card holder:"+str(request.POST.get('card_holder'))
        expirationMonth = "expiration month:"+str(request.POST.get('expiration_month'))
        expirationYear = "expiration year:"+str(request.POST.get('expiration_year'))
        cardNumber = "card number:"+str(request.POST.get('card_number'))
        cvc = "cvc:"+str(request.POST.get('cvc'))
        shipping_address = str(request.POST.get('address'))

        separator = ', '
        data = [cardHolder, expirationMonth, expirationYear, cardNumber, cvc]
        order_description = separator.join(data)

        order_total = cart.totalPrice

        order = OrderDAO.createOrder(user, cart, shipping_address, 
        order_description, order_total)
        
        try:
            OrderDAO.saveOrder(order)
        except:
            return HttpResponse("Order failed!")
            
        #succeed
        CartDAO.setOrdered(cart, True)
        CartDAO.saveCart(cart)
        # return HttpResponse("hehe")
        return render(request,'successpage/success.html')

class successPage(View):
    def get(self, request):
        return render(request, 'successpage/success.html')

class orderPage(LoginRequiredMixin, View):
    login_url='../login/'
    def get(self, request):
        user = request.user

        order_qset = OrderDAO.getAllOrderByUser(user)
        context = {"orderList": order_qset}
        return render(request, 'orderpage/order.html', context)

class orderDetailPage(LoginRequiredMixin, View):
    login_url='../login/'
    def get(self, request, order_id):
        order = OrderDAO.getOrderByID(order_id)
        cart = order.cart

        cartitem_qset = CartDAO.getAllCartItem(cart)

        context={"cart": cart, "cartitem_set": cartitem_qset, "order": order}
        return render(request, 'orderdetailpage/orderdetail.html', context)

#rest
class getAllProductAPIView(APIView):
    def get(self, request):
        list_product = ProductDAO.getActiveProduct()
        mydata = GetAllProductSerializer(list_product, many=True)
        return Response(data=mydata.data, status=status.HTTP_200_OK)
    
    def post(self, request): #post a new product
        mydata = GetAllProductSerializer(data=request.data)

        if not mydata.is_valid():
            return Response("sai du lieu", status=status.HTTP_400_BAD_REQUEST)

        title = mydata.data.get('title')
        description = mydata.data.get('description')
        category_id = mydata.data.get('category')
        product_img = mydata.data['product_img']
        price = mydata.data['price']
        active = mydata.data['active']
        newProd = ProductDAO.createProduct(title=title, description=description, category_id=category_id,
        product_img=product_img, price=price, active=active)
        return Response(data=newProd.id, status=status.HTTP_200_OK)

class getAProductAPIView(APIView):
    def get(self, request, product_id):
        product = ProductDAO.getProductByID(product_id)
        mydata = GetAllProductSerializer(product)
        return Response(data=mydata.data, status=status.HTTP_200_OK)

class getAllCategoryAPIView(APIView):
    def get(self, request):
        list_category = CategoryDAO.getActiveCategory()
        mydata = GetAllCategorySerializer(list_category, many=True)
        return Response(data=mydata.data, status=status.HTTP_200_OK)

class getACategoryAPIView(APIView):
    def get(self, request, category_id):
        category = CategoryDAO.getCategoryByID(category_id)
        mydata = GetAllCategorySerializer(category)
        return Response(data=mydata.data, status=status.HTTP_200_OK)

class getAllUserAPIView(APIView):
    def get(self, request):
        list_user = UserDAO.getAllUser()
        mydata = GetAllUserSerializer(list_user, many=True)
        return Response(data=mydata.data, status=status.HTTP_200_OK)

class getAUserAPIView(APIView):
    def get(self, request, user_id):
        user = UserDAO.getUserByID(user_id)
        mydata = GetAllUserSerializer(user)
        return Response(data=mydata.data, status=status.HTTP_200_OK)

class getAllCartAPIView(APIView):
    def get(self, request):
        list_cart = CartDAO.getAllCart()
        mydata = GetAllCartSerializer(list_cart, many=True)
        return Response(data=mydata.data, status=status.HTTP_200_OK)

class getCartByUserAPIView(APIView):
    def get(self, request, user_id):
        user = UserDAO.getUserByID(user_id)
        list_cart = CartDAO.getAllCartByUser(user)
        mydata = GetAllCartSerializer(list_cart, many=True)
        return Response(data=mydata.data, status=status.HTTP_200_OK)

class getAllCartItemAPIView(APIView):
    def get(self, request, cart_id):
        list_cartitem = CartDAO.getAllCartItem(cart_id)
        mydata = GetAllCartItemSerializer(list_cartitem, many=True)
        return Response(data=mydata.data, status=status.HTTP_200_OK)

class getAllOrderAPIView(APIView):
    def get(self, request):
        list_order = OrderDAO.getAllOrder()
        mydata = GetAllOrderSerializer(list_order, many=True)
        return Response(data=mydata.data, status=status.HTTP_200_OK)

class getOrderByUserAPIView(APIView):
    def get(self, request, user_id):
        user = UserDAO.getUserByID(user_id)
        list_order = OrderDAO.getAllOrderByUser(user)
        mydata = GetAllOrderSerializer(list_order, many=True)
        return Response(data=mydata.data, status=status.HTTP_200_OK)