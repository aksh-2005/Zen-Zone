from django.shortcuts import render,redirect
from django.template.loader import get_template
from .import models
from .import forms
import stripe  
from django.core.mail import EmailMessage
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Count
from datetime import timedelta
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
import json

class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('password_change_done_custom')

# Create your views here.
def home(request):
    banners = models.Banners.objects.all()
    services = models.Service.objects.all()[:3]
    return render(request, 'home.html', {'banners': banners, 'services': services})

def page_detail(request, id):
    try:
        page = models.Page.objects.get(id=id)
    except (models.Page.DoesNotExist, ValueError):
        page = None  # Set page to None if not found

    return render(request, 'page.html', {'page': page})


def enquiry(request):
    msg = ''
    form = forms.EnquiryForm()  # Initialize form for GET requests
    if request.method == 'POST':
        form = forms.EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            msg = "We'll be in touch shortly"
            form = forms.EnquiryForm() 

    return render(request, 'enquiry.html', {'form': form, 'msg': msg})

def pricing(request):
    pricing = models.SubPlan.objects.annotate(total_members=Count('subscription__id')).all().order_by('price')
    dfeatures = models.SubPlanFeature.objects.all().order_by('-order')
    return render(request, 'pricing.html', {'plans': pricing, 'dfeatures': dfeatures})

def signup(request):
    msg = None  
    form = forms.SignUp()  # Always initialize form

    if request.method == 'POST':
        form = forms.SignUp(request.POST)
        if form.is_valid():
            form.save()
            msg = "Your fitness journey starts now!"
            form = forms.SignUp()  # Reset form after successful signup
        else:
            msg = "There was an error. Please check your details."

    return render(request, 'registration/signup.html', {'form': form, 'msg': msg})

@login_required
def checkout(request,plan_id):
    planDetail = models.SubPlan.objects.get(pk=plan_id)
    return render(request, 'checkout.html', {'plan': planDetail})

stripe.api_key='sk_test_51R4HdOFhUKgubPsuorhrpElNREBBtfel2g7m7tSuZPDD4wpOEi6BDvzmSlLZ0QOYShciG8xSwxslrGpiiaoGT8pL00rqJvTWrg'
def checkout_session(request,plan_id):
    plan=models.SubPlan.objects.get(pk=plan_id)
    final_price = float(request.POST.get('final_price'))  
    session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': plan.title,
                    },
                    'unit_amount': int(final_price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/cancel',
            client_reference_id=plan_id
        )
    return redirect(session.url, code=303)


def success (request):
    session=stripe.checkout.Session.retrieve(request.GET['session_id'])
    plan_id=session.client_reference_id
    plan=models.SubPlan.objects.get(pk=plan_id)
    user=request.user
    models.Subscription.objects.create(
        plan=plan,
        user=user,
        price=plan.price
    )

    return render(request,'success.html')

def cancel (request):
    return render(request,'cancel.html')

@login_required
def user_dashboard(request):
    current_plan = models.Subscription.objects.filter(user=request.user).first()
    my_trainer = models.AssignSubscriber.objects.filter(user=request.user).first()
    
    message = None
    enddate = None

    if current_plan:
        enddate = current_plan.reg_date + timedelta(days=current_plan.plan.validity_days)
    else:
        message = "You have not purchased a subscription."

    data = models.Notify.objects.all().order_by('-id')
    totalUnread = 0

    for d in data:
        notifStatus = models.NotifUserStatus.objects.filter(user=request.user, notif=d).exists()
        if not notifStatus:
            totalUnread += 1

    return render(request, 'user/dashboard.html', {
        'current_plan': current_plan,
        'my_trainer': my_trainer,
        'totalUnread': totalUnread,
        'enddate': enddate,
        'message': message
    })


@login_required
def update_profile(request):
    msg=None
    if request.method=='POST':
        form=forms.ProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            msg='Your profile has been updated.'
    form=forms.ProfileForm(instance=request.user)
    return render(request,'user/update-profile.html',{'form':form,'msg':msg})


