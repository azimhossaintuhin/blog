from dataclasses import fields
from django import forms
from accounts.models import *
class UserRegForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username' , 'email' , 'phone' , 'password')
    
    def clean_username(self):
        usernmae = self.cleaned_data.get("username")
        model = self.Meta.model
        user = model.objects.filter(username__iexact = usernmae)
        if user.exists():
            raise forms.ValidationError("Username already Exsits")
        return usernmae

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')  
        model = self.Meta.model
        number = model.objects.filter(phone__iexact = phone)
        if number.exists():
            raise forms.ValidationError('Phone number Already Exsits')
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        model = self.Meta.model
        useremail = model.objects.filter(email__iexact = email)

        if useremail.exists():
            raise forms.ValidationError("Email Already Exsits")
        
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('password Not Matched')
        
        return password

class loginform(forms.Form):
    username = forms.CharField(max_length= 250, required=True)
    password = forms.CharField( max_length= 250, required=True , widget= forms.PasswordInput) 



class UserInfoUpdate(forms.ModelForm):
    def _init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
    class Meta: 
        model = User
        fields = ("first_name","last_name",'username' , 'email' , 'phone' , )
    
    def clean_username(self):
        usernmae = self.cleaned_data.get("username")
        model = self.Meta.model
        user = model.objects.filter(username__iexact = usernmae).exclude(pk = self.instance.pk)
        if user.exists():
            raise forms.ValidationError("Username already Exsits")
        return usernmae

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')  
        model = self.Meta.model
        number = model.objects.filter(phone__iexact = phone).exclude(pk=self.instance.pk)
        if number.exists():
            raise forms.ValidationError('Phone number Already Exsits')
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        model = self.Meta.model
        useremail = model.objects.filter(email__iexact = email).exclude(pk=self.instance.pk)

        if useremail.exists():
            raise forms.ValidationError("Email Already Exsits")
        
        return email
    def change_password(self):
        if 'new_password' in self.data and 'confirm_password' in self.data:
            new_password = self.data['new_password']
            confirm_password = self.data['confirm_password']
            if new_password != "" and confirm_password !="":
                if  new_password!=confirm_password:
                    raise forms.ValidationError('Password Not Matched')
                else:
                    self.instance.set_password(new_password)
                    self.instance.save()
    def clean(self):
        self.change_password()
    

class profile_picture(forms.Form):
    profile_image = forms.ImageField(required=True)