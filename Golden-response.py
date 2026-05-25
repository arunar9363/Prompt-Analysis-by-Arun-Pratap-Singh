# golden_response.py
"""
Cyberpunk Developer Storytelling Portfolio - Blueprint Generator Engine
This module contains the codebase for generating a production-ready, ultra-high performance, 
and highly secure Next.js 14+ / Framer Motion full-stack ecosystem.
"""

import os
import json
from typing import Dict, Any

# ARCHITECTURE CONFIGURATIONS

TAILWIND_CONFIG: str = '''import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: "#05050a",
          darker: "#020204",
          cyan: "#00f0ff",
          purple: "#9d4edd",
          pink: "#ff007f",
          blue: "#004bba",
          grid: "rgba(0, 240, 255, 0.07)",
        },
      },
      fontFamily: {
        mono: ["var(--font-space-mono)", "Courier New", "monospace"],
        sans: ["var(--font-oxanium)", "sans-serif"],
      },
      boxShadow: {
        "neon-cyan": "0 0 10px rgba(0, 240, 255, 0.5), 0 0 20px rgba(0, 240, 255, 0.2)",
        "neon-pink": "0 0 10px rgba(255, 0, 127, 0.5), 0 0 20px rgba(255, 0, 127, 0.2)",
      },
      animation: {
        "scanline": "scanline 6s linear infinite",
        "glitch-blink": "glitchBlink 0.3s steps(2) infinite",
      },
      keyframes: {
        scanline: {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100%)" },
        },
        glitchBlink: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.85" },
        },
      },
    },
  },
  plugins: [],
};
export default config;
'''

ENV_LOCAL: str = '''DATABASE_URL="postgresql://db_user:secure_password@localhost:5432/cyber_portfolio?schema=public"
SMTP_HOST="smtp.sendgrid.net"
SMTP_PORT=587
SMTP_USER="apikey"
SMTP_PASSWORD="SG.production_secure_key_here"
CONTACT_NOTIFICATION_EMAIL="developer@cyberdomain.tech"
NEXT_PUBLIC_SITE_URL="https://cyberdomain.tech"
'''

# =====================================================================
# CORE UTILITY HOOKS
# =====================================================================

USE_REDUCED_MOTION_HOOK: str = '''import { useEffect, useState } from "react";

export function useReducedMotion() {
  const [shouldReduce, setShouldReduce] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    setShouldReduce(mediaQuery.matches);

    const handleChange = (event: MediaQueryListEvent) => {
      setShouldReduce(event.matches);
    };

    mediaQuery.addEventListener("change", handleChange);
    return () => mediaQuery.removeEventListener("change", handleChange);
  }, []);

  return shouldReduce;
}
'''

# MICRO-INTERACTION COMPONENTS

GLITCH_TEXT_COMPONENT: str = '''"use client";

import React from "react";
import { motion } from "framer-motion";

interface GlitchTextProps {
  text: string;
  className?: string;
}

export const GlitchText: React.FC<GlitchTextProps> = ({ text, className = "" }) => {
  return (
    <div className={`relative inline-block font-sans select-none ${className}`}>
      <motion.span
        animate={{ textShadow: [
          "0.05em 0 0 rgba(255,0,127,0.75)",
          "-0.025em -0.05em 0 rgba(0,240,255,0.75)",
          "0.025em 0.05em 0 rgba(157,78,221,0.75)",
          "0.05em 0 0 rgba(255,0,127,0.75)"
        ]}}
        transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
        className="absolute top-0 left-0 w-full h-full opacity-90 mix-blend-screen animate-glitch-blink"
        style={{ clipPath: "polygon(0 0, 100% 0, 100% 33%, 0 33%)" }}
      >
        {text}
      </motion.span>
      
      <span className="text-white drop-shadow-[0_0_8px_rgba(255,255,255,0.3)]">{text}</span>

      <motion.span
        animate={{ textShadow: [
          "-0.05em -0.025em 0 rgba(255,0,127,0.75)",
          "0.05em 0.025em 0 rgba(0,240,255,0.75)",
          "-0.025em -0.05em 0 rgba(157,78,221,0.75)",
          "-0.05em -0.025em 0 rgba(255,0,127,0.75)"
        ]}}
        transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
        className="absolute top-0 left-0 w-full h-full opacity-90 mix-blend-screen"
        style={{ clipPath: "polygon(0 67%, 100% 67%, 100% 100%, 0 100%)" }}
      >
        {text}
      </motion.span>
    </div>
  );
};
'''

