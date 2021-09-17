from django.apps import AppConfig


class VerificationCodeConfig(AppConfig):
    name = 'verification_code'

    def ready(self):
        import verification_code.signals
