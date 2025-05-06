from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from app import app, db
from app.models import Task, Department, Assignee, PlannedExpense, ActualExpense
from collections import defaultdict

# Главная страница (список задач)
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/task/<int:id>')
def task(id):
    task = Task.query.get_or_404(id)
    return render_template('task.html', task=task)

# Страница создания задачи
@app.route('/task/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        task = Task(
            department_id=request.form['department_id'],
            assignee_id=request.form['assignee_id'],
            title=request.form['title'],
            start_date=datetime.fromisoformat(request.form['start_date']),
            end_date=datetime.fromisoformat(request.form['end_date']),
            priority=request.form['priority'],
            status=request.form['status'],
            task_type=request.form['task_type']
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('index'))

    departments = Department.query.all()
    return render_template('create_task.html', departments=departments)


# Страница редактирования задачи
@app.route('/task/<int:id>/edit', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.department_id = request.form['department_id']
        task.assignee_id = request.form['assignee_id']
        task.title = request.form['title']
        task.start_date = datetime.fromisoformat(request.form['start_date'])
        task.end_date = datetime.fromisoformat(request.form['end_date'])
        task.priority = request.form['priority']
        task.status = request.form['status']
        task.task_type = request.form['task_type']
        db.session.commit()
        return redirect(url_for('index'))

    departments = Department.query.all()
    return render_template('edit_task.html', task=task, departments=departments)


# Удаление задачи
@app.route('/task/<int:id>/delete', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


# Обновление статуса задачи (для доски задач)
@app.route('/task/<int:id>/update-status', methods=['POST'])
def update_task_status(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    task.status = data['status']
    db.session.commit()
    return jsonify({'success': True})


@app.route('/task/<int:task_id>/add-planned-expense', methods=['GET', 'POST'])
def add_planned_expense(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        planned_expense = PlannedExpense(
            task_id=task.id,
            date=datetime.fromisoformat(request.form['date']),
            amount=float(request.form['amount']),
            description=request.form['description']
        )
        db.session.add(planned_expense)
        db.session.commit()
        return redirect(url_for('task', id=task.id))
    return render_template('add_planned_expense.html', task=task)

# Редактирование плановой затраты
@app.route('/task/<int:task_id>/edit-planned-expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_planned_expense(task_id, expense_id):
    task = Task.query.get_or_404(task_id)
    planned_expense = PlannedExpense.query.get_or_404(expense_id)

    if request.method == 'POST':
        planned_expense.date = datetime.fromisoformat(request.form['date'])
        planned_expense.amount = float(request.form['amount'])
        planned_expense.description = request.form['description']
        db.session.commit()
        return redirect(url_for('task', id=task.id))

    return render_template('edit_planned_expense.html', task=task, planned_expense=planned_expense)

# Удаление плановой затраты
@app.route('/task/<int:task_id>/delete-planned-expense/<int:expense_id>', methods=['POST'])
def delete_planned_expense(task_id, expense_id):
    planned_expense = PlannedExpense.query.get_or_404(expense_id)
    db.session.delete(planned_expense)
    db.session.commit()
    return redirect(url_for('task', id=task_id))

@app.route('/task/<int:task_id>/add-actual-expense', methods=['GET', 'POST'])
def add_actual_expense(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        actual_expense = ActualExpense(
            task_id=task.id,
            date=datetime.fromisoformat(request.form['date']),
            amount=float(request.form['amount']),
            invoice_number=request.form['invoice_number'],
            description=request.form['description']
        )
        db.session.add(actual_expense)
        db.session.commit()
        return redirect(url_for('task', id=task.id))
    return render_template('add_actual_expense.html', task=task)

# Редактирование фактической затраты
@app.route('/task/<int:task_id>/edit-actual-expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_actual_expense(task_id, expense_id):
    task = Task.query.get_or_404(task_id)
    actual_expense = ActualExpense.query.get_or_404(expense_id)

    if request.method == 'POST':
        actual_expense.date = datetime.fromisoformat(request.form['date'])
        actual_expense.amount = float(request.form['amount'])
        actual_expense.invoice_number = request.form['invoice_number']
        actual_expense.description = request.form['description']
        db.session.commit()
        return redirect(url_for('task', id=task.id))

    return render_template('edit_actual_expense.html', task=task, actual_expense=actual_expense)

# Удаление фактической затраты
@app.route('/task/<int:task_id>/delete-actual-expense/<int:expense_id>', methods=['POST'])
def delete_actual_expense(task_id, expense_id):
    actual_expense = ActualExpense.query.get_or_404(expense_id)
    db.session.delete(actual_expense)
    db.session.commit()
    return redirect(url_for('task', id=task_id))

@app.route('/calendar')
def calendar():
    tasks = Task.query.order_by(Task.department_id, Task.task_type, Task.start_date).all()

    # Получаем список отделов и типов работ для фильтров
    departments = Department.query.all()
    task_types = sorted(set(task.task_type for task in tasks))

    # Фильтры из запроса
    selected_department = request.args.get('department')
    selected_task_type = request.args.get('task_type')

    # Фильтрация задач
    filtered_tasks = tasks
    if selected_department:
        filtered_tasks = [task for task in filtered_tasks if task.department.name == selected_department]
    if selected_task_type:
        filtered_tasks = [task for task in filtered_tasks if task.task_type == selected_task_type]

    # Получаем список месяцев
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Группировка задач по отделам, типам и месяцам
    grouped_tasks = {}
    for task in filtered_tasks:
        department_name = task.department.name
        task_type = task.task_type

        if department_name not in grouped_tasks:
            grouped_tasks[department_name] = {}
        if task_type not in grouped_tasks[department_name]:
            grouped_tasks[department_name][task_type] = {month: [] for month in months}

        # Добавляем задачу в соответствующие месяцы
        start_month = task.start_date.strftime('%B')
        end_month = task.end_date.strftime('%B')
        for month in months:
            if month in [start_month, end_month]:
                grouped_tasks[department_name][task_type][month].append(task)

    # Результирующие данные для каждого отдела
    department_results = {}
    for department, task_types in grouped_tasks.items():
        department_results[department] = {
            'task_count': {month: 0 for month in months},
            'planned_cost': {month: 0.0 for month in months},
            'actual_cost': {month: 0.0 for month in months}
        }
        for task_type, month_tasks in task_types.items():
            for month, tasks in month_tasks.items():
                department_results[department]['task_count'][month] += len(tasks)
                for task in tasks:
                    # Суммируем плановые траты
                    for planned_expense in task.planned_expenses:
                        if planned_expense.date.strftime('%B') == month:
                            department_results[department]['planned_cost'][month] += planned_expense.amount

                    # Суммируем фактические затраты
                    for actual_expense in task.actual_expenses:
                        if actual_expense.date.strftime('%B') == month:
                            department_results[department]['actual_cost'][month] += actual_expense.amount

    # Общая результирующая строка
    total_results = {
        'task_count': {month: 0 for month in months},
        'planned_cost': {month: 0.0 for month in months},
        'actual_cost': {month: 0.0 for month in months}
    }
    for department, results in department_results.items():
        for month in months:
            total_results['task_count'][month] += results['task_count'][month]
            total_results['planned_cost'][month] += results['planned_cost'][month]
            total_results['actual_cost'][month] += results['actual_cost'][month]

    return render_template(
        'calendar.html',
        grouped_tasks=grouped_tasks,
        months=months,
        departments=departments,
        task_types=task_types,
        selected_department=selected_department,
        selected_task_type=selected_task_type,
        department_results=department_results,
        total_results=total_results
    )

# Получение событий для календаря
@app.route('/calendar-events')
def calendar_events():
    tasks = Task.query.all()
    events = []
    for task in tasks:
        events.append({
            'title': task.title,
            'start': task.start_date.isoformat(),
            'end': task.end_date.isoformat(),
            'color': 'red' if task.priority == 'high' else 'orange' if task.priority == 'medium' else 'green'
        })
    return jsonify(events)


# Доска задач (Kanban Board)
@app.route('/kanban')
def kanban():
    tasks = Task.query.all()
    departments = Department.query.all()
    return render_template('kanban.html', tasks=tasks, departments=departments)


# Получение исполнителей для выбранного департамента (AJAX)
@app.route('/api/departments/<int:department_id>/assignees')
def get_assignees(department_id):
    assignees = Assignee.query.filter_by(department_id=department_id).all()
    return jsonify([{'id': a.id, 'name': a.name} for a in assignees])


# Обновление дат задачи (для календаря)
@app.route('/task/<int:id>/update-dates', methods=['POST'])
def update_task_dates(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    task.start_date = datetime.fromisoformat(data['start_date'])
    task.end_date = datetime.fromisoformat(data['end_date'])
    db.session.commit()
    return jsonify({'success': True})


@app.route('/charts')
def charts():
    selected_year = request.args.get('year', default=datetime.now().year, type=int)
    selected_department = request.args.get('department', type=int)

    departments_query = Department.query
    if selected_department:
        departments_query = departments_query.filter_by(id=selected_department)
    departments = departments_query.all()

    result = {}
    task_types = set()

    for department in departments:
        # Создаем структуру для хранения данных
        if department.name not in result:
            result[department.name] = {
                'id': department.id,
                'task_types': {}
            }

        # Получаем все задачи для отдела
        tasks = Task.query.filter_by(department_id=department.id).all()

        for task in tasks:
            # Инициализируем структуру для типа задачи, если ее еще нет
            if task.task_type not in result[department.name]['task_types']:
                result[department.name]['task_types'][task.task_type] = {
                    'planned': {m: 0 for m in range(1, 13)},
                    'actual': {m: 0 for m in range(1, 13)}
                }
                task_types.add(task.task_type)

            # Агрегируем плановые расходы по месяцам
            for expense in task.planned_expenses:
                if expense.date.year == selected_year:
                    month = expense.date.month
                    result[department.name]['task_types'][task.task_type]['planned'][month] += float(expense.amount)

            # Агрегируем фактические расходы по месяцам
            for expense in task.actual_expenses:
                if expense.date.year == selected_year:
                    month = expense.date.month
                    result[department.name]['task_types'][task.task_type]['actual'][month] += float(expense.amount)

    return render_template(
        'charts.html',
        data=result,
        task_types=sorted(task_types),
        departments=Department.query.all(),
        selected_year=selected_year,
        selected_department=selected_department
    )


@app.route('/department/<int:department_id>/charts')
def department_chart(department_id):
    selected_year = request.args.get('year', default=datetime.now().year, type=int)
    department = Department.query.get_or_404(department_id)

    tasks_data = []

    # Получаем все задачи отдела
    tasks = Task.query.filter_by(department_id=department_id).all()

    for task in tasks:
        task_entry = {
            'task': task,
            'planned': defaultdict(float),
            'actual': defaultdict(float)
        }

        # Агрегируем плановые расходы
        for expense in task.planned_expenses:
            if expense.date.year == selected_year:
                month = expense.date.month
                task_entry['planned'][month] += float(expense.amount)

        # Агрегируем фактические расходы
        for expense in task.actual_expenses:
            if expense.date.year == selected_year:
                month = expense.date.month
                task_entry['actual'][month] += float(expense.amount)

        # Добавляем только если есть данные
        if any(task_entry['planned'].values()) or any(task_entry['actual'].values()):
            tasks_data.append(task_entry)

    return render_template(
        'department_chart.html',
        department=department,
        tasks_data=tasks_data,
        selected_year=selected_year
    )