from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.db.models import Sum
from .models import Attendee, ActivityLog
from .forms import PointsForm, CSVForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import re, qrcode, cv2, csv, io, os

import numpy as np
import pyzbar.pyzbar as pyzbar

def index(request):
    context = {

    }

    return render(request, 'attendees/index.html')


def overview(request):
  sort = request.GET.get('sort')
  desc = request.GET.get('desc', '')

  if desc == 'true':
    desc = '-'
  
  if sort == None:
    sort = '-points_earned'

  queryset = Attendee.objects.order_by((str(desc)+str(sort)), 'last_name')
    
  ag = Attendee.objects.aggregate(tpe=Sum('points_earned'), tpr=Sum('points_redeemed'), tpb=Sum('points_balance'))
  page = request.GET.get('page', 1)
  
  paginator = Paginator(queryset, 50)

  try:
    attendees = paginator.page(page)
  except PageNotAnInteger:
    attendees = paginator.page(1)
  except:
    attendees = paginator.page(paginator.num_pages)

  context = {
    'attendees': attendees,
    'tpe': ag['tpe'],
    'tpr': ag['tpr'],
    'tpb': ag['tpb'],
  }

  return render(request, 'attendees/overview.html', context)

# class IndexListView(ListView):
#     model = Attendee
#     context_object_name = 'attendees'
#     template_name = 'attendees/index.html'
#     paginate_by = 20

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Attendees of the Event'
#         return context

#     def get_queryset(self):
#         queryset = Attendee.objects.order_by('-present','last_name', 'first_name').aggregate(tpe=Sum('points_earned'), tpr=Sum('points_redeemed'), tpb=Sum('points_balance'))
#         return queryset

def qrgenerated(request):
  qrattendees = Attendee.objects.all()
  attendees = Attendee.objects.order_by('-present','last_name', 'first_name')[:10]
  os.makedirs("QRCodes/", exist_ok=True)

  for a in qrattendees:
    qr = qrcode.QRCode(
      version=1,
      box_size=15,
      border=5
      )
    fullname = a.last_name+'_'+a.first_name
    aid = a.id
    data = 'Card Number: '+str(aid)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('QRCodes/QR_'+fullname+'.png')

  messages.success(request, 'QR Codes Successfully Generated')
  return redirect('overview/')

def confirmation(request, attendee_id):
  attendee = Attendee.objects.get(pk=attendee_id)
  response = "You're looking at the STORM CARDS confirmation link for attendee: "+attendee.first_name+' '+attendee.last_name+" with the id number: %s."
  return HttpResponse(response % attendee_id)

def qrscanner(request):
  cap = cv2.VideoCapture(0)
  font = cv2.FONT_HERSHEY_PLAIN
  aid = None
  while aid is None:
    _, frame = cap.read()
    decodedObjects = pyzbar.decode(frame)

    for obj in decodedObjects:
      aid = re.findall('Card Number: ([0-9]+)', str(obj.data))
      try:
        attendee = Attendee.objects.get(pk=str(aid[0]))
        attendee.present = True
        attendee.timestamp = timezone.now()
        attendee.activity.update_or_create(time_log=attendee.timestamp)
        attendee.save()
        messages.success(request, 'QR Successfully Scanned')
        context = {
          'attendee': attendee,
        }
      except:
          messages.error(request, 'Scan Unsuccessful')
          context = {}

    cv2.imshow("QR Reader", frame)

    if aid is not None:
      cv2.destroyAllWindows()
      break

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
      messages.error(request, 'No QR Scanned')
      context = {}
      cv2.destroyAllWindows()
      break

  return render(request, 'attendees/qrscanner.html', context)

# def details(request, attendee_id):
#     attendee = get_object_or_404(Attendee, pk=attendee_id)

#     context = {
#         'logcount': attendee.activity.count(),
#         'attendee': attendee,
#     }

#     return render(request, 'attendees/details.html', context)

class AttendeeActivities(DetailView):
    model = Attendee
    context_object_name = 'attendee'
    template_name = 'attendees/details.html'

class Activity(ListView):
    context_object_name = 'activity_log'
    template_name = 'attendees/activity_log.html'

    def get_queryset(self):
        return ActivityLog.objects.all().order_by('-time_log')

def attendee_upload(request):
    template = "attendees/attendee_upload.html"

    if request.method == "POST":
        form = CSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data.get('file')

            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'That was not a CSV file')
                return render(request, template, {'order': 'Order of the CSV should be first_name, last_name', 'form': form})

            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                _, created = Attendee.objects.update_or_create(
                    first_name=column[0],
                    last_name=column[1],
                )
            
            messages.success(request, 'File Successfully Uploaded')

            context = {
                'order': 'Order of the CSV should be first_name, last_name',
                'form': form
            }
            return render(request, template, context)

    else:
        form = CSVForm()

    return render(request, template, {'order': 'Order of the CSV should be first_name, last_name', 'form': form})


