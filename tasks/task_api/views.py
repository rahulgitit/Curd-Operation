from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import  BasicAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from tasks.models import Task
from tasks.task_api.serializers import TaskSerializer, SignUpSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CSRFTokenView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({'csrfToken': get_token(request)})
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

class SignUpView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username'] # type: ignore
            email = serializer.validated_data['email'] # type: ignore
            password = serializer.validated_data['password'] # type: ignore
            if not username and not email and not password:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            # if not request.data.get('email') or not request.data.get('username'):
            #     return Response(
            #         {'error': 'Email and username are required'},
            #         status=status.HTTP_400_BAD_REQUEST
            #     )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username'] # type: ignore
            password = serializer.validated_data['password'] # type: ignore
            if not username or not password:
                return Response(
                    {'error': 'Username and password are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({
                    'message':'Login successful',
                    'status':status.HTTP_201_CREATED
                })
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def logoutView(request):
    logout(request)
    return Response("you are logout!!")

# API ViewSet
@method_decorator(csrf_exempt, name='dispatch')
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticatedOrReadOnly]


    @action(detail=False, methods=['get'])
    def completed(self, request):
        completed_tasks = self.get_queryset().filter(completed=True)
        serializer = self.get_serializer(completed_tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        pending_tasks = self.get_queryset().filter(completed=False)
        serializer = self.get_serializer(pending_tasks, many=True)
        return Response(serializer.data)