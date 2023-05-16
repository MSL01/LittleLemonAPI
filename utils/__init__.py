from django import template
from .utils import user_is_manager

register = template.Library()
register.filter('user_is_manager', user_is_manager)
