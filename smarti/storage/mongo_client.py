"""mongo db access"""

import pymongo


def create_client(conn_string):  # pragma: no cover
    """create new Mongo Client"""
    return pymongo.MongoClient(conn_string)


def read_workbooks(client: pymongo.MongoClient, workbook_id: str) -> list:
    """read workbook from database"""
    return [client.smarti.name, workbook_id]
