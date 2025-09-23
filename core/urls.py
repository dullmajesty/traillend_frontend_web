from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("login/", views.admin_login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("verify_reset_code/", views.verify_reset_code, name="verify_reset_code"),
    path("reset_password/", views.reset_password, name="reset_password"),
    
    
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/create/', views.inventory_createitem, name='inventory-createitem'),
    path('inventory/edit/<int:item_id>/', views.inventory_edit, name='inventory_edit'),
    path('inventory/delete/<int:item_id>/', views.inventory_delete, name='inventory_delete'),
    path('inventory/<int:item_id>/', views.inventory_detail, name='inventory_detail'),
    path('inventory/block_date/<int:item_id>/', views.block_date, name='block_date'),


    path('verification/', views.verification, name='verification'),
    path('history/', views.history_log, name='history_log'),
    path('damage/', views.damage_report, name='damage_report'),
    path('statistics/', views.statistics, name='statistics'),
    path('change-password/', views.change_pass, name='change_pass'),
    path('list_of_users/', views.list_of_users, name='list_of_users'),
    path('logout/', views.logout, name='logout'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
