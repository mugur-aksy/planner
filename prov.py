from app import app, db
from app.models import Task

with app.app_context():
    tasks = Task.query.all()
    for task in tasks:
        if not task.status:
            task.status = 'todo'  # Установите статус по умолчанию
    db.session.commit()