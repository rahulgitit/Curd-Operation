from rest_framework import serializers
from account.models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    
class Signup_serializers(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    phone_no = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=150)


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    phone_no = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=150)
