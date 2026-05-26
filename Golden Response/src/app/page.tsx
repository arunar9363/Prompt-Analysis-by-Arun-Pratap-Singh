"use client";

import React, { useState } from "react";
import { Hero } from "@/components/sections/Hero";
import { About } from "@/components/sections/About";
import { SkillsMatrix } from "@/components/sections/SkillsMatrix";
import { ProjectShowcase } from "@/components/sections/ProjectShowcase";
import { Timeline } from "@/components/sections/Timeline";
import { ContactModal } from "@/components/sections/ContactModal";

export default function Home() {
  const [isContactOpen, setIsContactOpen] = useState(false);

  return (
    <main className="relative min-h-screen bg-cyber-bg text-white overflow-x-hidden selection:bg-cyber-cyan selection:text-black">
      {/* Cinematic Hero entry */}
      <Hero onContactTrigger={() => setIsContactOpen(true)} />
      
      {/* Biological Identity section */}
      <About />
      
      {/* Skillset matrix */}
      <SkillsMatrix />
      
      {/* Showcase projects archive */}
      <ProjectShowcase />
      
      {/* Chronological timeline logs */}
      <Timeline />
      
      {/* Secured SMTP contact modal */}
      <ContactModal 
        isOpen={isContactOpen} 
        onClose={() => setIsContactOpen(false)} 
      />
    </main>
  );
}