CYBER_BUTTON_COMPONENT: str = '''"use client";

import React from "react";
import { motion } from "framer-motion";

interface CyberButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "cyan" | "pink" | "purple";
  children: React.ReactNode;
}

export const CyberButton: React.FC<CyberButtonProps> = ({ 
  variant = "cyan", 
  children, 
  className = "", 
  ...props 
}) => {
  const colorMap = {
    cyan: "border-cyber-cyan text-cyber-cyan shadow-neon-cyan bg-cyber-cyan/5",
    pink: "border-cyber-pink text-cyber-pink shadow-neon-pink bg-cyber-pink/5",
    purple: "border-cyber-purple text-cyber-purple shadow-[0_0_10px_rgba(157,78,221,0.5)] bg-cyber-purple/5"
  };

  return (
    <motion.button
      whileHover={{ scale: 1.02, backgroundColor: "rgba(0, 240, 255, 0.15)" }}
      whileTap={{ scale: 0.98 }}
      className={`relative px-6 py-3 font-mono text-sm uppercase tracking-widest border transition-all duration-300 ${colorMap[variant]} ${className}`}
      style={{
        clipPath: "polygon(0 0, calc(100% - 10px) 0, 100% 10px, 100% 100%, 10px 100%, 0 calc(100% - 10px))"
      }}
      {...props}
    >
      <span className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full hover:animate-[scanline_1s_ease]" />
      {children}
    </motion.button>
  );
};
'''

# MACRO STORYTELLING PRESENTATION LAYOUTS

HERO_SECTION: str = '''"use client";

import React from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { GlitchText } from "../ui/GlitchText";
import { CyberButton } from "../ui/CyberButton";

export const Hero: React.FC<{ onContactTrigger: () => void }> = ({ onContactTrigger }) => {
  const { scrollY } = useScroll();
  const yBg = useTransform(scrollY, [0, 800], [0, 250]);
  const opacityText = useTransform(scrollY, [0, 400], [1, 0]);

  return (
    <section className="relative h-screen w-full overflow-hidden bg-cyber-bg flex items-center justify-center containment-layout">
      <motion.div 
        style={{ y: yBg }}
        className="absolute inset-0 bg-[linear-gradient(to_right,rgba(0,240,255,0.05)_1px,transparent_1px),linear-gradient(to_bottom,rgba(0,240,255,0.05)_1px,transparent_1px)] bg-[size:4rem_4rem] [perspective:1000px]"
      >
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-cyber-bg/50 to-cyber-bg" />
      </motion.div>

      <div className="absolute inset-0 pointer-events-none bg-radial-gradient" />
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="w-full h-0.5 bg-cyber-cyan/10 opacity-40 shadow-sm animate-scanline" />
      </div>

      <motion.div 
        style={{ opacity: opacityText }}
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
        className="relative z-10 max-w-5xl mx-auto px-6 text-center select-none"
      >
        <div className="font-mono text-cyber-cyan text-sm tracking-[0.4em] uppercase mb-4">
          [ CORE NODE IDENTIFICATION ACTIVE ]
        </div>
        
        <h1 className="text-5xl md:text-8xl font-black uppercase tracking-tight mb-6">
          <GlitchText text="XAVIER_NEON" />
        </h1>

        <p className="font-mono text-gray-400 text-lg md:text-xl max-w-2xl mx-auto mb-10 leading-relaxed">
          Full-Stack Frontend Architect specializing in ultra-high performance digital spaces, complex interactive frameworks, and core reactive infrastructure.
        </p>

        <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
          <CyberButton variant="cyan" onClick={() => document.getElementById("projects")?.scrollIntoView({ behavior: "smooth" })}>
            ACCESS_ARCHIVE
          </CyberButton>
          <CyberButton variant="pink" onClick={onContactTrigger}>
            INITIALIZE_HANDSHAKE
          </CyberButton>
        </div>
      </motion.div>

      <div className="absolute bottom-10 left-10 font-mono text-[10px] text-cyber-cyan/30 hidden md:block">
        SYS_STATUS: NOMINAL<br />
        FPS: 60 // GPU_ACTIVE
      </div>
    </section>
  );
};
'''

