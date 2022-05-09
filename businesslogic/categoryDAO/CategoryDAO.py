from product.models import Category

class CategoryDAO():
    def getActiveCategory():
        categoryList = Category.objects.filter(active=True)
        return categoryList

    def getCategoryByID(category_id):
        category_qset = Category.objects.get(pk=category_id, active=True)
        return category_qset
