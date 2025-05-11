# urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.login_view, name='login'),
    path('user_profile/', views.user_profile_view, name='user_profile'),
    path('home/', views.home_view, name='home'),
    path('book_meeting/', views.book_meeting_view, name='book_meeting'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('product-selection/', views.product_selection_view, name='product_selection'),
     path('contract/pdf/', views.contract_preview_view, name='contract_preview_view'),
     

]
