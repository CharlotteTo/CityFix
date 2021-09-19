from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required 
from django.views.decorators.csrf import csrf_exempt
from .models import SiteUser, ReportedProblem
import random
from datetime import datetime

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
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

@login_required
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
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = SiteUser.objects.create_user(username, email, password)
            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


@login_required
def index(request):
    return HttpResponseRedirect('/map')
@login_required
def map(request):
    problems = [i.getinfo() for i in ReportedProblem.objects.all()]
    return render(request, 'map.html', {'problems':problems})
def viewmarker(request, problemid):
    marker = ReportedProblem.objects.get(id=problemid).getinfo()
    return render(request, 'markerview.html', {'problem':marker})

@login_required
def reportproblme(request):
    if request.method == 'GET':
        return render(request, 'reportproblem.html')
    elif request.method == 'POST':
        imageb64 = 'e' #gets a string from a front end with an xhmhttprequest
        lat = 0.0 # gets float from front end
        lng = 0.0 # gets float from front end
        title = request.POST['title']
        desc = request.POST['desc']
        ptype = request.POST['ptype']
        severity = request.POST['severity']
        ReportedProblem.objects.create(user=request.user, title=title, descripton=desc, problemtype=ptype, Severity=severity, latitude=lat, longitude=lng, inage=imageb64)

        

@login_required
def delete(request, problemid):
    if request.user.is_superuser:
        ReportedProblem.objects.get(id=problemid).delete()



