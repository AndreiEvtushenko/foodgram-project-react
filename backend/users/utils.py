from datetime import datetime, timedelta
from django.conf import settings


def custom_jwt_payload(user):
    """Set"""

    return {
        'password': user.password,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(
            seconds=settings.JWT_EXPIRATION_DELTA
        )
    }
