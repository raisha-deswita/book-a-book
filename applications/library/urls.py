from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'library'

urlpatterns = [
    path('', views.index, name='index'), # Halaman utama
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/home/', views.dash_home, name='dash_home'),

    # Authentication
    path('registration/', views.registration, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='library/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Inventory
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
]