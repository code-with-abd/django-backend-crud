from django.urls import path
from django.conf.urls.static import static

from geeks_site import settings
from .views import items_view
from .views import auth_view
from .views import categories_view
 
urlpatterns = [
    path('', items_view.ApiOverview, name='home'),
    path('items', items_view.items, name='get-items'),
    path('item/add', items_view.add_items, name='add-items'),
    path('item/update/<str:id>', items_view.update_item, name='update-items'),
    path('item/delete/<str:id>', items_view.delete_item, name='delete-items'),
    path('categories', categories_view.categories, name='get-categories'),
    path('categories/add', categories_view.add_category, name='add-category'),
    path('categories/delete/<str:id>', categories_view.delete_category, name='delete-category'),
    path('sign_in', auth_view.sign_in, name='sign-in'),
    path('log_out', auth_view.log_out, name='log-out'),
    path('sign_up', auth_view.sign_up, name='sign-up'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
