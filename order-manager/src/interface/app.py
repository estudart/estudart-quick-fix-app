import os

from dotenv import load_dotenv

from src.interface.api import create_app



load_dotenv()

ENV = os.environ.get("ENV", "DEV")


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True if ENV == "DEV" else False)