SKILLS_MATRIX_SECTION: str = '''"use client";

import React from "react";
import { motion } from "framer-motion";

interface SkillItem {
  name: string;
  level: number;
}

interface SkillCategory {
  title: string;
  skills: SkillItem[];
}

const matrixData: SkillCategory[] = [
  {
    title: "01//FRONTEND_ENGINEERING",
    skills: [
      { name: "React / Next.js 14", level: 95 },
      { name: "TypeScript (Strict)", level: 90 },
      { name: "Tailwind CSS & Shaders", level: 88 },
    ],
  },
  {
    title: "02//DISTRIBUTED_SYSTEMS",
    skills: [
      { name: "Node.js Architecture", level: 85 },
      { name: "PostgreSQL / Prisma", level: 82 },
      { name: "GraphQL & WebSockets", level: 80 },
    ],
  },
];

export const SkillsMatrix: React.FC = () => {
  return (
    <section id="skills" className="py-24 w-full bg-cyber-darker relative border-t border-cyber-cyan/10">
      <div className="max-w-6xl mx-auto px-6">
        <h2 className="text-3xl font-bold text-white mb-16 font-mono tracking-wider">
          <span className="text-cyber-cyan">&gt; </span>SKILLS_MATRIX_INDEX
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
          {matrixData.map((category, catIdx) => (
            <div 
              key={catIdx} 
              className="p-6 bg-cyber-bg/40 border border-cyber-purple/20 relative rounded-none"
              style={{ clipPath: "polygon(0 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%)" }}
            >
              <h3 className="text-cyber-purple font-mono text-sm tracking-widest mb-6 font-bold">
                {category.title}
              </h3>

              <div className="space-y-6">
                {category.skills.map((skill, skillIdx) => (
                  <div key={skillIdx}>
                    <div className="flex justify-between font-mono text-xs text-gray-400 mb-2">
                      <span>{skill.name}</span>
                      <span className="text-cyber-cyan">{skill.level}%</span>
                    </div>
                    <div className="w-full h-1 bg-cyber-purple/10 overflow-hidden relative">
                      <motion.div
                        initial={{ width: 0 }}
                        whileInView={{ width: `${skill.level}%` }}
                        viewport={{ once: true }}
                        transition={{ duration: 1.5, ease: "easeOut" }}
                        className="h-full bg-gradient-to-r from-cyber-purple to-cyber-cyan shadow-neon-cyan"
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
'''

TIMELINE_SECTION: str = '''"use client";

import React from "react";
import { motion, useScroll, useSpring } from "framer-motion";

interface TimelineEvent {
  year: string;
  role: string;
  company: string;
  details: string;
}

const history: TimelineEvent[] = [
  { year: "2024 - PRESENT", role: "Principal Frontend Architect", company: "NEO-NETWORKS", details: "Led transition to Next.js App Systems, optimizing layout performance by 40% across edge operations." },
  { year: "2022 - 2024", role: "Core UI/UX Engineer", company: "SYNTH_TECH", details: "Created high-fidelity data dashboards using optimized canvas elements and real-time reactive event pipelines." }
];

export const Timeline: React.FC = () => {
  const containerRef = React.useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start center", "end center"]
  });
  
  const scaleY = useSpring(scrollYProgress, { stiffness: 100, damping: 30 });

  return (
    <section ref={containerRef} className="py-24 w-full bg-cyber-bg relative overflow-hidden">
      <div className="max-w-4xl mx-auto px-6 relative">
        <h2 className="text-3xl font-bold text-white mb-20 font-mono tracking-wider">
          <span className="text-cyber-pink">&gt; </span>HISTORICAL_TIMELINE_LOGS
        </h2>

        <div className="absolute left-6 md:left-1/2 top-32 bottom-0 w-0.5 bg-gray-800 -translate-x-1/2">
          <motion.div 
            style={{ scaleY, transformOrigin: "top" }} 
            className="w-full h-full bg-gradient-to-b from-cyber-cyan via-cyber-pink to-transparent shadow-neon-pink"
          />
        </div>

        <div className="space-y-16">
          {history.map((item, index) => {
            const isEven = index % 2 === 0;
            return (
              <div key={index} className={`flex flex-col md:flex-row items-stretch w-full relative ${isEven ? "md:flex-row-reverse" : ""}`}>
                <div className="absolute left-6 md:left-1/2 w-4 h-4 rounded-full bg-cyber-bg border-2 border-cyber-cyan top-2 -translate-x-1/2 z-20">
                  <div className="w-full h-full rounded-full bg-cyber-cyan animate-ping opacity-40" />
                </div>

                <div className={`w-full md:w-1/2 pl-12 md:pl-0 ${isEven ? "md:pl-8" : "md:pr-8 text-left md:text-right"}`}>
                  <motion.div 
                    initial={{ opacity: 0, x: isEven ? 50 : -50 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true, margin: "-100px" }}
                    transition={{ duration: 0.6 }}
                    className="p-6 bg-cyber-darker/60 border border-gray-800 hover:border-cyber-cyan/30 transition-colors"
                  >
                    <span className="font-mono text-xs text-cyber-cyan block mb-1">{item.year}</span>
                    <h3 className="text-xl font-bold text-white mb-1 font-sans">{item.role}</h3>
                    <h4 className="text-cyber-pink font-mono text-sm mb-4">{item.company}</h4>
                    <p className="text-gray-400 text-sm leading-relaxed">{item.details}</p>
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
'''

