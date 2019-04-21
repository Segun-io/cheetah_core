from django.db import models
from django.contrib.auth.models import AbstractUser

from shortuuidfield import ShortUUIDField

class User(AbstractUser):
    uuid = ShortUUIDField(primary_key=True)

    def __str__(self):
        return self.email

class UserKey(models.Model):

    DEFAULT_MONTHLY_MAX_REQUESTS = 1000
    DEFAULT_DAILY_MAX_REQUESTS = 100

    STATUS_NON_ACTIVE_CODE = 'A'
    STATUS_MONTHLY_CODE = 'B'
    STATUS_DAILY_CODE = 'C'
    STATUS_UNLIMITED_CODE = 'D'

    STATUS_CODES = (
        (STATUS_NON_ACTIVE_CODE, 'Disabled'),
        (STATUS_MONTHLY_CODE, 'Monthly quota'),
        (STATUS_DAILY_CODE, 'Daily quota'),
        (STATUS_UNLIMITED_CODE, 'Unlimited'),
    )

    user = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True)
    monthly_max_requests = models.PositiveIntegerField(
        'Monthly max requests', default=DEFAULT_MONTHLY_MAX_REQUESTS)
    daily_max_requests = models.PositiveIntegerField(
        'Daily max requests', default=DEFAULT_DAILY_MAX_REQUESTS)
    status = models.CharField('Key Status', max_length=1,
                              choices=STATUS_CODES, default=STATUS_NON_ACTIVE_CODE)

    def __str__(self):
        return 'User: {} - Key: {}'.format(self.user, self.pk)

class UserKeyUsage(models.Model):
    uuid = ShortUUIDField(primary_key=True)
    userkey = models.ForeignKey(
        'UserKey', on_delete=models.CASCADE)
    date = models.DateField('Date')
    requests = models.PositiveIntegerField('Requests', default=0)

    def __str__(self):
        return 'Date: {} - User: {} - Requests: {}'.format(self.date, self.userkey.user, self.requests)
