from django.contrib.auth.models import User
from django.db import models

class Auction(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    lister = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
#image
class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    starting_bid = models.IntegerField(default=0)  
    current_price = models.IntegerField(default=0)
class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    comment = models.TextField()

class Wishlist(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    auction = models.ManyToManyField(Auction)