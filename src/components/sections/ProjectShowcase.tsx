"use client";

import React from "react";
import { motion } from "framer-motion";
import { ExternalLink, Monitor } from "lucide-react";
import { useReducedMotion } from "@/hooks/useReducedMotion";
import { NeonCard } from "../ui/NeonCard";

interface ProjectItem {
  title: string;
  description: string;
  tech: string[];
  github: string;
  demo: string;
  featured: boolean;
  color: "cyan" | "pink" | "purple";
  tag: string;
}

const projectsData: ProjectItem[] = [
  {
    title: "Project AEGIS_GATE",
    description: "High-throughput serverless API firewall featuring active IP throttling, malicious header filtering, and low-latency database queries.",
    tech: ["Next.js App Router", "TypeScript", "Redis", "Tailwind CSS"],
    github: "https://github.com",
    demo: "https://example.com",
    featured: true,
    color: "cyan",
    tag: "[ SECTOR_FIREWALL ]",
  },
  {
    title: "Project SYNTH_CORE",
    description: "A canvas-driven WebAudio synthesizer featuring real-time node routing, visual wave oscillators, and latency-free keyboard events.",
    tech: ["React.js", "Web Audio API", "Framer Motion", "Vite"],
    github: "https://github.com",
    demo: "https://example.com",
    featured: true,
    color: "pink",
    tag: "[ AUDIO_MODULE ]",
  },
  {
    title: "Project NEURAL_LOG",
    description: "Structured JSON logging service with built-in email alerts, slack webhooks, and retry pipelines for serverless runtimes.",
    tech: ["Node.js", "Express", "Nodemailer", "PostgreSQL"],
    github: "https://github.com",
    demo: "https://example.com",
    featured: false,
    color: "purple",
    tag: "[ LOG_TELEMETRY ]",
  },
];

// Custom inline SVG GitHub Icon to bypass lucide-react brand icon versioning variations
const GithubIcon = (props: React.SVGProps<SVGSVGElement>) => (
  <svg
    viewBox="0 0 24 24"
    width="16"
    height="16"
    stroke="currentColor"
    strokeWidth="2"
    fill="none"
    strokeLinecap="round"
    strokeLinejoin="round"
    {...props}
  >
    <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
    <path d="M9 18c-4.51 2-5-2-7-2" />
  </svg>
);

export const ProjectShowcase: React.FC = () => {
  const shouldReduce = useReducedMotion();

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.15 },
    },
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 35 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] as const },
    },
  };

  return (
    <section 
      id="projects" 
      className="py-28 bg-cyber-darker relative border-t border-cyber-purple/10 overflow-hidden"
    >
      <div className="absolute top-0 right-0 w-96 h-96 rounded-full bg-cyber-pink/5 blur-3xl pointer-events-none" />

      <div className="max-w-6xl mx-auto px-6 relative z-10">
        {/* Title */}
        <h2 className="text-3xl md:text-4xl font-bold text-white mb-16 font-mono tracking-wider">
          <span className="text-cyber-pink">&gt; </span>PROJECTS_SHOWCASE_ARCHIVE
        </h2>

        {/* Projects Grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
        >
          {projectsData.map((project, idx) => (
            <motion.div key={idx} variants={cardVariants} className="h-full">
              <NeonCard 
                variant={project.color} 
                className="h-full flex flex-col justify-between group" 
                glowOnHover={true}
              >
                <div>
                  {/* Visual Layout Preview Box */}
                  <div className="relative w-full h-36 mb-6 overflow-hidden bg-cyber-darker/60 border border-white/5 flex items-center justify-center">
                    {/* Color overlay */}
                    <div className={`absolute inset-0 bg-gradient-to-br opacity-15 transition-opacity duration-300 group-hover:opacity-25 ${
                      project.color === "cyan" ? "from-cyber-cyan via-cyber-blue to-transparent" :
                      project.color === "pink" ? "from-cyber-pink via-cyber-purple to-transparent" :
                      "from-cyber-purple via-cyber-cyan to-transparent"
                    }`} />
                    
                    {/* Matrix grid inside preview */}
                    <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.01)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.01)_1px,transparent_1px)] bg-[size:10px_10px]" />
                    
                    {/* Monitored SVG Graphic */}
                    <Monitor className={`w-8 h-8 opacity-45 transition-all duration-300 group-hover:opacity-80 group-hover:scale-110 ${
                      project.color === "cyan" ? "text-cyber-cyan" :
                      project.color === "pink" ? "text-cyber-pink" :
                      "text-cyber-purple"
                    }`} />

                    <span className="absolute top-2 left-2 font-mono text-[9px] text-gray-500 tracking-wider">
                      {project.tag}
                    </span>
                    
                    {project.featured && (
                      <span className="absolute top-2 right-2 font-mono text-[8px] bg-cyber-pink/20 text-cyber-pink border border-cyber-pink/35 px-1.5 py-0.5 tracking-widest uppercase">
                        FEATURED_NODE
                      </span>
                    )}
                  </div>

                  <h3 className="text-xl font-bold text-white mb-3 font-mono tracking-wide">
                    {project.title}
                  </h3>

                  <p className="text-gray-400 text-xs md:text-sm leading-relaxed mb-6">
                    {project.description}
                  </p>
                </div>

                <div>
                  {/* Tech stack items */}
                  <div className="flex flex-wrap gap-2 mb-6">
                    {project.tech.map((t, tIdx) => (
                      <span 
                        key={tIdx} 
                        className="font-mono text-[9px] px-2 py-0.5 bg-cyber-darker border border-white/10 text-gray-400"
                      >
                        {t}
                      </span>
                    ))}
                  </div>

                  {/* Actions links */}
                  <div className="flex items-center justify-between border-t border-white/5 pt-4">
                    <a 
                      href={project.github} 
                      target="_blank" 
                      rel="noopener noreferrer" 
                      className="flex items-center gap-1.5 font-mono text-xs text-gray-400 hover:text-cyber-cyan transition-colors"
                      aria-label={`View GitHub repository for ${project.title}`}
                    >
                      <GithubIcon className="w-4 h-4 text-gray-400 group-hover:text-cyber-cyan transition-colors" />
                      <span>SOURCE</span>
                    </a>
                    
                    <a 
                      href={project.demo} 
                      target="_blank" 
                      rel="noopener noreferrer" 
                      className="flex items-center gap-1.5 font-mono text-xs text-cyber-pink hover:text-white transition-colors"
                      aria-label={`Open live demonstration for ${project.title}`}
                    >
                      <ExternalLink className="w-4 h-4" />
                      <span>LIVE_DEMO</span>
                    </a>
                  </div>
                </div>
              </NeonCard>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};
export default ProjectShowcase;
