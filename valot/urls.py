from django.urls import path
from . import views

from django.urls import path
from . import views  

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('', views.huoneet_lista, name='huoneet_lista'),
    path('huone/<int:huone_id>/', views.valojen_hallinta, name='valojen_hallinta'),
    path('valo/<int:valo_id>/muuta/', views.muuta_valon_tila, name='muuta_valon_tila'),
    path('', views.huoneet_lista, name='huoneet_lista'),
    path('lisaa-huone/', views.lisaa_huone, name='lisaa_huone'),
    path('poista-huone/<int:huone_id>/', views.poista_huone, name='poista_huone'),
    path('lisaa-valo/', views.lisaa_valo, name='lisaa_valo'),
    path('poista-valo/<int:valo_id>/', views.poista_valo, name='poista_valo'),
]