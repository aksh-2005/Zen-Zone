from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Banners(models.Model):
    img = models.ImageField(upload_to="banners/")
    alt_text = models.CharField(max_length=150)

    def __str__(self):
        return self.alt_text

    def image_tag(self):
        return mark_safe('<img src="%s" width="80" />' %(self.img.url)) 

    class Meta:
        verbose_name_plural = "Banners"

class Service(models.Model):
    title = models.CharField(max_length=150)
    detail = models.TextField()
    img = models.ImageField(upload_to="services/",null=True)
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="%s" width="80" />' %(self.img.url)) 


class Page(models.Model):
    title=models.CharField(max_length=200)
    detail=models.TextField()
    def __str__(self):
        return self.title

class Enquiry(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    mobile = models.CharField(max_length=15)
    detail = models.TextField()
    send_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.full_name
    
class SubPlan(models.Model):
    title=models.CharField(max_length=150)
    price=models.IntegerField()
    max_member=models.IntegerField(null=True)
    highlighted_status=models.BooleanField(default=False,null=True)
    validity_days=models.IntegerField(null=True)
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Plan" 

class SubPlanFeature(models.Model):
    subplan = models.ManyToManyField(SubPlan)
    title = models.CharField(max_length=150)
    order = models.PositiveIntegerField(default=0)  # ✅ Added order field

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Plan Features"
        ordering = ['-order'] 

    
class PlanDiscount(models.Model):
    subplan=models.ForeignKey(SubPlan,on_delete=models.CASCADE)
    total_months=models.IntegerField()
    total_discount=models.IntegerField()
    def __str__(self):
        return str(self.total_months)
    
class Subscriber(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    mobile=models.CharField(max_length=20)
    address=models.TextField(blank=True)
    def __str__(self):
        return str(self.user)
    
class Subscription(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    plan=models.ForeignKey(SubPlan,on_delete=models.CASCADE,null=True)
    price=models.CharField(max_length=50)
    reg_date=models.DateField(auto_now_add=True,null=True)
    
@receiver(post_save,sender=User)
def create_subscriber(sender,instance,created,**kwrags):
    if created:
        Subscriber.objects.create(user=instance)
            
class Trainer(models.Model):
    full_name=models.CharField(max_length=100)
    username=models.CharField(max_length=100,null=True)
    password=models.CharField(max_length=50,null=True)
    mobile=models.CharField(max_length=100)
    email=models.CharField(max_length=100,null=True)
    address=models.TextField(blank=True)
    is_active=models.BooleanField(default=False)
    detail=models.TextField(blank=True)
    salary=models.IntegerField(default=0)

    facebook=models.CharField(max_length=200,null=True)
    instagram=models.CharField(max_length=200,null=True)
    whatsapp=models.CharField(max_length=200,null=True)
    youtube=models.CharField(max_length=200,null=True)
    twitter=models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.full_name)    

class Notify(models.Model):
    notify_detail=models.TextField()
    read_by_user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return str(self.notify_detail)

    class Meta:
        verbose_name_plural = "Notifications"  
    
class NotifUserStatus(models.Model):
    notif=models.ForeignKey(Notify,on_delete=models.CASCADE)  
    user=models.ForeignKey(User,on_delete=models.CASCADE)  
    status=models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "User Notification Status"


class AssignSubscriber(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    trainer=models.ForeignKey(Trainer,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
    
    class Meta:
        verbose_name_plural = "Assign Subscriber" 
	
class TrainerAchivement(models.Model):
    trainer=models.ForeignKey(Trainer,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    detail=models.TextField(blank=True)
    year=models.IntegerField() 
    def __str__(self):
        return str(self.title) 

    class Meta:
        verbose_name_plural = "Trainer Achivement"    
    
class TrainerSalary(models.Model):
    trainer=models.ForeignKey(Trainer,on_delete=models.CASCADE)
    amt= models.IntegerField()
    amt_date=models.DateField()
    remarks=models.TextField(blank=True)
    def __str__(self):
        return str(self.trainer.full_name)
    
    class Meta:
        verbose_name_plural = "Trainer Salary"
  
class TrainerSubscriberReport(models.Model):
    report_for_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, blank=True, related_name='received_reports')
    report_for_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='received_reports_user')
    report_from_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, blank=True, related_name='submitted_reports')
    report_from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='submitted_reports_user')
    report_msg = models.TextField()

    class Meta:
        verbose_name_plural = "Reports"



    

class BMIRecord(models.Model):
  
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Link BMI record to a user
    height = models.FloatField()
    weight = models.FloatField()
    bmi = models.FloatField()
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.gender} - BMI: {self.bmi:.2f}"       
