"use client";

import React, { useState, useEffect } from "react";
import { Menu, X, Terminal } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useReducedMotion } from "@/hooks/useReducedMotion";

export const CyberNav: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const shouldReduce = useReducedMotion();

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 40);
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navItems = [
    { name: "CORE_NODE", href: "#home" },
    { name: "BIOLOGICAL_ID", href: "#about" },
    { name: "SKILLS_MATRIX", href: "#skills" },
    { name: "PROJECTS_INDEX", href: "#projects" },
    { name: "HISTORICAL_LOGS", href: "#experience" },
  ];

  return (
    <nav 
      className={`fixed top-0 left-0 w-full z-40 transition-all duration-300 ${
        scrolled 
          ? "bg-cyber-darker/85 backdrop-blur-md border-b border-cyber-cyan/15 py-3 shadow-md" 
          : "bg-transparent py-5"
      }`}
      aria-label="Main system navigation"
    >
      <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
        {/* Brand Logo */}
        <a 
          href="#home" 
          className="font-mono text-sm md:text-base font-bold tracking-widest text-cyber-cyan flex items-center gap-2"
          aria-label="Xavier Neon portfolio core link"
        >
          <Terminal className="w-5 h-5 text-cyber-pink animate-pulse" />
          <span className="hover:text-white transition-colors duration-200">[XAVIER_NEON]</span>
        </a>

        {/* Desktop Menu Link list */}
        <div className="hidden md:flex items-center gap-8">
          {navItems.map((item) => (
            <a
              key={item.name}
              href={item.href}
              className="font-mono text-[11px] tracking-[0.2em] text-gray-400 hover:text-cyber-cyan transition-colors relative group py-1"
            >
              <span>{item.name}</span>
              <span className="absolute bottom-0 left-0 w-0 h-[2px] bg-cyber-pink transition-all duration-300 group-hover:w-full" />
            </a>
          ))}
        </div>

        {/* Mobile Menu Toggler */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="md:hidden text-cyber-cyan hover:text-cyber-pink transition-colors focus:outline-none focus:ring-1 focus:ring-cyber-cyan"
          aria-label={isOpen ? "Close configuration menu" : "Open configuration menu"}
          aria-expanded={isOpen}
        >
          {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Drawer Panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={shouldReduce ? { opacity: 0 } : { opacity: 0, height: 0 }}
            animate={shouldReduce ? { opacity: 1 } : { opacity: 1, height: "auto" }}
            exit={shouldReduce ? { opacity: 0 } : { opacity: 0, height: 0 }}
            className="md:hidden bg-cyber-darker/95 border-b border-cyber-cyan/15 w-full overflow-hidden"
          >
            <div className="flex flex-col px-6 py-6 space-y-4 font-mono text-xs">
              {navItems.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  onClick={() => setIsOpen(false)}
                  className="tracking-wider text-gray-300 hover:text-cyber-cyan py-2 border-b border-gray-900 flex items-center justify-between"
                >
                  <span>&gt; {item.name}</span>
                  <span className="text-[9px] text-cyber-pink">[LOAD]</span>
                </a>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};
export default CyberNav;
