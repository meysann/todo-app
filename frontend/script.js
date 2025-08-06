// The base URL for our backend API.
// IMPORTANT: We use the name of the backend container as the hostname.
const BACKEND_URL = 'http://todo-backend:5000';

function displayTodo(item) {
    const todoList = document.getElementById('todo-list');
    const li = document.createElement('li');
    li.textContent = item;
    todoList.appendChild(li);
}

// Function to fetch all to-do items from the backend
async function fetchTodos() {
    try {
        const response = await fetch(`${BACKEND_URL}/todos`);
        const data = await response.json();
        // Here we'd typically loop through data.todos and call displayTodo()
        console.log('Fetched Todos:', data.message);
    } catch (error) {
        console.error('Failed to fetch todos:', error);
    }
}

// Function to add a new to-do item
async function addTodo() {
    const input = document.getElementById('todo-input');
    const item = input.value;
    if (!item) return;

    try {
        const response = await fetch(`${BACKEND_URL}/todos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ item: item }),
        });
        const data = await response.json();
        console.log('Todo added:', data.message);
        displayTodo(item); // Optimistically add to the list
        input.value = '';
    } catch (error) {
        console.error('Failed to add todo:', error);
    }
}

// Call fetchTodos on page load
// This will fail for now, but will work once our backend is ready.
document.addEventListener('DOMContentLoaded', fetchTodos);