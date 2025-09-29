from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend as SmtpEmailBackend


class EmailBackend(SmtpEmailBackend):
    def __init__(self, *args, **kwargs):
        fail_silently = kwargs.pop('fail_silently', False)
        kwargs['fail_silently'] = False
        super(EmailBackend, self).__init__(*args, **kwargs)
        kwargs['fail_silently'] = fail_silently
        print('email')

        host = getattr(settings, 'ALTERNATIVE_EMAIL_HOST', None)
        port = getattr(settings, 'ALTERNATIVE_EMAIL_PORT', None)

        if host is not None and port is not None:
            kwargs['username'] = getattr(settings, 'ALTERNATIVE_EMAIL_HOST_USER', self.username)
            kwargs['password'] = getattr(settings, 'ALTERNATIVE_EMAIL_HOST_PASSWORD', self.password)
            kwargs['use_tls'] = getattr(settings, 'ALTERNATIVE_EMAIL_USE_TLS', self.use_tls)
            self._alternative_backend = SmtpEmailBackend(
                host=host,
                port=port,
                **kwargs
            )
        else:
            self._alternative_backend = None

    def send_messages(self, email_messages):
        try:
            print('trying')

            return super(EmailBackend, self).send_messages(email_messages)
            print('sent')
        except Exception as e:
            print('error')
            if self._alternative_backend:
                print("shit happened here")
                return self._alternative_backend.send_messages(email_messages)
            else:
                print('raised e')
                raise e




from django.core.mail import EmailMessage
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  # replace with your settings module

mail = EmailBackend()

email = EmailMessage(
    "Test",
    "Bu test xat",
    "sirojiddinovsolohiddin961@gmail.com",
    ["sirojiddinovsolohiddin961@gmail.com"],
    # fail_silently=False
)

mail.send_messages([email])
