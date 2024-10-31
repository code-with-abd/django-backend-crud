
from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.ApiOverview, name='home'),
    path('items/', views.items, name='get-items'),
    path('create_item/', views.add_items, name='add-items'),
    path('update_item/<str:id>/', views.update_item, name='update-items'),
    path('delete_item/<str:id>/', views.delete_item, name='delete-items'),
    path('sign_in/', views.sign_in, name='sign-in'),
    path('sign_up/', views.sign_up, name='sign-up'),
]
