from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    title = models.CharField(max_length=50)
    def __unicode__(self):
        return self.title

class School(models.Model):
    school = models.CharField(max_length=30)
    def __unicode__(self):
        return self.school

class Race(models.Model):
    race = models.CharField(max_length=30)
    def __unicode__(self):
        return self.race

class Day(models.Model):
    day = models.CharField(max_length=10)
    def __unicode__(self):
        return self.day

class Year(models.Model):
    year = models.CharField(max_length = 15)
    def __unicode__(self):
        return self.year

class Time_slot(models.Model):
    time_slot = models.CharField(max_length=15)
    def __unicode__(self):
        return self.time_slot

class Tutor(models.Model):
    user = models.OneToOneField(User)
    sex = models.CharField(max_length=6, verbose_name="Sex (Male/Female)")
    race = models.ManyToManyField(Race)
    school = models.ManyToManyField(School)
    year = models.ManyToManyField(Year)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    subject = models.ManyToManyField(Subject)
    proficient_areas = models.CharField(max_length=200)
    fees_per_hour = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Fees per hour(in S$)")
    experience = models.TextField()
    days = models.ManyToManyField(Day)
    time_slots = models.ManyToManyField(Time_slot)
##    preference = models.CharField(max_length=20, verbose_name="Preference(Your center/Tutee's home)")
##    address = models.CharField(max_length = 70)

    def __unicode__(self):
        return self.user.first_name + ' ' +self.user.last_name
    def Meta(object):
        ordering = ['user.first_name']
    
class Student(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.first_name + ' ' +self.user.last_name

class Feedback(models.Model):
    username = models.CharField(max_length = 30)
    subjects_studied = models.ManyToManyField(Subject)
    tutor = models.ForeignKey(Tutor)
    year = models.ManyToManyField(Year)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode("%s: %s" % (self.tutor, self.body[:60]))

class Advertize4Tutor(models.Model):
    user = models.OneToOneField(User)
    subject = models.ManyToManyField(Subject)
    advertisement = models.TextField()

    def __unicode__(self):
        return self.user.first_name + ' ' +self.user.last_name
