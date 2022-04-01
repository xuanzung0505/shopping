from multiprocessing import context
from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from product.models import Product, Category
from cart.models import Cart, CartItem
from order.models import Order

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.forms.models import model_to_dict
from django.core import serializers

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
        productList = Product.objects.filter(active=True)
        categoryList = Category.objects.filter(active=True)
        # print(productList.count())
        context = {"productlist":productList, "categoryList": categoryList}
        return render(request,'catalogpage/catalog.html',context)

class catalogSearch(LoginRequiredMixin, View):
    login_url='../login/'
    def post(self, request, search_query):

        product_qset = Product.objects.filter(title__icontains = search_query, active=True)
        
        qset_json = serializers.serialize('json', product_qset)

        # size = int(product_qset.count())

        return JsonResponse(qset_json, status=200, safe=False)

class catalogFilter(LoginRequiredMixin, View):
    login_url='../login/'
    def post(self, request, category_id):
        
        if(int(category_id) != 0):
            
            category = Category.objects.get(pk=category_id)
            product_qset = Product.objects.filter(category = category, active=True)
            
            qset_json = serializers.serialize('json', product_qset)
        else:
            product_qset = Product.objects.filter(active=True)
            
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
        product = Product.objects.get(pk=product_id)
        context = {"product":product}
        return render(request,'productdetailpage/productdetail.html',context)

    def post(self, request, product_id):
        product = Product.objects.get(pk=product_id)

        quantity = int(request.POST.get('quantity'))
       

        #add a cart item to cart

        #get the cart from user credentials
        user = request.user
        
        cart_qset = Cart.objects.filter(user = user, is_ordered = False) #get the ONLY cart
        #if none then create new cart
        cart = Cart(user=user)
        
        for item in cart_qset:
            cart = item
        cart.save()

        cartTotalPrice = float(cart.totalPrice)

        #change the cartitem matched with the selected product
        cartitem_qset = CartItem.objects.filter(cart = cart, item = product) #cartitem query set ONLY 1
          
        totalPrice = float(product.price) * quantity
        if cartitem_qset.count() == 0: #does not exist
            cartitem = CartItem(cart = cart, item = product, price = product.price, quantity = quantity, totalPrice = totalPrice) 
            cartitem.save()

        else: #exists so add more
            for cartitem in cartitem_qset:
                #save the new quantity
                cartitemquantity = int(cartitem.quantity)
                cartitemquantity += quantity
                cartitem.quantity = cartitemquantity

                #save the new totalPrice
                cartitem.totalPrice = cartitem.price * cartitem.quantity
                cartitem.save()

        #add totalprice to carttotal
        cartTotalPrice += totalPrice
        cart.totalPrice = cartTotalPrice
        cart.save()

        context = {"product":product}
        return render(request,'productdetailpage/productdetail.html',context)
 
class cartPage(LoginRequiredMixin, View):
    login_url='../login/'
    def get(self, request):
        user = request.user

        cart_qset = Cart.objects.filter(user = user, is_ordered = False) #get the ONLY cart
        #if none then create new cart
        cart = Cart(user=user)
        
        for item in cart_qset:
            cart = item
        cart.save()

        cartitem_qset = CartItem.objects.filter(cart = cart) #get all cartitems in that cart
        
        context = { "cart":cart
            ,"cartitem_set":cartitem_qset}

        return render(request,'cartpage/cart.html',context)

    # def delete(self, request, cartitem_id):
    #     return HttpResponse(cartitem_id)

class cartItemDelete(LoginRequiredMixin, View):
    login_url='../login/'
    def post(self, request, id):
        user = request.user
        
        cartItem = CartItem.objects.get(id = id)

        cart_qset = Cart.objects.filter(user = user, is_ordered = False) #get the ONLY cart
        for item in cart_qset:
            cart = item

        cartItemTotalPrice = float(cartItem.totalPrice)
        cartTotalPrice = float(cart.totalPrice) 
        cartTotalPrice -= cartItemTotalPrice
        
        cart.totalPrice = cartTotalPrice
        cart.save()

        cartItem.delete()
        return JsonResponse({'result' : 'ok', 'cartTotal' : str(cartTotalPrice)}, status=200)

class cartItemQuantityChange(LoginRequiredMixin, View):
    login_url = '../login'
    def post(self,request,id, quantity):
        user = request.user
            
        cartItem = CartItem.objects.get(id = id)

        cart_qset = Cart.objects.filter(user = user, is_ordered = False) #get the ONLY cart
        for item in cart_qset:
            cart = item

        #save new cartitem quantity AND totalprice
        cartItemTotalPriceNew = float(cartItem.price) * int(quantity)
        cartItem.quantity = int(quantity)
        cartItem.totalPrice = cartItemTotalPriceNew
        cartItem.save()

        #also update the cart
        cartTotalPrice = 0.0
        cartItem_qset = CartItem.objects.filter(cart = cart)
        for cartItem in cartItem_qset:
            cartTotalPrice += float(cartItem.totalPrice)

        cart.totalPrice = cartTotalPrice
        cart.save()

        return JsonResponse({'result':'ok', 'cartItemTotal': str(cartItemTotalPriceNew),
        'cartTotal': str(cartTotalPrice)}, status=200)
        

class checkoutPage(LoginRequiredMixin, View):
    login_url='../login'
    def get(self,request):
        user = request.user

        cart_qset = Cart.objects.filter(user = user, is_ordered = False) #get the ONLY cart
        #if none then create new cart
        cart = Cart(user=user)
        for item in cart_qset:
            cart = item
        cart.save()

        cartitem_qset = CartItem.objects.filter(cart = cart) #get all cartitems in that cart
        
        context = { "cart":cart
            ,"cartitem_set":cartitem_qset}

        return render(request,'checkoutpage/checkout.html', context)
    
    def post(self,request):
        user = request.user

        cart_qset = Cart.objects.filter(user = user) #get the ONLY cart
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

        order = Order(user = user, cart = cart, shipping_address = shipping_address,
        order_description = order_description, order_total = order_total)
        
        try:
            order.save()
        except:
            return HttpResponse("Order failed!")
            
        #succeed
        cart.is_ordered = True
        cart.save()
        # return HttpResponse("hehe")
        return render(request,'successpage/success.html')

class successPage(View):
    def get(self, request):
        return render(request, 'successpage/success.html')

class orderPage(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        order_qset = Order.objects.filter(user = user) #get all order
        context = {"orderList": order_qset}
        return render(request, 'orderpage/order.html', context)

class orderDetailPage(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(pk= order_id) #get all order
        cart = order.cart

        cartitem_qset = CartItem.objects.filter(cart = cart) #get all cartitems in that cart

        context={"cart": cart, "cartitem_set": cartitem_qset, "order": order}
        return render(request, 'orderdetailpage/orderdetail.html', context)