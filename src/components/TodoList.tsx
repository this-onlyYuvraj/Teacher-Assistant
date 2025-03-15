import React, { useState } from 'react';
import { Task } from '../types';
import { format } from 'date-fns';
import { CheckCircle, Circle, Plus, X, Calendar } from 'lucide-react';

const TodoList = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState('');
  const [dueDate, setDueDate] = useState('');

  const addTask = () => {
    if (!newTask.trim()) return;
    
    const task: Task = {
      id: Date.now().toString(),
      title: newTask,
      completed: false,
      dueDate: dueDate || format(new Date(), 'yyyy-MM-dd'),
    };
    
    setTasks([...tasks, task]);
    setNewTask('');
    setDueDate('');
  };

  const toggleTask = (id: string) => {
    setTasks(tasks.map(task =>
      task.id === id ? { ...task, completed: !task.completed } : task
    ));
  };

  const deleteTask = (id: string) => {
    setTasks(tasks.filter(task => task.id !== id));
  };

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold">To-Do List</h2>
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-500">March</span>
          <Calendar size={20} className="text-gray-500" />
        </div>
      </div>
      
      <div className="flex gap-3 mb-6">
        <input
          type="text"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          placeholder="Add new task"
          className="flex-1 px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <input
          type="date"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
          className="px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <button
          onClick={addTask}
          className="bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600"
        >
          <Plus size={20} />
        </button>
      </div>

      <div className="space-y-3">
        {tasks.map((task) => (
          <div
            key={task.id}
            className="flex items-center justify-between p-4 bg-blue-50 rounded-xl"
          >
            <div className="flex items-center gap-3">
              <button 
                onClick={() => toggleTask(task.id)}
                className="focus:outline-none"
              >
                {task.completed ? (
                  <CheckCircle className="text-blue-500" size={20} />
                ) : (
                  <Circle className="text-gray-400" size={20} />
                )}
              </button>
              <div>
                <span className={task.completed ? 'line-through text-gray-500' : 'text-gray-700'}>
                  {task.title}
                </span>
                <p className="text-sm text-gray-500">
                  {format(new Date(task.dueDate), 'MMM d, yyyy')}
                </p>
              </div>
            </div>
            <button
              onClick={() => deleteTask(task.id)}
              className="text-gray-400 hover:text-red-500 focus:outline-none"
            >
              <X size={18} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TodoList;