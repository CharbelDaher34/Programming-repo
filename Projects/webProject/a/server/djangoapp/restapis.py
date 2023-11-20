import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        status_code = response.status_code  # Move this line inside the try block
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)  # Move this line inside the try block
        return json_data
    except Exception as e:  # Catch specific exceptions if possible
        # If any error occurs
        print("Network exception occurred:", e)
        return None

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, dealer_id=None,st=None):
    results = []
  
    json_result = get_request(url)  
    if json_result:
        if dealer_id is None and st is None:
            for dealer in json_result:
                dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                       id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                       short_name=dealer["short_name"],
                                       st=dealer["st"], zip=dealer["zip"])
                results.append(dealer_obj)
        elif dealer_id and st is None:
            for dealer in json_result:
                if dealer["id"] == int(dealer_id):
                    dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                           id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                           short_name=dealer["short_name"],
                                           st=dealer["st"], zip=dealer["zip"])
                    results.append(dealer_obj)
        elif st and dealer_id is None:
            for dealer in json_result:
                if dealer["st"] == int(st):
                    dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                           id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                           short_name=dealer["short_name"],
                                           st=dealer["st"], zip=dealer["zip"])
                    results.append(dealer_obj)                       
    return results
import random

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealers_review_from_cf(url):
    # Make the GET request
    response = requests.get(url)
    json_data = json.loads(response.text)

    sentiments = ["positive", "negative", "neutral"]

    # Check if the response is a list of reviews
    if isinstance(json_data, list):
        # Create a list of DealerReview objects
        reviews = []
        for review_data in json_data:

            review = DealerReview(
                dealership=review_data['dealership'],
                name=review_data['name'],
                purchase=review_data['purchase'],
                review=review_data['review'],
                purchase_date=None,  # You may need to extract this from your JSON data
                car_make=None,  # You may need to extract this from your JSON data
                car_model=None,  # You may need to extract this from your JSON data
                car_year=None,  # You may need to extract this from your JSON data
                sentiment=analyze_review_sentiments(review_data['review']),  # You may need to calculate this based on the review text
                id=review_data['id']
            )
            reviews.append(review)

        return reviews
    else:
        # Handle the case where the response is not a list
        return None
 





# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



def analyze_review_sentiments(text):

        return "positive"



    


