def time_track(ms):
    seconds, ms = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours < 1:
        return f'{int(minutes):01d}:{int(seconds):02d}'
    else:
        return f'{int(hours):1d}:{int(minutes):01d}:{int(seconds):02d}'
    

def time_play(ms):
    seconds, ms = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours < 1:
        return f'{int(minutes):01d}m {int(seconds):02d}s'
    else:
        return f'{int(hours):1d}h {int(minutes):01d}m'