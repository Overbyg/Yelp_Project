from django.shortcuts import render, redirect
from django.contrib import messages
from models import Business, Review
from ..login_app.models import User #Imports User table from Login app


# Returns a list of businesses that match the users search paramaters
def index(request):
    try:
        context = {
            "business_key" : Business.objects.filter(bus_city=request.POST["bus_city"], bus_category=request.POST["bus_category"]), #.filter(bus_category=request.POST["bus_category"])
            # "rating_key" : Review.objects.filter(business=Business.objects.filter(bus_city=request.POST["bus_city"], bus_category=request.POST["bus_category"]))
        }
        return render(request, "business_app/index.html", context);
    except KeyError:
        return redirect("/search")

    # Calculates and returns average rating of business  #Placing on hold for now.
    
    # print context['rating_key'][0].comment
    # for business in context["business_key"]:
    #     count = 0
    #     sum = 0
    #     print business
    # for x in context["rating_key"]:
    #     sum += x.rating
    #     count += 1
    #     # print x
    # avg = sum/count
    # print x
    # print avg
    # print count


# This view returns the business that the user clicked on.
def bus_results(request, bus_id):
    context = {
        "bus_id" : Business.objects.get(id=bus_id),
        "rating_key" : Review.objects.filter(business=Business.objects.get(id=bus_id))
    }
    #Try/Except so no error is returned since there are no reviews for newly created businesses.
    try:
        count = 0
        sum = 0
        for x in context["rating_key"]:
            sum += x.rating
            count += 1
        avg = sum/count
        return render(request, "business_app/bus_results.html", {"context": context, "avg": avg}) #created dict to pass in 2 variables
    except ZeroDivisionError:
        return render(request, "business_app/bus_results.html", {"context": context, "avg": "No Rating Yet"})

# Form to create a new Business
def new_bus(request):
    return render(request, "business_app/new_bus.html")


# Insertion of new business into DB
def add_bus(request): 
    #This runs validation to ensure new business name/address is not blank
    errors = Business.objects.new_bus_validator(request.POST)

    if len(errors) <= 0:
        Business.objects.create(bus_name=request.POST["bus_name"], bus_address=request.POST["bus_address"], bus_city=request.POST["bus_city"], bus_category=request.POST["bus_category"], description=request.POST["description"])
        last_bus = Business.objects.last()

        return redirect("/display/bus_results/{}".format(last_bus.id)) 
    else:
        for x in errors:
            messages.error(request, errors[x])
        return redirect("/display/new_bus")

# Page with review form
def write_review(request, bus_id):
    if "id" in request.session:
        context = {
            "business_key" : Business.objects.get(id=bus_id)
        }
        return render(request, "business_app/write_review.html", context)
    else:
        messages.error(request, "You need to be logged in to leave a review. Please log in.")
        return redirect( "/display/bus_results/{}".format(bus_id))

# Handles the form data from the review page.
def add_review(request, bus_id):
    # Need to have validation here to ensure no SQL injection.
    errors = Business.objects.review_validator(request.POST)

    if len(errors) <= 0:
        Review.objects.create(comment=request.POST["review_text"], rating=request.POST["rating"], business=Business.objects.get(id=bus_id), user=User.objects.get(id=request.session["id"]))
        messages.success(request, "Thank you for your review!")
        return redirect("/display/write_review/{}".format(bus_id))
    else:
        for x in errors:
            messages.error(request, errors[x])
        return redirect("/display/write_review/{}".format(bus_id))
        

# This admin page should only be accessable to admins, need to add validation for that.
def admin(request):
    context = {
        "business_key": Business.objects.all(),
        "rating_key": Review.objects.all(),
        "user_key": User.objects.all()
    }
    return render(request, "business_app/admin.html", context)

# Destroys a business from the DB
def destroy(request, bus_id):
    Business.objects.get(id=bus_id).delete()
    return redirect("/display/admin")

#Destroys a review from the DB
def destroy_review(request, review_id):
    Review.objects.get(id=review_id).delete()
    return redirect("/display/admin")


#Destroys a user from the DB
def destroy_user(request, user_id):
    User.objects.get(id=user_id).delete()
    try:
        del request.session['id']
        messages.success(request, "That user has been removed from the database.")
        return redirect("/display/admin")
    except KeyError:
        messages.success(request, "That user has been removed from the database.")
        return redirect("/display/admin")
