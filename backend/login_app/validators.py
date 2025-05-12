# myapp/validators.py
import re
from django.core.exceptions import ValidationError

class ComplexityPasswordValidator:
    def validate(self, password, user=None):#noqa: ARG002
        if not re.findall('[A-Z]', password):
            raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')
        if not re.findall('[a-z]', password):
            raise ValidationError('La contraseña debe contener al menos una letra minúscula.')
        if not re.findall('[0-9]', password):
            raise ValidationError('La contraseña debe contener al menos un número.')
        if not re.findall(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('La contraseña debe contener al menos un carácter especial.')

    def get_help_text(self):
        return 'Tu contraseña debe tener al menos una mayúscula, una minúscula, un número y un carácter especial.'
