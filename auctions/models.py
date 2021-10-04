from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"


class Auction(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    lister = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    starting_bid = models.IntegerField()  
    current_price = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return f"{self.title}"
        # return f"{self.title}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.IntegerField(default=0)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"{self.user}"

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.auction}"

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auction = models.ManyToManyField(Auction)
    
    def __str__(self):
        return f"{self.user}"