from django.http import HttpResponse
from django.shortcuts import render
from .login import check_user
from user.models import get_user_by_id, user
from django.db.models import Count
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password, check_password

def profile(request):
    return render(request, 'profile.html')

def login(request):
    data = {}
   
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        validation_result = check_user(username, password)

        if validation_result != False:
            request.session['user_id'] = validation_result
            return redirect('/dashboard/')
        else:
            data['error'] = "Login Failed."
    
    return render(request, 'login.html', data)
    
def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('/login/')

def change_password(request):
    data = {}
    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if check_password(current_password, request.META['current_user']['password']) == True:
            if confirm_password == new_password:
        
                change_password = user.objects.get(user_id=request.META['current_user']['user_id'])
                change_password.password = make_password(new_password)
                change_password.save()
                data['success'] = "Password changed successfully."
            else:
                data['error'] = "Passwords do not match."
        else:
            data['error'] = "The current password is not valid."

    return render(request, 'change_password.html', data)