"use client";

import React from "react";
import { HTMLMotionProps, motion } from "framer-motion";
import { useReducedMotion } from "@/hooks/useReducedMotion";

interface CyberButtonProps extends HTMLMotionProps<"button"> {
  variant?: "cyan" | "pink" | "purple";
  children: React.ReactNode;
}

export const CyberButton: React.FC<CyberButtonProps> = ({ 
  variant = "cyan", 
  children, 
  className = "", 
  style,
  ...props 
}) => {
  const shouldReduce = useReducedMotion();

  const colorMap = {
    cyan: "border-cyber-cyan text-cyber-cyan hover:shadow-neon-cyan hover:bg-cyber-cyan/15 focus-visible:bg-cyber-cyan/20",
    pink: "border-cyber-pink text-cyber-pink hover:shadow-neon-pink hover:bg-cyber-pink/15 focus-visible:bg-cyber-pink/20",
    purple: "border-cyber-purple text-cyber-purple hover:shadow-neon-purple hover:bg-cyber-purple/15 focus-visible:bg-cyber-purple/20"
  };

  const baseColor = {
    cyan: "rgba(0, 240, 255, 0.05)",
    pink: "rgba(255, 0, 127, 0.05)",
    purple: "rgba(157, 78, 221, 0.05)"
  }[variant];

  const hoverColor = {
    cyan: "rgba(0, 240, 255, 0.15)",
    pink: "rgba(255, 0, 127, 0.15)",
    purple: "rgba(157, 78, 221, 0.15)"
  }[variant];

  // Disable motion scale on hover/tap if reduced motion is enabled
  const hoverProps = shouldReduce 
    ? {} 
    : {
        whileHover: { scale: 1.03, backgroundColor: hoverColor },
        whileTap: { scale: 0.97 }
      };

  return (
    <motion.button
      {...hoverProps}
      className={`relative px-6 py-3 font-mono text-sm uppercase tracking-widest border transition-all duration-300 ${colorMap[variant]} ${className} cursor-pointer focus:outline-none focus-visible:ring-2 focus-visible:ring-cyber-cyan`}
      style={{
        backgroundColor: baseColor,
        clipPath: "polygon(0 0, calc(100% - 10px) 0, 100% 10px, 100% 100%, 10px 100%, 0 calc(100% - 10px))",
        ...style
      }}
      {...props}
    >
      {/* Visual cybernetic accent lines */}
      <span className="absolute top-0 left-0 w-2 h-[1px] bg-white opacity-40 animate-glitch-blink" />
      <span className="absolute bottom-0 right-0 w-2 h-[1px] bg-white opacity-40 animate-glitch-blink" />
      <span className="absolute top-0 left-0 w-[1px] h-2 bg-white opacity-40 animate-glitch-blink" />
      <span className="absolute bottom-0 right-0 w-[1px] h-2 bg-white opacity-40 animate-glitch-blink" />
      
      {/* Decorative scanner line */}
      <span className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full hover:animate-[scanline_1s_ease]" />
      
      <span className="relative z-10 flex items-center justify-center gap-2">
        {children}
      </span>
    </motion.button>
  );
};
export default CyberButton;
