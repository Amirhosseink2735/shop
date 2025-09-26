from django import forms
from .models import Customuser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.forms import ModelForm



class CreationUserForm(forms.ModelForm):
    password1=forms.CharField(max_length=30,label="رمز عبور",error_messages={"required":"این فیلد نباید خالی باشد"},widget=forms.PasswordInput())
    password2=forms.CharField(max_length=30,label="تکرار رمزعبور",error_messages={"required":"این فیلد نباید خالی باشد"},widget=forms.PasswordInput())
    class Meta:
        model=Customuser
        fields=["mobile_number","email","name","family","gender"]
        
        
    def clean_password2(self):
        pass1=self.cleaned_data["password1"]
        pass2=self.cleaned_data["password2"]
        if pass1 and pass2 and pass1!=pass2:
            return ValidationError("تکرار رمز عبور با رمز عبور یکسان نیست")
        return pass2

    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user
    
    
    
class ChangeUserForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField()
    class Meta:
        model=Customuser
        fields=["mobile_number","password","email","name","family","gender","is_active","is_admin"]
        
        
        
class RegisterUserForm(forms.Form):
    password1=forms.CharField(max_length=30,label="رمز عبور",error_messages={"required":"این فیلد نباید خالی باشد"},widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"رمز عبور","id":"pass"}))
    password2=forms.CharField(max_length=30,label="تکرار رمزعبور",error_messages={"required":"این فیلد نباید خالی باشد"},widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"تکرار رمز عبور","id":"compass"}))
    mobile_number=forms.CharField(max_length=15,label="شماره موبایل",error_messages={"required":"این فیلد را پر کنید"},widget=forms.TextInput(attrs={"class":"form-control","placeholder":"شماره موبایل","id":"emailname"}))
        
        
    def clean_password2(self):
        pass1=self.cleaned_data["password1"]
        pass2=self.cleaned_data["password2"]
        if pass1 and pass2 and pass1!=pass2:
            raise ValidationError("تکرار رمز عبور با رمز عبور یکسان نیست")
        return pass2

    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user
    
    
    
class LoginUserForm(forms.Form):
    mobile_number=forms.CharField(label="شماره موبایل",max_length=15,error_messages={"required":"این فیلد را پر کنید"},widget=forms.TextInput(attrs={"class":"form-control","placeholder":"شماره موبایل","id":"name"}))
    password1=forms.CharField(label="رمز عبور",error_messages={"required":"این فیلد را پر کنید"},widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"رمز عبور","id":"pass"}))
    


class Forgot(forms.Form):
    mobile_number=forms.CharField(label="",error_messages={"required":"این فیلد را پر کنید"},
                                  widget=forms.TextInput(attrs={"class":"form-control","id":"emailname","placeholder":"شماره موبایل را وارد کنید"}))
    
    
class Verify(forms.Form):
    active_code=forms.CharField(label="",error_messages={"required":"این فیلد را پر کنید"},
                                  widget=forms.TextInput(attrs={"class":"form-control","id":"emailname","placeholder":"کد فعالسازی را وارد کنید"}))
    
    
    
class Changepass(forms.Form):
    password1=forms.CharField(label="رمز عبور",error_messages={"required":"این فیلد را پر کنید"},
                              widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"رمز عبور"}))
    password2=forms.CharField(label="تکرار رمز عبور",error_messages={"required":"این فیلد را پر کنید"},
                              widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"تکرار رمز عبور"}))
    
    def clean_password2(self):
        pass1=self.cleaned_data["password1"]
        pass2=self.cleaned_data["password2"]
        if pass1 and pass2 and pass1!=pass2:
            raise ValidationError("تکرار رمز عبور با رمز عبور یکسان نیست")
        return pass2
class Delete_user_form(forms.Form):
    mobile_number=forms.CharField(label="",error_messages={"required":"این فیلد را پر کنید"},
                                  widget=forms.TextInput(attrs={"class":"form-control","id":"emailname","placeholder":"شماره موبایل را وارد کنید"}))
    
 
 
class Verify_for_delete_user_form(forms.Form):
    active_code=forms.CharField(label="",error_messages={"required":"این فیلد را پر کنید"},
                                  widget=forms.TextInput(attrs={"class":"form-control","id":"emailname","placeholder":"کد فعالسازی را وارد کنید"}))
    
       