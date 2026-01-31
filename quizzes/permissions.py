from rest_framework.permissions import BasePermission

#this permission is for quizzes
class IsPublicOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.owner.id or obj.is_public:
            return True
        return False

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.owner.id