from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class EmailTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )


email_validation_token = EmailTokenGenerator()
