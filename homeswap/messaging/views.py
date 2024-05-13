from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MessageForm

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            # Redirect to a success page.
            return redirect('message_sent_success')
    else:
        form = MessageForm()

    return render(request, 'messaging/send_message.html', {'form': form})

def message_sent_success(request):
    return render(request, 'messaging/message_sent_success.html')
