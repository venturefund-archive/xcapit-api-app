from rest_framework import filters


class UserFilterBackend(filters.BaseFilterBackend):
    """
    Filtra usuario por email y is_active.
    """

    def filter_queryset(self, request, queryset, view):
        email = request.query_params.get('email', None)
        is_active = request.query_params.get('is_active', None)
        if email is not None and email != '':
            queryset = queryset.filter(email__icontains=email)
        if is_active is not None and is_active != '' and is_active != 'all':
            queryset = queryset.filter(is_active=is_active)
        return queryset
