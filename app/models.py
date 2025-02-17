from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('assignee.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='todo')
    task_type = db.Column(db.String(50), nullable=False)

    department = db.relationship('Department', backref='tasks')
    assignee = db.relationship('Assignee', backref='tasks')

    def __repr__(self):
        return f'<Task {self.title}>'

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # Название департамента
    assignees = db.relationship('Assignee', backref='department', lazy=True)  # Связь с исполнителями

    def __repr__(self):
        return f'<Department {self.name}>'

class Assignee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Имя исполнителя
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)  # Внешний ключ

    def __repr__(self):
        return f'<Assignee {self.name}>'


class PlannedExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)  # Связь с задачей
    date = db.Column(db.DateTime, nullable=False)  # Дата плановой траты
    amount = db.Column(db.Float, nullable=False)  # Сумма плановой траты
    description = db.Column(db.String(200), nullable=True)  # Описание (необязательное поле)

    task = db.relationship('Task', backref='planned_expenses')  # Связь с задачей

    def __repr__(self):
        return f'<PlannedExpense {self.amount} for {self.date}>'


class ActualExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)  # Связь с задачей
    date = db.Column(db.DateTime, nullable=False)  # Дата фактической затраты
    amount = db.Column(db.Float, nullable=False)  # Сумма фактической затраты
    invoice_number = db.Column(db.String(50), nullable=False)  # Номер счета
    description = db.Column(db.String(200), nullable=True)  # Описание (необязательное поле)

    task = db.relationship('Task', backref='actual_expenses')  # Связь с задачей

    def __repr__(self):
        return f'<ActualExpense {self.amount} for {self.date}>'