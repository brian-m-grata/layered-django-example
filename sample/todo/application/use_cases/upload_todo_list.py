from todo.domain.todo import create_todo_list
from todo.data.models.todo import Todo
from todo.data.elasticsearch.search.todo import index_todo_list
from core.csv import read_csv_file
from core.use_case import UseCase


class UploadTodoListUseCase(UseCase):

    def __init__(self, todo_list_name: str, todo_list_file_name: str) -> None:
        self.todo_list_name = todo_list_name
        self.todo_list_file_name = todo_list_file_name

    def execute(self) -> None:
        todo_list = create_todo_list(self.todo_list_name)
        todo_list_csv_data = read_csv_file(self.todo_list_file_name)
        todo_list_items = []
        for todo_list_csv_row in todo_list_csv_data:
            todo = Todo(
                title=todo_list_csv_row["title"],
                description=todo_list_csv_row["description"],
                due_date=todo_list_csv_row["due_date"],
                list_id=todo_list.id
            )
            todo_list_items.append(todo)

        todo_list.todos = todo_list_items
        todo_list.save()
        index_todo_list(todo_list)

