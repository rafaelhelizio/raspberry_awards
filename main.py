import uvicorn

from app.application import create_app
from app.configs import get_environment

_env = get_environment()
app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "app.application:create_app",
        host=_env.APPLICATION_HOST,
        port=_env.APPLICATION_PORT,
        reload=True,
    )
