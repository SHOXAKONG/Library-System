import datetime
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from django.utils.timezone import now


class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_active = request.session.get('last_activity')
            if last_active:
                last_active_time = datetime.datetime.fromisoformat(last_active)
                if (now() - last_active_time).total_seconds() > 8400000:
                    logout(request)
                request.session['last_activity'] = now().isoformat()
        response = self.get_response(request)
        return response

class FileUploadRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/upload/') and not request.user.is_authenticated:
            return HttpResponseForbidden("Enter FileUpload System")
        response = self.get_response(request)
        return response