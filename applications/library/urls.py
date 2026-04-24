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

    # CRUD User Management (Khusus Admin)
    path('dashboard/users/', views.user_management, name='user_management'),
    path('dashboard/users/add/', views.user_add, name='user_add'),
    path('dashboard/users/edit/<int:user_id>/', views.user_edit, name='user_edit'),
    path('dashboard/users/delete/<int:user_id>/', views.user_delete, name='user_delete'),

    # Inventory
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('inventory/add/', views.book_add, name='book_add'),
    path('inventory/edit/<int:book_id>/', views.book_edit, name='book_edit'),
    path('inventory/delete/<int:book_id>/', views.book_delete, name='book_delete'),

    # Transactions
    path('dashboard/inventory/', views.inventory_management, name='inventory_management'),
    path('book/<int:book_id>/request/', views.request_borrow, name='request_borrow'),
    path('borrowing/<int:borrowing_id>/return/', views.return_book, name='return_book'),
    path('borrowing/<int:borrowing_id>/<str:action>/', views.process_borrow_request, name='process_borrow'),
    path('dashboard/explore/', views.dashboard_book_list, name='dash_book_list'),

    # CRUD Category
    path('dashboard/categories/', views.category_management, name='category_management'),
    path('dashboard/categories/add/', views.category_add, name='category_add'),
    path('dashboard/categories/edit/<int:cat_id>/', views.category_edit, name='category_edit'),
    path('dashboard/categories/delete/<int:cat_id>/', views.category_delete, name='category_delete'),

    # CRUD Book_Item
    path('inventory/book/<int:book_id>/items/', views.book_items_manage, name='book_items_manage'),
    path('inventory/item/edit/<int:item_id>/', views.book_item_edit, name='book_item_edit'),
    path('inventory/item/delete/<int:item_id>/', views.book_item_delete, name='book_item_delete'),

    # Fine processing modules
    path('dashboard/fines/', views.fine_management, name='fine_management'),
    path('fines/<int:record_id>/pay/', views.pay_fine, name='pay_fine'),

    # Management
    path('dashboard/loans/', views.loan_management, name='loan_management'),

    # Export CSV
    path('dashboard/loans/export/', views.export_loans_csv, name='export_loans'),
]