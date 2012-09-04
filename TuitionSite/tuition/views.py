from decimal import Decimal
import decimal
import user
from django.http import HttpResponse, HttpResponseRedirect, Http404, QueryDict
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from tuition.models import Tutor, Subject, Student, Day, Time_slot, Year, Feedback, Race, School
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import *
from tuition.forms import UserRegistrationForm, TutorForm, FeedbackForm
from django.conf import settings
from django.db.models import Q
from django.forms import ModelForm
from django import forms
from django.core.urlresolvers import reverse
from forms import get_advertize_form, AdvancedSearchForm
from models import Advertize4Tutor

##
# this function checks the user group and returns to the calling function.
##

def check_user_group(request):
    if request.user.is_authenticated():
        if Student.objects.filter(user=request.user):
            return "Student"
        elif Tutor.objects.filter(user=request.user):
            return "Tutor"
        else:
            return "Not specified"
    else:
        return "Guest"


def home(request):
    user_group = check_user_group(request)
    return render_to_response('tuition/home.html',
                              {'user_group': user_group, 'current_home': "current"},
                              context_instance=RequestContext(request))


##
# this function returns all the Tutor objects and displays the list only if the user is Student,
# else it displays some text and prompts to register or sign in.
##

def students(request):
    user_group = check_user_group(request)    
    tutors = Tutor.objects.all()
    return render_to_response('tuition/students.html',
                              {'user_group': user_group, 'tutors':tutors, 'current_student': "current"},
                              context_instance=RequestContext(request))

##
# this function displays a login form, checks the user group and lets the user log in.
##

def log_in(request):
    user_group = check_user_group(request)
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password = password)
    if user is not None and user.is_active:
        auth.login(request, user)
        user_group = check_user_group(request)
        if user_group == 'Student':
            return HttpResponseRedirect('/students/')
        elif user_group == 'Tutor':
            tutor = Tutor.objects.get(user = user)
            return HttpResponseRedirect(reverse("TuitionSite.tuition.views.tutor_record", args=[tutor.user.username]))
        else:
            return HttpResponseRedirect('/students/register_student/')
    else:
        return render_to_response('tuition/home.html', {'user_group': user_group, 'current_home': "current"}, context_instance = RequestContext(request))


##
# this function allows the user to log out.
##

