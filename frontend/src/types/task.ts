export interface Task {
  id: string;
  title?: string; // Added for frontend use - not in backend
  description: string;
  is_completed: boolean; // Matches backend field name
  user_id: string;
  created_at: string;
  updated_at: string;
}