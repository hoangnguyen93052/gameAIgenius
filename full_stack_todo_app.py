from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<TodoItem {self.task}>'

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = TodoItem.query.all()
    return jsonify([{'id': todo.id, 'task': todo.task, 'done': todo.done} for todo in todos])

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.json
    new_todo = TodoItem(task=data['task'], done=data['done'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'id': new_todo.id, 'task': new_todo.task, 'done': new_todo.done}), 201

@app.route('/api/todos/<int:todo_id>', methods=['POST'])
def update_todo(todo_id):
    data = request.json
    todo = TodoItem.query.get(todo_id)
    if todo:
        todo.task = data['task']
        todo.done = data['done']
        db.session.commit()
        return jsonify({'id': todo.id, 'task': todo.task, 'done': todo.done})
    return jsonify({'message': 'Todo not found'}), 404

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = TodoItem.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'message': 'Todo deleted'}), 200
    return jsonify({'message': 'Todo not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

# React frontend
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
    const [todos, setTodos] = useState([]);
    const [newTodo, setNewTodo] = useState('');

    useEffect(() => {
        fetchTodos();
    }, []);

    const fetchTodos = async () => {
        const response = await fetch('http://localhost:5000/api/todos');
        const data = await response.json();
        setTodos(data);
    };

    const addTodo = async () => {
        if (newTodo) {
            const response = await fetch('http://localhost:5000/api/todos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ task: newTodo, done: false }),
            });
            if (response.ok) {
                fetchTodos();
                setNewTodo('');
            }
        }
    };

    const toggleTodo = async (id, done) => {
        const response = await fetch(`http://localhost:5000/api/todos/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ task: todos.find(todo => todo.id === id).task, done: !done }),
        });
        if (response.ok) {
            fetchTodos();
        }
    };

    const deleteTodo = async (id) => {
        const response = await fetch(`http://localhost:5000/api/todos/${id}`, {
            method: 'DELETE',
        });
        if (response.ok) {
            fetchTodos();
        }
    };

    return (
        <div className="App">
            <h1>To-Do List</h1>
            <input
                type="text"
                value={newTodo}
                onChange={(e) => setNewTodo(e.target.value)}
                placeholder="Add a new task"
            />
            <button onClick={addTodo}>Add</button>
            <ul>
                {todos.map(todo => (
                    <li key={todo.id}>
                        <input
                            type="checkbox"
                            checked={todo.done}
                            onChange={() => toggleTodo(todo.id, todo.done)}
                        />
                        {todo.task}
                        <button onClick={() => deleteTodo(todo.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;

const rootElement = document.getElementById('root');
ReactDOM.render(<App />, rootElement);