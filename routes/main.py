from flask import Blueprint, render_template, request, jsonify
from models.tasks import (
    add_task, get_tasks, update_task_status, delete_task,
    create_list, get_lists, edit_task
)

main = Blueprint('main', __name__)

@main.route('/')
def home():
    lists = get_lists()
    tasks = get_tasks(category='Tasks')
    return render_template('index.html', lists=lists, tasks=tasks, page='Tasks')

@main.route('/myday')
def myday():
    lists = get_lists()
    tasks = get_tasks(category='My Day')
    return render_template('myday.html', lists=lists, tasks=tasks, page='My Day')



@main.route('/planned')
def planned():
    lists = get_lists()
    tasks = get_tasks(category='Planned')
    return render_template('planned.html', lists=lists, tasks=tasks, page='Planned')

@main.route('/tasks', methods=['GET'])
def fetch_tasks():
    filter_by = request.args.get('filter')
    search = request.args.get('search')
    category = request.args.get('category')
    list_name = request.args.get('list_name')
    sort_by = request.args.get('sort_by')
    tasks = get_tasks(filter_by, search, category, list_name, sort_by)
    return jsonify(tasks)
@main.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    data = request.get_json()
    edit_task(
        task_id,
        title=data.get('title'),
        due_date=data.get('due_date'),
        priority=data.get('priority'),
        list_name=data.get('list_name')
    )
    return jsonify({'status': 'success'})

@main.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    title = data.get('title')
    due_date = data.get('due_date')
    priority = data.get('priority')
    list_name = data.get('list_name') or 'Tasks'
    add_task(title, due_date, list_name, priority)
    return jsonify({'status': 'success'})

@main.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    update_task_status(task_id, True)
    return jsonify({'status': 'success'})

@main.route('/incomplete/<int:task_id>', methods=['POST'])
def incomplete(task_id):
    update_task_status(task_id, False)
    return jsonify({'status': 'success'})



@main.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    delete_task(task_id)
    return jsonify({'status': 'success'})

@main.route('/lists', methods=['POST'])
def add_list():
    data = request.get_json()
    list_name = data.get('list_name')
    create_list(list_name)
    return jsonify({'status': 'success'})
