from product.models import Product, Category

class ProductDAO():
    def createProduct(title, description, category_id, product_img, price, active):
        newProd = Product.objects.create(title=title, description=description, 
        category=Category.objects.get(pk=category_id), product_img=product_img, price=price, active=active)
        return newProd

    def getActiveProduct():
        productList = Product.objects.filter(active=True)
        return productList

    def searchActiveProductByName(search_query):
        product_qset = Product.objects.filter(title__icontains = search_query, active=True)
        return product_qset

    def searchActiveProductByCategory(category):
        product_qset = Product.objects.filter(category = category, active=True)
        return product_qset

    def getProductByID(product_id):
        product = Product.objects.get(pk=product_id)
        return product