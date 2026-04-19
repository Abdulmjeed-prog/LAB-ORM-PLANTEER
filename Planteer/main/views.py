from django.shortcuts import render
from django.http import HttpRequest
from plants.models import Plant
from .forms import ContactForm
from .models import Contact
# Create your views here.

def home_view(request: HttpRequest):

    plants = Plant.objects.all().order_by('?')[:3]
    return render(request, 'main/home.html',{'plants': plants})

def contact_view(request:HttpRequest):

    if request.method == 'POST':

        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
        else:
            return render(request, 'main/contact.html',{'contact_form': contact_form})

    return render(request, 'main/contact.html')


def contact_msg_view(request:HttpRequest):
    contact_msg = Contact.objects.all()

    return render(request, 'main/contact_msg.html',{'messages': contact_msg})