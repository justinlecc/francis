import datetime, pytz

def naivelocal_to_naiveutc(naivelocal_dt, local_tz):
    local = pytz.timezone(local_tz)
    # TODO: is_dst=None means ambiguous datetimes (caused by daylight savings time) will
    #   will throw an error. Need way of handling this.
    local_dt = local.localize(naivelocal_dt, is_dst=None) 
    utc_dt = local_dt.astimezone (pytz.utc)
    utc_naive = utc_dt.replace(tzinfo=None)
    return utc_naive
