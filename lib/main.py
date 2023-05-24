import os
from pathlib import Path
from types import SimpleNamespace

import strawberry
from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from strawberry.asgi import GraphQL

from lib import config, routers
from lib.models.types.mutation import Mutation
from lib.models.types.query import Query
from lib.services import myjwt
from lib.services.dynamic_entity_loader import dynamic_entities_loader
from lib.init_sellers import import_sellers_from_json

load_dotenv()

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)

app = FastAPI()
static_directory = Path("./static")
app.mount("/static", StaticFiles(directory=static_directory), name="static")


@app.on_event("startup")
async def start():
    await init_beanie(
        connection_string=config.CONNECTION,
        document_models=app.state.document_models,
    )
    await import_sellers_from_json()
    print("initialized beanie odm")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def auth(request: Request, call_next):
    auth_header = request.headers.get("Authorization")
    if auth_header:
        token = auth_header[len("Bearer ") :]
        decoded = myjwt.decode(token)
        if decoded.get("userId"):
            request.state.auth_user = SimpleNamespace(id=decoded.get("userId"))

    return await call_next(request)


root_dir = os.path.join(os.path.dirname(__file__), "models", "entities")
dynamic_entities_loader(app, root_dir)


app.include_router(routers.router)
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
