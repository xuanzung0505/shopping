from rest_framework import serializers
from .models import CustomerUser

class GetAllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields=('id', 'username', 'phone_number', 'address')