def claim_points(request):
    if request.method == "POST":
        form = PointsForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            claim_points = float(amount)

            cap = cv2.VideoCapture(0)
            font = cv2.FONT_HERSHEY_PLAIN
            aid = None

            while aid is None:
                _, frame = cap.read()
                
                decodedObjects = pyzbar.decode(frame)

                for obj in decodedObjects:
                    aid = re.findall('Card Number: ([0-9]+)', str(obj.data))
                    cv2.putText(frame, str(aid), (50, 50), font, 3, (255, 255, 255), 2)

                    try:
                        attendee = get_object_or_404(Attendee, pk=str(aid[0]))
                        attendee.present = True
                        attendee.timestamp = timezone.now()
                        attendee.points_earned += claim_points
                        attendee.points_balance += claim_points
                        attendee.activity.update_or_create(
                            time_log=attendee.timestamp,
                            points_claim=claim_points,
                            total_points_earned=attendee.points_earned,
                            total_points_balance=attendee.points_balance
                            )
                        attendee.save()
                        messages.success(request, 'QR Successfully Scanned')
                        context = {
                            'scan': 'QR Successfully Scanned',
                            'payment': amount,
                            'claim_points': claim_points,
                            'attendee': attendee,
                        }
                    except:
                        messages.error(request, 'Scan Unsuccessful')
                        context = {
                            'noscan': 'QR Scan Unsuccessful'
                        }
                    

                cv2.imshow("QR Scanner", frame)

                if aid is not None:
                    cv2.destroyAllWindows()
                    break

                key = cv2.waitKey(1) & 0xFF
                if key == 27:
                    context = {
                        'noscan': 'No QR Scanned',
                    }
                    cv2.destroyAllWindows()
                    break

            return render(request, 'attendees/qrscanner.html', context)

    else:
        form = PointsForm()
        
    return render(request, 'attendees/cr_points.html', {'order': 'Set the amount of points to claim', 'breadcrumb':'Claim Points', 'form': form})


def redeem_points(request):
    if request.method == "POST":
        form = PointsForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            redeem_points = float(amount)

            cap = cv2.VideoCapture(0)
            font = cv2.FONT_HERSHEY_PLAIN

            aid = None

            while aid is None:
                _, frame = cap.read()
                
                decodedObjects = pyzbar.decode(frame)

                for obj in decodedObjects:
                    aid = re.findall('Card Number: ([0-9]+)', str(obj.data))
                    cv2.putText(frame, str(aid), (50, 50), font, 3, (255, 255, 255), 2)

                    try:
                      attendee = get_object_or_404(Attendee, pk=str(aid[0]))
                      attendee.present = True
                      attendee.timestamp = timezone.now()
                      attendee.points_redeemed += redeem_points
                      attendee.points_balance -= redeem_points
                      attendee.activity.update_or_create(
                          time_log=attendee.timestamp,
                          points_redeem=redeem_points,
                          total_points_redeemed=attendee.points_redeemed,
                          total_points_balance=attendee.points_balance,
                          )
                      attendee.save()
                      messages.success(request, 'QR Successfully Scanned')
                      context = {
                          'scan': 'QR Successfully Scanned',
                          'payment': amount,
                          'redeem_points': redeem_points,
                          'attendee': attendee,
                      }
                    except:
                      messages.error(request, 'Scan Unsuccessful')
                      context = {
                          'noscan': 'QR Scan Unsuccessful'
                      }

                cv2.imshow("QR Scanner", frame)

                if aid is not None:
                    cv2.destroyAllWindows()
                    break

                key = cv2.waitKey(1) & 0xFF
                if key == 27:
                    context = {
                        'noscan': 'No QR Scanned',
                    }
                    cv2.destroyAllWindows()
                    break

            return render(request, 'attendees/qrscanner.html', context)

    else:
        form = PointsForm()
        
    return render(request, 'attendees/cr_points.html', {'order': 'Set the amount to use for redemption', 'breadcrumb':'Redeem Points', 'form': form})

class AttendeeUpdateView(UpdateView):
    model = Attendee
    pk_url_kwarg = 'pk'
    fields = ('first_name', 'last_name',)
    template_name = 'attendees/edit_attendee.html'
    context_object_name = 'attendee'

    def form_valid(self, form):
        attendee = form.save(commit=True)
        return redirect('attendees:details', pk=attendee.pk)


        
    
    

