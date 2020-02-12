from django.views.generic import View

from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import ContactForm
from django.contrib import messages
from .models import Profile

def index(request):
    profile = get_object_or_404(Profile, pk=1)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        print('------------------------request is post------------------------')
        if form.is_valid():
            contact = form.save(commit=False)

            messages.success(request, 'Message Sent!')
            return redirect(reverse('index'))

    else:
        form = ContactForm()

    context = {
        'form': form,
        'resume': profile.resume
    }

    return render(request, 'myapps/index.html', context)

def about(request):
    profile = get_object_or_404(Profile, pk=1)
    return render (request, 'myapps/about.html', {'resume': profile.resume})

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

# def notfound(request, Exception=None):
#     return render (request, 'myapps/notfound.html', {})


class FrontendRenderView(View):
    def get(self, request, *args, **kwargs):
        return render (request, 'myapps/notfound.html', {})