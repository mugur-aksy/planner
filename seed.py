from app import app, db
from app.models import Department, Assignee, Task
from datetime import datetime

def seed_database():
    with app.app_context():
        # Удаляем все существующие данные
        db.drop_all()
        db.create_all()

        # Создаем департаменты
        departments = [
            Department(name='ЦЭТ'),
            Department(name='СЭТС'),
            Department(name='СЭТТС'),
            Department(name='МСДП')
        ]
        db.session.add_all(departments)
        db.session.commit()

        # Создаем исполнителей
        assignees = [
            Assignee(name='Ондар Менги М.', department_id=1),
            Assignee(name='Чадамба Чейнеш О.', department_id=1),
            Assignee(name='Монгуш Чингис Д.', department_id=1),
            Assignee(name='Хураган-оол Ачыты-Мерген Э.', department_id=1),
            Assignee(name='Намчын Алимаа В.', department_id=1),

            Assignee(name='Монгуш Буян Д.', department_id=2),
            Assignee(name='Ангыр-оол Адыгжы С.', department_id=2),
            Assignee(name='Биче-оол Эреспей М.', department_id=2),
            Assignee(name='Ховалыг Эдуард Х.', department_id=2),
            Assignee(name='Монгуш Андрей А.', department_id=2),
            Assignee(name='Намзырай Очур М.', department_id=2),
            Assignee(name='Сыргыт-оол Айхан А.', department_id=2),
            Assignee(name='Ондар Чаян А.', department_id=2),
            Assignee(name='Куулар Аяс К.', department_id=2),

            Assignee(name='Кильдияров Анвар М.', department_id=3),
            Assignee(name='Оюн Орлан О.', department_id=3),
            Assignee(name='Оюн Роберт О.', department_id=3),

            Assignee(name='Монгуш Дмитрий В.', department_id=4),
            Assignee(name='Одушпай Эртине С.', department_id=4),
        ]
        db.session.add_all(assignees)
        db.session.commit()

        # # Для теста в Python Console
        # task = Task(
        #     title="Test Task",
        #     start_date=datetime(2024, 1, 15),
        #     end_date=datetime(2024, 2, 20),
        #     department=Department(name="IT"),
        #     task_type="Development"
        # )
        # db.session.add(task)
        # db.session.commit()

if __name__ == '__main__':
    seed_database()