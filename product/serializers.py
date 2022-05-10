from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields=('id', 'title', 'slug', 'description', 'active')

class GetAllProductSerializer(serializers.ModelSerializer):
    # category_id = CategorySerializer(source='category')
    category_detail = CategorySerializer(source='category',read_only = True)
    
    class Meta:
        model = Product
        fields="__all__"

    # def to_representation(self, instance):
    #     self.fields['category'] =  CategorySerializer(read_only=True)
    #     return super(GetAllProductSerializer, self).to_representation(instance)

class GetAllCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields=('id', 'title', 'slug', 'description', 'active')

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields=('id', 'title', 'description', 'category', 'product_img', 'price', 'active')

    def to_representation(self, instance):
        self.fields['category'] =  CategorySerializer(read_only=True)
        return super(ProductSerializer, self).to_representation(instance)
        
    # title = serializers.CharField(max_length=255)
    # description = serializers.CharField(max_length=255)
    # # category = serializers.PrimaryKeyRelatedField()
    # product_img = serializers.CharField(max_length=255)
    # price = serializers.FloatField(default=0)
    # active = serializers.BooleanField(default=True)
