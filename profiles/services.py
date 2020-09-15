from profiles.models import Profile


class ProfileUpdateService:
    def __init__(self, serializer_class, profile: Profile, data: dict):
        self.serializer_class = serializer_class
        self.data = data
        self.profile = profile
        self.errors = []

    def update(self):
        serializer = self.serializer_class(instance=self.profile, data=self.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return True
        else:
            self.errors = serializer.errors
