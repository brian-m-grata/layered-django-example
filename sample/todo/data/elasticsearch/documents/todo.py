from elasticsearch_dsl import Document, Text, Date, Integer

class TodoIndex(Document):
    title = Text()
    description = Text()
    due_date = Date()
    list_id = Integer()

    class Index:
        name = "todo"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }
