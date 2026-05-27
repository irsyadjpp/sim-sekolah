"""
Authorization services for AI Platform

This module provides role-based access control (RBAC) functionality.
"""

from typing import Dict, List, Set, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class Permission(Enum):
    """System permissions."""
    # Document permissions
    DOCUMENT_READ = "document:read"
    DOCUMENT_WRITE = "document:write"
    DOCUMENT_DELETE = "document:delete"
    
    # User permissions
    USER_READ = "user:read"
    USER_WRITE = "user:write"
    USER_DELETE = "user:delete"
    
    # System permissions
    SYSTEM_ADMIN = "system:admin"
    SYSTEM_MONITOR = "system:monitor"
    
    # AI service permissions
    AI_QUERY = "ai:query"
    AI_TRAIN = "ai:train"
    AI_DEPLOY = "ai:deploy"


@dataclass
class Role:
    """User role with permissions."""
    name: str
    permissions: Set[Permission] = field(default_factory=set)
    description: str = ""
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if role has permission."""
        return permission in self.permissions
    
    def add_permission(self, permission: Permission):
        """Add permission to role."""
        self.permissions.add(permission)
    
    def remove_permission(self, permission: Permission):
        """Remove permission from role."""
        self.permissions.discard(permission)


class RoleManager:
    """
    Role-based access control manager.
    
    Manages roles, permissions, and authorization checks.
    """
    
    def __init__(self):
        """Initialize role manager."""
        self.roles: Dict[str, Role] = {}
        self.user_roles: Dict[str, Set[str]] = {}  # user_id -> role_names
        self._setup_default_roles()
    
    def _setup_default_roles(self):
        """Setup default system roles."""
        # Admin role - all permissions
        admin_role = Role(
            name="admin",
            permissions=set(Permission),
            description="System administrator with full access"
        )
        self.add_role(admin_role)
        
        # Teacher role
        teacher_role = Role(
            name="teacher",
            permissions={
                Permission.DOCUMENT_READ,
                Permission.DOCUMENT_WRITE,
                Permission.USER_READ,
                Permission.AI_QUERY,
                Permission.AI_TRAIN,
            },
            description="Teacher with content creation and AI training access"
        )
        self.add_role(teacher_role)
        
        # Student role
        student_role = Role(
            name="student",
            permissions={
                Permission.DOCUMENT_READ,
                Permission.AI_QUERY,
            },
            description="Student with read and query access"
        )
        self.add_role(student_role)
        
        # Viewer role
        viewer_role = Role(
            name="viewer",
            permissions={
                Permission.DOCUMENT_READ,
            },
            description="Read-only access"
        )
        self.add_role(viewer_role)
    
    def add_role(self, role: Role):
        """
        Add a role to the manager.
        
        Args:
            role: Role to add
        """
        self.roles[role.name] = role
        logger.info(f"Added role: {role.name}")
    
    def get_role(self, role_name: str) -> Optional[Role]:
        """
        Get a role by name.
        
        Args:
            role_name: Name of the role
            
        Returns:
            Role instance if found, None otherwise
        """
        return self.roles.get(role_name)
    
    def remove_role(self, role_name: str) -> bool:
        """
        Remove a role.
        
        Args:
            role_name: Name of the role to remove
            
        Returns:
            True if role was removed
        """
        if role_name in self.roles:
            del self.roles[role_name]
            # Remove role from all users
            for user_id, roles in self.user_roles.items():
                roles.discard(role_name)
            logger.info(f"Removed role: {role_name}")
            return True
        return False
    
    def assign_role(self, user_id: str, role_name: str) -> bool:
        """
        Assign a role to a user.
        
        Args:
            user_id: User ID
            role_name: Name of the role
            
        Returns:
            True if role was assigned
        """
        if role_name not in self.roles:
            logger.warning(f"Role not found: {role_name}")
            return False
        
        if user_id not in self.user_roles:
            self.user_roles[user_id] = set()
        
        self.user_roles[user_id].add(role_name)
        logger.info(f"Assigned role {role_name} to user {user_id}")
        return True
    
    def remove_role_from_user(self, user_id: str, role_name: str) -> bool:
        """
        Remove a role from a user.
        
        Args:
            user_id: User ID
            role_name: Name of the role
            
        Returns:
            True if role was removed
        """
        if user_id in self.user_roles:
            if role_name in self.user_roles[user_id]:
                self.user_roles[user_id].discard(role_name)
                logger.info(f"Removed role {role_name} from user {user_id}")
                return True
        return False
    
    def get_user_roles(self, user_id: str) -> List[str]:
        """
        Get all roles assigned to a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of role names
        """
        return list(self.user_roles.get(user_id, set()))
    
    def get_user_permissions(self, user_id: str) -> Set[Permission]:
        """
        Get all permissions for a user based on their roles.
        
        Args:
            user_id: User ID
            
        Returns:
            Set of permissions
        """
        permissions = set()
        
        for role_name in self.get_user_roles(user_id):
            role = self.get_role(role_name)
            if role:
                permissions.update(role.permissions)
        
        return permissions
    
    def has_permission(self, user_id: str, permission: Permission) -> bool:
        """
        Check if a user has a specific permission.
        
        Args:
            user_id: User ID
            permission: Permission to check
            
        Returns:
            True if user has permission
        """
        user_permissions = self.get_user_permissions(user_id)
        return permission in user_permissions
    
    def has_any_permission(self, user_id: str, permissions: List[Permission]) -> bool:
        """
        Check if a user has any of the specified permissions.
        
        Args:
            user_id: User ID
            permissions: List of permissions to check
            
        Returns:
            True if user has any of the permissions
        """
        user_permissions = self.get_user_permissions(user_id)
        return any(perm in user_permissions for perm in permissions)
    
    def has_all_permissions(self, user_id: str, permissions: List[Permission]) -> bool:
        """
        Check if a user has all of the specified permissions.
        
        Args:
            user_id: User ID
            permissions: List of permissions to check
            
        Returns:
            True if user has all permissions
        """
        user_permissions = self.get_user_permissions(user_id)
        return all(perm in user_permissions for perm in permissions)


def require_permission(permission: Permission, role_manager: Optional[RoleManager] = None):
    """
    Decorator to require specific permission for function access.
    
    Args:
        permission: Required permission
        role_manager: Optional role manager
        
    Returns:
        Decorator function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get user ID from kwargs or args (assuming first arg is self or user_id)
            user_id = kwargs.get('user_id')
            if user_id is None and len(args) > 0:
                # Try to get user_id from first argument if it's a string
                if isinstance(args[0], str):
                    user_id = args[0]
            
            if user_id is None:
                raise PermissionError("User ID not provided")
            
            _role_manager = role_manager or get_role_manager()
            
            if not _role_manager.has_permission(user_id, permission):
                raise PermissionError(f"User {user_id} does not have required permission: {permission.value}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def has_permission(user_id: str, permission: Permission, role_manager: Optional[RoleManager] = None) -> bool:
    """
    Check if a user has a specific permission.
    
    Args:
        user_id: User ID
        permission: Permission to check
        role_manager: Optional role manager
        
    Returns:
        True if user has permission
    """
    _role_manager = role_manager or get_role_manager()
    return _role_manager.has_permission(user_id, permission)


# Global role manager instance
_global_role_manager: Optional[RoleManager] = None


def get_role_manager() -> RoleManager:
    """
    Get or create the global role manager.
    
    Returns:
        Role manager instance
    """
    global _global_role_manager
    if _global_role_manager is None:
        _global_role_manager = RoleManager()
    return _global_role_manager