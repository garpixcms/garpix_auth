from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView, RedirectView
from django.utils.translation import gettext_lazy as _


class LogoutView(RedirectView):
    def get_redirect_url(self):
        logout(self.request)
        return self.url


class LoginView(TemplateView):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
            # return JsonResponse({'success': True})
        elif user and not user.is_active:
            return JsonResponse({'detail': _('User is inactive. You must confirm the registration email address at registration.')}, status=400)
        return JsonResponse({'detail': _('Invalid: username / password')}, status=403)
