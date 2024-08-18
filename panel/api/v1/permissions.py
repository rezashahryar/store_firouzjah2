from rest_framework import permissions

from store.models import Store

# create your permissions here


class HasStore(permissions.BasePermission):
    # message = 'salam' # for return custom message when permission denied
    
    def has_permission(self, request, view):
        try:
            store = Store.objects.get(user=request.user)
            if store:
                return True
        except Store.DoesNotExist:
            return False
