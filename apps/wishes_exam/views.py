from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Count
from . models import User, Wish


def index(request):
    return render(request, 'wishes_exam/index.html')


def login(request):
    email = request.POST['email']
    errors = User.objects.login_check(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    user = User.objects.get(email = email)
    request.session['email'] = email
    return redirect('/wishes')


def logout(request):
    sess_email = request.session['email']

    del sess_email
    return redirect('/')


def add(request):
    email = request.POST['email']
    errors = User.objects.register_validate(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        User.objects.make_new_user(request.POST)
        request.session['email'] = email
        return redirect('/wishes')


def wishes(request):
    sess_email = request.session['email']

    if 'email' not in request.session:
        return redirect('/')
    context = {
        'wishes': Wish.objects.all(),
        'user': User.objects.all().get(email = sess_email)
    }
    return render(request,'wishes_exam/wishes.html',context)


def new(request):
    sess_email = request.session['email']

    if 'email' not in request.session:
        return redirect('/')
    user = User.objects.get(email = sess_email)
    context = {
        'user': user
    }
    return render(request, 'wishes_exam/new.html',context)


def create(request):
    sess_email = request.session['email']
    errors = Wish.objects.validation(request.POST)

    if 'email' not in request.session:
        return redirect('/')
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/new')
    else:
        user = User.objects.get(email = sess_email)
        Wish.objects.new_wish(request.POST, user)
        return redirect('/wishes')


def edit(request, wish_id):
    sess_email = request.session['email']

    if 'email' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(email = sess_email),
        'wish': Wish.objects.get(id = wish_id)
    }
    return render(request, 'wishes_exam/edit.html',context)


def update(request, wish_id):
    errors = Wish.objects.validation(request.POST)

    if 'email' not in request.session:
        return redirect('/')
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/edit/' + str(wish_id))
    else:
        Wish.objects.edit_wish(request.POST, wish_id)
        return redirect('/wishes')


def delete(request, wish_id):
    if 'email' not in request.session:
        return redirect('/')
    Wish.objects.destroy_wish(wish_id)
    return redirect('/wishes')


def grant(request, wish_id):
    if 'email' not in request.session:
        return redirect('/')
    wish = Wish.objects.get(id = wish_id)
    wish.granted = True
    wish.save()
    return redirect('/wishes')


def stats(request):
    sess_email = request.session['email']

    if 'email' not in request.session:
        return redirect('/')
    user = User.objects.get(email = sess_email)
    context = {
        'user':user,
        'total_wishes_granted': Wish.objects.annotate(x = Count('granted')).filter(granted = True),
        'my_granted_wishes': Wish.objects.annotate(x = Count('granted')).filter(granted = True, creator = user),
        'my_pending_wishes': Wish.objects.annotate(x = Count('granted')).filter(granted = False, creator = user)
    }
    return render(request, 'wishes_exam/stats.html', context)


def like(request, wish_id, user_id):
    wish = Wish.objects.get(id = wish_id)
    user = User.objects.get(id = user_id)

    if 'email' not in request.session:
        return redirect('/')
    if wish.creator_id is user.id:
        return redirect('/wishes')
    try:
        was_liked = wish.likes.get(user_id = user_id, post_id = wish_id)
    except:
        outcome = False
    if outcome is False:
        wish.likes.add(user)
    return redirect('/wishes')
