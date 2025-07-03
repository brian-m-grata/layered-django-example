from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from celery import subtask


@api_view(["POST"])
@renderer_classes([JSONRenderer])
def process_todo_upload_task(request):
    """
    API endpoint to process todo upload asynchronously
    """
    file_path = request.data.get('file_path')
    if not file_path:
        return Response(
            {"error": "file_path is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    task = subtask("todo.interfaces.tasks.process_todo_upload")
    task.apply_async(args=[file_path])
    
    return Response({
        "message": "Todo upload processing started",
        "file_path": file_path
    }, status=status.HTTP_202_ACCEPTED)


@api_view(["POST"])
@renderer_classes([JSONRenderer])
def cleanup_old_todos_task(request):
    """
    API endpoint to cleanup old completed todos
    """
    task = subtask("todo.interfaces.tasks.cleanup_old_todos")
    task.apply_async()
    
    return Response({
        "message": "Cleanup of old todos started"
    }, status=status.HTTP_202_ACCEPTED)


@api_view(["POST"])
@renderer_classes([JSONRenderer])
def send_todo_reminders_task(request):
    """
    API endpoint to send todo reminders
    """
    task = subtask("todo.interfaces.tasks.send_todo_reminders")
    task.apply_async()
    
    return Response({
        "message": "Todo reminders processing started"
    }, status=status.HTTP_202_ACCEPTED)


@api_view(["GET"])
@renderer_classes([JSONRenderer])
def get_available_tasks(request):
    """
    API endpoint to list available tasks
    """
    available_tasks = [
        {
            "name": "process_todo_upload",
            "endpoint": "/tasks/upload",
            "method": "POST",
            "description": "Process uploaded todo files asynchronously",
            "required_params": ["file_path"]
        },
        {
            "name": "cleanup_old_todos",
            "endpoint": "/tasks/cleanup",
            "method": "POST",
            "description": "Clean up old completed todos",
            "required_params": []
        },
        {
            "name": "send_todo_reminders",
            "endpoint": "/tasks/reminders",
            "method": "POST",
            "description": "Send reminders for overdue todos",
            "required_params": []
        }
    ]
    
    return Response({
        "available_tasks": available_tasks
    }, status=status.HTTP_200_OK) 