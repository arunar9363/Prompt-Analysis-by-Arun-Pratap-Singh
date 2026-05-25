"use client";

import React from "react";
import { motion, useScroll, useSpring } from "framer-motion";
import { useReducedMotion } from "@/hooks/useReducedMotion";

export const ScrollProgress: React.FC = () => {
  const { scrollYProgress } = useScroll();
  const shouldReduce = useReducedMotion();

  // Create a spring physics mapping for smooth, decoupled scroll-tracking
  const scaleX = useSpring(scrollYProgress, {
    stiffness: 120,
    damping: 25,
    restDelta: 0.001
  });

  if (shouldReduce) return null;

  return (
    <motion.div
      className="fixed top-0 left-0 right-0 h-[3px] bg-gradient-to-r from-cyber-cyan via-cyber-purple to-cyber-pink z-50 origin-left shadow-[0_0_8px_rgba(0,240,255,0.5)]"
      style={{ scaleX }}
      aria-hidden="true"
    />
  );
};
export default ScrollProgress;
