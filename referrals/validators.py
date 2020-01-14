from rest_framework import serializers


class AlreadyExistUserEmailValidator:

    def __init__(self, queryset, message=''):
        self.queryset = queryset
        self.message = message

    def __call__(self, value):
        result = self.queryset.filter(email=value)
        if len(result):
            raise serializers.ValidationError(self.message)
