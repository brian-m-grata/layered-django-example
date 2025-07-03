from rest_framework import serializers
from todo.data.models.todo import Todo, TodoList


class TodoListSerializer(serializers.ModelSerializer):
    """
    Serializer for TodoList model
    """
    class Meta:
        model = TodoList
        fields = ['id', 'name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TodoListDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for TodoList with todos count
    """
    todos_count = serializers.SerializerMethodField()
    
    class Meta:
        model = TodoList
        fields = ['id', 'name', 'todos_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_todos_count(self, obj):
        return obj.todos.count()


class TodoSerializer(serializers.ModelSerializer):
    """
    Serializer for Todo model
    """
    list_name = serializers.CharField(source='list.name', read_only=True)
    
    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'due_date', 'list', 'list_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


 