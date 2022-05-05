# JngMkk
from django import template
import datetime

register = template.Library()

@register.filter
def datedelta(date):
    now = datetime.date.today()
    day = (now - date).days
    if day >= 0:
        day = "+" + str(day)
    return day

@register.filter
def howmanyday(date):
    meetday = (datetime.date.today() - date).days
    return meetday