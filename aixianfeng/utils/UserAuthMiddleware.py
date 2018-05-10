from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from users.models import UserModel


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ticket = request.COOKIES.get('ticket')
        if request.path == '/users/cart/':
            ticket = request.COOKIES.get('ticket')
            if not ticket:
                return HttpResponseRedirect('/users/login/')
            users = UserModel.objects.filter(t_ticket=ticket)
            if users:
                request.user = users[0]
            else:
                return HttpResponseRedirect('/users/login/')
        else:
            if not ticket:
                return None
            users = UserModel.objects.filter(t_ticket=ticket)
            if users:
                request.user = users[0]