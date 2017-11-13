
def get_chan(channels, chan):
    return channels.setdefault(chan['name'], {'producers': [], 'consumers': [], 'data': chan})
