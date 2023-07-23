# -*- coding=utf-8 -*-
import signal
import sys

from docopt import docopt

from tonexus.app import create_app
from tonexus.config import Config
from tonexus.loggers import logger


def handle_signal(sig, frame):
    logger.info("receive signal: {}".format(sig))
    sys.exit(0)


def main():
    USAGES = """
    Usage:
        manager run [--host=<HOST>] [--port=<PORT>] [--debug]

    Commands:
        run                            Run server with host and port

    Options:
        -p, --port PORT                Port [default: 8080]
        -h, --host HOST                Host [default: 0.0.0.0]
        -d, --debug                    Debug
    """

    signal.signal(signal.SIGINT | signal.SIGTERM | signal.SIGKILL, handle_signal)

    options = docopt(USAGES, argv=sys.argv[1:], version="tonexus v0.1.0")

    if options.get("run"):
        app = create_app()
        host = options.get("--host") or Config.APP_HOST
        port = options.get("--port") or Config.APP_PORT
        debug = options.get("--debug") or Config.DEBUG
        app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()
