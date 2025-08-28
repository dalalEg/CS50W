from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied
class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    Non-admin users can only read objects.
    """
    def has_permission(self, request, view):
        # Allow read-only access for non-admin users
        if request.method in SAFE_METHODS:
            return True 
        # Allow write access only for admin users
        return request.user and request.user.is_staff
    

class IsReviewOwnerOrReadOnly(BasePermission):
    message = "You can only edit or delete your own review."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if obj.user != request.user:
            raise PermissionDenied(detail=self.message)
        return True
    
class IsBookingOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
   
        return (obj.user == request.user or request.user.is_staff) and request.user.is_authenticated


class IsNotificationOwnerOrStaff(BasePermission):
      def has_object_permission(self, request, view, obj):
      
        return (obj.user == request.user or request.user.is_staff) and request.user.is_authenticated
class IsAuthenticated(BasePermission):
    """
    Custom permission to only allow authenticated users to access the view.
    """
    def has_permission(self, request, view):
        # Allow access only if the user is authenticated
        return request.user and request.user.is_authenticated
    

class IsWatchlistOwnerOrStaff(BasePermission):
    """
    Custom permission to only allow owners of a watchlist or staff users to edit it.
    """
    def has_object_permission(self, request, view, obj):
      
        return (obj.user == request.user or request.user.is_staff) and request.user.is_authenticated

class IsUserEmailVerified(BasePermission):
    """
    Custom permission to only allow users with verified email to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.email_verified

    def has_object_permission(self, request, view, obj):
        # same check at the object level
        return self.has_permission(request, view)
