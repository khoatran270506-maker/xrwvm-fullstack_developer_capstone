# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate

# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration` view to handle sign up request
# @csrf_exempt
# def registration(request):
# ...

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...


# Get all car makes and models
def get_cars(request):
    if CarMake.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = []

    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    return JsonResponse({"CarModels": cars})


def get_dealerships(request):
    """Render the homepage with the dealership list from the Node.js API."""
    from django.shortcuts import render
    from urllib.request import urlopen

    dealerships = []

    try:
        with urlopen(
            "http://127.0.0.1:3030/fetchDealers",
            timeout=10
        ) as response:
            dealerships = json.loads(
                response.read().decode("utf-8")
            )
    except Exception:
        logger.exception("Unable to retrieve dealerships from Node.js API")

    states = sorted({
        dealer.get("state", "")
        for dealer in dealerships
        if dealer.get("state")
    })
    return render(request, "Home.html", {
        "dealers": dealerships,
        "states": states,
        "selected_state": ""
    })


def get_dealers_by_state(request, state):
    """Display dealerships filtered by state."""
    from django.shortcuts import render
    from urllib.request import urlopen

    dealerships = []

    try:
        with urlopen(
            "http://127.0.0.1:3030/fetchDealers",
            timeout=10
        ) as response:
            dealerships = json.loads(
                response.read().decode("utf-8")
            )
    except Exception:
        logger.exception("Unable to retrieve dealerships from Node.js API")

    states = sorted({
        dealer.get("state", "")
        for dealer in dealerships
        if dealer.get("state")
    })

    filtered_dealers = [
        dealer for dealer in dealerships
        if dealer.get("state", "").casefold() == state.casefold()
    ]

    return render(request, "Home.html", {
        "dealers": filtered_dealers,
        "states": states,
        "selected_state": state
    })


def get_dealer_details(request, dealer_id):
    """Retrieve one dealership from the Node.js API."""
    import json
    from urllib.request import urlopen
    from django.http import JsonResponse

    try:
        url = f"http://127.0.0.1:3030/fetchDealer/{dealer_id}"
        with urlopen(url, timeout=10) as response:
            dealer_data = json.loads(response.read().decode("utf-8"))
        return JsonResponse({"status": 200, "dealer": dealer_data})
    except Exception as error:
        return JsonResponse(
            {"status": 500, "dealer": [], "error": str(error)},
            status=500
        )


def get_dealer_reviews(request, dealer_id):
    """Retrieve reviews for one dealership from the Node.js API."""
    import json
    from urllib.request import urlopen
    from django.http import JsonResponse

    try:
        url = f"http://127.0.0.1:3030/fetchReviews/dealer/{dealer_id}"
        with urlopen(url, timeout=10) as response:
            reviews_data = json.loads(response.read().decode("utf-8"))
        return JsonResponse({"status": 200, "reviews": reviews_data})
    except Exception as error:
        return JsonResponse(
            {"status": 500, "reviews": [], "error": str(error)},
            status=500
        )


def dealer_detail_page(request, dealer_id):
    """Render dealership details and its customer reviews."""
    from django.shortcuts import render
    from urllib.request import urlopen

    dealer = None
    reviews = []
    dealer_error = ""
    reviews_error = ""

    try:
        url = f"http://127.0.0.1:3030/fetchDealer/{dealer_id}"
        with urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
        dealer = data[0] if data else None
    except Exception as error:
        logger.exception("Unable to retrieve dealership details")
        dealer_error = str(error)

    try:
        url = f"http://127.0.0.1:3030/fetchReviews/dealer/{dealer_id}"
        with urlopen(url, timeout=10) as response:
            reviews = json.loads(response.read().decode("utf-8"))
    except Exception as error:
        logger.exception("Unable to retrieve dealership reviews")
        reviews_error = str(error)

    return render(request, "DealerDetails.html", {
        "dealer": dealer,
        "reviews": reviews,
        "dealer_error": dealer_error,
        "reviews_error": reviews_error,
    })


def post_review_page(request, dealer_id):
    """Display and submit a customer review for a dealership."""
    from django.shortcuts import render, redirect
    from urllib.request import Request, urlopen

    dealer = None
    error = ""

    try:
        url = f"http://127.0.0.1:3030/fetchDealer/{dealer_id}"
        with urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
        dealer = data[0] if data else None
    except Exception as exc:
        logger.exception("Unable to retrieve dealership")
        error = str(exc)

    if request.method == "POST" and dealer:
        name = request.POST.get("name", "").strip()
        review_text = request.POST.get("review", "").strip()
        purchase_date = request.POST.get("purchase_date", "")
        car_choice = request.POST.get("car_model", "")
        year = request.POST.get("year", "")

        if not all([name, review_text, purchase_date, car_choice, year]):
            error = "All details are mandatory."
        else:
            try:
                year = int(year)
                if year < 2015 or year > 2023:
                    raise ValueError("Car year must be between 2015 and 2023.")

                car_make, car_model = car_choice.split(" ", 1)
                payload = {
                    "name": name,
                    "dealership": dealer_id,
                    "review": review_text,
                    "purchase": True,
                    "purchase_date": purchase_date,
                    "car_make": car_make,
                    "car_model": car_model,
                    "car_year": year,
                }
                node_request = Request(
                    "http://127.0.0.1:3030/insert_review",
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urlopen(node_request, timeout=10):
                    pass
                return redirect(f"/dealer/{dealer_id}/")
            except Exception as exc:
                error = str(exc)

    if CarMake.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.select_related("car_make").all()

    return render(request, "PostReview.html", {
        "dealer": dealer,
        "car_models": car_models,
        "reviewer_name": (
            request.user.username if request.user.is_authenticated else ""
        ),
        "error": error,
    })
