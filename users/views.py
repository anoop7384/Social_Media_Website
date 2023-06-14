from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm ,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
from .email import sendEmailOTP

# Create your views here.
def register(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        # message = "Password should contain letters, symbols and numbers"
        if form.is_valid():
            form.save()
            username= form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            request.session['email'] = email
            sendEmailOTP(email)
            return redirect('verify-otp')
        message=form.errors
        print(message)
        return render(request, 'users/register.html',{'form':form,'message':message})
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html',{'form':form})


def verifyotp(request):
    if request.method == 'POST':
        user_email = request.session['email']
        user = User.objects.get(email=user_email)
        if 'resend_otp' in request.POST:
            sendEmailOTP(user_email)
            message = "New OTP SEND"
            return render(request, 'users/otp.html', {'message': message})
        otp = request.POST.get('enter_otp')
        message = "Wrong OTP"
        if otp==user.profile.otp:
            user.profile.isVerified = True
            user.save()
            del request.session['email']
            return redirect('login')
        return render(request, 'users/otp.html', {'message': message})
    return render(request, 'users/otp.html')

@login_required
def editprofile(request):
    if request.method=='POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('connect-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request,'users/editProfile.html',context)