def trainerlogin(request):
    msg = ''
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        trainer=models.Trainer.objects.filter(username=username,password=password).count()
        if trainer>0:
            trainer=models.Trainer.objects.filter(username=username,password=password).first()
            request.session['trainerlogin']=True
            request.session['trainerid']=trainer.id
            return redirect('/trainer_dashboard')
        else:
            msg='Invalid!'    
    form = forms.TrainerLoginForm  # Reset the form after successful submission
    return render(request,'trainer/trainerlogin.html',{'form':form,'msg':msg})


def trainer_dashboard(request):
    trainer=models.Trainer.objects.get(pk=request.session['trainerid'])
    trainer_sub=models.AssignSubscriber.objects.filter(trainer=trainer).order_by('-id')
    trainer_pay=models.TrainerSalary.objects.filter(trainer=trainer).order_by('-id')
    return render(request,'trainer/dashboard.html',{'trainer_sub':trainer_sub,'trainer_pay':trainer_pay})


def trainer_profile(request):
    t_id=request.session['trainerid']
    trainer=models.Trainer.objects.get(pk=t_id)
    msg=None
    if request.method=='POST':
         form=forms.TrainerProfileForm(request.POST,instance=trainer)
         if form.is_valid():
          form.save()
          msg='Your profile has been updated.'
    form=forms.TrainerProfileForm(instance=trainer)
    return render(request, 'trainer/profile.html',{'form':form,'msg':msg})


def trainerlogout(request):
    del request.session['trainerlogin']
    return redirect('trainerlogin')     

# Notifications
@login_required
def notifs(request):
	data=models.Notify.objects.all().order_by('-id')
	return render(request, 'notifs.html')

# Get All Notifications

def get_notifs(request):
	data=models.Notify.objects.all().order_by('-id')
	notifStatus=False
	jsonData=[]
	totalUnread=0
	for d in data:
		try:
			notifStatusData=models.NotifUserStatus.objects.get(user=request.user,notif=d)
			if notifStatusData:
				notifStatus=True
		except models.NotifUserStatus.DoesNotExist:
			notifStatus=False
		if not notifStatus:
			totalUnread=totalUnread+1
		jsonData.append({
				'pk':d.id,
				'notify_detail':d.notify_detail,
				'notifStatus':notifStatus
			})
	# jsonData=serializers.serialize('json', data)
	return JsonResponse({'data':jsonData,'totalUnread':totalUnread})

# Mark Read By user
def mark_read_notif(request):
	notif=request.GET['notif']
	notif=models.Notify.objects.get(pk=notif)
	user=request.user
	models.NotifUserStatus.objects.create(notif=notif,user=user,status=True)
	return JsonResponse({'bool':True})


def trainer_subscriber(request):
     trainer=models.Trainer.objects.get(pk=request.session['trainerid'])
     trainer_sub=models.AssignSubscriber.objects.filter(trainer=trainer).order_by('-id')
     return render(request,'trainer/trainer_subscriber.html',{'trainer_sub':trainer_sub})


def trainer_payment(request):
     trainer=models.Trainer.objects.get(pk=request.session['trainerid'])
     trainer_pay=models.TrainerSalary.objects.filter(trainer=trainer).order_by('-id')
     return render(request,'trainer/trainer_payment.html',{'trainer_pay':trainer_pay})



