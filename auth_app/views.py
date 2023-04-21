from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, SetPasswordForm, PasswordResetForm
from django.contrib import messages
from home_app.models import Community

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.db.models.query_utils import Q




def signup_redirect(request):
    messages.error(request, "Something wrong here, it may be that you already have account")
    return redirect("home")

def activate_account(request, uidb64, token):
    User = get_user_model()
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
    except:
        User = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='auth_app.backends.EmailBackend')
        
        messages.success(request, "Welcome. You completed the email confirmation.")
        return redirect('home')
    
    else:
        
        messages.error(request, "Activation link is invalid or expired.")
            
    return redirect('home')

 
def email_confirmation(request, user, to_email):
    
    mail_subject = "Activate your user account"
    #domain = "http://127.0.0.1:8000/"
    message = render_to_string("message_auth_account.html",{
        'user': user.username,
        'domain': get_current_site(request).domain,
        #'domain' : domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
        
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
    
        messages.success(request, f'Hello {user}, please check your email {to_email} inbox and click on the link \
                             we sent you to confirm and complete the registration. Also check your spam folder.')
    else:
        
        message.error(request, f'Problem sending email to {to_email}, check if you type correctly or try later.')


def signup(request):
    """
    Allows register new users.
    """
    # If the user is already authenticated(registered), It won't allow to register again, just redirect to home page.
    if request.user.is_authenticated:
         return redirect('/')
    
    # If the new user actives POST pressing the buttom
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        # If the informaton from the text boxes is valid then register the new user.
        if form.is_valid():
            # Commit = False means it wont be saved on the db
            user=form.save(commit=False)
            # If the user doesnt have a activated account by email, this user will be False and not allowed to login.
            user.is_active=False
            user.save()
            email_confirmation(request, user, form.cleaned_data.get('email'))
            return redirect('home')
        # Otherwise, show me the error using this array to find it.
        else:
            for i in form.error_messages:
                messages.error(request, form.error_messages[i])
    
    # This is the form the user will see the first time without pressing the buttom.
    else:
        form = UserRegistrationForm()

    return render(request, "auth_app/auth.html", {"form":form})


def log_out(request):
    
    """
    Function to log out the session.
    
    """
    
    if not request.user.is_authenticated:
        return redirect('home')
    
    else:   
        logout(request)
        return redirect('home')


def log_in(request):
    
    """
    Function to log in the session.
    """
    
    # If the user activates POST pressing the buttom, then...
    if request.method == 'POST':
        
        # Save the auth form with the text boxes information(password and username).
        login_form=UserLoginForm(request, data=request.POST)
        
        # Conditional to valid the previous information.
        if login_form.is_valid():
            
            # Save username information form username text box
            username1=login_form.cleaned_data.get("username")
            # Save password information form password text box.
            password1=login_form.cleaned_data.get("password")
            
       
            # To check the previous information on database, this throw None
            # if there are not information that match.
            user=authenticate(username=username1, password=password1)
            
            if user is not None:
                login(request, user)
                
                return redirect('home')
            else:
                
                messages.error(request, "Invalid user or password")
                
        else:
            
            for key, error in list(login_form.errors.items()):
                if key == 'captcha' and error[0]=='This field is required.':
                    messages.error(request, 'Please, complete the captcha verification.')
                    continue
                    
                messages.error(request, error)
            
                
    
    # This is the form the user will see the first time without pressing the buttom..
    login_form= UserLoginForm()
    
    return render(request, "login/login.html", {"login_form": login_form})





def profile(request, username):
    
    match = Community.objects.all()
    
    # If tyhe user press the buttom...
    if request.method == "POST":
        
        user = request.user
        
        form = UserUpdateForm(request.POST, request.FILES, instance=user)

        # If the informaton form the form is valid, save it on db, put a msg and redirect to the same page.
        if form.is_valid():
            
            user_form=form.save()
            messages.success(request, f'{user_form}, Your profile has been updated!')
            return redirect("profile", user_form.username)

        # In case there are any errors.
        for error in list(form.errors.values()):
            messages.error(request, error)
            
            
    # Find username(user) on database. returns (BOOL).
    user = get_user_model().objects.filter(username=username).first()
    
    # If the username match..
    if user:
        
        form = UserUpdateForm(instance=user)
        form.fields['description'].widget.attrs = {'rows': 1}
        
        return render(request, "profile/profile.html", {"form": form, "c_objects":match})
    
    return redirect('home')



def change_pass(request):
    
    if not request.user.is_authenticated:
        messages.error(request, "You must to login first!")
        return redirect('/')
    
        
    else:
        
        user = request.user
        if request.method == "POST":
            
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password changed successfully!")
                return redirect('log_in_session')
            
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        
        form= SetPasswordForm(user)
        return render(request, 'passwords/pass_confirm.html', {"form": form})
   

  
def pass_reset_request(request):
    
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form= PasswordResetForm(request.POST)
            if form.is_valid():
                user_email = form.cleaned_data['email']
                associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
                # if the email match with db..
                if associated_user:
                    
                    subject = 'Password reset request'
                    message = render_to_string("passwords/pass_reset_email_format.html",{
                        'user': associated_user,
                        'domain': get_current_site(request).domain,
                        'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                        'token': account_activation_token.make_token(associated_user),
                        'protocol': 'https' if request.is_secure() else 'http'
                    })
                    
                    email = EmailMessage(subject,message, to=[associated_user.email])
                    if email.send():
                        
                        messages.success(request, 
                            """
                            <h2>Password reset sent</h2><hr>
                            <p>
                                We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                                You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                                you registered with, and check your spam folder.
                            </p>
                            """
                        )
                    else:
                        messages.error(request, 'Problem sending the reset password email')
                else:
                        messages.error(request, f'There is not any account associated with this email: {user_email}')
                    
                
                return redirect('home')
            
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0]=='This field is required.':
                    messages.error(request, 'Please, complete the captcha verification.')
                    continue



        form = PasswordResetForm()
        return render(request, 'passwords/pass_reset.html', {"form": form})
        
        
def pass_reset_confirm(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
    except:
        User = None

    # if the user exists and the token is valid, then...
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()

                messages.success(request, "Your new password has been set. You may go go ahead and login.")
                return redirect("home")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
    
        form = SetPasswordForm(user)
        return render(request, 'passwords/pass_confirm.html', {'form':form})
    else:
        messages.error(request, "Link is expired")   
        
    messages.error(request, "Something went wrong, redirecctiong back to homepage")
    return redirect('home')
            