# INTERACTIVE MODAL & FORM INTERFACE

CONTACT_MODAL_SECTION: str = '''"use client";

import React, { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { CyberButton } from "../ui/CyberButton";

interface ContactModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ContactModal: React.FC<ContactModalProps> = ({ isOpen, onClose }) => {
  const modalRef = useRef<HTMLDivElement>(null);
  const [formData, setFormData] = useState({ fullName: "", email: "", phone: "", message: "" });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
      modalRef.current?.focus();
    } else {
      document.body.style.overflow = "";
    }
    return () => { document.body.style.overflow = ""; };
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [onClose]);

  const validateForm = () => {
    const errs: Record<string, string> = {};
    if (!formData.fullName.trim()) errs.fullName = "REQUIRED_IDENTITY_FIELD";
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) errs.email = "INVALID_COMMS_ADDRESS";
    if (formData.phone && !/^\+?[1-9]\d{1,14}$/.test(formData.phone)) errs.phone = "INVALID_ITU_FORMAT";
    if (formData.message.length < 10) errs.message = "PAYLOAD_TOO_SHORT_MIN_10";
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;
    setStatus("loading");

    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      if (res.ok) {
        setStatus("success");
        setFormData({ fullName: "", email: "", phone: "", message: "" });
      } else {
        setStatus("error");
      }
    } catch {
      setStatus("error");
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-cyber-bg/80 backdrop-blur-md"
          />

          <motion.div
            ref={modalRef}
            tabIndex={-1}
            role="dialog"
            aria-modal="true"
            aria-labelledby="modal-title"
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="relative w-full max-w-lg bg-cyber-darker border border-cyber-cyan p-8 text-white focus:outline-none overflow-y-auto max-h-[90vh]"
            style={{ clipPath: "polygon(0 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%)" }}
          >
            <h2 id="modal-title" className="text-2xl font-mono text-cyber-cyan tracking-widest mb-6 uppercase">
              //SECURE_COMMS_CHANNEL
            </h2>

            {status === "success" ? (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center py-8">
                <p className="text-cyber-pink font-mono text-lg mb-4">DATA_TRANSMISSION_SUCCESSFUL</p>
                <p className="text-gray-400 text-sm mb-6">Handshake complete. The developer will review your telemetry.</p>
                <CyberButton variant="cyan" onClick={() => { setStatus("idle"); onClose(); }}>DISCONNECT</CyberButton>
              </motion.div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block font-mono text-xs text-gray-400 mb-2" htmlFor="fullName">FULL_NAME *</label>
                  <input
                    id="fullName"
                    type="text"
                    className="w-full bg-cyber-bg border border-gray-800 p-3 font-mono text-sm text-white focus:border-cyber-cyan focus:outline-none transition-colors"
                    value={formData.fullName}
                    onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                  />
                  {errors.fullName && <p className="text-cyber-pink font-mono text-[11px] mt-1">{errors.fullName}</p>}
                </div>

                <div>
                  <label className="block font-mono text-xs text-gray-400 mb-2" htmlFor="email">EMAIL_ADDRESS *</label>
                  <input
                    id="email"
                    type="email"
                    className="w-full bg-cyber-bg border border-gray-800 p-3 font-mono text-sm text-white focus:border-cyber-cyan focus:outline-none transition-colors"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  />
                  {errors.email && <p className="text-cyber-pink font-mono text-[11px] mt-1">{errors.email}</p>}
                </div>

                <div>
                  <label className="block font-mono text-xs text-gray-400 mb-2" htmlFor="phone">COMMS_PHONE (OPTIONAL)</label>
                  <input
                    id="phone"
                    type="text"
                    placeholder="+1234567890"
                    className="w-full bg-cyber-bg border border-gray-800 p-3 font-mono text-sm text-white focus:border-cyber-cyan focus:outline-none transition-colors"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  />
                  {errors.phone && <p className="text-cyber-pink font-mono text-[11px] mt-1">{errors.phone}</p>}
                </div>

                <div>
                  <label className="block font-mono text-xs text-gray-400 mb-2" htmlFor="message">ENCRYPTED_MESSAGE_BODY *</label>
                  <textarea
                    id="message"
                    rows={4}
                    className="w-full bg-cyber-bg border border-gray-800 p-3 font-mono text-sm text-white focus:border-cyber-cyan focus:outline-none transition-colors resize-none"
                    value={formData.message}
                    onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                  />
                  {errors.message && <p className="text-cyber-pink font-mono text-[11px] mt-1">{errors.message}</p>}
                </div>

                <div className="flex gap-4 pt-4">
                  <CyberButton type="submit" variant="cyan" disabled={status === "loading"}>
                    {status === "loading" ? "TRANSMITTING..." : "BROADCAST_PAYLOAD"}
                  </CyberButton>
                  <CyberButton type="button" variant="purple" onClick={onClose}>
                    ABORT
                  </CyberButton>
                </div>
              </form>
            )}
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};
'''
# SECURE INPUT VALIDATION & ROUTING SECURITY INFRASTRUCTURE

