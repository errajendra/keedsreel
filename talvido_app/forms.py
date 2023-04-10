from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Talvidouser


"""Creating custom creation form for admin"""

class TalvidouserCreationForm(UserCreationForm):

    class Meta:
        model = Talvidouser
        fields = ('email',)


"""Creating custom change form for admin"""

class TalvidouserChangeForm(UserChangeForm):
    
    class Meta:
        model = Talvidouser
        fields = ('email',)
