from django.core.exceptions import ValidationError


class CustomPasswordValidator(object):
    '''This verifies that a password is correct.'''

    def validate(self, password, user=None):
        '''This checks to see if there is an int, upper and lowercase
        letter, and that there are special characters.'''
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        # This checks to see is the password has upper and lowercase letters,
        # an integer, and a special character.
        found_upper = False
        found_lower = False
        found_special = False
        found_int = False
        for letter in password:
            if letter in special_characters:
                found_special = True
            else:
                if letter.isdigit():
                    found_int = True
                elif letter.isupper():
                    found_upper = True
                else:
                    found_lower = True

        # Checks to see if any letter is not found.
        if (not found_lower or not found_upper
                or not found_special or not found_int):
            raise ValidationError('Password must contain an upper and ' +
                                  'lowercase letter as well as ' +
                                  ' a special character and integer.')

    def get_help_text(self):
        return ('Password must contain an upper and lowercase letter'
                ' as well as a special character and integer.')
