from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout/", views.logout_view, name="logout"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path('map/', views.map, name="map"),
    path('marker/<str:problemid>', views.viewmarker, name='viewmarker')

]
