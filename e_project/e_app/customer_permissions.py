from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, SAFE_METHODS

excptionMessage = "access denied you cannot perfom this operation"

class IsOwner(permissions.BasePermission):
    message = excptionMessage

    def has_object_permission(self, request, view, obj):
        return obj.customer_id == request.user


class IsOwnerUser(permissions.BasePermission):
    message = excptionMessage

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAdminUserOrReadOnly(IsAdminUser):
    message = excptionMessage
    def has_permission(self, request, view):
        is_admin = super(
            IsAdminUserOrReadOnly, 
            self).has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin