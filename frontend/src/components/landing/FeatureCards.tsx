'use client';

import { motion } from 'framer-motion';
import { Shield, Zap, Brain } from 'lucide-react';

const FeatureCards = () => {
  const features = [
    {
      icon: <Shield className="w-16 h-16 text-[#051df5]" />,
      title: "Secure Auth",
      description: "Military-grade authentication powered by industry-standard JWT tokens and end-to-end encrypted sessions. Your personal data and productivity insights are kept safe with multi-layered security protocols, ensuring seamless sync across all your devices.",
    },
    {
      icon: <Zap className="w-16 h-16 text-[#051df5]" />,
      title: "Smart Todo",
      description: "Experience the next generation of task management. Our intelligent AI-driven engine automatically prioritizes your tasks based on deadlines, urgency, and your personal workflow patterns to help you focus on what truly matters every single day.",
    },
    {
      icon: <Brain className="w-16 h-16 text-[#051df5]" />,
      title: "AI Teaser",
      description: "Stay ahead of the curve with our upcoming AI-powered personal assistant. Get automated task suggestions, smart rescheduling, and detailed productivity reports that analyze your habits to optimize your daily efficiency autonomously.",
    },
  ];

  return (
    <section className="py-20 bg-white dark:bg-[#020617]">
      <div className="max-w-6xl mx-auto px-6 sm:px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              whileHover={{ y: -10 }}
              className="bg-[#051df5] dark:bg-[#020617] rounded-xl py-14 px-8 text-center border border-slate-200 dark:border-slate-700 min-h-[450px] flex flex-col justify-center shadow-sm hover:shadow-md transition-shadow duration-300"
            >
              <div className="flex justify-center mb-4">
                <div className="bg-slate-50 dark:bg-slate-800 p-3 rounded-lg border border-slate-200 dark:border-slate-600">
                  {feature.icon}
                </div>
              </div>
              <h3 className="text-xl font-bold mb-2 text-slate-50 dark:text-slate-200">{feature.title}</h3>
              <p className="text-slate-50 dark:text-slate-300 flex-grow leading-relaxed">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeatureCards;