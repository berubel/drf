from rest_framework import permissions

from .permissions import isStaffEditorPermission

class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser, isStaffEditorPermission]