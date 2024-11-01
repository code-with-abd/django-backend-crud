
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
    path('sign_in', views.sign_in, name='sign-in'),
    path('sign_up', views.sign_up, name='sign-up'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
