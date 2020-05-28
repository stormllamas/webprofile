# Views
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView


from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail


class Index(TemplateView):
  template_name = 'myapps/index.html'

  # def get_context_data(self, **kwargs):
  #   send_mail(
  #     'Welcome to Tech Llama',
  #     'My name is Storm Llamas and I can help you build your website',
  #     'me@stormllamas.tech',
  #     ['storm_sia_llamas@yahoo.com'],
  #     fail_silently=False
  #   )
  #   return super().get_context_data(**kwargs)


class About(TemplateView):
  template_name = 'myapps/about.html'


class ContactView(FormView):
  template_name = 'myapps/contact.html'
  form_class = ContactForm

  def form_valid(self, form):
    form.save()
    return super().form_valid(form)

  def form_invalid(self, form):
    messages.error(self.request, 'Please fill in the required fields')
    return super().form_invalid(form)
  
  def get_success_url(self):
    messages.success(self.request, 'Message Sent!')
    return reverse('contact')

class FrontendRenderView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'myapps/notfound.html', {})
