import logging
from typing import Dict, Optional

import requests


class GotifyHandler(logging.Handler):
    def __init__(
        self,
        server_url: str,
        app_token: str,
        alert_on_log_level: int = logging.WARNING,
        extras: Optional[Dict] = None,
    ) -> None:
        """
        :param server_url: The base URL of the Gotify server to utilize
        :type server_url: str
        :param app_token: A valid Application token for the Gotify instance
        :type app_token: str
        :param alert_on_log_level: The lowest log level for which
            to set the gotify message's priority to 5,
            creating a notification/alert
        :type alert_on_log_level: int
        :param extras: If specified, an "extras" dict to be sent for all logged
            messages, according to gotify's specifications
            https://gotify.net/docs/msgextras#clientnotification
        :type extras: Optional[Dict]
        :rtype: None
        """

        super(GotifyHandler, self).__init__()
        self.server_url = server_url
        self.gotify_session = requests.Session()
        self.gotify_session.headers["X-Gotify-Key"] = app_token
        self.alert_on_log_level = alert_on_log_level
        if extras is None:
            self.extras = dict()
        else:
            self.extras = extras

    def emit(self, record):
        try:
            if record.levelno < self.alert_on_log_level:
                priority = 0  # silent
            else:
                priority = 5  # causes an alert

            res = self.gotify_session.post(
                f"{self.server_url}/message",
                json={
                    "message": record.getMessage(),
                    "title": f"{record.levelname}:{record.name}",
                    "priority": priority,
                    "extras": self.extras,
                },
            )
            res.raise_for_status()

        except BaseException:
            self.handleError(record)
