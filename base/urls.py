from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    path('authenticateImage/', views.authenticateImage, name="authenticateImage"),
    path('success/', views.upload_success, name="success"),
    path('image/<str:pk>/', views.image_page, name="image"),
    path('results/<str:pk>/', views.get_similar_results, name="similarity"),
]
 