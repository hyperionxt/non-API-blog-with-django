from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class UserRegistrationForm(UserCreationForm):
    
    email = forms.EmailField(help_text='A valid email address, please', required=True)
    
    class Meta:
        # Get the user
        model= get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        """
        Allows save the form.
        """
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    
    """
    Custom form that allows login with username or email.
    """
    
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        
    username = forms.CharField(widget=forms.TextInput(
        
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")
    
    password = forms.CharField(widget=forms.PasswordInput(
        
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    
    # Captcha implementation
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    



class UserUpdateForm(forms.ModelForm):
    
    """
    Form to update the name, lastname email and description.
    """
    
    email = forms.EmailField()
    
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'image','description']


class SetPasswordForm(SetPasswordForm):
    
    class Meta:
        model = get_user_model()
        fields = ['new_password','new_password2']
        

class PasswordResetForm(PasswordResetForm):
    
    """
    Allows recover the password
    """
    
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        
    # Captcha implementation
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    