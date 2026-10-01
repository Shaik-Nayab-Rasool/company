import json

from django.http import JsonResponse
from django.shortcuts import render
from .models import EmployeeDetails
from django.views.decorators.csrf import csrf_exempt
import bcrypt
from .serializers import EmployeeDetailsSerialzer
from .validations import password_hash, password_check

# Create your views here.
@csrf_exempt
def entry_page(req):
    valid = False
    if req.method == 'POST':
        username = req.POST.get('username') # ramesh123
        password = req.POST.get('password')
        emp_obj = EmployeeDetails.objects.get(username=username)
        if password == emp_obj.password:
            response = JsonResponse({'status':'Cookie Set'})
            response.set_cookie(
                key='logged_in',
                value=True,
            )
            return response
        else:
            valid = True
            return render(req,'login.html',{'valid':valid})
    return render(req,'login.html',{'valid':valid})

@csrf_exempt
def home(req):
    print(req.body)
    data = json.loads(req.body)
    print(data)
    return JsonResponse({})
    # print(req.COOKIES.get('logged_in'))
    # if req.COOKIES.get('logged_in') == 'True':
    #     return render(req,'home.html')
    # else:
    #     return JsonResponse({'status':'Login First'})

def dark_theme(req):
    response = JsonResponse({'status':'Theme set!'})
    response.set_cookie(
        key='Theme',
        value='Dark'
    )
    return response

def logout(req):
    response = JsonResponse({'status':'Logged-out'})
    response.delete_cookie('logged_in')
    return response

# Client -> Entry -> Home -> Entry -> Client 
@csrf_exempt
def register(req):
    json_data = json.loads(req.body)
    json_data['password'] = password_hash(json_data.get('password'))
    new_emp = EmployeeDetailsSerialzer(data=json_data)

    if new_emp.is_valid():
        new_emp.save()
        return JsonResponse({'status':'Employee Added!'})
    else:
        return JsonResponse(new_emp.errors)

@csrf_exempt
def login(req):
    json_data = json.loads(req.body)
    emp_obj = EmployeeDetails.objects.get(username=json_data['username'])
    if password_check(json_data.get('password'),emp_obj.password):
        return JsonResponse({'status':'Login Success!'})
    else:
        return JsonResponse({'status':'Login Failed!'})

@csrf_exempt
def update(req):
    json_data = json.loads(req.body)
    emp_obj = EmployeeDetails.objects.get(username=json_data['username'])
    json_data['password'] = password_hash(json_data.get('password'))
    updated_pass = EmployeeDetailsSerialzer(emp_obj,data=json_data,partial=True)

    if updated_pass.is_valid():
        updated_pass.save()
        return JsonResponse({'status':'Password Updated!'})
    else:
        return JsonResponse(updated_pass.errors)

def show(req):
    print('Iam View')
    return JsonResponse({'status':'Request Reached!'})