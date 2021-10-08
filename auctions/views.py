from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
            title_test = Auction.objects.filter(title=title)

            if not title_test:
                listing = Auction(title=title, description=description, category=category, image=image, lister=user, starting_bid=bid)
                listing.save()
                print(listing)
                return redirect( "index" )

            else:
                return render(request, "auctions/new-listing.html", {
                    "message": "Listing already exist"
                })            

        else:
            return redirect("login")
    else:
        return render(request, "auctions/new-listing.html")



# New Listing Page
# New Listing Page
# New Listing Page
def listing(request, slug):
    listing = Auction.objects.get(title=slug)
    user = request.user
    if user.is_authenticated:
        if Wishlist.objects.filter(user=user).exists():
            wishlist = Wishlist.objects.get(user=user)
            if Auction.objects.filter(wishlist__id=wishlist.id, title=listing.title).exists():
                return render(request, "auctions/listing.html", 
                context = {
                    'auction_in_wishlist': 'yes',
                    'listing': listing
                })
            else:
                return render(request, "auctions/listing.html", 
                context = {
                    'listing': listing
                })
        else:
            return render(request, "auctions/listing.html", 
            context = {
                'listing': listing
            })

    else:
        context = {
            'listing': listing
        }
        return render(request, "auctions/listing.html", context)

# Add or Delete to wishlist
# Add or Delete to wishlist
# Add or Delete to wishlist
@login_required
def add_or_delete_wishlist(request, slug):
    listing = Auction.objects.get(title=slug)
    if Wishlist.objects.filter(user=request.user).exists():
        wishlist = Wishlist.objects.get(user=request.user)
        auction_in_wishlist = Auction.objects.filter(wishlist__id=wishlist.id, title=listing.title)
        if auction_in_wishlist:
            wishlist.auctions.remove(listing)
        else:
            wishlist.auctions.add(listing)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        wishlist = Wishlist(user=request.user)
        wishlist.save()
        wishlist.auctions.add(listing)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
