from django.urls import path
from . import views

app_name = 'plants'

urlpatterns = [
    path('all/', views.all_plants_view, name='all_plants_view'),
    path('<plant_id>/detail/', views.details_view, name='details_view'),
    path('new/', views.add_plant, name='add_plant'),
    path('<plant_id>/update/', views.update_plant, name='update_plant'),
    path('<plant_id>/delete/', views.delete_plant, name='delete_plant'),
    path('search/', views.search_plant, name='search_plant'),
]