from rest_framework import viewsets
from account.models import Account
from account.serializers import LoginSerializers,Signup_serializers,AccountSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CSRFTokenView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({'csrfToken': get_token(request)})
    
@method_decorator(csrf_exempt, name='dispatch')
class UserDataViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

@method_decorator(csrf_exempt, name='dispatch')
class SignupView(APIView):
    def post(self, request):
        serializer = Signup_serializers(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username'] # type: ignore
            email = serializer.validated_data['email'] # type: ignore
            phone_no=serializer.validated_data['phone_no'] # type: ignore
            address=serializer.validated_data['address'] # type: ignore
            password = serializer.validated_data['password'] # type: ignore
            user = Account.objects.create(username=username, email=email, phone_no=phone_no, address = address,password = password)
            
            if user is not None:
                return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
                # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializers(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username'] # type: ignore
            email = serializer.validated_data['email'] # type: ignore
            phone_no=serializer.validated_data['phone_no'] # type: ignore
            address=serializer.validated_data['address'] # type: ignore
            password = serializer.validated_data['password'] # type: ignore
            user = Account.objects.filter(username=username, email=email, phone_no=phone_no, address = address, password = password)
            if user is not None:
                return Response({"message": "User logged in successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


