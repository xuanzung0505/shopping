from order.models import Order

class OrderDAO():

    def getAllOrder():
        order_qset = Order.objects.all() #get all order
        return order_qset

    def getAllOrderByUser(user):
        order_qset = Order.objects.filter(user = user) #get all order
        return order_qset

    def getOrderByID(order_id):
        order = Order.objects.get(pk= order_id)
        return order

    def createOrder(user, cart, shipping_address, order_description, order_total):
        order = Order(user = user, cart = cart, shipping_address = shipping_address,
        order_description = order_description, order_total = order_total)
        return order

    def saveOrder(order):
        order.save()