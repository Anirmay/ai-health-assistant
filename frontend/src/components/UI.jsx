import React from 'react';
import { motion } from 'framer-motion';

export const LoadingSpinner = () => (
  <motion.div
    animate={{ rotate: 360 }}
    transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
    className="w-8 h-8 border-3 border-cyan-500 border-t-transparent rounded-full"
  />
);

export const SuccessAlert = ({ message }) => (
  <motion.div
    initial={{ opacity: 0, y: -20 }}
    animate={{ opacity: 1, y: 0 }}
    className="p-4 bg-green-500/20 border border-green-500/50 rounded-lg text-green-300"
  >
    ✅ {message}
  </motion.div>
);

export const ErrorAlert = ({ message }) => (
  <motion.div
    initial={{ opacity: 0, y: -20 }}
    animate={{ opacity: 1, y: 0 }}
    className="p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-300"
  >
    ❌ {message}
  </motion.div>
);

export const RiskBadge = ({ level }) => {
  const colors = {
    Low: 'bg-green-500/20 text-green-300 border-green-500/50',
    Medium: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/50',
    High: 'bg-red-500/20 text-red-300 border-red-500/50',
    Critical: 'bg-red-600/20 text-red-200 border-red-600/50',
  };
  
  return (
    <span className={`px-3 py-1 rounded-full border ${colors[level]}`}>
      {level}
    </span>
  );
};

export const ConfidenceBar = ({ confidence }) => (
  <div className="w-full bg-gray-700/50 rounded-full h-2 overflow-hidden">
    <motion.div
      initial={{ width: 0 }}
      animate={{ width: `${confidence * 100}%` }}
      transition={{ duration: 1 }}
      className="h-full bg-gradient-to-r from-cyan-500 to-purple-500"
    />
  </div>
);
