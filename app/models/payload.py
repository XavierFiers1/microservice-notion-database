from pydantic import BaseModel


class DatabaseId(BaseModel):
    database_id: str


class Payload(BaseModel):
    master_database_id: str
    relation_database_id: str
    database_relation_name: str
    page_name: str
    gpt_4_description: str
