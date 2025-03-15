import React, { useState } from 'react';
import { Assignment, Test } from '../types';
import { CheckCircle, Circle, Plus } from 'lucide-react';

const Tasks = () => {
  const [assignments, setAssignments] = useState<Assignment[]>([
    {
      id: '1',
      title: 'Math Homework Ch. 5',
      dueDate: '2024-03-20',
      subject: 'Mathematics',
      isChecked: true,
      submissions: [
        { studentId: '1', studentName: 'John Doe', submitted: true, score: 85 },
        { studentId: '2', studentName: 'Jane Smith', submitted: true, score: 92 },
        { studentId: '3', studentName: 'Mike Johnson', submitted: false },
      ],
    },
  ]);

  const [tests, setTests] = useState<Test[]>([
    {
      id: '1',
      title: 'Mid-term Test',
      date: '2024-03-25',
      subject: 'Chemistry',
      isChecked: false,
      submissions: [
        { studentId: '1', studentName: 'John Doe', submitted: true, score: 88 },
        { studentId: '2', studentName: 'Jane Smith', submitted: true, score: 95 },
        { studentId: '3', studentName: 'Mike Johnson', submitted: true, score: 78 },
      ],
    },
  ]);

  const [selectedItem, setSelectedItem] = useState<Assignment | Test | null>(null);
  const [showSubmissions, setShowSubmissions] = useState(false);

  const toggleCheck = (id: string, type: 'assignment' | 'test') => {
    if (type === 'assignment') {
      setAssignments(assignments.map(a =>
        a.id === id ? { ...a, isChecked: !a.isChecked } : a
      ));
    } else {
      setTests(tests.map(t =>
        t.id === id ? { ...t, isChecked: !t.isChecked } : t
      ));
    }
  };

  return (
    <div className="p-6 ml-64">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Tasks</h1>
        <div className="space-x-4">
          <button className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">
            <Plus className="inline-block mr-2" size={20} />
            Create Assignment
          </button>
          <button className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600">
            <Plus className="inline-block mr-2" size={20} />
            Create Test
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Assignments</h2>
          <div className="space-y-3">
            {assignments.map((assignment) => (
              <div
                key={assignment.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded cursor-pointer hover:bg-gray-100"
                onClick={() => {
                  setSelectedItem(assignment);
                  setShowSubmissions(true);
                }}
              >
                <div className="flex items-center space-x-3">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleCheck(assignment.id, 'assignment');
                    }}
                  >
                    {assignment.isChecked ? (
                      <CheckCircle className="text-green-500" size={20} />
                    ) : (
                      <Circle className="text-gray-400" size={20} />
                    )}
                  </button>
                  <div>
                    <h3 className="font-medium">{assignment.title}</h3>
                    <p className="text-sm text-gray-500">
                      {assignment.subject} - Due: {assignment.dueDate}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Tests</h2>
          <div className="space-y-3">
            {tests.map((test) => (
              <div
                key={test.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded cursor-pointer hover:bg-gray-100"
                onClick={() => {
                  setSelectedItem(test);
                  setShowSubmissions(true);
                }}
              >
                <div className="flex items-center space-x-3">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleCheck(test.id, 'test');
                    }}
                  >
                    {test.isChecked ? (
                      <CheckCircle className="text-green-500" size={20} />
                    ) : (
                      <Circle className="text-gray-400" size={20} />
                    )}
                  </button>
                  <div>
                    <h3 className="font-medium">{test.title}</h3>
                    <p className="text-sm text-gray-500">
                      {test.subject} - Date: {test.date}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {showSubmissions && selectedItem && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white rounded-lg p-6 w-2/3">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">{selectedItem.title} - Submissions</h2>
              <button
                onClick={() => setShowSubmissions(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                Close
              </button>
            </div>
            <div className="divide-y">
              {selectedItem.submissions.map((submission) => (
                <div key={submission.studentId} className="py-3">
                  <div className="flex justify-between items-center">
                    <div>
                      <p className="font-medium">{submission.studentName}</p>
                      <p className="text-sm text-gray-500">
                        {submission.submitted ? 'Submitted' : 'Not Submitted'}
                      </p>
                    </div>
                    {submission.submitted && submission.score && (
                      <p className="text-lg font-semibold">
                        Score: {submission.score}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Tasks;