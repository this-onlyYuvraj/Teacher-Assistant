import React, { useState, useMemo } from 'react';
import { Student } from '../types';
import { BookOpen, TrendingUp, CheckCircle2, ChevronDown, Users, Award, ClipboardCheck } from 'lucide-react';

const Reports = () => {
  const [students] = useState<Student[]>([
    {
      id: '1',
      name: 'John Doe',
      subjects: [
        {
          subject: 'Mathematics',
          testAverage: 88,
          assignmentsCompleted: 15,
          totalAssignments: 16,
          performance: 'Excellent'
        },
        {
          subject: 'Physics',
          testAverage: 82,
          assignmentsCompleted: 14,
          totalAssignments: 15,
          performance: 'Good'
        }
      ]
    },
    {
      id: '2',
      name: 'Jane Smith',
      subjects: [
        {
          subject: 'Mathematics',
          testAverage: 95,
          assignmentsCompleted: 16,
          totalAssignments: 16,
          performance: 'Excellent'
        },
        {
          subject: 'Physics',
          testAverage: 90,
          assignmentsCompleted: 15,
          totalAssignments: 15,
          performance: 'Excellent'
        }
      ]
    },
    {
      id: '3',
      name: 'Mike Johnson',
      subjects: [
        {
          subject: 'Mathematics',
          testAverage: 75,
          assignmentsCompleted: 12,
          totalAssignments: 16,
          performance: 'Average'
        },
        {
          subject: 'Physics',
          testAverage: 68,
          assignmentsCompleted: 11,
          totalAssignments: 15,
          performance: 'Needs Improvement'
        }
      ]
    }
  ]);

  const [expandedStudents, setExpandedStudents] = useState<Record<string, boolean>>({});

  const overallStats = useMemo(() => {
    let totalTestScore = 0;
    let totalAssignmentsCompleted = 0;
    let totalAssignments = 0;
    let totalSubjects = 0;
    const performanceCounts: Record<string, number> = {
      'Excellent': 0,
      'Good': 0,
      'Average': 0,
      'Needs Improvement': 0
    };

    students.forEach(student => {
      student.subjects.forEach(subject => {
        totalTestScore += subject.testAverage;
        totalAssignmentsCompleted += subject.assignmentsCompleted;
        totalAssignments += subject.totalAssignments;
        totalSubjects++;
        performanceCounts[subject.performance]++;
      });
    });

    return {
      averageTestScore: Math.round(totalTestScore / totalSubjects),
      assignmentCompletionRate: Math.round((totalAssignmentsCompleted / totalAssignments) * 100),
      totalStudents: students.length,
      performanceSummary: performanceCounts
    };
  }, [students]);

  const toggleStudent = (studentId: string) => {
    setExpandedStudents(prev => ({
      ...prev,
      [studentId]: !prev[studentId]
    }));
  };

  const getPerformanceColor = (performance: string) => {
    switch (performance) {
      case 'Excellent':
        return 'text-green-600 bg-green-100';
      case 'Good':
        return 'text-blue-600 bg-blue-100';
      case 'Average':
        return 'text-yellow-600 bg-yellow-100';
      case 'Needs Improvement':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="p-6 ml-64">
      <h1 className="text-3xl font-bold mb-6">Class Reports</h1>
      
      {/* Overall Performance Summary */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Overall Class Performance</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-blue-50 rounded-lg p-4">
            <div className="flex items-center mb-2">
              <Award className="w-6 h-6 text-blue-500 mr-2" />
              <h3 className="text-lg font-medium">Average Test Score</h3>
            </div>
            <p className="text-3xl font-bold text-blue-600">{overallStats.averageTestScore}%</p>
          </div>
          
          <div className="bg-green-50 rounded-lg p-4">
            <div className="flex items-center mb-2">
              <ClipboardCheck className="w-6 h-6 text-green-500 mr-2" />
              <h3 className="text-lg font-medium">Assignment Completion</h3>
            </div>
            <p className="text-3xl font-bold text-green-600">{overallStats.assignmentCompletionRate}%</p>
          </div>
          
          <div className="bg-purple-50 rounded-lg p-4">
            <div className="flex items-center mb-2">
              <Users className="w-6 h-6 text-purple-500 mr-2" />
              <h3 className="text-lg font-medium">Total Students</h3>
            </div>
            <p className="text-3xl font-bold text-purple-600">{overallStats.totalStudents}</p>
          </div>
        </div>

        <div className="mt-6">
          <h3 className="text-lg font-medium mb-3">Performance Distribution</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(overallStats.performanceSummary).map(([performance, count]) => (
              <div key={performance} className={`rounded-lg p-3 ${getPerformanceColor(performance)}`}>
                <h4 className="font-medium">{performance}</h4>
                <p className="text-2xl font-bold">{count}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Individual Student Reports */}
      <h2 className="text-xl font-semibold mb-4">Individual Student Reports</h2>
      <div className="space-y-4">
        {students.map((student) => (
          <div key={student.id} className="bg-white rounded-lg shadow overflow-hidden">
            <button
              onClick={() => toggleStudent(student.id)}
              className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
            >
              <h2 className="text-xl font-semibold">{student.name}</h2>
              <ChevronDown
                className={`w-5 h-5 text-gray-500 transition-transform ${
                  expandedStudents[student.id] ? 'transform rotate-180' : ''
                }`}
              />
            </button>
            
            {expandedStudents[student.id] && (
              <div className="px-6 pb-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                  {student.subjects.map((subject, index) => (
                    <div key={index} className="bg-gray-50 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-medium">{subject.subject}</h3>
                        <span
                          className={`px-3 py-1 rounded-full text-sm font-medium ${getPerformanceColor(
                            subject.performance
                          )}`}
                        >
                          {subject.performance}
                        </span>
                      </div>
                      <div className="space-y-3">
                        <div className="flex items-center">
                          <TrendingUp className="w-5 h-5 mr-2 text-blue-500" />
                          <span className="text-gray-600">Test Average:</span>
                          <span className="ml-auto font-semibold">{subject.testAverage}%</span>
                        </div>
                        <div className="flex items-center">
                          <CheckCircle2 className="w-5 h-5 mr-2 text-green-500" />
                          <span className="text-gray-600">Assignments Completed:</span>
                          <span className="ml-auto font-semibold">
                            {subject.assignmentsCompleted}/{subject.totalAssignments}
                          </span>
                        </div>
                        <div className="flex items-center">
                          <BookOpen className="w-5 h-5 mr-2 text-purple-500" />
                          <span className="text-gray-600">Completion Rate:</span>
                          <span className="ml-auto font-semibold">
                            {Math.round((subject.assignmentsCompleted / subject.totalAssignments) * 100)}%
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Reports;