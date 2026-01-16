import React from 'react';

interface SkeletonProps {
  className?: string;
  count?: number;
}

const Skeleton: React.FC<SkeletonProps> = ({ className = '', count = 1 }) => {
  const skeletons = Array.from({ length: count }, (_, index) => (
    <div
      key={index}
      className={`rounded-xl bg-gradient-to-r from-gray-700/20 via-gray-600/20 to-gray-700/20 animate-pulse ${className}`}
    />
  ));

  return <>{skeletons}</>;
};

export default Skeleton;