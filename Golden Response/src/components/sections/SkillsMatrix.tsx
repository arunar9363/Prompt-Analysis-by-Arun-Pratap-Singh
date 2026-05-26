"use client";

import React from "react";
import { motion } from "framer-motion";
import { useReducedMotion } from "@/hooks/useReducedMotion";
import { NeonCard } from "../ui/NeonCard";

interface SkillItem {
  name: string;
  level: number;
}

interface SkillCategory {
  title: string;
  variant: "cyan" | "pink" | "purple";
  skills: SkillItem[];
}

const matrixData: SkillCategory[] = [
  {
    title: "01 // FRONTEND_ENGINEERING",
    variant: "cyan",
    skills: [
      { name: "React.js / Next.js 14-15", level: 96 },
      { name: "TypeScript (Strict System)", level: 92 },
      { name: "Tailwind CSS & Web Shaders", level: 90 },
      { name: "Framer Motion Animations", level: 88 },
      { name: "Canvas / SVG Graphic Nodes", level: 78 },
    ],
  },
  {
    title: "02 // DISTRIBUTED_BACKEND",
    variant: "purple",
    skills: [
      { name: "Node.js (Express & NestJS)", level: 88 },
      { name: "MongoDB & Mongoose DB", level: 85 },
      { name: "PostgreSQL & Prisma Client", level: 82 },
      { name: "Restful API / GraphQL", level: 90 },
      { name: "SMTP Email / Web Sockets", level: 80 },
    ],
  },
  {
    title: "03 // DEVOPS_CLOUDS_AI",
    variant: "pink",
    skills: [
      { name: "Docker Container Configs", level: 75 },
      { name: "AWS Cloud Deployments", level: 70 },
      { name: "CI / CD Deployment Pipelines", level: 82 },
      { name: "LLM Agent Orchestrations", level: 78 },
      { name: "Vector Database Integrations", level: 74 },
    ],
  },
];

export const SkillsMatrix: React.FC = () => {
  const shouldReduce = useReducedMotion();

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.12 },
    },
  };
  const cardVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] as const },
    },
  };

  return (
    <section 
      id="skills" 
      className="py-28 w-full bg-cyber-bg relative border-t border-cyber-cyan/10 overflow-hidden"
    >
      {/* Background ambient lighting */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom,rgba(0,240,255,0.03),transparent_70%)] pointer-events-none" />

      <div className="max-w-6xl mx-auto px-6 relative z-10">
        {/* Title */}
        <h2 className="text-3xl md:text-4xl font-bold text-white mb-16 font-mono tracking-wider">
          <span className="text-cyber-cyan">&gt; </span>SKILLS_MATRIX_INDEX
        </h2>

        {/* Dashboard Categories Grid */}
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
        >
          {matrixData.map((category, catIdx) => (
            <motion.div key={catIdx} variants={cardVariants} className="h-full">
              <NeonCard 
                variant={category.variant} 
                className="h-full flex flex-col justify-between" 
                glowOnHover={true}
              >
                <div>
                  {/* Category Title */}
                  <h3 className="text-white font-mono text-sm tracking-widest mb-8 font-bold border-b border-white/5 pb-3">
                    {category.title}
                  </h3>

                  {/* Skills Progress list */}
                  <div className="space-y-6">
                    {category.skills.map((skill, skillIdx) => (
                      <div key={skillIdx} className="group">
                        <div className="flex justify-between font-mono text-[11px] text-gray-400 group-hover:text-white transition-colors duration-200 mb-2">
                          <span>{skill.name}</span>
                          <span className="text-cyber-cyan font-bold">{skill.level}%</span>
                        </div>
                        <div className="w-full h-1.5 bg-cyber-darker overflow-hidden relative">
                          <motion.div
                            initial={{ width: 0 }}
                            whileInView={{ width: `${skill.level}%` }}
                            viewport={{ once: true }}
                            transition={{ duration: 1.5, ease: "easeOut", delay: skillIdx * 0.04 }}
                            className={`h-full bg-gradient-to-r ${
                              category.variant === "cyan"
                                ? "from-cyber-cyan to-cyber-blue shadow-[0_0_8px_#00f0ff]"
                                : category.variant === "pink"
                                ? "from-cyber-pink to-cyber-purple shadow-[0_0_8px_#ff007f]"
                                : "from-cyber-purple to-cyber-cyan shadow-[0_0_8px_#9d4edd]"
                            }`}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Footer readouts */}
                <div className="mt-8 font-mono text-[9px] text-gray-500 tracking-widest flex justify-between">
                  <span>MODULE_READOUT_0{catIdx + 1}</span>
                  <span>INTEGRITY: NOMINAL</span>
                </div>
              </NeonCard>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};
export default SkillsMatrix;
