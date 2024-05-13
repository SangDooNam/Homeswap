from django.shortcuts import render
from django.core.mail import send_mail
from .forms import SupportForm
from django.conf import settings

def submit_support_request(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            # Process the support request
            # For example, save the support request to the database
            form.save()

            # Send a response email to the user
            user_email = form.cleaned_data['email']  # Assuming 'email' is the field for user's email address
            send_support_response_email(user_email)

            # Optionally, you can display a success message or redirect the user to a thank you page
            return render(request, 'support/thank_you.html')
    else:
        form = SupportForm()

    return render(request, 'support/submit_support_request.html', {'form': form})


def send_support_response_email(user_email):
    # Define the email subject and message
    subject = 'Thank you for your support request'
    message = 'We have received your support request and will respond as soon as possible.'

    # Set the sender email address
    sender_email = settings.EMAIL_HOST_USER  # Use the email address specified in settings

    # Send the email
    send_mail(subject, message, sender_email, [user_email])
