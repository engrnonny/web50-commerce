from django.contrib import admin

from .models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']


class AuctionAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'description', 'lister', 'date_added', 'image', 'starting_bid', 'current_price', 'closed']


class BidAdmin(admin.ModelAdmin):
    list_display = ['user', 'bid', 'auction']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['auction', 'message', 'user']


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category']


admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Category, CategoryAdmin)
