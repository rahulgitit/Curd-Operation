from rest_framework import serializers
from ..models import Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, error_messages={"required": "title is required."})
    description = serializers.CharField(required=True, error_messages={"required": "desicription is required."})
    conplete = serializers.CharField(required=True, error_messages={"required": "True and false is required."})

    # password = serializers.CharField(
    #     write_only=True, error_messages={"required": "password is required."}
    # )
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at'] 


        
class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(
        required=True, error_messages={"required": "Username is required."}
    )
    email = serializers.EmailField(
        required=True, error_messages={"required": "Email is required."}
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return data