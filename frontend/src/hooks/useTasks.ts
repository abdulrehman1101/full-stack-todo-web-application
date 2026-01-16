import { useState, useCallback } from 'react';
import { toast } from 'sonner';
import { taskService } from '@/src/services/task-service';
import { Task } from '@/src/types/task';

export const useTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false); // Start as false initially
  const [error, setError] = useState<string | null>(null);

  // Load tasks from the API
  const loadTasks = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await taskService.getAllTasks();
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
      console.error('Error loading tasks:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Create a new task with optimistic update
  const createTask = useCallback(async (title: string, description?: string) => {
    try {
      // Optimistic update: add to local state immediately with temporary ID
      const tempId = `temp-${Date.now()}`;
      const tempTask = {
        id: tempId,
        title,
        description: description || '',
        is_completed: false,
        user_id: '', // Will be set by backend
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };

      setTasks(prev => [tempTask, ...prev]);

      // Actually create the task via API
      const newTask = await taskService.createTask(title, description);

      // Replace the temporary task with the actual one
      setTasks(prev => prev.map(t =>
        t.id === tempId ? newTask : t
      ));

      toast.success('Task created successfully!');
      return newTask;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task');

      // Remove the temporary task if API call failed
      setTasks(prev => prev.filter(t => !t.id.startsWith('temp-')));

      console.error('Error creating task:', err);
      toast.error('Failed to create task');
      throw err;
    }
  }, []);

  // Toggle task completion with optimistic update
  const toggleTaskCompletion = useCallback(async (taskId: string) => {
    try {
      // Find the task in the current state
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;

      // Optimistic update: toggle completion status immediately
      const newStatus = !task.is_completed;
      setTasks(prev => prev.map(t =>
        t.id === taskId ? { ...t, is_completed: newStatus } : t
      ));

      // Update the task via API
      await taskService.toggleTaskCompletion(taskId);

      toast.success(`Task ${newStatus ? 'completed' : 'marked as active'}!`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to toggle task completion');

      // If there's an error, revert the optimistic update
      const task = tasks.find(t => t.id === taskId);
      if (task) {
        setTasks(prev => prev.map(t =>
          t.id === taskId ? { ...t, is_completed: !task.is_completed } : t
        ));
      }

      console.error('Error toggling task completion:', err);
      toast.error('Failed to update task status');
      throw err;
    }
  }, [tasks]);

  // Update a task with optimistic update
  const updateTask = useCallback(async (taskId: string, updatedData: Partial<Task>) => {
    try {
      // Find the task in the current state
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;

      // Optimistic update: update local state immediately
      setTasks(prev => prev.map(t =>
        t.id === taskId ? { ...t, ...updatedData } : t
      ));

      // Update the task via API - use title if provided, otherwise use existing title
      const updatedTask = await taskService.updateTask(taskId, {
        title: updatedData.title || task.title,
        description: updatedData.description || task.description,
        is_completed: updatedData.is_completed ?? task.is_completed,
      });

      // Update with the server response to ensure consistency
      setTasks(prev => prev.map(t =>
        t.id === taskId ? updatedTask : t
      ));

      toast.success('Task updated successfully!');
      return updatedTask;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task');

      // If there's an error, revert the optimistic update
      const task = tasks.find(t => t.id === taskId);
      if (task) {
        setTasks(prev => prev.map(t =>
          t.id === taskId ? task : t
        ));
      }

      console.error('Error updating task:', err);
      toast.error('Failed to update task');
      throw err;
    }
  }, [tasks]);

  // Delete a task with optimistic update
  const deleteTask = useCallback(async (taskId: string) => {
    try {
      // Find the task before removing it (for potential rollback)
      const taskToDelete = tasks.find(t => t.id === taskId);

      // Optimistic update: remove from local state immediately
      setTasks(prev => prev.filter(t => t.id !== taskId));

      // Delete the task via API
      await taskService.deleteTask(taskId);

      toast.success('Task deleted successfully!');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task');

      // If there's an error, add the task back to the state
      if (taskToDelete) {
        setTasks(prev => [...prev, taskToDelete]);
      }

      console.error('Error deleting task:', err);
      toast.error('Failed to delete task');
      throw err;
    }
  }, [tasks]);

  // Get completed tasks count
  const getCompletedCount = () => {
    return tasks.filter(task => task.is_completed).length;
  };

  // Get pending tasks count
  const getPendingCount = () => {
    return tasks.filter(task => !task.is_completed).length;
  };

  return {
    tasks,
    loading,
    error,
    loadTasks,
    createTask,
    toggleTaskCompletion,
    updateTask,
    deleteTask,
    getCompletedCount,
    getPendingCount,
  };
};