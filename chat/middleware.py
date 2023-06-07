from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from channels.middleware import BaseMiddleware

User = get_user_model()

@database_sync_to_async
def get_user(scope):
    if 'session' in scope:
        session_key = scope['session'].session_key
        if session_key:
            return User.objects.get_or_create(
                session_key=session_key
            )[0]
    return AnonymousUser()

class AuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        access_token = headers[b"authorization"].decode()
        print(access_token)
        scope["user"] = access_token
        # Run the inner application along with the scope
        return await self.inner(scope, receive, send)
