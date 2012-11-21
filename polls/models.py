from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class Poll(models.Model):
    # ...
    def __unicode__(self):
        return self.question
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published Recently?'
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    # ...
    def __unicode__(self):
        return self.choice
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()