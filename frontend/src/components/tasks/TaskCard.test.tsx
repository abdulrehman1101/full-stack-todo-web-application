// Test file to validate the TaskCard component functionality
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TaskCard from './TaskCard';

// Mock task data
const mockTask = {
  id: '1',
  description: 'Test task description',
  is_completed: false,
  user_id: 'user-123',
  created_at: '2026-01-15T10:00:00Z',
  updated_at: '2026-01-15T10:00:00Z'
};

describe('TaskCard Component', () => {
  test('renders task description correctly', () => {
    render(
      <TaskCard
        task={mockTask}
        onToggleComplete={() => {}}
        onEdit={() => {}}
        onDelete={() => {}}
      />
    );

    expect(screen.getByText(/Test task description/i)).toBeInTheDocument();
  });

  test('applies correct glow effect for incomplete tasks', () => {
    render(
      <TaskCard
        task={mockTask}
        onToggleComplete={() => {}}
        onEdit={() => {}}
        onDelete={() => {}}
      />
    );

    const card = screen.getByRole('button', { name: /Mark as complete/i }).closest('.glass');
    expect(card).toHaveClass('border-indigo-500/50'); // indigo glow for incomplete
  });

  test('applies correct glow effect for completed tasks', () => {
    const completedTask = { ...mockTask, is_completed: true };

    render(
      <TaskCard
        task={completedTask}
        onToggleComplete={() => {}}
        onEdit={() => {}}
        onDelete={() => {}}
      />
    );

    const card = screen.getByRole('button', { name: /Mark as incomplete/i }).closest('.glass');
    expect(card).toHaveClass('border-cyan-400/50'); // cyan glow for completed
  });

  test('calls onToggleComplete when checkbox is clicked', () => {
    const toggleMock = jest.fn();

    render(
      <TaskCard
        task={mockTask}
        onToggleComplete={toggleMock}
        onEdit={() => {}}
        onDelete={() => {}}
      />
    );

    const checkboxButton = screen.getByRole('button', { name: /Mark as complete/i });
    fireEvent.click(checkboxButton);

    expect(toggleMock).toHaveBeenCalledWith(mockTask.id);
  });

  test('calls onDelete when delete button is clicked', () => {
    const deleteMock = jest.fn();

    render(
      <TaskCard
        task={mockTask}
        onToggleComplete={() => {}}
        onEdit={() => {}}
        onDelete={deleteMock}
      />
    );

    const deleteButton = screen.getByRole('button', { name: /Delete task/i });
    fireEvent.click(deleteButton);

    expect(deleteMock).toHaveBeenCalledWith(mockTask.id);
  });

  test('calls onEdit when edit button is clicked', () => {
    const editMock = jest.fn();

    render(
      <TaskCard
        task={mockTask}
        onToggleComplete={() => {}}
        onEdit={editMock}
        onDelete={() => {}}
      />
    );

    const editButton = screen.getByRole('button', { name: /Edit task/i });
    fireEvent.click(editButton);

    expect(editMock).toHaveBeenCalledWith(mockTask);
  });
});