
def get_chan(channels, chan):
    channels.setdefault(chan['name'], {'producers': [], 'consumers': [], 'data': chan})
