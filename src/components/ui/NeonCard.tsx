"use client";

import React from "react";
import { motion } from "framer-motion";
import { useReducedMotion } from "@/hooks/useReducedMotion";

interface NeonCardProps {
  children: React.ReactNode;
  variant?: "cyan" | "pink" | "purple";
  className?: string;
  glowOnHover?: boolean;
}

export const NeonCard: React.FC<NeonCardProps> = ({
  children,
  variant = "purple",
  className = "",
  glowOnHover = true,
}) => {
  const shouldReduce = useReducedMotion();

  const borderGlowColors = {
    cyan: "border-cyber-cyan/20 hover:border-cyber-cyan/70 focus-within:border-cyber-cyan/70 hover:shadow-neon-cyan focus-within:shadow-neon-cyan bg-cyber-cyan/[0.02]",
    pink: "border-cyber-pink/20 hover:border-cyber-pink/70 focus-within:border-cyber-pink/70 hover:shadow-neon-pink focus-within:shadow-neon-pink bg-cyber-pink/[0.02]",
    purple: "border-cyber-purple/20 hover:border-cyber-purple/70 focus-within:border-cyber-purple/70 hover:shadow-neon-purple focus-within:shadow-neon-purple bg-cyber-purple/[0.02]",
  };

  const hoverAnimation = shouldReduce || !glowOnHover
    ? {}
    : {
        whileHover: { 
          y: -6,
          transition: { duration: 0.25, ease: "easeOut" as const }
        }
      };

  return (
    <motion.div
      {...hoverAnimation}
      className={`relative border p-6 backdrop-blur-md transition-all duration-300 ${borderGlowColors[variant]} ${className}`}
      style={{
        clipPath: "polygon(0 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%)",
      }}
    >
      {/* Tech Grid Micro-Lines Background */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.015)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.015)_1px,transparent_1px)] bg-[size:16px_16px] pointer-events-none" />

      {/* Glowing Tech Dot Accents */}
      <span className="absolute top-2 left-2 w-1.5 h-1.5 rounded-full bg-cyber-cyan opacity-40 animate-pulse-slow" />
      <span className="absolute bottom-4 right-2 w-1.5 h-1.5 rounded-full bg-cyber-pink opacity-40" />

      {/* Cybernetic Corner Borders */}
      <div className="absolute top-0 left-0 w-4 h-[1px] bg-cyber-cyan opacity-35" />
      <div className="absolute top-0 left-0 w-[1px] h-4 bg-cyber-cyan opacity-35" />
      
      <div className="absolute bottom-[15px] right-0 w-[1px] h-4 bg-cyber-pink opacity-35" />
      <div className="absolute bottom-0 right-[15px] w-4 h-[1px] bg-cyber-pink opacity-35" />

      {/* Inside Content */}
      <div className="relative z-10 h-full flex flex-col justify-between">
        {children}
      </div>
    </motion.div>
  );
};
export default NeonCard;
