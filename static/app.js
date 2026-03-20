// app.js - Handles AJAX, UI, and interactions

let currentFilter = 'all';
let currentCategory = 'My Day';
let gridView = false;

function fetchTasks() {
    const search = document.getElementById('searchBar').value;
    fetch(`/tasks?filter=${currentFilter}&search=${search}`)
        .then(res => res.json())
        .then(tasks => renderTasks(tasks));
}

function renderTasks(tasks) {
    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '';
    if (!tasks.length) {
        taskList.innerHTML = '<div class="col-12 text-center text-muted">No tasks found.</div>';
        return;
    }
    tasks.forEach(task => {
        const colClass = gridView ? 'col-md-4' : 'col-12';
        taskList.innerHTML += `
            <div class="${colClass}">
                <div class="card shadow-sm">
                    <div class="card-body d-flex align-items-center">
                        <input type="checkbox" class="form-check-input me-2" ${task[2] ? 'checked' : ''} onclick="toggleComplete(${task[0]}, this.checked)">
                        <div class="flex-grow-1">
                            <div class="fw-bold ${task[2] ? 'text-decoration-line-through text-muted' : ''}">${task[1]}</div>
                            <div class="small text-secondary">Due: ${task[4] || 'N/A'} | Priority: ${task[5] || 'None'} | ${task[6] || ''}</div>
                        </div>
                        <button class="btn btn-danger btn-sm ms-2" onclick="deleteTask(${task[0]})">Delete</button>
                    </div>
                </div>
            </div>
        `;
    });
}

function addTask() {
    const title = document.getElementById('taskTitle').value;
    const due_date = document.getElementById('taskDueDate').value;
    const priority = document.getElementById('taskPriority').value;
    fetch('/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, due_date, priority, category: currentCategory })
    }).then(() => {
        document.getElementById('taskTitle').value = '';
        document.getElementById('taskDueDate').value = '';
        document.getElementById('taskPriority').value = '';
        fetchTasks();
    });
}

function deleteTask(id) {
    fetch(`/delete/${id}`, { method: 'POST' }).then(fetchTasks);
}

function toggleComplete(id, completed) {
    fetch(`/${completed ? 'complete' : 'incomplete'}/${id}`, { method: 'POST' }).then(fetchTasks);
}

// Event Listeners

document.getElementById('addTaskBtn').onclick = addTask;
document.getElementById('searchBar').oninput = fetchTasks;

Array.from(document.getElementsByClassName('filter-btn')).forEach(btn => {
    btn.onclick = () => {
        currentFilter = btn.dataset.filter;
        fetchTasks();
    };
});

Array.from(document.querySelectorAll('.sidebar .nav-link')).forEach(link => {
    link.onclick = () => {
        currentCategory = link.dataset.category;
        fetchTasks();
        Array.from(document.querySelectorAll('.sidebar .nav-link')).forEach(l => l.classList.remove('active'));
        link.classList.add('active');
    };
});

document.getElementById('gridToggle').onclick = () => { gridView = true; fetchTasks(); };
document.getElementById('listToggle').onclick = () => { gridView = false; fetchTasks(); };

document.addEventListener('DOMContentLoaded', fetchTasks);

// Dark mode toggle
const darkModeToggle = document.getElementById('darkModeToggle');
darkModeToggle.onclick = () => {
    document.body.classList.toggle('dark-mode');
    darkModeToggle.classList.toggle('btn-dark');
};
