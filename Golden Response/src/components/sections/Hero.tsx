"use client";

import React from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { GlitchText } from "../ui/GlitchText";
import { CyberButton } from "../ui/CyberButton";
import { MatrixRain } from "../ui/MatrixRain";
import { useReducedMotion } from "@/hooks/useReducedMotion";
import { ChevronDown } from "lucide-react";

interface HeroProps {
  onContactTrigger: () => void;
}

export const Hero: React.FC<HeroProps> = ({ onContactTrigger }) => {
  const { scrollY } = useScroll();
  const shouldReduce = useReducedMotion();

  // Decoupled scrolling transforms for parallax depth
  const yBg = useTransform(scrollY, [0, 800], [0, 220]);
  const opacityContent = useTransform(scrollY, [0, 450], [1, 0]);
  const scaleContent = useTransform(scrollY, [0, 450], [1, 0.96]);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.18,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { y: 25, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] as const },
    },
  };

  return (
    <section 
      id="home"
      className="relative h-screen w-full overflow-hidden bg-cyber-bg flex items-center justify-center containment-layout"
    >
      {/* Matrix Code Layer */}
      <MatrixRain />

      {/* Cyber Grid Background (Parallax motion) */}
      <motion.div 
        style={shouldReduce ? {} : { y: yBg }}
        className="absolute inset-0 bg-[linear-gradient(to_right,rgba(0,240,255,0.04)_1px,transparent_1px),linear-gradient(to_bottom,rgba(0,240,255,0.04)_1px,transparent_1px)] bg-[size:4.5rem_4.5rem] [perspective:1000px] pointer-events-none"
      >
        <div className="absolute inset-0 bg-radial-gradient" />
      </motion.div>

      {/* Ambient glowing shapes */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full bg-cyber-cyan/5 blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full bg-cyber-pink/5 blur-3xl pointer-events-none" />

      {/* Hero content */}
      <motion.div 
        style={shouldReduce ? {} : { opacity: opacityContent, scale: scaleContent }}
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="relative z-10 max-w-5xl mx-auto px-6 text-center select-none"
      >
        <motion.div 
          variants={itemVariants}
          className="font-mono text-cyber-cyan text-xs md:text-sm tracking-[0.45em] uppercase mb-4"
        >
          [ CORE_SYSTEMS_INITIATED_NODE: 7719 ]
        </motion.div>
        
        <motion.h1 
          variants={itemVariants}
          className="text-4xl sm:text-6xl md:text-8xl font-black uppercase tracking-tighter mb-6 font-sans"
        >
          <GlitchText text="XAVIER_NEON" speed={2.5} />
        </motion.h1>

        <motion.p 
          variants={itemVariants}
          className="font-mono text-gray-400 text-sm sm:text-base md:text-lg max-w-2xl mx-auto mb-10 leading-relaxed"
        >
          Full-Stack Frontend Architect specializing in ultra-high performance reactive digital interfaces, WebGL/motion experiences, and secure serverless gateways.
        </motion.p>

        <motion.div 
          variants={itemVariants}
          className="flex flex-col sm:flex-row gap-5 justify-center items-center"
        >
          <CyberButton 
            variant="cyan" 
            onClick={() => document.getElementById("projects")?.scrollIntoView({ behavior: "smooth" })}
            aria-label="View developer projects archives"
          >
            ACCESS_ARCHIVE
          </CyberButton>
          
          <CyberButton 
            variant="pink" 
            onClick={onContactTrigger}
            aria-label="Initialize comms channel handshake"
          >
            INITIALIZE_HANDSHAKE
          </CyberButton>
        </motion.div>
      </motion.div>

      {/* Futuristic status readout indicators */}
      <div className="absolute bottom-10 left-10 font-mono text-[9px] text-cyber-cyan/35 hidden md:block">
        SYS_STATUS: ONLINE<br />
        IP_GATE: SECURED<br />
        CORE_LOAD: OPTIMAL // 60FPS_ACTIVE
      </div>

      <div className="absolute bottom-10 right-10 font-mono text-[9px] text-cyber-pink/35 hidden md:block text-right">
        SECTOR: F-12<br />
        protocol: CYBER_NET_STABLE
      </div>

      {/* Floating Animated Scroll Down Node */}
      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex flex-col items-center gap-1 opacity-50">
        <span className="font-mono text-[9px] text-gray-500 tracking-widest">SCROLL_DOWN</span>
        <motion.div
          animate={shouldReduce ? {} : { y: [0, 6, 0] }}
          transition={{ repeat: Infinity, duration: 1.5, ease: "easeInOut" }}
        >
          <ChevronDown className="w-4 h-4 text-cyber-cyan" />
        </motion.div>
      </div>
    </section>
  );
};
export default Hero;
