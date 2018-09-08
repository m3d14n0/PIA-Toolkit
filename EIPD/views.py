from .forms import ContactForm
from django.views.generic.edit import FormView
from django.http import HttpResponse
from django.urls import reverse_lazy

class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        c_name = form.cleaned_data['contact_name']
        c_email = form.cleaned_data['contact_email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['content']
        form.send_contact_email(c_name, c_email, subject, message)
        return super(ContactView, self).form_valid(form)

def download_guide_PILAR_es(request, **kwargs):
    filepath = 'EIPD/www/static/PILAR_manual.pdf'
    fsock = open(filepath, 'rb')
    response = HttpResponse(fsock, content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename=int_PILAR_es.pdf"
    return response

def download_manual_es(request, **kwargs):
    filepath = 'EIPD/www/static/PIA Toolkit_manual_es.pdf'
    fsock = open(filepath, 'rb')
    response = HttpResponse(fsock, content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename=PIA Toolkit_manual_es.pdf"
    return response