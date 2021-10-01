from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *


def index(request):
    active_listings = Auction.objects.all().order_by('title')
    context = {
        "active_listings": active_listings
    }
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# New Listing Page
# New Listing Page
# New Listing Page
def new_listing(request):
    if request.method == "POST":        
        title = request.POST["title"]   
        description = request.POST["description"]   
        category = request.POST["category"]   
        bid = request.POST["bid"]   
        image = request.POST["image"]
        
        if request.user.is_authenticated:
            user = request.user
            try:
                listing = Auction(title=title, description=description, category=category, image=image, lister=user)
                listing.save()
                listing_bid = Bid(auction=listing, starting_bid=bid)
                listing_bid.save()
                print(listing)
                print(listing_bid)
                return redirect( "index" )

            except IntegrityError:
                return render(request, "auctions/new-listing.html", {
                    "message": "Listing already exist"
                })

        else:
            return redirect("login")
    else:
        return render(request, "auctions/new-listing.html")