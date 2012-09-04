from TuitionSite.tuition.models import Subject, Day, Time_slot, Student, Tutor, Feedback, Advertize4Tutor, School, Race, Year
from django.contrib import admin
from django.contrib.sites.models import Site
from django.conf import settings

admin.site.register(Subject)
admin.site.register(Day)
admin.site.register(School)
admin.site.register(Student)
admin.site.register(Time_slot)
admin.site.register(Advertize4Tutor)
admin.site.register(Race)
admin.site.register(Feedback)
admin.site.register(Year)

class TutorAdmin(admin.ModelAdmin):
    list_display = ('user', 'sex', 'proficient_areas')
    search_field = ('subjects', 'proficient_areas', 'days', 'school')
    list_filter = ('fees_per_hour',)

admin.site.register(Tutor, TutorAdmin)

