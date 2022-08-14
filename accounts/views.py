
from django.shortcuts import redirect, render , get_object_or_404
from accounts.forms import UserRegForm , loginform , UserInfoUpdate, profile_picture
from django.contrib import messages
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login , logout,authenticate
from accounts.decorators import not_login_required
# Create your views here.
@not_login_required
def loginuser(request):
    form = loginform()
    if request.method == "POST":
        form = loginform(request.POST)
        if form.is_valid():
            user =  authenticate(
                username =  form.cleaned_data.get("username"),
                password = form.cleaned_data.get('password') 
                )
            if user:
                login(request, user)
                return redirect ('profile')
            else:
                messages.warning(request , "Invalid Credintial")
    context = {
        'form':form
    }
    return render(request, 'login.html',context)

@not_login_required
def registretion(request):
    form = UserRegForm()
    if request.method == "POST":
        form = UserRegForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request , 'Registretion Successfull')
            return redirect('login')
        else:
            pass


    context= {
        'form': form
    }
    return render(request , 'reg.html',context)

@login_required(login_url="login")
def userprofile(request):
    account = get_object_or_404(User , pk = request.user.pk)
    form = UserInfoUpdate(instance = account)
    if request.method == "POST":
        if request.user.pk != account.pk:
            return redirect('index')
        form = UserInfoUpdate(request.POST , instance = account)
        if form.is_valid():
            form.save()
            messages.success(request , 'profile update sucessfully')
            return redirect('profile')
        else:
            print(form.errors)
    context = {
        'account':account,
        'form': form
    }
   
    return render(request,'profile.html',context)
@login_required
def change_profile_picture(request):
    if request.method == 'POST':
       form = profile_picture(request.POST, request.FILES)
    if form.is_valid():
        image = request.FILES['profile_image']
        user  = get_object_or_404(User , pk = request.user.pk)
        if request.user.pk != user.pk:
            return redirect("index")
        user.profile_image = image
        user.save()
        messages.success(request, "Profile image Updated Successfully")
        print(request.FILES)
        return redirect('profile')

def logoutuser(request):
   logout(request)
   return redirect('login')