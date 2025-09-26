from django import forms
from .models import PaymentType



class OrderForm(forms.Form):
    name=forms.CharField(label="",error_messages={"required":"این فیلد نباد خالی باشد"},
                         widget=forms.TextInput(attrs={"class":"form-control","id":"fname",'placeholder':"نام خود را وارد کنید"}))
    family=forms.CharField(label="",error_messages={"required":"این فیلد نباد خالی باشد"},
                         widget=forms.TextInput(attrs={"class":"form-control","id":"lname",'placeholder':"نام خانوادگی خود را وارد کنید"}))
    
    mobile_number=forms.CharField(label="",error_messages={"required":"این فیلد نباد خالی باشد"},
                         widget=forms.TextInput(attrs={"class":"form-control",'placeholder':"شماره موبایل خود را وارد کنید"}))
    
    email=forms.CharField(label="",error_messages={"required":"این فیلد نباد خالی باشد"},
                         widget=forms.TextInput(attrs={"class":"form-control","id":"email",'placeholder':"ایمیل خود را وارد کنید"}))

    address=forms.CharField(label="",error_messages={"required":"این فیلد نباد خالی باشد"},
                         widget=forms.TextInput(attrs={"class":"form-control","id":"address",'placeholder':"آدرس خود را وارد کنید"}))
    
    
    

    
    payment_type=forms.ChoiceField(label="",
                                   choices=[(item.pk,item.payment_title) for item in PaymentType.objects.all()],
                                   widget=forms.RadioSelect(attrs={"id":"credit"}))
    code_posti=forms.ChoiceField(label="",error_messages={"required":"کد پستی را وارد کنید "},
                                 widget=forms.TextInput(attrs={"class":"form-control","placeholder":"کد پستی ","id":"zip"}))
    
    
class Cupon_Code(forms.Form):
    copoun_code=forms.CharField(label="",widget=forms.TextInput(attrs={"class":"form-control","id":"number","placeholder":"کد تخفیف"}))