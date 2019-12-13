from django.shortcuts import render, redirect, reverse
from .forms import ContactForm
from django.contrib import messages

def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        print('------------------------request is post------------------------')
        if form.is_valid():
            contact = form.save(commit=False)

            messages.success(request, 'Message Sent!')
            return redirect(reverse('index'))

    else:
        form = ContactForm()

    return render(request, 'myapps/index.html', {'form':form})

def about(request):
    return render (request, 'myapps/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            messages.success(request, 'Message Sent!')
            return redirect(reverse('contact'))

        else:
            messages.error(request, 'Please fill in the required fields')

    else:
        form = ContactForm()

    return render (request, 'myapps/contact.html', {'form':form})
