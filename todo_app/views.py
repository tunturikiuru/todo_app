import traceback
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .models import Event

# FLAW 5 - CSRF MISSING
@csrf_exempt
def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        return redirect("user", username)

    # FLAW 2.1 - CRYPTOGRAPHIC FAILURES
    username = request.GET.get("username")
    if username:
        password = request.GET.get("password")

    #FLAW 2.1 - FIX
    #if request.method == "POST":
    #    username = request.POST["username"]
    #    password = request.POST["password"]"""

        profile = authenticate(request, username=username, password=password)

        if profile is not None:
            login(request, profile)
            return redirect("user", profile=profile.username)
        else:
            # FLAW 3 — IDENTIFICATION AND AUTHENTICATION FAILURES
            try:
                User.objects.get(username=username)
                messages.add_message(request, messages.INFO, "Incorrect password")
            except Exeption:
                messages.add_message(request, messages.INFO, "Username not found")
            # FLAW 3 — FIX
            #messages.add_message(request, messages.INFO, "Incorrect username or password")

    return render(request, "todo_app/index.html")

# FLAW 5 - CSRF MISSING
@csrf_exempt
def user(request, profile):
    # FLAW 1: BROKEN ACCESS CONTROL
    if request.user.is_authenticated:
        username = request.user.username    #only needed to show which user is logged in
        # FLAW 1: FIX
        #if profile != username:
        #    return HttpResponse('Unauthorized', status=401)
    else:
        return HttpResponse('Unauthorized', status=401)

    if request.method == "POST":
        logout(request)
        return redirect("index")
    if request.method == "GET":
        text = request.GET.get('find_event')
        if text:
            # FLAW 1: BROKEN ACCESS CONTROL
            name = User.objects.get(username=profile)
            event_list = Event.objects.filter(user=name, event_text__icontains=text)
            # FLAW 1: FIX
            #event_list = Event.objects.filter(user=request.user, event_text__icontains=text)
        else:
            # FLAW 1: BROKEN ACCESS CONTROL
            name = User.objects.get(username=profile)
            event_list = Event.objects.filter(user=name).order_by("-id")
            # FLAW 1: FIX
            #event_list = Event.objects.filter(user=request.user).order_by("-id")

    context = {
        "event_list": event_list,
        "username": username
    }

    return render(request, "todo_app/user.html", context)

# FLAW 5 - CSRF MISSING
@csrf_exempt
@login_required
def new(request):
    username = request.user.username
    if request.method == "GET":
        return render(request, "todo_app/new.html")
    if request.method == "POST":
        text = request.POST.get('event_text')
        important = "important" in request.POST
        profile = User.objects.get(username=username)
        event = Event(event_text=text, important=important, user=profile)
        event.save()
        return redirect("user", username)

# FLAW 5 - CSRF MISSING
@csrf_exempt
def detail(request):
    if request.method == "POST":
        try:
            User.objects.filter(passwor="a")
        except Exception:
            # FLAW 4 — SECURITY MISCONFIGURATION
            stack_trace = traceback.format_exc()
            messages.add_message(request, messages.INFO, stack_trace)
            # FLAW 4 — FIX
            #messages.add_message(request, messages.INFO, "error occurred")
    return render(request, "todo_app/detail.html")
