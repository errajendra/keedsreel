from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Talvidouser



class TalvidouserCreationForm(UserCreationForm):
    class Meta:
        model = Talvidouser
        fields = ('email',)


class TalvidouserChangeForm(UserChangeForm):
    class Meta:
        model = Talvidouser
        fields = ('email',)