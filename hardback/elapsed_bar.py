import datetime
from progress.bar import ChargingBar


class ElapsedBar(ChargingBar):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.start_time = datetime.datetime.now()
        self.index = 0

    def next_item(self, message):
        self.index += 1
        elapsed = datetime.datetime.now() - self.start_time
        time_per_item = elapsed / self.index
        remaining_items = 1 + (self.max - self.index)
        remaining = time_per_item * remaining_items

        def fmt(t):
            return str(t).split('.', 1)[0]

        self.message = '%s %s elapsed, %s to go' % (
            message, fmt(elapsed), fmt(remaining))

        self.next()
