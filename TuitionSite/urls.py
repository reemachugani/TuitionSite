from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from TuitionSite.tuition import views
from TuitionSite import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
)

urlpatterns += patterns('TuitionSite.tuition.views',
   
##    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^users/login/$', 'log_in'),
    (r'^users/logout/$', 'log_out'),
    
    (r'^$',  'home'),
    (r'^home/$',  'home'),
    (r'^students/$',  'students'),
    (r'^tutors/$', 'tutors'),
    (r'^tuition/search/$',  'search'),
    (r'^tuition/advanced_search/$',  'advanced_search'),

    )

urlpatterns += patterns('TuitionSite.tuition.views',

    (r'^students/login/$', direct_to_template, {'template':'tuition/student_login.html'}),
    (r'^students/register_student/$', 'register_student'),
    (r'^students/advertise4tutor/$','advertize4tutor'),
    (r'^students/changeAdvertYorN/$','changeAdvertYorN'),
    (r'^students/subjects/$','subjects'),
    (r'^students/tutors/$','tutors_available'),
    (r'^students/faqs/$','students_faqs'),
    (r'^students/tutor/(?P<un>\w+)/$', 'tutor_record'),
    (r'^students/add_feedback/(?P<un>\w+)/$', 'add_feedback'),
    (r'^students/tutors_by_subjects/(?P<subj>\w+)/$', 'tutors_by_subjects'),
)

urlpatterns += patterns('TuitionSite.tuition.views',

    (r'^tutors/login/$','log_in'),
    (r'^tutors/register_tutor/$','register_tutor'),
##    (r'^tutors/detail_form/(?P<username>\w+)/$','tutor_detail_form', name="tutor_form"),
    (r'^tutors/jobs_for_tutors/$','jobs4tutors'),
    (r'^tutors/tuteeProfile/(\d+)/$','tuteeProfile'),
    (r'^tutors/faqs/$','tutors_faqs'),
#    (r'^tutors/tutor_profile/$', 'tutor_profile'),
)

urlpatterns += patterns('TuitionSite.tuition.views',

    (r'^about_us/$', 'about_us'),
    (r'^privacy_policy/$', 'privacy_policy'),
    (r'^contact_us/$', 'contact_us'),
    (r'^site_map/$', 'site_map'),                        
        )

urlpatterns += patterns('',
        (r'^photologue/', include('photologue.urls')),
    )