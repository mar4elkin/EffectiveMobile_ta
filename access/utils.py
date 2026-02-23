def is_admin_user(user):
    if not user or not user.is_authenticated:
        return False
    return user.user_roles.filter(role__code="admin").exists()
