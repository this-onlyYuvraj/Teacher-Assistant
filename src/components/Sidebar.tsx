import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, ClipboardList, FileBarChart, Settings, HelpCircle } from 'lucide-react';

const Sidebar = () => {
  return (
    <div className="h-screen w-64 bg-white fixed left-0 top-0 p-6 border-r border-gray-100">
      <div className="mb-8">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-blue-600 rounded-lg"></div>
          <h1 className="text-xl font-bold">Logo</h1>
        </div>
      </div>
      
      <nav className="space-y-2">
        <NavLink
          to="/"
          className={({ isActive }) =>
            `flex items-center space-x-3 p-3 rounded-lg transition-colors ${
              isActive ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50'
            }`
          }
        >
          <LayoutDashboard size={20} />
          <span className="font-medium">Dashboard</span>
        </NavLink>
        <NavLink
          to="/tasks"
          className={({ isActive }) =>
            `flex items-center space-x-3 p-3 rounded-lg transition-colors ${
              isActive ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50'
            }`
          }
        >
          <ClipboardList size={20} />
          <span className="font-medium">Task</span>
        </NavLink>
        <NavLink
          to="/reports"
          className={({ isActive }) =>
            `flex items-center space-x-3 p-3 rounded-lg transition-colors ${
              isActive ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50'
            }`
          }
        >
          <FileBarChart size={20} />
          <span className="font-medium">Report</span>
        </NavLink>
      </nav>

      <div className="absolute bottom-6 left-6 right-6 space-y-2">
        <button className="flex items-center space-x-3 p-3 rounded-lg transition-colors text-gray-600 hover:bg-gray-50 w-full">
          <Settings size={20} />
          <span className="font-medium">Settings</span>
        </button>
        <button className="flex items-center space-x-3 p-3 rounded-lg transition-colors text-gray-600 hover:bg-gray-50 w-full">
          <HelpCircle size={20} />
          <span className="font-medium">Support</span>
        </button>
      </div>
    </div>
  );
}

export default Sidebar;