def trainer_pass(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            trainer_id = request.session.get('trainerid')

            if trainer_id:
                UpdateRes = models.Trainer.objects.filter(pk=trainer_id).update(pwd=new_password)

                if UpdateRes:
                    request.session.pop('trainerLogin', None)  # Safely remove session key
                    messages.success(request, "Password updated successfully. Please log in again.")
                    return redirect('/trainerlogin')
                else:
                    messages.error(request, "Something went wrong.")
            else:
                messages.error(request, "Session expired. Please log in again.")
                return redirect('/trainerlogin')

    form = forms.TrainerChangePassword()
    return render(request, 'trainer/trainer_pass.html', {'form': form})


def report_for_user(request):
	trainer=models.Trainer.objects.get(id=request.session['trainerid'])
	msg=''
	if request.method=='POST':
		form=forms.ReportForUserForm(request.POST)
		if form.is_valid():
			new_form=form.save(commit=False)
			new_form.report_from_trainer=trainer
			new_form.save()
			msg='Report Sent'
		else:
			msg='Invalid Response!!'
	form=forms.ReportForUserForm
	return render(request, 'trainer/report.html',{'form':form,'msg':msg})  

@login_required
def report_for_trainer(request):
	user=request.user
	msg=''
	if request.method=='POST':
		form=forms.ReportForTrainerForm(request.POST)
		if form.is_valid():
			new_form=form.save(commit=False)
			new_form.report_from_user=user
			new_form.save()
			msg='Report Sent'
		else:
			msg='Invalid Response!!'
	form=forms.ReportForTrainerForm
	return render(request, 'user/report.html',{'form':form,'msg':msg})

@login_required
def calculate_bmi(request):
    if request.method == "POST":
        form = forms.BMIForm(request.POST)
        if form.is_valid():
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']

            if height >= 100:  # Convert cm to meters safely
                height = height / 100  

            if height <= 0:
                messages.error(request, "Invalid height! Must be greater than 0.")
                return redirect('bmi_form')

            bmi = round(weight / (height ** 2), 2)  # Round BMI for better readability

            # ✅ Save BMI Record for the Logged-in User
            models.BMIRecord.objects.create(
                user=request.user,
                height=height,
                weight=weight,
                bmi=bmi
            )

            messages.success(request, f"BMI calculated successfully: {bmi:.2f}")
            return redirect('bmi_results')
    else:
        form = forms.BMIForm()

    return render(request, 'bmi_form.html', {'form': form})

@login_required
def bmi_results(request):
    if request.method == "POST" and "record_id" in request.POST:
        record_id = request.POST["record_id"]
        record = get_object_or_404(models.BMIRecord, id=record_id, user=request.user)
        record.delete()
        messages.success(request, "BMI record deleted successfully.")
        return redirect('bmi_results')

    # ✅ Fetch only the logged-in user's BMI records
    records = models.BMIRecord.objects.filter(user=request.user).order_by('-date_recorded')

    # ✅ Get the latest BMI record
    latest_record = records.first()  
    current_bmi = latest_record.bmi if latest_record else None

    # ✅ Categorize BMI using a cleaner approach
    bmi_status, status_class = None, ""
    if current_bmi:
        bmi_categories = [
            (18.5, "Underweight", "text-warning"),
            (24.9, "Normal weight", "text-success"),
            (29.9, "Overweight", "text-warning"),
            (float('inf'), "Obese", "text-danger")
        ]
        for threshold, status, css_class in bmi_categories:
            if current_bmi <= threshold:
                bmi_status, status_class = status, css_class
                break

    # ✅ Prepare data for visualization
    labels = [record.date_recorded.strftime("%Y-%m-%d") for record in records]
    bmi_values = [record.bmi for record in records]

    return render(request, 'bmi_results.html', {
        'records': records,
        'labels': json.dumps(labels),
        'bmi_values': json.dumps(bmi_values),
        'current_bmi': current_bmi,
        'bmi_status': bmi_status,
        'status_class': status_class,
    })


def delete_bmi_record(request, record_id):
    if request.method == "POST":
        record = get_object_or_404(models.BMIRecord, id=record_id)
        record.delete()
    return redirect('bmi_results')

def custom_404(request, exception):
    return render(request, 'user/404.html', status=404)

def custom_500(request):
    return render(request, 'user/404.html', status=500)

def custom_403(request):
    return render(request, 'user/404.html', status=403)

from django.shortcuts import render

def test_404(request):
    response = render(request, 'user/404.html')
    response.status_code = 404
    return response




