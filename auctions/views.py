
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *


def index(request):
    active_listings = Auction.objects.filter(closed=False).order_by('title')
    closed_listings = Auction.objects.filter(closed=True).order_by('title')
    context = {
        "active_listings": active_listings,
        "closed_listings": closed_listings
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

            if Category.objects.filter(category=category).exists():
                pass
            else:
                new_category = Category(category=category)
                new_category.save()

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
    comments = Comment.objects.filter(auction=listing).order_by('-date_added')
    user = request.user
    if user.is_authenticated:
        if Watchlist.objects.filter(user=user).exists():
            watchlist = Watchlist.objects.get(user=user)
            if Bid.objects.filter(auction=listing).order_by('-bid').exists():
                highest_bid = Bid.objects.filter(auction=listing).order_by('-bid')[0]
                if Auction.objects.filter(watchlist__id=watchlist.id, title=listing.title).exists():
                    context = {
                        'auction_in_watchlist': 'yes',
                        'comments': comments,
                        'highest_bid': highest_bid,
                        'listing': listing
                    }
                    return render(request, "auctions/listing.html", context)
                else:                    
                    context = {
                        'comments': comments,
                        'highest_bid': highest_bid,
                        'listing': listing
                    }
                    return render(request, "auctions/listing.html", context)
            else:     
                if Auction.objects.filter(watchlist__id=watchlist.id, title=listing.title).exists():
                    context = {
                        'auction_in_watchlist': 'yes',
                        'comments': comments,
                        'listing': listing
                    }
                    return render(request, "auctions/listing.html", context)
                else:                    
                    context = {
                        'comments': comments,
                        'listing': listing
                    }
                    return render(request, "auctions/listing.html", context) 
                
        else:
            if Bid.objects.filter(auction=listing).order_by('-bid').exists():
                highest_bid = Bid.objects.filter(auction=listing).order_by('-bid')[0]
                context = {
                    'comments': comments,
                    'highest_bid': highest_bid,
                    'listing': listing
                }
                return render(request, "auctions/listing.html", context)
            else:                    
                context = {
                    'comments': comments,
                    'listing': listing
                }
                return render(request, "auctions/listing.html", context) 

    else:
        context = {          
            'comments': comments,  
            'listing': listing
        }
        return render(request, "auctions/listing.html", context)


# Add or Delete to watchlist
# Add or Delete to watchlist
# Add or Delete to watchlist
@login_required
def add_or_delete_watchlist(request, slug):
    listing = Auction.objects.get(title=slug, closed=False)
    if Watchlist.objects.filter(user=request.user).exists():
        watchlist = Watchlist.objects.get(user=request.user)
        auction_in_watchlist = Auction.objects.filter(watchlist__id=watchlist.id, title=listing.title)
        if auction_in_watchlist:
            watchlist.auctions.remove(listing)
        else:
            watchlist.auctions.add(listing)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        watchlist = Watchlist(user=request.user)
        watchlist.save()
        watchlist.auctions.add(listing)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Bid for a listing
# Bid for a listing
# Bid for a listing
@login_required
def bid(request, slug):
    if request.method == 'POST':
        listing = Auction.objects.get(title=slug, closed=False)
        user_bid = int(request.POST["bid"])
        if Bid.objects.filter(auction=listing).exists():
            highest_bid = Bid.objects.filter(auction=listing).order_by('-bid')[0]
            if user_bid > highest_bid.bid and user_bid > listing.starting_bid:
                new_bid = Bid(user=request.user, auction=listing, bid=user_bid)
                new_bid.save()
                listing.current_price = user_bid
                listing.save()
                messages.info(request, "Your bid has been submitted. You are currently the highest bid.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, "Your bid must be higher than the current bid and the starting bid.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            highest_bid = Bid(user=request.user, bid=user_bid, auction=listing)
            highest_bid.save()
            listing.current_price = user_bid
            listing.save()
            messages.info(request, "Your bid has been submitted. You are currently the highest bid.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        pass


# Close a listing
# Close a listing
# Close a listing
@login_required
def close_listing(request, slug):
    listing = Auction.objects.get(title=slug, closed=False)
    listing.closed = True
    listing.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  


# Comment on a listing
# Comment on a listing
# Comment on a listing
@login_required
def comment(request, slug):
    if request.method == "POST":
        listing = Auction.objects.get(title=slug, closed=False)
        comment_message = request.POST["message"]
        comment = Comment(auction=listing, message=comment_message, user=request.user)
        comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    
    else:
        pass


# watchlist page
# watchlist page
# watchlist page
@login_required
def watchlist(request):
    if Watchlist.objects.filter(user=request.user).exists():
        watchlist = Watchlist.objects.get(user=request.user)
        
        listings = Auction.objects.filter(watchlist__id=watchlist.id)
        
        context = {
            'listings': listings
        }
        return render(request, "auctions/watchlist.html", context)

    else:
        return render(request, "auctions/watchlist.html")


# Categories page
# Categories page
# Categories page
def categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, "auctions/categories.html", context)


# Category page
def category(request, slug):
    listings = Auction.objects.filter(category=slug, closed=False)
    context = {
        'listings': listings,
        'category': slug
    }
    return render(request, "auctions/category.html", context)

