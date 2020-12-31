from django.shortcuts import render, redirect, HttpResponse
from . import models
import re


def validate_text(text, min_length=2):
    verified = True
    if not text:
        verified = False
    elif len(text) < min_length:
        verified = False
    return verified


def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email):
        if not models.is_duplicate_email(email):
            return True
    return False


def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        passwd = request.POST['password']
        cnf_passwd = request.POST['confirm']
        print(request.POST)
        if validate_text(first_name) and validate_text(last_name) and validate_text(passwd, min_length=8) \
            and validate_email(email) and passwd == cnf_passwd:
            user = models.insert_new_user(first_name, last_name, email, passwd)
            if 'user_id' not in request.session:
                request.session['user_id'] = user.id
                request.session['first_name'] = first_name
                request.session['last_name'] = last_name
            return redirect('/wall')
    return redirect('/')


def wall(request):
    if 'user_id' in request.session:
        mesgs = {}
        all_mesgs = models.get_all_mesgs()
        for mesg in all_mesgs:
            mesgs[mesg.id] = {'mesg': mesg, 'comments': models.get_comments(mesg.id)}
        context = {
            "first_name": request.session['first_name'],
            "last_name": request.session['last_name'],
            "mesgs": mesgs
        }
        print(mesgs)
        return render(request, "welcome.html", context)
    return redirect('/')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        passwd = request.POST['password']
        user = models.get_user(email, passwd)
        print(user)
        if user is not None:
            if 'user_id' not in request.session:
                request.session['user_id'] = user.id
                request.session['first_name'] = user.first_name
                request.session['last_name'] = user.last_name
            return redirect('/wall')
    return redirect('/')


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        del request.session['first_name']
        del request.session['last_name']
    return redirect('/')


def reg_or_login(request):
    if "user_id" in request.session:
        return redirect("/wall")
    return render(request, "index.html")


def add_mesg(request):
    if request.method == "POST":
        body = request.POST['mesg']
        mesg = models.insert_mesg(request.session['user_id'], body)
    return redirect('/wall')


def add_comment(request, id):
    if request.method == "POST":
        body = request.POST['comment']
        comment = models.insert_comment(request.session['user_id'], body, id)
    return redirect('/wall')
