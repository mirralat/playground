from fastapi import Request, Response, status, FastAPI


def get_app() -> FastAPI:
    app = FastAPI()
    return app
