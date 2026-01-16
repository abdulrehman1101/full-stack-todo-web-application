'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Plus, Edit3, Trash2, CheckCircle, BarChart3 } from 'lucide-react';

interface ActionCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  glowColor?: 'indigo' | 'cyan';
  onClick: () => void;
  count?: number;
  disabled?: boolean;
  children?: React.ReactNode;
}

const ActionCard: React.FC<ActionCardProps> = ({
  title,
  description,
  icon,
  onClick,
  count,
  disabled = false,
  children
}) => {

  return (
    <motion.div
      whileHover={{ scale: 1.03, y: -5 }}
      whileTap={{ scale: 0.98 }}
      className={`rounded-2xl p-6 border border-white/10 bg-[#051df5] dark:bg-[#020617]/50 dark:border-indigo-500/50 shadow-lg shadow-blue-500/20 dark:shadow-[0_0_15px_rgba(34,211,238,0.3)] transition-all duration-300 cursor-pointer ${
        disabled ? 'cursor-not-allowed' : 'hover:shadow-[0_0_25px_rgba(5,29,245,0.4)] dark:hover:shadow-[0_0_25px_rgba(34,211,238,0.4)]'
      }`}
      onClick={!disabled ? onClick : undefined}
    >
      <div className="flex flex-col h-full">
        <div className="flex items-center justify-between mb-4">
          <div className="p-3 rounded-xl bg-white/10 dark:bg-indigo-900/30 text-white dark:text-slate-200">
            {icon}
          </div>
          {count !== undefined && (
            <span className="text-lg font-bold px-3 py-1 rounded-full bg-white/20 dark:bg-indigo-900/30 text-white dark:text-slate-200">
              {count}
            </span>
          )}
        </div>

        <h3 className="text-xl font-semibold text-white dark:text-slate-200 mb-2">{title}</h3>
        <p className="text-white dark:text-slate-300 text-sm flex-grow">{description}</p>

        {children && (
          <div className="mt-3">
            {children}
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default ActionCard;