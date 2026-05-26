"use client";

import React from "react";
import { motion } from "framer-motion";
import { useReducedMotion } from "@/hooks/useReducedMotion";

interface GlitchTextProps {
  text: string;
  className?: string;
  speed?: number;
}

export const GlitchText: React.FC<GlitchTextProps> = ({ 
  text, 
  className = "", 
  speed = 2 
}) => {
  const shouldReduce = useReducedMotion();

  if (shouldReduce) {
    return <span className={`text-white font-sans ${className}`}>{text}</span>;
  }

  return (
    <div className={`relative inline-block font-sans select-none tracking-wide ${className}`}>
      {/* Red Glitch Layer (Top Clip) */}
      <motion.span
        animate={{ 
          textShadow: [
            "0.05em 0 0 rgba(255,0,127,0.75)",
            "-0.025em -0.05em 0 rgba(0,240,255,0.75)",
            "0.025em 0.05em 0 rgba(157,78,221,0.75)",
            "0.05em 0 0 rgba(255,0,127,0.75)"
          ],
          x: [2, -2, 1, -1, 0, 2],
          y: [-1, 2, -2, 1, 0, -1]
        }}
        transition={{ 
          repeat: Infinity, 
          duration: speed, 
          ease: "linear" 
        }}
        className="absolute top-0 left-0 w-full h-full opacity-90 mix-blend-screen animate-glitch-blink text-cyber-pink"
        style={{ clipPath: "polygon(0 0, 100% 0, 100% 33%, 0 33%)" }}
      >
        {text}
      </motion.span>
      
      {/* Core Base Text */}
      <span className="text-white drop-shadow-[0_0_8px_rgba(255,255,255,0.3)] select-text">
        {text}
      </span>

      {/* Cyan Glitch Layer (Bottom Clip) */}
      <motion.span
        animate={{ 
          textShadow: [
            "-0.05em -0.025em 0 rgba(255,0,127,0.75)",
            "0.05em 0.025em 0 rgba(0,240,255,0.75)",
            "-0.025em -0.05em 0 rgba(157,78,221,0.75)",
            "-0.05em -0.025em 0 rgba(255,0,127,0.75)"
          ],
          x: [-2, 2, -1, 1, 0, -2],
          y: [1, -2, 2, -1, 0, 1]
        }}
        transition={{ 
          repeat: Infinity, 
          duration: speed * 0.75, 
          ease: "linear" 
        }}
        className="absolute top-0 left-0 w-full h-full opacity-90 mix-blend-screen text-cyber-cyan"
        style={{ clipPath: "polygon(0 67%, 100% 67%, 100% 100%, 0 100%)" }}
      >
        {text}
      </motion.span>
    </div>
  );
};
