from rest_framework.exceptions import PermissionDenied


def superuser_only(function):
    def _inner(class_instance, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(class_instance, request, *args, **kwargs)

    return _inner
