"""Timed execution of tasks."""

# Builtins

import logging

# Packages

from phylline.util.timing import TimeoutTimer

from phyllo.util.logging import IndentedLogger


class Counter(object):
    """Timed counter class."""

    def __init__(
        self, timer=None, event_type='events', time_unit='second',
        report_interval=None, logger_name='Counter', logger_indentation=0
    ):
        """Initialize members."""
        if timer is None:
            timer = TimeoutTimer()
        self.timer = timer
        self.count = 0
        self.event_type = event_type
        self.report_interval = report_interval
        self.time_unit = time_unit
        self.logger = IndentedLogger(logging.getLogger(logger_name), {
            'class': self.__class__.__qualname__,
            'indentation': logger_indentation
        })

    def start(self):
        """Start the timer."""
        self.timer.start()

    def increment(self):
        """Increment the counter."""
        self.count += 1

    def report(self, force=False):
        """Report counts and rate."""
        if self.report_interval is None:
            return

        if force or self.count % self.report_interval == 0:
            self.logger.info(
                '{} {} ({:.4} {} per {})'
                .format(
                    self.count, self.event_type,
                    self.average_rate, self.event_type, self.time_unit
                )
            )

    @property
    def average_rate(self):
        """Report the average counter increment rate."""
        return self.count / self.timer.elapsed


if __name__ == '__main__':
    # TODO: test the counter
    pass
