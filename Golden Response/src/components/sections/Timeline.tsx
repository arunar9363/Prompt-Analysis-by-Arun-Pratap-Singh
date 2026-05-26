"use client";

import React, { useRef } from "react";
import { motion, useScroll, useSpring } from "framer-motion";
import { useReducedMotion } from "@/hooks/useReducedMotion";
import { Award, Briefcase, GraduationCap, ShieldCheck } from "lucide-react";

interface TimelineEvent {
  year: string;
  role: string;
  institution: string;
  details: string;
  type: "experience" | "education" | "achievement" | "certification";
}

const history: TimelineEvent[] = [
  {
    year: "2024 - PRESENT",
    role: "Principal Frontend Architect",
    institution: "NEO-NETWORKS CORP",
    details: "Architecting micro-frontend frameworks using Next.js 15, reducing core bundle sizes by 32% and achieving high lighthouse scores across systems.",
    type: "experience",
  },
  {
    year: "2022 - 2024",
    role: "Core UI/UX Engineer",
    institution: "SYNTH_TECH LLC",
    details: "Created reactive WebAudio visualization interfaces and canvas graphs, reducing rendering cycle overhead by 22ms per frame.",
    type: "experience",
  },
  {
    year: "2019 - 2022",
    role: "B.S. in Computer Science",
    institution: "CYBERNETIC UNIVERSITY OF TECHNOLOGIES",
    details: "Focused on human-computer interaction, graph database structures, and high-performance browser rendering models.",
    type: "education",
  },
  {
    year: "2023",
    role: "Open Source Contributor of the Year",
    institution: "REACT FRAMEWORKS INITIATIVE",
    details: "Recognized for performance improvements submitted to community scroll storytelling wrappers and styling hooks.",
    type: "achievement",
  },
  {
    year: "2022",
    role: "Certified AWS Cloud Practitioner",
    institution: "AMAZON WEB SERVICES (AWS)",
    details: "Validated knowledge of cloud deployment strategies, security safeguards, and container environments.",
    type: "certification",
  },
];

export const Timeline: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const shouldReduce = useReducedMotion();

  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start center", "end center"],
  });

  const scaleY = useSpring(scrollYProgress, { stiffness: 100, damping: 30 });

  const getIcon = (type: string) => {
    switch (type) {
      case "experience":
        return <Briefcase className="w-4 h-4 text-cyber-cyan" />;
      case "education":
        return <GraduationCap className="w-4 h-4 text-cyber-purple" />;
      case "achievement":
        return <Award className="w-4 h-4 text-cyber-pink" />;
      case "certification":
        return <ShieldCheck className="w-4 h-4 text-cyber-blue" />;
      default:
        return <Briefcase className="w-4 h-4" />;
    }
  };

  const getBorderColor = (type: string) => {
    switch (type) {
      case "experience":
        return "border-cyber-cyan/30 hover:border-cyber-cyan";
      case "education":
        return "border-cyber-purple/30 hover:border-cyber-purple";
      case "achievement":
        return "border-cyber-pink/30 hover:border-cyber-pink";
      case "certification":
        return "border-cyber-blue/30 hover:border-cyber-blue";
      default:
        return "border-gray-800 hover:border-white/30";
    }
  };

  return (
    <section 
      ref={containerRef} 
      id="experience" 
      className="py-28 w-full bg-cyber-bg relative overflow-hidden"
    >
      <div className="max-w-4xl mx-auto px-6 relative">
        <h2 className="text-3xl font-bold text-white mb-20 font-mono tracking-wider">
          <span className="text-cyber-pink">&gt; </span>HISTORICAL_TIMELINE_LOGS
        </h2>

        {/* Dynamic Center Tracking Node Line */}
        <div className="absolute left-6 md:left-1/2 top-32 bottom-0 w-[2px] bg-gray-900 -translate-x-1/2">
          {!shouldReduce && (
            <motion.div
              style={{ scaleY, transformOrigin: "top" }}
              className="w-full h-full bg-gradient-to-b from-cyber-cyan via-cyber-pink to-transparent shadow-neon-pink"
            />
          )}
        </div>

        <div className="space-y-16">
          {history.map((item, index) => {
            const isEven = index % 2 === 0;
            return (
              <div 
                key={index} 
                className={`flex flex-col md:flex-row items-stretch w-full relative ${
                  isEven ? "md:flex-row-reverse" : ""
                }`}
              >
                {/* Node Pulsar */}
                <div className="absolute left-6 md:left-1/2 w-8 h-8 rounded-full bg-cyber-darker border border-gray-800 top-4 -translate-x-1/2 z-20 flex items-center justify-center">
                  {getIcon(item.type)}
                  {!shouldReduce && (
                    <div className="absolute inset-0 rounded-full border border-cyber-cyan animate-ping opacity-25" />
                  )}
                </div>

                {/* Event Card */}
                <div className={`w-full md:w-1/2 pl-14 md:pl-0 ${isEven ? "md:pl-10" : "md:pr-10 text-left md:text-right"}`}>
                  <motion.div
                    initial={shouldReduce ? { opacity: 1 } : { opacity: 0, x: isEven ? 40 : -40 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true, margin: "-100px" }}
                    transition={{ duration: 0.6, ease: "easeOut" }}
                    className={`p-6 bg-cyber-darker/60 border ${getBorderColor(
                      item.type
                    )} transition-all duration-300 rounded-none relative`}
                    style={{
                      clipPath: isEven
                        ? "polygon(0 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%)"
                        : "polygon(0 0, 100% 0, 100% 100%, 10px 100%, 0 calc(100% - 10px))",
                    }}
                  >
                    <span className="font-mono text-[10px] text-cyber-cyan block mb-2 tracking-widest">
                      // {item.year}
                    </span>
                    <h3 className="text-lg md:text-xl font-bold text-white mb-1 font-sans">{item.role}</h3>
                    <h4 className="text-cyber-pink font-mono text-xs md:text-sm mb-4 tracking-wider">{item.institution}</h4>
                    <p className="text-gray-400 text-xs md:text-sm leading-relaxed">{item.details}</p>
                  </motion.div>
                </div>
                <div className="hidden md:block w-1/2" />
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
export default Timeline;
