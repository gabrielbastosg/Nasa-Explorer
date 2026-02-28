from django.urls import path
from . import views



urlpatterns = [
    path('', views.apod_view, name='apod_view'),  # <- adicionamos name
    path('home/', views.home, name='home'),
    path('add_favorite/', views.add_favorite, name='add_favorite'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('remove_favorite/<int:fav_id>/', views.remove_favorite, name='remove_favorite'),
    path('history/', views.history_list, name='history_list'),
    path('limpar_historico/',views.limpar_historico, name='limpar_historico'),
    path("like/<int:history_id>/", views.like_apod, name="like_apod"),
    path('random/', views.random_apod, name='random_apod'),
]