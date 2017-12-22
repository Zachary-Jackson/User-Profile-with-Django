from django import forms

from . import models


class ProfileForm(forms.ModelForm):
    '''This is the form for the profile model.'''
    email_confirmation = forms.EmailField(required=False)

    class Meta:
        model = models.Profile
        fields = [
            'first_name',
            'last_name',
            'bio',
            'country',
            'date_of_birth',
            'hobby',
            'avatar',
            'email',
        ]

    def clean_bio(self):
        '''This checks to see if the bio is at least 10 characters long.'''
        bio = self.cleaned_data['bio']
        if len(bio) < 10:
            raise forms.ValidationError(
                "The bio must be at least ten characters")
        return bio

    def clean_email_confirmation(self):
        '''This checks to see if email and email_confirmation are the same.'''
        email = self.cleaned_data['email']
        email_confirmation = self.cleaned_data['email_confirmation']
        if email != email_confirmation:
            raise forms.ValidationError("Emails must match")
        return email_confirmation
