from django.contrib import admin

# Register your models here.
from .import models

admin.site.site_header = "Zen Zone Admin"  
admin.site.site_title = "Zen Zone"


class BannerAdmin(admin.ModelAdmin):
    list_display=('alt_text','image_tag')
admin.site.register(models.Banners,BannerAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display=('title','image_tag')
admin.site.register(models.Service,ServiceAdmin) 

class PageAdmin(admin.ModelAdmin):
    list_display=('title',)
admin.site.register(models.Page,PageAdmin)

class EnquiryAdmin(admin.ModelAdmin):
    list_display=('full_name','email','mobile','detail','send_time')
admin.site.register(models.Enquiry,EnquiryAdmin)

class SubPlanAdmin(admin.ModelAdmin):
    list_display=('title','price','max_member','highlighted_status')
admin.site.register(models.SubPlan,SubPlanAdmin)

class SubPlanFeatureAdmin(admin.ModelAdmin):
    list_display=('title','subplans')
    def subplans(self,obj):
        return "|".join([sub.title for sub in obj.subplan.all()])
admin.site.register(models.SubPlanFeature,SubPlanFeatureAdmin)

class PlanDiscountAdmin(admin.ModelAdmin):
    list_display=('subplan','total_months','total_discount')
admin.site.register(models.PlanDiscount,PlanDiscountAdmin)

class SubscriberAdmin(admin.ModelAdmin):
    list_display=('user','mobile')
admin.site.register(models.Subscriber,SubscriberAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display=('user','plan','reg_date','price')
admin.site.register(models.Subscription,SubscriptionAdmin)

class TrainerAdmin(admin.ModelAdmin):
    list_display=('full_name','mobile','is_active','salary')
admin.site.register(models.Trainer,TrainerAdmin)

class NotifyAdmin(admin.ModelAdmin):
    list_display=('notify_detail','read_by_user')
admin.site.register(models.Notify,NotifyAdmin)

class NotifUserStatusAdmin(admin.ModelAdmin):
    list_display=('notif','user','status')
admin.site.register(models.NotifUserStatus,NotifUserStatusAdmin)

class AssignSubscriberAdmin(admin.ModelAdmin):
    list_display=('user','trainer')
admin.site.register(models.AssignSubscriber,AssignSubscriberAdmin)

class TrainerAchivementAdmin(admin.ModelAdmin):
    list_display=('title','detail','year')
admin.site.register(models.TrainerAchivement,TrainerAchivementAdmin)

class TrainerSalaryAdmin(admin.ModelAdmin):
    list_display=('trainer','amt','amt_date')
admin.site.register(models.TrainerSalary,TrainerSalaryAdmin)

class TrainerSubscriberReportAdmin(admin.ModelAdmin):
    list_display=('report_msg','report_from_trainer','report_from_user','report_for_trainer','report_for_user')
admin.site.register(models.TrainerSubscriberReport,TrainerSubscriberReportAdmin)



