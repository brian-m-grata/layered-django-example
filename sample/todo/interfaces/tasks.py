import logging
from celery import shared_task
from todo.application.use_cases.upload_todo_list import UploadTodoListUseCase

logger = logging.getLogger(__name__)


@shared_task
def process_todo_upload(file_path: str, *args, **kwargs) -> None:
    """
    Process a todo list upload asynchronously.
    
    Args:
        file_path: Path to the uploaded file
    """
    try:
        logger.info(f"Starting todo upload processing for file: {file_path}")
        UploadTodoListUseCase().execute(file_path=file_path)
        logger.info(f"Successfully processed todo upload for file: {file_path}")
    except Exception as e:
        logger.error(f"Error processing todo upload for file {file_path}: {str(e)}")
        raise


@shared_task
def cleanup_old_todos(*args, **kwargs) -> None:
    """
    Clean up old completed todos asynchronously.
    """
    try:
        logger.info("Starting cleanup of old completed todos")
        # TODO: Implement cleanup use case
        # CleanupOldTodosUseCase().execute()
        logger.info("Successfully cleaned up old completed todos")
    except Exception as e:
        logger.error(f"Error cleaning up old todos: {str(e)}")
        raise


@shared_task
def send_todo_reminders(*args, **kwargs) -> None:
    """
    Send reminders for overdue todos asynchronously.
    """
    try:
        logger.info("Starting todo reminder processing")
        # TODO: Implement reminder use case
        # SendTodoRemindersUseCase().execute()
        logger.info("Successfully sent todo reminders")
    except Exception as e:
        logger.error(f"Error sending todo reminders: {str(e)}")
        raise