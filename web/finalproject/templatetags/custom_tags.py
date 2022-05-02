from django import template
from pytz import timezone
import datetime

register = template.Library()

@register.filter
def datedelta(date):
    now = datetime.datetime.now(timezone("Asia/Seoul")).date()
    day = str(now - date).split(" ")[0]
    if int(day) > 0:
        day = "+" + day
    return day