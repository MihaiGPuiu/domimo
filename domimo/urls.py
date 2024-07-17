from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Render the home template as the homepage
    path('apartamente/', views.display_columns, name='display_columns'),  # URL pattern for displaying apartments
    path('search/', views.display_columns, name='search'),  # Search page (assuming it uses display_columns view)
    path('favorites/', views.favorites, name='favorites'),  # Favorites page
    path('submit_form/', views.submit_form, name='submit_form'),  # URL for form submission
    path('form/', views.form_view, name='form'),  # Render the form template
    path('ajax_is_favorite/', views.ajax_is_favorite, name='ajax_is_favorite'),  # AJAX endpoint for marking favorite
    path('login/', views.login_view, name='login_view'),  # URL pattern for handling user login
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('toggle_favorite/<int:apartment_id>/', views.toggle_favorite, name='toggle_favorite'),
]
