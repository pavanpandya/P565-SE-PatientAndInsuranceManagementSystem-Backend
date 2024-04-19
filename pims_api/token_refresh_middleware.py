from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

class TokenRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the access token is about to expire
        if hasattr(request, 'user') and request.user.is_authenticated:
            access_token_lifetime = timedelta(seconds=RefreshToken.lifetime)
            token_expires_at = request.user.access_token['exp']
            current_time = timezone.now()
            time_until_expiry = token_expires_at - current_time.timestamp()
            if time_until_expiry < access_token_lifetime.total_seconds():
                # Refresh the access token
                refresh = RefreshToken(request.user.refresh_token)
                access_token = str(refresh.access_token)
                response.set_cookie(key='access_token', value=access_token, httponly=True)

        return response
