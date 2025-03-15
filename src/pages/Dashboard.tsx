import React from 'react';
import TodoList from '../components/TodoList';
import { Calendar, CheckCircle2, Clock, Bell } from 'lucide-react';

const timetable = [
  { day: 'Monday', time: '9:00 AM', subject: 'Mathematics', class: '10-A' },
  { day: 'Monday', time: '11:00 AM', subject: 'Physics', class: '11-B' },
  { day: 'Tuesday', time: '10:00 AM', subject: 'Chemistry', class: '12-A' },
];

const recentAssignments = [
  { title: 'Math Homework Ch. 5', dueDate: '2024-03-20', subject: 'Mathematics' },
  { title: 'Physics Lab Report', dueDate: '2024-03-22', subject: 'Physics' },
];

const recentTests = [
  { title: 'Mid-term Test', date: '2024-03-25', subject: 'Chemistry' },
  { title: 'Chapter Test', date: '2024-03-28', subject: 'Mathematics' },
];

const Dashboard = () => {
  return (
    <div className="p-6 ml-64">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold mb-1">Hi, Layla Walker</h1>
          <p className="text-gray-500">Welcome back to your dashboard</p>
        </div>
        <div className="flex items-center gap-4">
          <button className="p-2 rounded-lg bg-white text-gray-600 hover:bg-gray-50">
            <Bell size={20} />
          </button>
          <button className="flex items-center gap-2 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">
            <span>Login</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2">
          <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold">Class Performance Overview</h2>
              <button className="text-blue-500 hover:text-blue-600 font-medium">View All</button>
            </div>
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-blue-50 p-4 rounded-xl">
                <h3 className="text-gray-600 font-medium mb-2">Average Score</h3>
                <p className="text-2xl font-bold text-blue-600">85%</p>
              </div>
              <div className="bg-blue-50 p-4 rounded-xl">
                <h3 className="text-gray-600 font-medium mb-2">Assignments Completed</h3>
                <p className="text-2xl font-bold text-blue-600">92%</p>
              </div>
              <div className="bg-blue-50 p-4 rounded-xl">
                <h3 className="text-gray-600 font-medium mb-2">Test Participation</h3>
                <p className="text-2xl font-bold text-blue-600">95%</p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-6">
            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold">Recent Assignments</h2>
                <button className="text-blue-500 hover:text-blue-600 font-medium">Create New</button>
              </div>
              <div className="space-y-4">
                {recentAssignments.map((assignment, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-blue-50 rounded-xl">
                    <div>
                      <h3 className="font-medium">{assignment.title}</h3>
                      <p className="text-sm text-gray-500">{assignment.subject}</p>
                    </div>
                    <div className="flex items-center text-sm text-gray-500">
                      <Calendar size={16} className="mr-1" />
                      {assignment.dueDate}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold">Recent Tests</h2>
                <button className="text-blue-500 hover:text-blue-600 font-medium">Create New</button>
              </div>
              <div className="space-y-4">
                {recentTests.map((test, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-blue-50 rounded-xl">
                    <div>
                      <h3 className="font-medium">{test.title}</h3>
                      <p className="text-sm text-gray-500">{test.subject}</p>
                    </div>
                    <div className="flex items-center text-sm text-gray-500">
                      <Calendar size={16} className="mr-1" />
                      {test.date}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-xl font-semibold mb-6">Today's Timetable</h2>
            <div className="space-y-4">
              {timetable.map((entry, index) => (
                <div key={index} className="flex items-center space-x-4 p-4 bg-blue-50 rounded-xl">
                  <Clock size={20} className="text-blue-500" />
                  <div>
                    <p className="font-medium">{entry.subject}</p>
                    <p className="text-sm text-gray-500">
                      {entry.time} - {entry.class}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <TodoList />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;