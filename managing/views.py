from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from user.models import get_user_by_id, user, Company, Office
from django.db import connection
import json

def users(request):
    data = {}
    data['users'] = user.objects.all()

    return render(request, 'manage_users.html', data)

def manage_user(request, user_id):
    data = {}
    user_query = user.objects.filter(user_id = user_id)
    if len(user_query):
        data['user'] = user_query.last()
        if request.method == "POST":
            update_field = {}
            update_field['username'] = request.POST['username']
            update_field['full_name'] = request.POST['full_name']
            update_field['office_id'] = request.POST['office']
            update_field['company_id'] = request.POST['company']
            update_field['max_cost'] = request.POST['max_cost']
            update_field['max_tokens'] = request.POST['max_tokens']
            update_field['max_chats'] = request.POST['max_chats']

            update_field['permissions'] = json.dumps(request.POST.getlist('permission[]'))

            if len(request.POST['password']) > 0:
                
                update_field['password'] = make_password(request.POST['password'])

            p = user(**update_field)
            p.save()
            
            new_id = user.objects.latest()
            #print(new_id)
            data['success'] = "Data saved."
            return render(request, 'manage_user.html', data)

        else:
            return render(request, 'manage_user.html', data)


    return render(request, '404.html')

def delete_user(request, user_id):
    data = {}
    
    if request.method == "POST":
        user.objects.filter(user_id=user_id).delete()
        return redirect('/manage/users/')

def add_user(request):
    
    data = {}
    data['companies'] = Company.objects.all()
    data['offices'] = Office.objects.all()
    if request.method == "POST":
        update_field = {}
        update_field['username'] = request.POST['username']
        update_field['full_name'] = request.POST['full_name']
        update_field['office_id'] = request.POST['office']
        update_field['company_id'] = request.POST['company']
        update_field['max_cost'] = request.POST['max_cost']
        update_field['max_tokens'] = request.POST['max_tokens']
        update_field['max_chats'] = request.POST['max_chats']

        update_field['permissions'] = json.dumps(request.POST.getlist('permission[]'))

        if len(request.POST['password']) > 0:
            
            update_field['password'] = make_password(request.POST['password'])

        p = user(**update_field)
        p.save()
        
        new_id = user.objects.latest()
        #print(new_id)
        data['success'] = "Data saved."
        return redirect('/manage/user/' + str(p.pk))

    else:
        return render(request, 'add_user.html', data)

def companies(request):
    data = {}
    data['companies'] = Company.objects.all().order_by('id')[1:]

    return render(request, 'manage_companies.html', data)

def manage_company(request, company_id):
    data = {}
    companies = Company.objects.filter(id = company_id)
    if len(companies):
        company = companies.last()
        data['company'] = company
        if request.method == "POST":
            update_field = {}
            update_field['name'] = request.POST['name']
            update_field['industry'] = request.POST['industry']
            update_field['employee_count'] = request.POST['employee_count']
            update_field['primary_contact_name'] = request.POST['primary_contact_name']
            update_field['primary_contact_email'] = request.POST['primary_contact_email']
            update_field['secondary_contact_name'] = request.POST['secondary_contact_name']
            update_field['secondary_contact_email'] = request.POST['secondary_contact_email']

            p = Company(**update_field)
            p.save()
            #print(new_id)
            data['success'] = "Data saved."
            return render(request, 'manage_company.html', data)

        else:
            return render(request, 'manage_company.html', data)


    return render(request, '404.html')

def delete_company(request, company_id):
    data = {}
    
    if request.method == "POST":
        Company.objects.filter(id=company_id).delete()
        return redirect('/manage/companies/')

def add_company(request):
    data = {}
    if request.method == "POST":
        update_field = {}
        update_field['name'] = request.POST['name']
        update_field['industry'] = request.POST['industry']
        update_field['employee_count'] = request.POST['employee_count']
        update_field['primary_contact_name'] = request.POST['primary_contact_name']
        update_field['primary_contact_email'] = request.POST['primary_contact_email']
        update_field['secondary_contact_name'] = request.POST['secondary_contact_name']
        update_field['secondary_contact_email'] = request.POST['secondary_contact_email']

        p = Company(**update_field)
        p.save()
        #print(new_id)
        data['success'] = "Data saved."
        return redirect('/manage/company/' + str(p.pk))

    else:
        return render(request, 'add_company.html', data)