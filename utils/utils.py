from django.contrib.auth.models import Group

def user_is_manager(user):
    return user.groups.filter(name='Manager').exists()