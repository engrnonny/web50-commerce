from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-listing", views.new_listing, name="new-listing"),
    path("listings/<slug>", views.listing, name="listing"),
    path("add-or-delete-watchlist/<slug>", views.add_or_delete_watchlist, name="add-or-delete-watchlist"),
    path("listings/<slug>/bid", views.bid, name="bid"),
    path("listings/<slug>/close", views.close_listing, name="close-listing"),
    path("listings/<slug>/comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<slug>", views.category, name="category")
]
