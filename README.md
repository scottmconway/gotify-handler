# gotify-handler
This repo contains an extremely simple logging handler that relays log events to gotify.

## Installation
`pip install gotify_handler`

## Usage
```python
import logging
from gotify_handler import GotifyHandler

logger = logging.getLogger()
logging.basicConfig()

gh = GotifyHandler(server_url="https://gotify.example.com",
                   app_token="$APP_TOKEN",
                   alert_on_log_level=logging.WARNING
                   )
logger.addHandler(gh)

logger.info("Example info (doesn't cause a notification)")
logger.warning("Example warning (causes a notification)")
```

`alert_on_log_level` defaults to `logging.WARNING`, but can be set to any value to make log events trigger notifications on gotify. If the log level is below this value, records are sent to gotify with a priority value of 0. Else, records are sent with a priority value of 5.
