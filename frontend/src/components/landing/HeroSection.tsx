'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';

const HeroSection = () => {
  return (
    <section className="relative min-h-[60vh] lg:min-h-[70vh] grid grid-cols-1 lg:grid-cols-2 px-6 lg:px-20 pt-10 py-12 lg:py-16 overflow-hidden bg-white dark:bg-[#020617] gap-10 lg:gap-16">
      <div className="order-last lg:order-first flex flex-col justify-center items-center lg:items-start text-center lg:text-left h-full py-12 lg:py-16">
        {/* Main heading with gradient text */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="mb-8"
        >
          <h1 className="text-4xl md:text-6xl font-bold mb-4">
            <span className="text-[#051df5]">Transform Your Productivity</span>
          </h1>
          <p className="text-xl text-slate-700 dark:text-slate-300 max-w-2xl mt-6">
            Experience the future of task management with AI-powered insights,
            secure authentication, and seamless collaboration.
          </p>
        </motion.div>

        {/* Glowing "Get Started" button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <Link
            href="/dashboard"
            className="inline-block rounded-lg bg-blue-50 px-8 py-3 text-[#051df5] border border-blue-200 hover:bg-[#051df5] hover:text-white hover:scale-105 hover:shadow-[0_0_20px_rgba(5,29,245,0.4)] transition-all duration-300"
          >
            Get Started
          </Link>
        </motion.div>
      </div>
      <div className="order-first lg:order-last col-span-1 flex items-center justify-center p-4">
        <img
          src="/hero-bg.png"
          alt="Hero background"
          className="max-w-full h-auto object-contain"
        />
      </div>
    </section>
  );
};

export default HeroSection;