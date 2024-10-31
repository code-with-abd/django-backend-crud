
from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.ApiOverview, name='home'),
    path('create_item/', views.add_items, name='add-items'),
    path('update_item/<str:id>/', views.add_items, name='update-items'),
]
