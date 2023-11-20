
from django.shortcuts import render
from .models import CarModel
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.http import JsonResponse
import random
from .restapis import get_dealers_from_cf,get_dealers_review_from_cf
# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context={}
    if request.method == 'GET':
        
        return render(request, 'djangoapp/about.html',context)

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context={}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact_us.html',context)
# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...


def login_request(request):
    context = {}
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            url = "http://localhost:3000/api/dealerships/get"
             # Get dealers from the URL
            dealerships = get_dealers_from_cf(url)
     
                 
             # Create a dictionary to hold the data
            context = {
                 'dealership_list': dealerships
            }
            return render(request, 'djangoapp/index.html', context)
    
    # If authentication fails or it's a GET request, render the index.html template
    return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    # Get the user object based on session id in request
    context={}
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return render(request, 'djangoapp/index.html', context)
# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context={}

    if (request.method == 'GET'):
        return render(request,'djangoapp/registration.html',context)
    elif (request.method == 'POST'):
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        user_exist=False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return render(request,"djangoapp/index.html",context)
        else:
            return render(request,"djangoapp/index.html",context)
       
# Update the `get_dealerships` view to render the index page with a list of dealerships

def get_dealerships(request):
    if request.method == "GET":
        url = "http://localhost:3000/api/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)

            
        # Create a dictionary to hold the data
        context = {
            'dealership_list': dealerships
        }
        # Return a JSON response
        return render(request, 'djangoapp/index.html', context)
    
def get_dealership_id(request,dealer_id):
    if request.method == "GET":
        url = f"http://localhost:3000/api/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url,dealer_id=dealer_id)

        # Create a dictionary to hold the data
        response_data = {
            'dealerships': dealerships
        }
        # Return a JSON response
        return HttpResponse(dealerships)



# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == 'GET':
        url = f"http://localhost:5000/api/get_reviews/{dealer_id}"
        reviews = get_dealers_review_from_cf(url)
        context={}
        context['reviews']=reviews
        context['dealer_id']=dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
import requests  # Import the requests library for making HTTP requests
from django.http import JsonResponse
from datetime import datetime
import datetime
from dateutil import parser
def add_review(request, dealer_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            # User is authenticated, you can proceed with your logic here
            
            url= "http://localhost:5000/api/post_review"  # Replace with the actual URL of the other function
            cars = CarModel.objects.get(id=request.POST.get("car"))
            purchase_date= request.POST.get("purchasedate").replace("/","-")
            # # Define the data you want to send to the other function, including required fields
            review = {
                "id":cars.id,
                "name":request.user.username,  # Assuming you want to use the authenticated user's name
                "dealership" : float(cars.dealer_id),                
                "review": request.POST.get("review"),  # Extract the review from the POST request
                "purchase": request.POST.get("purchasecheck"),  # Extract purchase info from POST
                "purchase_date":purchase_date,  # Extract purchase date from POST
                "car_make": cars.make.name,  # Extract car make from POST
                "car_model": cars.type,  # Extract car model from POST
                "car_year": cars.year,  # Extract car year from POST
            }
            review=json.dumps(review,default=str)

        
            try:
                # Make an HTTP POST request to the other function's URL

                response = requests.post(url, json=review)

    
                if response.status_code == 201:
                    # Successfully posted the review via the other function
                    return JsonResponse({"message": "Review posted successfully"}, status=201)
                else:
                    # Handle the case where the other function returns an error status code
                    return JsonResponse({"error": "Failed to post review"}, status=500)
    
            except Exception as e:
                # Handle exceptions if the HTTP request fails
                return JsonResponse({"error": str(e)}, status=500)
        if request.method=="GET":
            cars = CarModel.objects.filter(dealer_id=dealer_id)
            context={}
            context["cars"] = cars
            context["dealer_id"] = dealer_id
            return render(request,"djangoapp/add_review.html",context)
            

            


    else:
        # User is not authenticated, handle this case as needed
        return JsonResponse({"error": "User is not authenticated"}, status=401)

def post_review_view(request,dealer_id):
    context={}
    context['dealer_id'] =dealer_id
    return render(request,"djangoapp/add_review.html",context)

