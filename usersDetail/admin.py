from django.contrib import admin
from django import forms
from django.contrib.auth.hashers import make_password
from .models import usersDetail

from django.contrib import admin
from .models import HealthyInstitution
class UsersDetailForm(forms.ModelForm):
    class Meta:
        model = usersDetail
        fields = '__all__'
        widgets = {
                    'password': forms.PasswordInput(render_value=True), 
                }
    def save(self, commit=True):
        instance = super(UsersDetailForm, self).save(commit=False)
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            hashed_password = make_password(password)
            instance.password = hashed_password
        if commit:
            instance.save()
        return instance

class UsersDetailAdmin(admin.ModelAdmin):
    form = UsersDetailForm

admin.site.register(HealthyInstitution)


admin.site.register(usersDetail, UsersDetailAdmin)
