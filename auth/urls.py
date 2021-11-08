
from django.urls import path
from user import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.Home,name="home"),
    path("register/",views.Register,name='register'),
    path("login/",views.Login,name='login'),
    path("logout/",views.Logout,name='logout'),
    path("login_page/",views.LoginPage,name='loginpage'),
    path("register_page/",views.RegisterPage,name='registerpage'),
]
