import Link from 'next/link';

const Footer = () => {
  return (
    <footer className="border-t border-slate-200 dark:border-slate-700 bg-white dark:bg-[#020617] py-12">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-lg font-bold text-[#051df5] mb-4">CyberTodo</h3>
            <p className="text-slate-700 dark:text-slate-300 text-sm">
              The future of productivity awaits. Secure, smart, and intuitive task management.
            </p>
          </div>

          <div>
            <h4 className="text-lg font-semibold text-slate-900 dark:text-slate-200 mb-4">Product</h4>
            <ul className="space-y-2">
              <li><Link href="#" className="text-slate-700 dark:text-slate-300 hover:text-[#051df5] dark:hover:text-indigo-400 transition-colors text-sm">Features</Link></li>
              <li><Link href="#" className="text-slate-700 dark:text-slate-300 hover:text-[#051df5] dark:hover:text-indigo-400 transition-colors text-sm">Pricing</Link></li>
              <li><Link href="#" className="text-slate-700 dark:text-slate-300 hover:text-[#051df5] dark:hover:text-indigo-400 transition-colors text-sm">Roadmap</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-lg font-semibold text-slate-900 dark:text-slate-200 mb-4">Company</h4>
            <ul className="space-y-2">
              <li><Link href="#" className="text-slate-700 dark:text-slate-300 hover:text-[#051df5] dark:hover:text-indigo-400 transition-colors text-sm">About</Link></li>
              <li><Link href="#" className="text-slate-700 dark:text-slate-300 hover:text-[#051df5] dark:hover:text-indigo-400 transition-colors text-sm">Blog</Link></li>
              <li><Link href="#" className="text-slate-700 dark:text-slate-300 hover:text-[#051df5] dark:hover:text-indigo-400 transition-colors text-sm">Careers</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-lg font-semibold text-slate-900 dark:text-slate-200 mb-4">Support</h4>
            <ul className="space-y-2">
              <li><Link href="#" className="text-slate-700 dark:text-slate-300 hover:text-[#051df5] dark:hover:text-indigo-400 transition-colors text-sm">Help Center</Link></li>
              <li><Link href="#" className="text-slate-700 dark:text-slate-300 hover:text-[#051df5] dark:hover:text-indigo-400 transition-colors text-sm">Contact</Link></li>
              <li><Link href="#" className="text-slate-700 dark:text-slate-300 hover:text-[#051df5] dark:hover:text-indigo-400 transition-colors text-sm">Privacy Policy</Link></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-slate-200 dark:border-slate-700 mt-12 pt-8 text-center text-slate-500 dark:text-slate-400 text-sm">
          <p>&copy; {new Date().getFullYear()} CyberTodo. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;