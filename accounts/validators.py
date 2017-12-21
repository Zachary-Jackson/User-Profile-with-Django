from django.core.exceptions import ValidationError


class CustomPasswordValidator(object):
    '''This verifies that a password is correct.'''

    def validate(self, password, user=None):
        '''This checks to see if there is an int, upper and lowercase
        letter, and that there are special characters.'''
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        # This checks to see is the password has upper and lowercase letters.
        found_upper = False
        found_lower = False
        found_special = False
        for letter in password:
            if letter in special_characters:
                found_special = True
            else:
                if letter.isupper():
                    found_upper = True
                else:
                    found_lower = True

        # Checks to see if any letter is not found.
        if not found_lower or not found_upper or not found_special:
            raise ValidationError('Password must contain an upper and ' +
                                  'lowercase letter as well as ' +
                                  ' a special character.')

    def get_help_text(self):
        return ('Password must contain an upper and lowercase letter'
                ' as well as a special character.')
