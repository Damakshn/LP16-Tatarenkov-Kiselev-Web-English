from web_english import create_app
import config

app = create_app(config.DevConfig)
