'use client';

import { useAuth } from '@/src/contexts/AuthContext';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, Edit3, Trash2, CheckCircle, BarChart3 } from 'lucide-react';
import dynamic from 'next/dynamic';
import DashboardLayout from '@/src/components/dashboard/DashboardLayout';
import ActionCard from '@/src/components/dashboard/ActionCard';
import Skeleton from '@/src/components/common/Skeleton';

import { useTasks } from '@/src/hooks/useTasks';
import TaskCard from '@/src/components/tasks/TaskCard';

const DashboardPage = () => {
  const { user, loading, isAuthenticated } = useAuth();
  const router = useRouter();
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [showTaskList, setShowTaskList] = useState(false);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [taskFilter, setTaskFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [sortOrder, setSortOrder] = useState<'desc' | 'asc'>('desc'); // Default to descending (latest first)

  // Use the custom tasks hook
  const {
    tasks,
    loading: tasksLoading,
    error,
    loadTasks,
    createTask: createTaskApi,
    toggleTaskCompletion,
    updateTask,
    deleteTask,
    getCompletedCount,
    getPendingCount
  } = useTasks();

  // Sort and filter tasks based on search term and filter
  const filteredAndSortedTasks = tasks
    .filter(task => {
      // Apply filter
      if (taskFilter === 'active') return !task.is_completed;
      if (taskFilter === 'completed') return task.is_completed;
      return true; // 'all' filter
    })
    .filter(task => {
      // Apply search
      const searchLower = searchTerm.toLowerCase();
      return (
        (task.title && task.title.toLowerCase().includes(searchLower)) ||
        task.description.toLowerCase().includes(searchLower)
      );
    })
    .sort((a, b) => {
      // Sort by created_at, descending by default (latest first)
      const dateA = new Date(a.created_at).getTime();
      const dateB = new Date(b.created_at).getTime();
      return sortOrder === 'desc' ? dateB - dateA : dateA - dateB;
    });

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, loading, router]);

  // Load tasks when component mounts and user is authenticated
  useEffect(() => {
    if (isAuthenticated) {
      loadTasks();
    }
  }, [isAuthenticated, loadTasks]);

  const createTask = async () => {
    if (!newTaskTitle.trim()) return;

    try {
      await createTaskApi(newTaskTitle, newTaskDescription);
      setNewTaskTitle('');
      setNewTaskDescription('');
      setShowTaskForm(false); // Hide form after creating
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  // Show loading screen while authentication is loading
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#020617]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-400 mx-auto"></div>
          <p className="mt-4 text-gray-300">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Will be redirected by useEffect
  }

  // Import TaskCardSkeleton inside the component
  const TaskCardSkeleton = dynamic(() => import('@/src/components/tasks/TaskCardSkeleton'), { ssr: false });

  // Show loading screen only when fetching tasks (after auth is confirmed)
  if (tasksLoading && tasks.length === 0) {
    return (
      <DashboardLayout>
        <div className="p-8">
          <div className="max-w-6xl mx-auto">
            <header className="mb-10">
              <h1 className="text-4xl font-bold glow-text">Action Hub</h1>
              <p className="text-gray-400 mt-2">Welcome back, {user?.name || user?.username || (user?.email ? user.email.split('@')[0] : 'User')}! Your command center.</p>
            </header>

            {/* Action Cards Grid - Skeleton */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
              {[...Array(5)].map((_, index) => (
                <Skeleton key={index} className="glass rounded-2xl p-6 h-32 border backdrop-blur-md bg-white/5 border-indigo-500/50 shadow-[0_0_10px_rgba(99,102,241,0.3)]" />
              ))}
            </div>

            {/* Task List Header */}
            <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 mb-4">
              <div className="flex items-center gap-4">
                <h2 className="text-2xl font-semibold text-cyan-400">Your Tasks</h2>
                <span className="text-gray-400">Loading...</span>
              </div>
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search tasks..."
                  disabled
                  className="w-full sm:w-64 p-2 pl-10 rounded-lg glass border border-gray-700 text-white placeholder-gray-500 bg-gray-800/50 dark:bg-slate-900/50 dark:text-white dark:placeholder-slate-400"
                />
                <svg
                  className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
              </div>
            </div>

            {/* Task Skeletons */}
            <div className="space-y-3">
              {[...Array(5)].map((_, index) => (
                <TaskCardSkeleton key={index} index={index} />
              ))}
            </div>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="p-8">
        <div className="max-w-6xl mx-auto">
          <header className="mb-10">
            <h1 className="text-4xl font-bold glow-text">Action Hub</h1>
            <p className="text-gray-400 mt-2">Welcome back, {user?.name || user?.username || (user?.email ? user.email.split('@')[0] : 'User')}! Your command center.</p>
          </header>

          {/* Action Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            {/* Create Task Card */}
            <ActionCard
              title="Create Task"
              description="Add a new task to your list"
              icon={<Plus size={24} />}
              glowColor="indigo"
              onClick={() => setShowTaskForm(!showTaskForm)}
              count={tasks.length}
            />

            {/* Manage Tasks Card */}
            <ActionCard
              title="Manage Tasks"
              description="View and edit your tasks"
              icon={<Edit3 size={24} />}
              glowColor="cyan"
              onClick={() => {
                setShowTaskList(!showTaskList);
                // Scroll to task list section if showing
                if (!showTaskList) {
                  setTimeout(() => {
                    const taskListElement = document.getElementById('your-tasks-section');
                    if (taskListElement) {
                      taskListElement.scrollIntoView({ behavior: 'smooth' });
                    }
                  }, 100);
                }
              }}
              count={getPendingCount()}
            />

            {/* Analytics Card */}
            <ActionCard
              title="Task Analytics"
              description={`Completion Rate: ${tasks.length > 0 ? Math.round((getCompletedCount() / tasks.length) * 100) : 0}%`}
              icon={<BarChart3 size={24} />}
              glowColor="indigo"
              onClick={() => {}}
              count={getCompletedCount()}
            >
              {/* Progress bar visualization */}
              <div className="mt-2 w-full bg-gray-700 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-cyan-500 to-blue-500 h-2 rounded-full"
                  style={{ width: `${tasks.length > 0 ? Math.round((getCompletedCount() / tasks.length) * 100) : 0}%` }}
                ></div>
              </div>
            </ActionCard>

            {/* Delete/Cleanup Card */}
            <ActionCard
              title="Cleanup Tasks"
              description="Manage completed tasks"
              icon={<Trash2 size={24} />}
              glowColor="cyan"
              onClick={() => {
                // Filter out completed tasks for deletion
                tasks.filter(task => task.is_completed).forEach(task => deleteTask(task.id));
              }}
              count={getCompletedCount()}
              disabled={getCompletedCount() === 0}
            />

            {/* Quick Stats Card */}
            <ActionCard
              title="Quick Stats"
              description={`Active: ${getPendingCount()}, Completed: ${getCompletedCount()}`}
              icon={<CheckCircle size={24} />}
              glowColor="indigo"
              onClick={() => {
                // Cycle through the filters
                setTaskFilter(prev => {
                  if (prev === 'all') return 'active';
                  if (prev === 'active') return 'completed';
                  return 'all';
                });
              }}
              count={tasks.length}
            >
              <div className="flex justify-between mt-2 text-xs">
                <span className={`px-2 py-1 rounded ${
                  taskFilter === 'active'
                    ? 'bg-indigo-500/30 text-indigo-300 shadow-[0_0_8px_rgba(99,102,241,0.6)]'
                    : 'text-gray-400'
                }`}>
                  {getPendingCount()} Active
                </span>
                <span className={`px-2 py-1 rounded ${
                  taskFilter === 'completed'
                    ? 'bg-indigo-500/30 text-indigo-300 shadow-[0_0_8px_rgba(99,102,241,0.6)]'
                    : 'text-gray-400'
                }`}>
                  {getCompletedCount()} Done
                </span>
              </div>
            </ActionCard>
          </div>

          {/* Task Form - Only show when create task card is clicked */}
          <AnimatePresence>
            {showTaskForm && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="rounded-2xl p-6 mb-8 border border-white/10 bg-[#051df5] shadow-lg shadow-blue-500/20"
              >
                <h2 className="text-xl font-semibold mb-4 text-white">Create New Task</h2>
                <div className="space-y-4">
                  <input
                    type="text"
                    value={newTaskTitle}
                    onChange={(e) => setNewTaskTitle(e.target.value)}
                    placeholder="Task title..."
                    className="w-full p-3 rounded-lg bg-white dark:bg-slate-900/50 text-slate-950 dark:text-white border border-black dark:border-blue-500/50 placeholder:text-slate-400 dark:placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-500 focus:border-black dark:focus:border-blue-500"
                    onKeyDown={(e) => e.key === 'Enter' && createTask()}
                  />
                  <textarea
                    value={newTaskDescription}
                    onChange={(e) => setNewTaskDescription(e.target.value)}
                    placeholder="Task description (optional)..."
                    className="w-full p-3 rounded-lg bg-white dark:bg-slate-900/50 text-slate-950 dark:text-white border border-black dark:border-blue-500/50 placeholder:text-slate-400 dark:placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-500 focus:border-black dark:focus:border-blue-500"
                    rows={2}
                  />
                  <div className="flex gap-4">
                    <button
                      onClick={createTask}
                      disabled={!newTaskTitle.trim()}
                      className="flex items-center gap-2 px-4 py-2 bg-white text-[#051df5] border border-blue-200 font-semibold rounded-lg hover:bg-[#051df5] hover:text-white hover:scale-105 hover:shadow-[0_0_20px_rgba(5,29,245,0.4)] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <Plus size={18} />
                      Add Task
                    </button>
                    <button
                      onClick={() => setShowTaskForm(false)}
                      className="px-4 py-2 bg-white text-black border border-black rounded-lg hover:bg-slate-100 hover:scale-105 transition-all duration-300"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Task List - Only show when manage tasks card is clicked */}
          <AnimatePresence>
            {showTaskList && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                id="your-tasks-section"
              >
                <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 mb-4">
                  <div className="flex items-center gap-4">
                    <h2 className="text-2xl font-semibold text-white">Your Tasks</h2>
                    <span className="text-white">{filteredAndSortedTasks.length} {filteredAndSortedTasks.length === 1 ? 'task' : 'tasks'} {taskFilter !== 'all' && `(${taskFilter})`}</span>
                  </div>
                  <div className="relative">
                    <input
                      type="text"
                      placeholder="Search tasks..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="w-full sm:w-64 p-2 pl-10 rounded-lg bg-white dark:bg-slate-900/50 text-slate-950 dark:text-white border border-black dark:border-blue-500/50 placeholder:text-slate-400 dark:placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-500 focus:border-black dark:focus:border-blue-500"
                    />
                    <svg
                      className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-950"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                  </div>
                </div>

                {/* Task List */}
                {filteredAndSortedTasks.length === 0 ? (
                  <div className="rounded-2xl p-8 text-center border border-white/10 bg-[#051df5] shadow-lg shadow-blue-500/20">
                    <p className="text-white">
                      {searchTerm
                        ? `No tasks found for "${searchTerm}". Try a different search.`
                        : `No ${taskFilter === 'active' ? 'active' : taskFilter === 'completed' ? 'completed' : ''} tasks yet. ${taskFilter === 'all' ? 'Time to create a new mission!' : 'Time to relax or create a new mission!'}`}
                    </p>
                  </div>
                ) : (
                  <motion.div
                    layout
                    className="space-y-3"
                  >
                    <AnimatePresence>
                      {filteredAndSortedTasks.map((task, index) => (
                        <TaskCard
                          key={task.id}
                          task={{
                            ...task,
                            title: task.title || task.description.substring(0, 50) || 'Untitled Task' // Fallback to description or untitled
                          }}
                          onToggleComplete={toggleTaskCompletion}
                          onEdit={updateTask}
                          onDelete={deleteTask}
                          index={index}
                        />
                      ))}
                    </AnimatePresence>
                  </motion.div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default DashboardPage;