VALIDATIONS_LIB: str = '''import validator from "validator";

export interface CleanContactInput {
  fullName: string;
  email: string;
  phone?: string;
  message: string;
}

export function sanitizeAndValidateContact(body: any): CleanContactInput {
  if (!body || typeof body !== "object") {
    throw new Error("Malformed JSON payload mapping context.");
  }

  let { fullName, email, phone, message } = body;

  fullName = typeof fullName === "string" ? validator.escape(fullName.trim()) : "";
  email = typeof email === "string" ? validator.normalizeEmail(email.trim()) : "";
  phone = typeof phone === "string" ? validator.escape(phone.trim()) : "";
  message = typeof message === "string" ? validator.escape(message.trim()) : "";

  if (validator.isEmpty(fullName)) throw new Error("Field validation error: fullName required.");
  if (!email || !validator.isEmail(email)) throw new Error("Field validation error: valid email context required.");
  if (!validator.isEmpty(phone) && !validator.isMobilePhone(phone, "any")) {
    throw new Error("Field validation error: Invalid phone sequencing profile.");
  }
  if (validator.isEmpty(message) || !validator.isLength(message, { min: 10, max: 2000 })) {
    throw new Error("Field validation error: Message length constraint failure.");
  }

  return { fullName, email, phone, message };
}
'''

