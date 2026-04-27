from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/<user_name>/', views.profile_view, name='profile_view')

]