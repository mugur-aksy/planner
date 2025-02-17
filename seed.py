from app import app, db
from app.models import Department, Assignee

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
            Department(name='МСДП'),
        ]
        db.session.add_all(departments)
        db.session.commit()

        # Создаем исполнителей
        assignees = [
            Assignee(name='Ондар Менги М.', department_id=1),
            Assignee(name='Монгуш Буян Д.', department_id=2),
            Assignee(name='Кильдияров Анвар М.', department_id=3),
            Assignee(name='Монгуш Дмитрий В.', department_id=4),
        ]
        db.session.add_all(assignees)
        db.session.commit()

if __name__ == '__main__':
    seed_database()