from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-listing", views.new_listing, name="new-listing"),
    path("listing/<slug>", views.listing, name="listing"),
    path("add-or-delete-wishlist/<slug>", views.add_or_delete_wishlist, name="add-or-delete-wishlist")
]
