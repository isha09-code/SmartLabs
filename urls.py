from django.contrib import admin
from django.urls import path
from booking import views

urlpatterns = [

    # 🔧 Admin
    path('admin/', admin.site.urls),

    # 🔐 Login / Logout
    path('', views.login_view, name='login'),      # default
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 🏠 Home
    path('home/', views.equipment_list, name='home'),

    # 📦 Equipment Booking
    path('book/<int:id>/', views.book_equipment, name='book_equipment'),
    path('success/<int:booking_id>/', views.booking_success, name='booking_success'),

    # 🏫 Teacher Lab Booking
    path('book-lab/', views.book_lab, name='book_lab'),
    path('lab-success/<int:id>/', views.lab_booking_success, name='lab_booking_success'),

    # 📜 History
    path('history/', views.booking_history, name='history'),
]