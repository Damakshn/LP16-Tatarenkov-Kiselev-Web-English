from web_english import create_app
import config

if __name__ == "__main__":
    app = create_app(config.DevConfig)
    app.run()