def log_out(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/users/login')
    else:
        logout(request)
        return HttpResponseRedirect('/')

##
# this function allows the Student to register by assigning the user to the Student group.
##

def register_student(request):
    user_group = check_user_group(request)
    if not request.user.is_authenticated() or user_group == 'Not specified':
        if request.method == "POST":
            form = UserRegistrationForm(data=request.POST)
            if form.is_valid():
                form.save()
                u = User.objects.get(username=request.POST.get('username'))
                gid = Group.objects.get(name='Student')
                u.groups.add(gid.id)
                s = Student(user = u)
                s.save()
                return HttpResponseRedirect('/students/')
            else:
                return render_to_response('tuition/student_register.html', {'user_group': user_group,'form': form,
                    'do_not_show_nav': 1, 'current_student': "current"}, context_instance = RequestContext(request))
        else:	
            form = UserRegistrationForm()
            return render_to_response('tuition/student_register.html', {'user_group': user_group,'form': form,
                    'do_not_show_nav': 1, 'current_student': "current"}, context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/')


##
# this function allows the Tutor to register by assigning the user to the Tutor group.
# mention the instance for the form that has a related data already mentioned, like a user is created first
# when UserCreationForm is saved. So now an instance of Tutor can be made by assigning this user to the user field
# of Tutor object and the POSTed form will point to this instance now. Hereafter this object's fields can be assigned
# cleaned_data from the form. Similar thing is also done in advertize4tutor(). Compare.
##

def register_tutor(request):
    user_group = check_user_group(request)
    authentic = False
    success = False
    tform = ""
    uform = ""
    if not request.user.is_authenticated() or user_group == 'Not specified':
        authentic = True

        if request.method == "POST":

            uform = UserRegistrationForm(request.POST)
            if uform.is_valid():
                success = True
                user = uform.save()
                tutor = Tutor(user=user)
                tform = TutorForm(request.POST, instance = tutor)

                if tform.is_valid():
                    tutor = tform.save(commit = False)
                    tutor.sex = tform.cleaned_data['sex']
                    tutor.cgpa = tform.cleaned_data['cgpa']
                    tutor.proficient_areas = tform.cleaned_data['proficient_areas']
                    tutor.fees_per_hour = tform.cleaned_data['fees_per_hour']
                    tutor.experience = tform.cleaned_data['experience']
                    tutor.save()
                    tutor.race = tform.cleaned_data['race']
                    tutor.year = tform.cleaned_data['year']
                    tutor.school = tform.cleaned_data['school']
                    tutor.subject = tform.cleaned_data['subject']
                    tutor.days = tform.cleaned_data['days']
                    tutor.time_slots = tform.cleaned_data['time_slots']
                    gid = Group.objects.get(name='Tutor')
                    user.groups.add(gid.id)
                    tutor.save()

        else:
            uform = UserRegistrationForm()
            tform = TutorForm()

    return render_to_response('tuition/tutor_register.html', {'authentic':authentic, 'success': success, 'uform': uform, 'tform': tform, 'user_group': user_group,
                        'do_not_show_nav': 1, 'current_tutor': "current"}, context_instance = RequestContext(request))


##
# this function checks the user_group of the user and displays some text if he's a Tutor. It renders Tutor's main page.
##

def tutors(request):
    user_group = check_user_group(request)
    return render_to_response('tuition/tutors.html', {'user_group': user_group, 'current_tutor': "current"}, context_instance = RequestContext(request))

##
# this function returns the Tutor object for the current user and renders a page with his particulars. NOT NEEDED
##

#def tutor_profile(request):
#    user_group = check_user_group(request)
#    tutor = Tutor.objects.get(user=request.user)
#    return render_to_response('tuition/tutor_profile.html', {'user_group': user_group, 'tutor': tutor}, context_instance = RequestContext(request))

##
# this function displays a feedback form and saves the posted data, redirecting it to the tutor_record views
# which allows the displaying of all the feedbacks for that tutor.
##

def add_feedback(request, un):
    p = request.POST

    if p.has_key("body") and p["body"]:

        feedback = Feedback(tutor = Tutor.objects.get(user__username=un))
        form = FeedbackForm(p, instance=feedback)
        if form.is_valid():
            feedback = form.save(commit = False)
            feedback.username = request.user.first_name
            feedback.save()
            feedback.subjects_studied = form.cleaned_data['subjects_studied']
            feedback.year = form.cleaned_data['year']
            feedback.save()

    return HttpResponseRedirect(reverse("TuitionSite.tuition.views.tutor_record", args=[un]))

##
# this function displays the tutor's record only if he is signed in, hence @login_required.
##

@login_required
def tutor_record(request, un):
    user_group = check_user_group(request)
    tutor = Tutor.objects.get(user__username=un)
    feedbacks = Feedback.objects.filter(tutor = tutor)
    return render_to_response('tuition/tutor_record.html', {'current_tutor': "current", 'user_group': user_group, 'tutor': tutor, 'feedbacks':feedbacks, 'form':FeedbackForm, 'user':request.user},
                              context_instance = RequestContext(request))

##
# this function ensures that a student doesn't advertize twice. If a student chooses to advertize again,
# a previous entry with the same username is deleted and the page is redirected to Advertize4Tutor form.
##

def changeAdvertYorN(request):
    user_group = check_user_group(request)
    if request.method == "POST":
        if 'Yes' in request.POST:
            u = Advertize4Tutor.objects.filter(user = request.user)
            if u:
                u.delete()
            return HttpResponseRedirect(reverse("TuitionSite.tuition.views.advertize4tutor"))
        elif 'No' in request.POST:
            return HttpResponseRedirect(reverse("TuitionSite.tuition.views.main_index"))

    return render_to_response('tuition/changeAdvertYorN.html', {'current_student': "current", 'user_group':user_group},
                              context_instance = RequestContext(request))


##
# ** the get_advertisement_form() method is now irrelevant since there is
# not much tweaking done in the Meta class or save() method of the form
# and also the Advertize4Tutor model is updated in views itself.
# ** this function allows the student to advertize for a tutor.
# ** Note that a ModelForm's data is directly added to the model object when the instance is specified,
# and form_name.save() is done. cleaned_data is only needed when we need to play around with the data
# for some other evaluation, display, etc. its not needed in simple assigning to model fields.
# but for assigning m2m fields, cleaned_data shd be used again since all fields cannot be saved at once.
# If even one is m2m, then first form needs to be saved temporarily using commit = False and
# then all non-m2m fields have to be assigned first using cleaned_data,
# after which the form has to be saved and then m2m fields
# need to be saved followed by the saving of the form once again.
##

def advertize4tutor(request):
    user_group = check_user_group(request)
    success = False
    first_name1=""
    last_name1=""
    email1=""
    subject1=""
    advertisement1=""
    #tutee = {}
    form = ""
    if request.user.is_authenticated and user_group == 'Student':
        form_class = get_advertize_form(request.user)
        if request.method == 'POST':
            advertize = Advertize4Tutor(user = request.user)
            form = form_class(data=request.POST, instance = advertize)
            if form.is_valid():
                success = True
                advertize = form.save(commit=False)
                advertize.user = request.user
                advertize.advertisement = form.cleaned_data['advertisement']
                advertize.save()
                sub = form.cleaned_data['subject']
                advertize.subject = sub ## the instance of the model needs to be saved before adding any m2m fields.
                advertize.save()
                #advertize.subject.add(sub) ## returns an error - int() argument must be a string or a number, not 'QueryDict'
                #advertize.setlist('subject',sub)
                first_name1 = request.user.first_name
                last_name1 = request.user.last_name
                email1 = request.user.email
                subject1 = form.cleaned_data['subject']
                advertisement1 = form.cleaned_data['advertisement']
                #Advertize4Tutor.objects.create(username = request.user.username, first_name = first_name1, last_name = last_name1, email = email1, subject = subject1, advertisement = advertisement1)
        else:
            form = form_class()
            ## the below written line causes an error - query doesn't match
        #tutee = Advertize4Tutor.objects.get(username = request.user.username)
    return render_to_response('tuition/advertise4tutor.html', {'current_student': "current", 'user_group': user_group, 'form':form, 'success':success, 'first_name':first_name1, 'last_name':last_name1, 'email': email1, 'subject':subject1, 'advertisement':advertisement1
    #'tutee':tutee
    }, context_instance = RequestContext(request))
        
##
# this function displays all the subjects available and hyperlinks them to the list of tutors teaching those subjects.
##

def subjects(request):
    user_group = check_user_group(request)
    subjects = Subject.objects.all()
    return render_to_response('tuition/subjects.html', {'current_student': "current", 'user_group': user_group, 'subjects':subjects}, context_instance = RequestContext(request))

##
# this function displays a list of tutors available for the students.
##

def tutors_available(request):
    user_group = check_user_group(request)
    tutors = Tutor.objects.all()
    return render_to_response('tuition/tutors_available.html',
                              {'current_student': "current", 'user_group': user_group, 'tutors':tutors}, context_instance=RequestContext(request))

##
# this function renders an html with all the faqs for students.
##

def students_faqs(request):
    user_group = check_user_group(request)
    return render_to_response('tuition/students_faqs.html', {'current_student': "current", 'user_group': user_group}, context_instance=RequestContext(request))

##
# this function returns all the tutors teaching a particular subject.
##

def tutors_by_subjects(request, subj):
    user_group = check_user_group(request)
##    tutors = []
##    allTutors = Tutor.objects.all()
##    for t in allTutors:
##        for s in t.subject.all:
##            if s.title == subj:
##                tutors += t

    tutors = Tutor.objects.filter(Q(subject__title__icontains=subj))
        
    return render_to_response('tuition/tutors_by_subjects.html',
                              {'user_group': user_group, 'current_student': "current", 'tutors':tutors, 'subj':subj}, context_instance=RequestContext(request))

##
# this function returns the jobs available for tutors, ie all the Advertize4Tutor objects.
##

#@login_required
def jobs4tutors(request):
    user_group = check_user_group(request)
    jobs = Advertize4Tutor.objects.all()
    return render_to_response('tuition/jobs4tutors.html', {'current_tutor': "current", 'user_group': user_group, 'jobs':jobs},
                              context_instance=RequestContext(request))

##
# this function returns the detailed requirements and particulars of the Student who advertized for a tutor.
##

def tuteeProfile(request, pk):
    user_group = check_user_group(request)
    tutee = Advertize4Tutor.objects.get(pk=pk)
    return render_to_response('tuition/tuteeProfile.html', {'current_tutor': "current", 'user_group': user_group, 'tutee':tutee},
                              context_instance=RequestContext(request))

##
# this function renders an html with all the faqs for students.
##

def tutors_faqs(request):
    user_group = check_user_group(request)
    return render_to_response('tuition/tutors_faqs.html', {'current_tutor': "current", 'user_group': user_group},
                              context_instance=RequestContext(request))

##
# this function renders an html with the details about us.
##

def about_us(request):
    user_group = check_user_group(request)
    return render_to_response('tuition/about_us.html', {'current_home': "current", 'user_group': user_group},
                              context_instance=RequestContext(request))

##
# this function renders an html with our privacy policy.
##

def privacy_policy(request):
    user_group = check_user_group(request)
    return render_to_response('tuition/privacy_policy.html', {'current_home': "current", 'user_group': user_group},
                              context_instance=RequestContext(request))

##
# this function renders an html with our contact details or a contact form.
##

def contact_us(request):
    user_group = check_user_group(request)
    return render_to_response('tuition/contact_us.html', {'current_home': "current", 'user_group': user_group},
                              context_instance=RequestContext(request))

##
# this function renders an html with the site_map.
##

def site_map(request):
    user_group = check_user_group(request)
    return render_to_response('tuition/site_map.html', {'current_home': "current", 'user_group': user_group},
                              context_instance=RequestContext(request))

##
# this function matches the query from the search box to return the matched cases.
##

def search(request):
    user_group = check_user_group(request)
    query = request.GET.get('q', '')
    #full_name = (first_name + last_name)
    if query:
        qset = (
            Q(subject__title__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
#            Q(first_name=query__icontains) |
#            Q(last_name=query__icontains) |
            Q(proficient_areas__icontains=query) |
            Q(school__school__icontains=query) |
            Q(days__day__icontains=query) |
            Q(race__race__icontains=query)
         )
        tutors = Tutor.objects.filter(qset).distinct()

    else:
        tutors = []
    return render_to_response('tuition/search.html',
                              {'user_group': user_group, 'current_home': "current", 'tutors':tutors, 'query':query},
                              context_instance=RequestContext(request))


##
# Advanced search
##

def advanced_search(request):
    user_group = check_user_group(request)
    empty = True
    form = AdvancedSearchForm(data = request.POST or None)
    tutors = []
    post = False
    if request.method == "POST":
        post = True
        if form.is_valid():
            first = form.cleaned_data['first_name']
            last = form.cleaned_data['last_name']
            school = form.cleaned_data['school']
            subj = form.cleaned_data['subject']
            proficient_area = form.cleaned_data['proficient_area']
            fees = form.cleaned_data['fees']
            experience = form.cleaned_data['experience']
            days = form.cleaned_data['days']
            cgpa = form.cleaned_data['cgpa']
            if first is not "":
                empty = False
                tutors += Tutor.objects.filter(Q(user__first_name__icontains=first)).distinct()
            if last is not "":
                empty = False
                tutors += Tutor.objects.filter(Q(user__last_name__icontains=last)).distinct()
            if school is not "":
                empty = False
                tutors += Tutor.objects.filter(Q(school__school__icontains=school)).distinct()
            if subj is not "":
                empty = False
                tutors += Tutor.objects.filter(Q(subject__title__icontains=subj)).distinct()
            if days is not "":
                empty = False
                tutors += Tutor.objects.filter(Q(days__day__icontains=days)).distinct()
            if experience is not "":
                empty = False
                tutors += Tutor.objects.filter(Q(experience__icontains=experience)).distinct()
            if proficient_area is not "":
                empty = False
                tutors += Tutor.objects.filter(Q(proficient_areas__icontains=proficient_area)).distinct()
            if fees is not None:
                empty = False
                tutors += Tutor.objects.filter(fees_per_hour <= fees).distinct()
            if cgpa is not None:
                empty = False
                tutors += Tutor.objects.filter(cgpa >= cgpa).distinct()

    return render_to_response('tuition/advanced_search.html',
                              {'user_group': user_group, 'current_home': "current", 'tutors':tutors, 'post':post, 'empty':empty, 'form':form},
                              context_instance=RequestContext(request))

        
    

## Advanced search with specified fields...
## googlemap location preference
## tuition service
## change the model to add subjects as per schools...check if the subject entered is valid and add it to the subjects available database.
## dynamic creation of check-boxes when school is added
# each school associated with courses.
# then each tutor associated with each school.