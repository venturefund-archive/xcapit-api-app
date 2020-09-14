import re
from rest_framework import serializers


def lowercase_validator(password):
    if re.search(r'[a-z]', password):
        return password
    else:
        raise serializers.ValidationError('La password debe contener al menos una minúscula')


def uppercase_validator(password):
    if re.search(r'[A-Z]', password):
        return password
    else:
        raise serializers.ValidationError('La password debe contener al menos una mayúscula')


def number_validator(password):
    if re.search(r'[0-9]', password):
        return password
    else:
        raise serializers.ValidationError('La password debe contener al menos un número')
