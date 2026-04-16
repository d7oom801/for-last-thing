from .models import AuditLog


class MedicalAuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Let the request pass through to the view normally
        response = self.get_response(request)

        # 2. Check if this is an action we want to log
        # We only care if a logged-in user is Modifying (PATCH), Creating (POST), or Deleting (DELETE) data.
        # We ignore 'GET' requests so we don't flood the database every time someone just loads a page.
        if request.user.is_authenticated and request.method in ['POST', 'PATCH', 'PUT', 'DELETE']:

            # 3. Grab the user's IP Address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            # 4. Create a readable description of what they did
            action_desc = f"Performed {request.method} request on {request.path}"

            # 5. Silently save the log to the database
            AuditLog.objects.create(
                user=request.user,
                action=action_desc,
                ip_address=ip
            )

        return response