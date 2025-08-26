from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    '''Custom Permission class for users'''
    def has_permission(self, request, view):
        if view.action == "list":
            return request.user.is_authenticated
        if view.action is None:  # use some actions with browsable api
            return True

        elif view.action in [
            "create",
            "retrieve",
            "update",
            "partial_update",
            "destroy",
            "login",
        ]:
            return True
        else:
            return False