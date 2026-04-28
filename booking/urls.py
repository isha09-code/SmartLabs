from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.equipment_list, name='home'),
    path('book/<int:id>/', views.book_equipment, name='book_equipment'),
    path('success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('book-lab/', views.book_lab, name='book_lab'),
    path('lab-success/<int:id>/', views.lab_booking_success, name='lab_booking_success'),
    path('history/', views.booking_history, name='history'),
]