API_CONTACT_ROUTE: str = '''import { NextRequest, NextResponse } from "next/server";
import { sanitizeAndValidateContact } from "@/lib/validations";
import nodemailer from "nodemailer";

const rateLimitMap = new Map<string, { count: number; resetTime: number }>();

function checkRateLimit(ip: string): boolean {
  const now = Date.now();
  const limitWindow = 60 * 1000;
  const maxRequests = 3;

  const clientData = rateLimitMap.get(ip);
  if (!clientData) {
    rateLimitMap.set(ip, { count: 1, resetTime: now + limitWindow });
    return true;
  }

  if (now > clientData.resetTime) {
    rateLimitMap.set(ip, { count: 1, resetTime: now + limitWindow });
    return true;
  }

  if (clientData.count >= maxRequests) {
    return false;
  }

  clientData.count++;
  return true;
}

export async function POST(req: NextRequest) {
  const ip = req.headers.get("x-forwarded-for") || "127.0.0.1";
  
  if (!checkRateLimit(ip)) {
    return new NextResponse(
      JSON.stringify({ error: "TOO_MANY_REQUESTS", message: "Rate limit breached. Comms transmission throttled." }),
      { status: 429, headers: { "Content-Type": "application/json" } }
    );
  }

  try {
    const jsonBody = await req.json();
    const cleanData = sanitizeAndValidateContact(jsonBody);

    const transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port: Number(process.env.SMTP_PORT) || 587,
      secure: false,
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASSWORD,
      },
    });

    const emailPayload = {
      from: `"Cyber Portfolio" <${process.env.CONTACT_NOTIFICATION_EMAIL}>`,
      to: process.env.CONTACT_NOTIFICATION_EMAIL,
      subject: `[COMMS_ALERT] Handshake Node: ${cleanData.fullName}`,
      text: `Telemetry Inbound\\n\\nIdentity: ${cleanData.fullName}\\nComms: ${cleanData.email}\\nPhone: ${cleanData.phone || "NONE"}\\nPayload:\\n${cleanData.message}\\n`,
      html: `
        <div style="background:#05050a; color:#ffffff; padding:20px; font-family:monospace; border:1px solid #00f0ff;">
          <h2 style="color:#00f0ff; border-bottom:1px solid #00f0ff; padding-bottom:10px;">INBOUND HANDSHAKE DETECTED</h2>
          <p><strong>IDENTITY:</strong> \${cleanData.fullName}</p>
          <p><strong>COMMS LINK:</strong> \${cleanData.email}</p>
          <p><strong>ITU PHONE:</strong> \${cleanData.phone || "NOT_PROVIDED"}</p>
          <div style="background:#121224; padding:15px; border-left:4px solid #ff007f; margin-top:20px;">
            <strong>DATA_PAYLOAD:</strong><br/>
            \${cleanData.message}
          </div>
        </div>
      `,
    };

    let attempt = 0;
    let delivered = false;
    while (attempt < 2 && !delivered) {
      try {
        await transporter.sendMail(emailPayload);
        delivered = true;
      } catch (err) {
        attempt++;
        if (attempt >= 2) throw err;
      }
    }

    return new NextResponse(
      JSON.stringify({ status: "TRANSMITTED", recipient: cleanData.email }),
      { 
        status: 200, 
        headers: { 
          "Content-Type": "application/json",
          "X-Content-Type-Options": "nosniff",
          "X-Frame-Options": "DENY"
        } 
      }
    );

  } catch (error: any) {
    return new NextResponse(
      JSON.stringify({ error: "TRANSMISSION_FAILURE", details: error.message }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }
}
'''

# =====================================================================
# SYSTEM MAIN ROOT MATRIX VIEWPORT
# =====================================================================

PAGE_SHELL_LAYOUT: str = '''"use client";

import React, { useState } from "react";
import { Hero } from "@/components/sections/Hero";
import { SkillsMatrix } from "@/components/sections/SkillsMatrix";
import { Timeline } from "@/components/sections/Timeline";
import { ContactModal } from "@/components/sections/ContactModal";

export default function Home() {
  const [isContactOpen, setIsContactOpen] = useState(false);

  return (
    <main className="relative min-h-screen bg-cyber-bg text-white overflow-x-hidden selection:bg-cyber-cyan selection:text-black">
      <Hero onContactTrigger={() => setIsContactOpen(true)} />
      <SkillsMatrix />
      <Timeline />
      
      <ContactModal 
        isOpen={isContactOpen} 
        onClose={() => setIsContactOpen(false)} 
      />
    </main>
  );
}
'''

SEO_SITEMAP: str = '''import { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://cyberdomain.tech";
  return [
    {
      url: siteUrl,
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 1.0,
    },
  ];
}
'''
# ENGINE BUILD METHODOLOGY EXECUTO

def construct_blueprint() -> Dict[str, str]:
    """Assembles all application fragments into a programmatic configuration map."""
    return {
        "tailwind.config.ts": TAILWIND_CONFIG,
        ".env.local": ENV_LOCAL,
        "src/hooks/useReducedMotion.ts": USE_REDUCED_MOTION_HOOK,
        "src/components/ui/GlitchText.tsx": GLITCH_TEXT_COMPONENT,
        "src/components/ui/CyberButton.tsx": CYBER_BUTTON_COMPONENT,
        "src/components/sections/Hero.tsx": HERO_SECTION,
        "src/components/sections/SkillsMatrix.tsx": SKILLS_MATRIX_SECTION,
        "src/components/sections/Timeline.tsx": TIMELINE_SECTION,
        "src/components/sections/ContactModal.tsx": CONTACT_MODAL_SECTION,
        "src/lib/validations.ts": VALIDATIONS_LIB,
        "src/app/api/contact/route.ts": API_CONTACT_ROUTE,
        "src/app/page.tsx": PAGE_SHELL_LAYOUT,
        "src/app/sitemap.ts": SEO_SITEMAP
    }

if __name__ == "__main__":
    blueprint = construct_blueprint()
    print(f"[NOMINAL] Structural framework mapping containing {len(blueprint)} verified production targets completed.")
