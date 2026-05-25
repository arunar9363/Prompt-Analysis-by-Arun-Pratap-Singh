"use client";

import React from "react";
import { motion } from "framer-motion";
import { useReducedMotion } from "@/hooks/useReducedMotion";
import { NeonCard } from "../ui/NeonCard";

export const About: React.FC = () => {
  const shouldReduce = useReducedMotion();

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.16, delayChildren: 0.1 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.7, ease: [0.16, 1, 0.3, 1] as const },
    },
  };

  return (
    <section 
      id="about" 
      className="py-28 bg-cyber-darker relative border-t border-cyber-purple/10 overflow-hidden"
    >
      {/* Background radial atmosphere */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(157,78,221,0.03),transparent_70%)] pointer-events-none" />

      <div className="max-w-6xl mx-auto px-6 relative z-10">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
        >
          {/* Section title */}
          <motion.h2 
            variants={itemVariants}
            className="text-3xl md:text-4xl font-bold font-mono tracking-wider text-white mb-16"
          >
            <span className="text-cyber-purple">&gt; </span>BIOLOGICAL_ID_METRICS
          </motion.h2>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
            {/* Hologram Card Bio Left */}
            <motion.div variants={itemVariants} className="lg:col-span-7">
              <NeonCard variant="purple" className="h-full hologram-effect" glowOnHover={true}>
                <div className="font-mono text-xs text-cyber-purple mb-4">[ SYS_IDENTITY_TELEMETRY ]</div>
                <h3 className="text-2xl font-bold text-white mb-6 uppercase tracking-wider">XAVIER_NEON // BIOMASS</h3>
                
                <div className="space-y-4 font-sans text-gray-300 leading-relaxed text-sm md:text-base">
                  <p>
                    I operate at the convergence of high-fidelity creative UI design and strictly typed, high-performance web engineering. Specializing in hardware-accelerated animations, pixel-perfect render pipelines, and robust system modularity.
                  </p>
                  <p>
                    For over six years, my engineering path has been guided by a core philosophy: <strong className="text-cyber-cyan">digital experiences should feel alive</strong>. I reject static, uninspired templates in favor of cinematic digital interfaces that respond organically to interaction.
                  </p>
                  <p>
                    My workflow involves Next.js architectures, React reactive layers, strict TypeScript configurations, and secure microservices backed by Node.js.
                  </p>
                </div>
              </NeonCard>
            </motion.div>

            {/* Philosophy Cards Right */}
            <motion.div variants={itemVariants} className="lg:col-span-5 flex flex-col justify-between gap-6">
              <NeonCard variant="cyan" glowOnHover={true} className="flex-1">
                <div className="font-mono text-xs text-cyber-cyan mb-2">// TECHNICAL_MIND</div>
                <h4 className="text-base md:text-lg font-bold text-white mb-3 tracking-wide">SYSTEMATIC ARCHITECTURE</h4>
                <p className="text-gray-400 text-xs md:text-sm leading-relaxed">
                  Structuring robust directories, strict separation of concerns, and reusable atomic design components that build scalable applications.
                </p>
              </NeonCard>

              <NeonCard variant="pink" glowOnHover={true} className="flex-1">
                <div className="font-mono text-xs text-cyber-pink mb-2">// CREATION_PHILOSOPHY</div>
                <h4 className="text-base md:text-lg font-bold text-white mb-3 tracking-wide">INTERACTION WITH PURPOSE</h4>
                <p className="text-gray-400 text-xs md:text-sm leading-relaxed">
                  Animations are visual communication links. Every hover glow and scroll parallax serves to guide user attention and render responsive feedback.
                </p>
              </NeonCard>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};
export default About;
