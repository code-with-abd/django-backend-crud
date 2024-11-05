
from django.urls import path
from django.conf.urls.static import static

from geeks_site import settings
from . import views
 
urlpatterns = [
    path('', views.ApiOverview, name='home'),
    path('items', views.items, name='get-items'),
    path('item/add', views.add_items, name='add-items'),
    path('item/update/<str:id>', views.update_item, name='update-items'),
    path('item/delete/<str:id>', views.delete_item, name='delete-items'),
    path('categories', views.categories, name='get-categories'),
    path('categories/add', views.add_category, name='add-category'),
    path('categories/delete/<str:id>', views.delete_category, name='delete-category'),
    path('sign_in', views.sign_in, name='sign-in'),
    path('log_out', views.log_out, name='log-out'),
    path('sign_up', views.sign_up, name='sign-up'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
