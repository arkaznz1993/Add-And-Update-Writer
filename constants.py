import os

ADD_WRITER_LIST = '6222ea389eea1d363085cc2a'
UPDATE_WRITER_LIST = '622abc8e5e8812674393efc7'

UPDATE_LIST_IDS = [ADD_WRITER_LIST, UPDATE_WRITER_LIST]

PARAMS = {
    "key": os.environ.get("TRELLO_API_KEY"),
    "token": os.environ.get("TRELLO_TOKEN"),
}

HEADERS = {
    "Accept": "application/json"
}
