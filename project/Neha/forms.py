from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','created_at','created_by','is_admin','soft_delete')
        # fields = ('first_name', 'last_name', 'phone', 'email', 'pan_card','profile_pic')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AutoProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone', 'email', 'pan_card','profile_pic')

    def __init__(self, *args, **kwargs):
        super(AutoProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class PasswordChange(forms.Form):
    new_password1 = forms.PasswordInput()
    new_password2 = forms.PasswordInput()

    def clean(self):
        cleaned_data = super(PasswordChange, self).clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if not new_password1 and not new_password2:
            raise forms.ValidationError('You have to Enter Password!')
        if new_password1 != new_password2:
            raise forms.ValidationError('You have to Enter Same Password!')