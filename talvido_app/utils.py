from django.core.validators import RegexValidator
from datetime import datetime


"""phone number validation"""

phone_regex = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
)

"""get the duration"""

def get_duration(data):
    difference = datetime.now() - data.created_at.replace(tzinfo=None)
    m, s = divmod(difference.total_seconds(), 60)
    hours = int(m // 60)
    month = (hours//24)//30
    minutes = int(60 - m%60)

    if hours <=0:
        return f"{60 - minutes}m ago"
    elif hours > 0 and hours <= 24:
        return f"{hours}h ago"
    elif hours > 24 and hours//24 <= 30:
        return f"{hours//24}d ago"
    elif month > 12:
        return f"{month//12}y ago"
    else:
        return f"{month}month ago"
