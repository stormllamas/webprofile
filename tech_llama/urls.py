from django.contrib import admin
from django.urls import path, include, re_path

# from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from myapps import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapps.urls')),
    path('qr/', include('attendees.urls')),

    # path('signup/', accounts_views.signup, name='signup'),
    # path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('settings/account/', accounts_views.UserUpdateView.as_view(), name='my_account'),
    
    # path('reset/',
    #     auth_views.PasswordResetView.as_view(
    #     template_name='accounts/password_reset.html',
    #     email_template_name='accounts/password_reset_email.html',
    #     subject_template_name='accounts/password_reset_subject.txt'
    #     ),
    #     name='password_reset'),
    # path('reset/done/',
    #     auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
    #     name='password_reset_done'),
    # path('reset/<uidb64>/<token>/',
    #     auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
    #     name='password_reset_confirm'),
    # path('reset/complete/',
    #     auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
    #     name='password_reset_complete'),

    # path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
    #     name='password_change'),
    # path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
    #     name='password_change_done'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    re_path(r'^(?P<path>.*)/$', views.FrontendRenderView.as_view(), name='notfound')
]

# handler404 = 'myapps.views.notfound'
# handler500 = 'myapps.views.notfound'