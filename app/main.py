import os

from dotenv import load_dotenv
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from models.payload import DatabaseId, Payload
from notion_client import APIResponseError, Client
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

load_dotenv()
app = FastAPI()
notion = Client(auth=os.environ["NOTION_API_KEY"])
limiter = Limiter(key_func=get_remote_address, default_limits=["1/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SlowAPIMiddleware)


@app.get("/")
def index() -> Response:
    return Response("Microservice -- Notion Database")


@app.get("/database/{database_id}")
def database(database_id: str):
    # print(payload.database_id)
    results = notion.databases.query(**{
        "database_id": database_id,
    }).get("results")
    print(results[0])
    return results[0]


# insert a page into a Notion master database
@app.post("/insert_page")
def insert_page(payload: Payload) -> Response:
    relation_database_id = get_database_relation_page_id(
        payload.relation_database_id, payload.database_relation_name)

    new_page = {
        "Name": {
            "title": [{
                "text": {
                    "content": payload.page_name
                }
            }]
        },
        "Book relation": {
            "type": "relation",
            "relation": [{
                "id": relation_database_id
            }]
        },
        "gpt-4 description": {
            "rich_text": [{
                "text": {
                    "content": payload.gpt_4_description
                }
            }]
        },
    }
    try:
        notion.pages.create(parent={"database_id": payload.master_database_id},
                            properties=new_page)
    except APIResponseError as e:
        return {"error", e}
    return Response(
        f"page with page name {payload.page_name} inserted succesfuly")


# master database usually has a relation database
def get_database_relation_page_id(database_id: str,
                                  database_relation_name: str):
    print(database_id, database_relation_name)
    results = notion.databases.query(
        **{
            "database_id": database_id,
            "filter": {
                "property": "Name",
                "title": {
                    "equals": database_relation_name
                }
            }
        }).get("results")
    return results[0]['id']
