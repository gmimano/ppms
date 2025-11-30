from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Client(TenantMixin):
    # As per TDD.md: Represents the Political Party
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=200, blank=True)
    primary_color = models.CharField(max_length=7, default='#1F2937') # Default: Cool Gray 800
    secondary_color = models.CharField(max_length=7, default='#FBBF24') # Default: Amber 400
    logo_url = models.URLField(blank=True, null=True)
    
    # This setting is required by django-tenants.
    # It will automatically create the schema for the tenant when a new Client is created.
    auto_create_schema = True

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    # This model is required by django-tenants to map a domain to a tenant.
    # The 'tenant' ForeignKey, 'domain' CharField, and 'is_primary' BooleanField
    # are all included in the DomainMixin.
    pass