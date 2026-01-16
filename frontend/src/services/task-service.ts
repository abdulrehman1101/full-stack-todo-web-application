import { Task } from '@/src/types/task';
import apiClient from '@/src/lib/api-client';

interface CreateTaskRequest {
  title: string;
  description?: string;
  is_completed?: boolean;
}

interface UpdateTaskRequest {
  title?: string;
  description?: string;
  is_completed?: boolean;
}

class TaskService {
  async getAllTasks(): Promise<Task[]> {
    const response = await apiClient.get('/tasks/');
    return response.data;
  }

  async createTask(title: string, description?: string): Promise<Task> {
    const response = await apiClient.post('/tasks/', {
      title,
      description: description || ''
    });
    return response.data;
  }

  async updateTask(id: string, taskData: UpdateTaskRequest): Promise<Task> {
    const response = await apiClient.put(`/tasks/${id}/`, taskData);
    return response.data;
  }

  async toggleTaskCompletion(id: string): Promise<Task> {
    const response = await apiClient.patch(`/tasks/${id}/complete/`);
    return response.data;
  }

  async deleteTask(id: string): Promise<void> {
    await apiClient.delete(`/tasks/${id}/`);
  }
}

export const taskService = new TaskService();