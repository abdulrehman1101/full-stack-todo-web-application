'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, Edit3, Trash2, Save, X } from 'lucide-react';

interface Task {
  id: string;
  title?: string;
  description: string;
  is_completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TaskCardProps {
  task: Task;
  onToggleComplete: (id: string) => void;
  onEdit: (id: string, updatedTask: Partial<Task>) => void;
  onDelete: (id: string) => void;
  index?: number;
}

const TaskCard: React.FC<TaskCardProps> = ({
  task,
  onToggleComplete,
  onEdit,
  onDelete,
  index = 0
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title || '');
  const [editDescription, setEditDescription] = useState(task.description);

  const glowClass = task.is_completed
    ? 'shadow-[0_0_15px_rgba(34,211,238,0.5)] border-cyan-400/50' // cyan-400 glow
    : 'shadow-[0_0_10px_rgba(99,102,241,0.3)] border-indigo-500/50'; // indigo-500 glow

  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.3,
        ease: 'easeOut',
        delay: index * 0.1
      }
    },
    exit: { opacity: 0, scale: 0.9, transition: { duration: 0.2 } }
  };

  const handleSave = () => {
    onEdit(task.id, { title: editTitle, description: editDescription });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditTitle(task.title || '');
    setEditDescription(task.description);
    setIsEditing(false);
  };

  return (
    <motion.div
      variants={cardVariants}
      initial="hidden"
      animate="visible"
      exit="exit"
      className={`rounded-xl p-4 border border-white/10 bg-[#051df5] dark:bg-[#020617]/50 dark:border-indigo-500/50 shadow-lg shadow-blue-500/20 dark:shadow-[0_0_15px_rgba(34,211,238,0.3)] transition-all duration-300`}
    >
      <AnimatePresence mode="wait">
        {!isEditing ? (
          <motion.div
            key="view-mode"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex items-start gap-3"
          >
            <button
              onClick={() => onToggleComplete(task.id)}
              className={`mt-1 flex-shrink-0 w-5 h-5 rounded-full border flex items-center justify-center transition-colors ${
                task.is_completed
                  ? 'bg-cyan-500 border-cyan-400 text-white dark:bg-cyan-500 dark:border-cyan-400'
                  : 'border-white text-white hover:border-cyan-400 dark:border-slate-300 dark:text-slate-200 dark:hover:border-cyan-400'
              }`}
              aria-label={task.is_completed ? 'Mark as incomplete' : 'Mark as complete'}
            >
              {task.is_completed && <CheckCircle size={12} />}
            </button>

            <div className="flex-1 min-w-0">
              <h3 className={`font-medium truncate ${task.is_completed ? 'text-cyan-200 line-through dark:text-cyan-200' : 'text-white dark:text-slate-200'}`}>
                {task.title || task.description.substring(0, 50) || 'Untitled Task'}
              </h3>
              {task.description && (
                <p className={`text-sm mt-1 ${task.is_completed ? 'text-cyan-300/70 dark:text-cyan-300/70' : 'text-white dark:text-slate-200'}`}>
                  {task.description.substring(0, 100)}{task.description.length > 100 ? '...' : ''}
                </p>
              )}
            </div>

            <div className="flex gap-2 ml-2 flex-shrink-0">
              <button
                onClick={() => setIsEditing(true)}
                className="p-1.5 rounded-lg hover:bg-white/10 dark:hover:bg-slate-700/50 transition-colors text-white dark:text-slate-200 hover:text-cyan-400 dark:hover:text-cyan-400"
                aria-label="Edit task"
              >
                <Edit3 size={16} />
              </button>
              <button
                onClick={() => onDelete(task.id)}
                className="p-1.5 rounded-lg hover:bg-red-500/20 dark:hover:bg-red-700/50 transition-colors text-white dark:text-slate-200 hover:text-red-400 dark:hover:text-red-400"
                aria-label="Delete task"
              >
                <Trash2 size={16} />
              </button>
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="edit-mode"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="space-y-3"
          >
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              className="w-full p-2 rounded-lg bg-white dark:bg-slate-900/50 text-slate-950 dark:text-white border border-black dark:border-blue-500/50 placeholder:text-slate-400 dark:placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-500 focus:border-black dark:focus:border-blue-500 text-sm"
              placeholder="Task title..."
              autoFocus
            />
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              className="w-full p-2 rounded-lg bg-white dark:bg-slate-900/50 text-slate-950 dark:text-white border border-black dark:border-blue-500/50 placeholder:text-slate-400 dark:placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-500 focus:border-black dark:focus:border-blue-500 text-sm"
              placeholder="Task description..."
              rows={2}
            />
            <div className="flex justify-end space-x-2 pt-1">
              <button
                onClick={handleCancel}
                className="p-1.5 rounded-lg hover:bg-gray-600 dark:hover:bg-slate-600 transition-colors text-white dark:text-slate-200 hover:text-white dark:hover:text-slate-200"
                aria-label="Cancel edit"
              >
                <X size={16} />
              </button>
              <button
                onClick={handleSave}
                className="p-1.5 rounded-lg hover:bg-green-600/20 dark:hover:bg-green-700/50 transition-colors text-white dark:text-slate-200 hover:text-green-400 dark:hover:text-green-400"
                aria-label="Save task"
              >
                <Save size={16} />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default TaskCard;