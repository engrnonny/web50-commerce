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
    lister = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    starting_bid = models.FloatField(blank=True, null=True)
    current_price = models.FloatField(blank=True, null=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"
        # return f"{self.title}"


class Bid(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    bid = models.IntegerField(default=0)
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.user}"


class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    message = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.auction}"


class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auctions = models.ManyToManyField(Auction)

    def __str__(self):
        return f"{self.user} - {self.auctions}"


class Category(models.Model):
    category = models.CharField(max_length=255)
