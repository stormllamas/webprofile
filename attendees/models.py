from django.db import models
import qrcode
from django.utils import timezone
from django.core.validators import MinLengthValidator

class Designation(models.Model):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(1)], blank=False)

    def __str__(self):
        return self.name

class Attendee(models.Model):
    designation = models.ForeignKey(Designation, related_name='designation', on_delete=models.DO_NOTHING, null=True, blank=True)
    first_name = models.CharField(max_length=50, validators=[MinLengthValidator(1)], blank=False)
    last_name = models.CharField(max_length=50, validators=[MinLengthValidator(1)], blank=False)
    email = models.EmailField(null=True, blank=True)
    contact = models.IntegerField(null=True, blank=True)
    present = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    points_redeemed = models.IntegerField(default=0)
    points_balance = models.IntegerField(default=0)
    timestamp = models.DateTimeField('timestamp', default=timezone.now)

    def activities(self):
        return ActivityLog.objects.filter(attendee=self).count()

    def activities_ordered(self):
        return ActivityLog.objects.filter(attendee=self).order_by('-time_log')
    
    def __str__(self):
        # return '{} {} {} {}'.format(self.last_name, self.first_name, self.present, self.timestamp)

        fullname = '{0.last_name}, {0.first_name}| {0.present} | {0.timestamp}'
        return fullname.format(self)

        # return '%s %s %s %s'%(self.last_name, self.first_name, self.present, self.timestamp)

        # return f'{self.last_name, self.first_name, self.present, self.timestamp}'

class ActivityLog(models.Model):
    attendee = models.ForeignKey(Attendee, related_name='activity', on_delete=models.CASCADE)
    time_log = models.DateTimeField('time_logs', null = True)
    points_claim = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    points_redeem = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    total_points_earned = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    total_points_redeemed = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    total_points_balance = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    # def __str__(self):
    #     return self.time_log.strftime("%m/%d/%Y, %H:%M:%S")
       
    