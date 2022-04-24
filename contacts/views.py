
from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']
        #check for duplicacy:
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'Enquiry has already been submitted')
                return redirect('/listings/'+listing_id)
        contact = Contact(
            listing=listing,
            listing_id=listing_id,
            name=name,
            phone=phone,
            email=email,
            message=message,
            user_id=user_id,
            )
        contact.save()

        #mailing
        send_mail(
            'Property listing inquiry',
            'There has been an inquiry for the listing ' + listing + 'sign in admin panel for more info',
            'barui240@gmail.com',
            [realtor_email, 'barui504@gmail.com',],
            fail_silently=False
        )
        messages.success(request, 'your request has been submitted')
        return redirect('/listings/'+listing_id)