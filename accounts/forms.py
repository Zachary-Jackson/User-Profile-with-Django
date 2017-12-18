from django import forms

from . import models


class ProfileForm(forms.ModelForm):
    '''This is the form for the profile model.'''
    email_confirmation = forms.EmailField()

    class Meta:
        model = models.Profile
        fields = [
            'first_name',
            'last_name',
            'email',
            'date_of_birth',
            'bio',
            'avatar',
            'hobby',
            'country'
        ]

    def clean_email_confirmation(self):
        '''This checks to see if email and email_confirmation are the same.'''
        email = self.cleaned_data['email']
        email_confirmation = self.cleaned_data['email_confirmation']
        if email != email_confirmation:
            raise forms.ValidationError("Emails must match")
