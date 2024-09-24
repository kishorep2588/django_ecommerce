from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:name>/', views.category_view, name='category')
]
