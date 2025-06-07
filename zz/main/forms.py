from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.forms import User
from  .import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = models.Enquiry
        fields = ('full_name', 'email', 'mobile', 'detail')

    def __init__(self, *args, **kwargs):
        super(EnquiryForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['mobile'].widget.attrs.update({
            'class': 'form-control',
            'type': 'number',
            'minlength': '10'
        })
        self.fields['detail'].widget.attrs.update({'class': 'form-control', 'rows': '4'})

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile', '')
        mobile_str = str(mobile).strip()

        if not mobile_str.isdigit():
            raise forms.ValidationError("Mobile number must contain only digits.")
        if len(mobile_str) < 10:
            raise forms.ValidationError("Mobile number must be at least 10 digits long.")
        return mobile_str

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address.")
        return email


class SignUp(UserCreationForm):
       class Meta:
            model=User
            fields=('first_name','last_name','email','username','password1','password2')

class ProfileForm(UserChangeForm):
       class Meta:
            model=User
            fields=('first_name','last_name','email','username')

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())  

class TrainerLoginForm(forms.ModelForm):
    class Meta:
        model = models.Trainer
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
        }


class TrainerProfileForm(forms.ModelForm):
       class Meta:
            model=models.Trainer
            fields=('full_name','mobile','address','detail')                       

class TrainerChangePassword(forms.Form):
    old_password = forms.CharField(max_length=50,required=True)
    new_password = forms.CharField(max_length=50,required=True)
    confirm_password = forms.CharField(max_length=50,required=True)

class ReportForTrainerForm(forms.ModelForm):
    class Meta:
            model=models.TrainerSubscriberReport
            fields=('report_for_trainer','report_msg')  
  

class ReportForUserForm(forms.ModelForm):
	class Meta:
		model=models.TrainerSubscriberReport
		fields=('report_for_user','report_msg','report_from_trainer')
		widgets = {'report_from_trainer': forms.HiddenInput()}   

from django import forms
from .models import BMIRecord

class BMIForm(forms.ModelForm):
    class Meta:
        model = BMIRecord
        fields = ['height', 'weight']
        labels = {
            'height': 'Height (in cm)',
            'weight': 'Weight (in kg)',
        }
                                                    