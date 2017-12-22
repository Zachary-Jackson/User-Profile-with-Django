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
        # I can find bio's contents with self.cleaned_data['bio']
        # This clean_bio function causes bio to be null
        import pdb; pdb.set_trace()
        pass

    def clean_email_confirmation(self):
        '''This checks to see if email and email_confirmation are the same.'''
        email = self.cleaned_data['email']
        email_confirmation = self.cleaned_data['email_confirmation']
        if email != email_confirmation:
            raise forms.ValidationError("Emails must match")
