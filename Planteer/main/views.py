from django.shortcuts import render
from django.http import HttpRequest
from plants.models import Plant
from .forms import ContactForm
from .models import Contact
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string

# Create your views here.

def home_view(request: HttpRequest):

    plants = Plant.objects.all().order_by('?')[:3]
    return render(request, 'main/home.html',{'plants': plants})

def contact_view(request:HttpRequest):

    if request.method == 'POST':
        name = request.POST['first_name']
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            content = render_to_string("main/mail/contact_mail.html",{'name': name})
            send_to = request.POST['email']
            email_message = EmailMessage("Thank You", content, settings.EMAIL_HOST_USER, [send_to])
            email_message.content_subtype = "html"
            email_message.send()
            messages.success(request,'Your message has been receive we will contact you soon', 'alert-success')
            return render(request, 'main/contact.html')
        else:
            messages.error(request,"Something goes wrong", "alert-danger")
            return render(request, 'main/contact.html',{'contact_form': contact_form})

    return render(request, 'main/contact.html')


def contact_msg_view(request:HttpRequest):
    contact_msg = Contact.objects.all()

    return render(request, 'main/contact_msg.html',{'messages': contact_msg})