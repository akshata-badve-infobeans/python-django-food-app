"""foodtracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from FoodTrackerApp import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView,name='index' ),  
    path('login/',views.loginView, name="login"),
    path('logout/',views.logoutView,name="logout"),  
    path('register/',views.registerView, name="register"),
    path('food_add/',views.addFoodView, name="food_add"),
    re_path(r"^(?P<pk>\d+)/$", views.FoodDetailView.as_view(), name="food_detail"),
    re_path(r"^update/(?P<pk>\d+)/$", views.FoodUpdateView.as_view(), name="update"),
    re_path(r"^delete/(?P<pk>\d+)/$", views.FoodDeleteView.as_view(), name="delete"),
    path('add_cat/', views.CreateCategoryView.as_view(), name="add_cat"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
