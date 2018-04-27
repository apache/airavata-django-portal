from django import template

register = template.Library()

@register.filter
def index(List, i):
    return List[int(i)]

@register.filter
def getApplicationsToBeUsed(Queryset):
    return Queryset.applicationsToBeUsed

@register.filter
def getReviewedServiceUnits(Queryset):
    return Queryset.reviewedServiceUnits

@register.filter
def getSpecificResource(Queryset):
    return Queryset.specificResource

@register.filter
def getResourceType(Queryset):
    return Queryset.resourceType

@register.filter
def getComments(Queryset):
    return Queryset.comments

@register.filter
def split(value):
    return value.split('_')[0]