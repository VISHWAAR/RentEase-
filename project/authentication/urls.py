from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Import views from the current app
#from .views import CustomLoginView

urlpatterns = [
    path('signup/', views.signup, name='signup'),  # URL for signup
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # URL for logout
]
