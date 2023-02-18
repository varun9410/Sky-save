from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import file
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from datetime import date
# Create your views here.
def index(request):
    return render(request,'home.html')

def register(request):
	if request.method=='POST':
		first_name=request.POST['first_name']
		last_name=request.POST['last_name']
		User_id=request.POST['User_id']
		Email=request.POST['email']
		password=request.POST['password1']
		password2=request.POST['password2']
		if password==password2:
			if User.objects.filter(username=User_id).exists():
			    messages.warning(request,'This User Id or Email already Exists')
			elif User.objects.filter(email=Email).exists():
				messages.warning(request,'This User Id or Email already Exists')
			else:
				user=User.objects.create_user(username=User_id,email=Email,password=password,first_name=first_name,last_name=last_name)
				user.save()
				return redirect('/')
		else:
			messages.warning(request,'please enter the same password ')	
	return render(request,'register.html')
def login(request):
    if request.method=='POST':
        userid=request.POST['userid']
        password=request.POST['password']
        user=authenticate(request,username=userid,password=password)
        if user is not None:
            auth_login(request,user)
            if user.is_authenticated==True:
                return redirect('/drive')     
    return render(request,'login.html')
@login_required(login_url='login')
def drive(request):
    upload=file.objects.filter(User=request.user)
    upload={'upload':upload}
    return render(request,'drive.html',upload)
def logout(request):
    auth_logout(request)
    return redirect('/')
@login_required(login_url='login')
def upload(request):
    if request.method == "POST":
        upload=file()
        upload.User=request.user
        upload.Title=request.POST['title']
        upload.Date=date.today()
        upload.File=request.FILES.get('file',False)
        upload.save()
        return redirect('/drive')
    return render(request,'uploadfile.html')
def download(request,file_url):
    file_path = os.path.join(settings.MEDIA_ROOT, file_url)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
def table(request):
    return render(request,'table.html')
def delete(request,id):
     file.objects.filter(File_id=id).delete()
     return redirect('/drive')