from app.application import create_app
from app.configs import get_environment

_env = get_environment()
app = create_app()