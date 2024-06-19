
def verbose_timedelta(seconds):
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    if seconds < 1:
        seconds = 1
    locals_ = locals()
    magnitudes_str = ("{n} {magnitude}".format(n=int(locals_[magnitude]), magnitude=magnitude)
                      for magnitude in ("days", "hours", "minutes", "seconds") if locals_[magnitude])
    return ", ".join(magnitudes_str)


def get_earningscall_secret_api_key():
    try:
        with open(".earnings-call-api-key", "r") as fd:
            return fd.read().strip()
    except FileNotFoundError:
        return None

