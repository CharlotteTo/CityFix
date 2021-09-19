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
@csrf_exempt
def reportproblem(request):
    if request.method == 'GET':
        return render(request, 'reportproblem.html')
    elif request.method == 'POST':
        response = str(request.body).split(',sugoma,')
        imageb64 = response[0].split(',')[1]
        title = response[1]
        lat = float(response[2]) # gets float from front end
        lng = float(response[3]) # gets float from front end
        desc = response[4]
        ptype = response[5]
        severity = int(response[6])
        a = ReportedProblem(user=request.user)
        a.title = title
        a.latitude = lat
        a.longitude = lng
        a.description = desc
        a.image = imageb64
        a.problemtype = ptype
        a.Severity = severity
        a.save()

@login_required
def delete(request, problemid):
    if request.user.is_superuser:
        ReportedProblem.objects.get(id=problemid).delete()



