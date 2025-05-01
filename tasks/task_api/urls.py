from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TaskViewSet, SignUpView, LoginView, CSRFTokenView,LogoutView,logout

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path("logout/",logout ),  # type: ignore
    path('csrf-token/', CSRFTokenView.as_view(), name='csrf-token'),
    path('tasks/', include(router.urls)),
] 