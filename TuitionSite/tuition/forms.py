from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import TuitionSite.tuition.models
from models import Advertize4Tutor, Tutor, Feedback, Day, Subject, School

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label="Username")
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
            help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
            error_messages = {'Error!': _("Username can only contain letters, digits and @/./+/-/_.")})
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Confirm Password"), widget=forms.PasswordInput,
	        help_text = _("Retype the password here"))
    email = forms.EmailField(label="Email address")
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


def get_advertize_form(user):
    class Advertize4TutorForm(forms.ModelForm):

        class Meta:
            model = Advertize4Tutor
            fields = ['subject', 'advertisement']

        #def save(self):
        #   data = self.cleaned_data
        #  Advertize4Tutor.objects.create(username = user.username, first_name = user.first_name, last_name = user.last_name, email = user.email, subject = data['subject'], advertisement = data['advertisement'])

    return Advertize4TutorForm


class TutorForm(ModelForm):

    class Meta:
        model = Tutor
        exclude = ['user',]

#    def save(self, user):
#        self.instance.user = user
#        return super(TutorForm, self).save(commit=True)


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        exclude = ['tutor', 'username']


class AdvancedSearchForm(forms.Form):
    first_name = forms.CharField(label="First Name", required=False)
    last_name = forms.CharField(label="Last Name", required=False)
    school = forms.ModelChoiceField(queryset= School.objects.all(), label="School", required=False)
    subject = forms.ModelChoiceField(queryset= Subject.objects.all(), label="Subject", required=False)
    proficient_area = forms.CharField(label = "Proficient Areas", required=False)
    fees = forms.DecimalField(decimal_places=2, label="Maximum fees per hour", required=False)
    experience = forms.CharField(label="Experience", required=False)
    days = forms.ModelChoiceField(queryset = Day.objects.all(), label="Day", required=False)
    cgpa = forms.DecimalField(decimal_places=2, label="CGPA lower limit", required=False)





#class vModelChoiceField(forms.ModelChoiceField):
#  def label_from_instance(self, obj):
#    return "%s" % obj.day
#
#class daysList(forms.Form):
#  n = vModelChoiceField(queryset=Day.objects.all(), empty_label="All")