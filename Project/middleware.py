from django.shortcuts import redirect
from django.http import HttpResponse, HttpRequest,HttpResponseRedirect
from django.contrib import messages, auth

class LogoutRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the user is logged out and trying to access a protected page
        if not request.user.is_authenticated and response.status_code == 404:
            messages.error(request, 'Please Login to access this feature..!')
            return redirect('log')  # Redirect to the login page or any other desired page
        if request.user.is_authenticated and response.status_code == 404:
            messages.error(request, 'We are working on the Requested Page')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return response