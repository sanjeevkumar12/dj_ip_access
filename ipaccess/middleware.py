from django.core.exceptions import PermissionDenied
from .models import BlockIPAddress


class IPAccessMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.validate_user_by_ip_address(request)
        return self.get_response(request)

    def get_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def validate_user_by_ip_address(self, request):
        client_ip = self.get_ip(request)
        if BlockIPAddress.objects.filter(network__supernets=client_ip).exists():
            raise PermissionDenied('You ip address is blocked')
        return True
