from accounts.models import *
from accounts.constants import *
from django import template

register = template.Library()


@register.filter(name='total_customers')
def total_customers(key):
	return User.objects.filter(role_id=CUSTOMER).count()


@register.filter(name='total_service_providers')
def total_service_providers(key):
	return User.objects.filter(role_id=SERVICE_PROVIDER).count()


@register.filter(name='total_cities')
def total_cities(key):
	return Cities.objects.all().count() 