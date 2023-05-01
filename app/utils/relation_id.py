from notion_client import Client


def get_database_relation_page_id(notion_client: Client, database_id: str,
                                  database_relation_name: str):
    results = notion_client.databases.query(
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
