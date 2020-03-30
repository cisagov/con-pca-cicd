"""
This is an example script.

It seems that it has to have THIS docstring with a summary line, a blank line
and sume more text like here. Wow.
"""
# Standard Python Libraries
from datetime import datetime
import logging
from os import getenv
import threading


class Service(threading.Thread):
    """This is the service class."""

    _start_date = datetime.utcnow()

    def __init__(self, name):
        """This is the init def, on creatin adds self name."""
        threading.Thread.__init__(self)
        self.name = name

    def start(self):
        """Start service."""
        logging.info("Starting service: {}".format(self.name))

    def stop(self):
        """Stop Service."""
        logging.info("Stopping service {}".format(self.name))


def main():
    """This is the Main method for starting the service."""
    logging.basicConfig(level=logging.getLevelName(getenv("LOG_LEVEL", "INFO")))
    service = Service("data-service")
    try:
        service.start()
    except KeyboardInterrupt:
        service.stop()


if __name__ == "__main__":
    main()
