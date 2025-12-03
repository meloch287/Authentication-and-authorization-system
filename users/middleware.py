from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import User, Session
from .jwt_utils import decode_jwt_token


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.current_user = None

        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            payload = decode_jwt_token(token)
            if payload:
                user_id = payload.get('user_id')
                try:
                    user = User.objects.get(id=user_id, is_active=True)
                    request.current_user = user
                    return
                except User.DoesNotExist:
                    pass

        session_token = request.COOKIES.get('session_id')
        if session_token:
            try:
                session = Session.objects.select_related('user').get(
                    session_token=session_token,
                    expires_at__gt=timezone.now()
                )
                if session.user.is_active:
                    request.current_user = session.user
            except Session.DoesNotExist:
                pass
