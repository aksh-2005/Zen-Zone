
from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from .views import ChangePasswordView
from django.contrib.auth.views import PasswordChangeDoneView

def password_change_done(request):
    return render(request, 'registration/pass_done.html')

urlpatterns = [

    path('admin/', admin.site.urls),
   
    path('',views.home,name='home'), 
    path('pagedetail/<int:id>/',views.page_detail,name='pagedetail'),
    path('enquiry',views.enquiry,name='enquiry'),
    path('pricing',views.pricing,name='pricing'), 
    path('account/signup',views.signup,name='signup'),
    path('checkout/<int:plan_id>/',views.checkout,name='checkout'),
    path('checkout_session/<int:plan_id>/',views.checkout_session,name='checkout_session'),
    path('success',views.success,name='success'),
    path('cancel',views.cancel,name='cancel'),

    path('user_dashboard',views.user_dashboard,name='user_dashboard'),
    path('update_profile',views.update_profile,name='update_profile'),
    path('report_for_trainer',views.report_for_trainer,name='report_for_trainer'),
    path('password/',ChangePasswordView.as_view(), name='change_password'),
    path('password-change-done/', password_change_done, name='password_change_done_custom'),

    path('trainerlogin',views.trainerlogin,name='trainerlogin'),
    path('trainerlogout',views.trainerlogout,name='trainerlogout'),
    path('trainer_dashboard',views.trainer_dashboard,name='trainer_dashboard'),
    path('trainer_profile',views.trainer_profile,name='trainer_profile'),
    path('trainer_subscriber',views.trainer_subscriber,name='trainer_subscriber'),
    path('trainer_payments',views.trainer_payment,name='trainer_payments'),
    path('trainer_pass',views.trainer_pass,name='trainer_pass'),
    path('report_for_user',views.report_for_user,name='report_for_user'),

    path('notifs',views.notifs,name='notifs'),
    path('get_notifs',views.get_notifs,name='get_notifs'),
    path('mark_read_notif',views.mark_read_notif,name='mark_read_notif'),
    path('bmi_calculator',views.calculate_bmi,name='bmi_calculator'),
    path('results/', views.bmi_results, name='bmi_results'),
     path('delete_bmi_record/<int:record_id>/', views.delete_bmi_record, name='delete_bmi_record'),

     path('test-404/', views.test_404, name='test_404'),



]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = 'main.views.custom_404'
handler500 = 'main.views.custom_500'
handler500 = 'main.views.custom_403'
