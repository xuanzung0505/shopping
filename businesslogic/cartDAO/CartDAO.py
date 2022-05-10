from cart.models import Cart, CartItem

class CartDAO():

    def createCartByUser(user):
        cart = Cart(user=user)
        return cart

    def getAllCart():
        cart_qset = Cart.objects.all() #get the ONLY cart
        return cart_qset

    def getFreeCartByUser(user):
        cart_qset = Cart.objects.filter(user = user, is_ordered = False) #get the ONLY cart
        return cart_qset

    def getAllCartByUser(user):
        cart_qset = Cart.objects.filter(user = user) #get the ONLY cart
        return cart_qset

    def getACartItemByID(id):
        cartItem = CartItem.objects.get(id = id)
        return cartItem

    def getACartItemByProduct(cart, product):
        cartitem_qset = CartItem.objects.filter(cart = cart, item = product) #cartitem query set ONLY 1
        return cartitem_qset

    def createCartItem(cart, product, quantity, totalPrice):
        cartitem = CartItem(cart = cart, item = product, price = product.price, quantity = quantity, totalPrice = totalPrice) 
        return cartitem

    def getAllCartItem(cart):
        cartitem_qset = CartItem.objects.filter(cart = cart) #get all cartitems in that cart
        return cartitem_qset

    def setOrdered(cart, ordered):
        cart.is_ordered = ordered

    def saveCart(cart):
        cart.save()

    def saveCartItem(cartItem):
        cartItem.save()

    def deleteCartItem(cartItem):
        cartItem.delete()
