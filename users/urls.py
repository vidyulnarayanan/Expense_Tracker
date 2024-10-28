from django.urls import path
from .views import RegisterView, LoginView,logout_view  

urlpatterns = [
    path('', LoginView.as_view(), name='home'), 
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

]