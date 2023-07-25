from datetime import datetime, timedelta


def time_ago(date_reported):
    now = datetime.utcnow()
    time_difference = now - date_reported

    if time_difference < timedelta(seconds=60):
        return f"{int(time_difference.total_seconds())} seconds ago"
    elif time_difference < timedelta(minutes=60):
        return f"{int(time_difference.total_seconds() / 60)} minutes ago"
    elif time_difference < timedelta(hours=24):
        return f"{int(time_difference.total_seconds() / 3600)} hours ago"
    else:
        return f"{int(time_difference.days)} days ago"