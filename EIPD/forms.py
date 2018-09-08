from django import forms
from django.conf import settings
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    subject = forms.CharField(label=("Subject"), required=False)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

    def send_contact_email(self,contact_name, contact_email, contact_subject, content):
        text_content = 'Contact Form from PIA Toolkit'
        subject = 'ContactForm'
        template_name = "contact/contact_email.html"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipients = ['m3d14n0@protonmail.com']

        context = {
            'contact_name': contact_name,
            'contact_email': contact_email,
            'subject': contact_subject,
            'content': content,
        }

        html_content = render_to_string(template_name, context)
        email = EmailMultiAlternatives(subject, text_content, from_email, recipients)
        email.attach_alternative(html_content, "text/html")
        email.send()