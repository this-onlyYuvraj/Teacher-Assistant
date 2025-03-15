export interface Task {
  id: string;
  title: string;
  completed: boolean;
  dueDate: string;
}

export interface TimeTableEntry {
  day: string;
  time: string;
  subject: string;
  class: string;
}

export interface Assignment {
  id: string;
  title: string;
  dueDate: string;
  subject: string;
  isChecked: boolean;
  submissions: StudentSubmission[];
}

export interface Test {
  id: string;
  title: string;
  date: string;
  subject: string;
  isChecked: boolean;
  submissions: StudentSubmission[];
}

export interface StudentSubmission {
  studentId: string;
  studentName: string;
  submitted: boolean;
  score?: number;
}

export interface Student {
  id: string;
  name: string;
  subjects: SubjectReport[];
}

export interface SubjectReport {
  subject: string;
  testAverage: number;
  assignmentsCompleted: number;
  totalAssignments: number;
  performance: 'Excellent' | 'Good' | 'Average' | 'Needs Improvement';
}