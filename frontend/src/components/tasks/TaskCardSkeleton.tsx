import React from 'react';
import { motion } from 'framer-motion';
import Skeleton from '../common/Skeleton';

interface TaskCardSkeletonProps {
  index?: number;
}

const TaskCardSkeleton: React.FC<TaskCardSkeletonProps> = ({ index = 0 }) => {
  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    exit: { opacity: 0, scale: 0.9, transition: { duration: 0.2 } }
  };

  return (
    <motion.div
      variants={cardVariants}
      initial="hidden"
      animate={{
        opacity: 1,
        y: 0,
        transition: {
          duration: 0.3,
          ease: "easeOut" as const,
          delay: index * 0.1
        }
      }}
      exit="exit"
      className="glass rounded-xl p-4 border backdrop-blur-md bg-white/5 border-indigo-500/50 shadow-[0_0_10px_rgba(99,102,241,0.3)]"
    >
      <div className="flex items-start gap-3">
        <Skeleton className="mt-1 flex-shrink-0 w-5 h-5 rounded-full border" />

        <div className="flex-1 min-w-0">
          <Skeleton className="h-5 w-3/4 mb-2 rounded" />
          <Skeleton className="h-4 w-full rounded" />
        </div>

        <div className="flex gap-2 ml-2 flex-shrink-0">
          <Skeleton className="w-6 h-6 rounded-lg" />
          <Skeleton className="w-6 h-6 rounded-lg" />
        </div>
      </div>
    </motion.div>
  );
};

export default TaskCardSkeleton;