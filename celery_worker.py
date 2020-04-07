import config
from web_english import celery, create_app


app = create_app(config.Config)
app.app_context().push()
