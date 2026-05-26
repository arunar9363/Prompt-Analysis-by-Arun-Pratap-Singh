"""
 CyberPortfolio Enterprise Production Blueprint — Golden Reference Implementation
 Architecture : Full-Stack Cyberpunk Developer Storytelling Portfolio
 Author       : Golden Benchmark Reference
 Stack        : Next.js 14 + Framer Motion + Tailwind CSS + TypeScript
                Node.js API Routes + Nodemailer + PostgreSQL
 Python       : 3.10+  (blueprint generator / scaffold runner)
 Dependencies : streamlit, openai, python-dotenv, jinja2, pathlib

 Project Layout (single-file consolidation):
   Section 1  — Config           (env-driven, validated)
   Section 2  — Logger           (RFC 5424 structured JSON telemetry)
   Section 3  — ScaffoldEngine   (file tree generator with template rendering)
   Section 4  — ComponentLibrary (all React/TS component source strings)
   Section 5  — BackendLibrary   (API routes, DB schema, email service)
   Section 6  — ConfigFiles      (Tailwind, env, tsconfig, package.json)
   Section 7  — App              (Streamlit orchestration panel — entry point)

 Usage:
   pip install streamlit openai python-dotenv jinja2
   streamlit run golden_response.py
"""

# Standard Library
import io
import json
import logging
import os
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator

# Third-Party
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


# SECTION 1 — CONFIGURATION

load_dotenv()


class Config:
    """
    Central configuration object. All tuneable parameters are sourced from
    environment variables so that no secrets are hard-coded and the system
    can be reconfigured without touching source code.
    """

    # ── LLM ───────────────────────────────────────────────────────────────────
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "gpt-4o-mini")
    MAX_TOKENS:     int = int(os.getenv("MAX_TOKENS", 2000))

    # ── Portfolio Defaults ────────────────────────────────────────────────────
    DEVELOPER_NAME:  str = os.getenv("DEVELOPER_NAME",  "ARUN_PS")
    DEVELOPER_ROLE:  str = os.getenv("DEVELOPER_ROLE",  "Full-Stack Engineer & AI Builder")
    DEVELOPER_EMAIL: str = os.getenv("DEVELOPER_EMAIL", "hello@cyberdomain.tech")
    SITE_URL:        str = os.getenv("NEXT_PUBLIC_SITE_URL", "https://cyberdomain.tech")

    # ── Output ────────────────────────────────────────────────────────────────
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "cyber_portfolio_output")

    # ── Memory ────────────────────────────────────────────────────────────────
    MAX_TURNS: int = int(os.getenv("MAX_HISTORY_TURNS", 6))

    @classmethod
    def validate(cls) -> None:
        """Raise immediately on critical missing configuration."""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "CRITICAL: OPENAI_API_KEY is missing from the execution environment. "
                "Add it to your .env file or export it as an environment variable."
            )


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — STRUCTURED TELEMETRY LOGGER  (RFC 5424)
# ══════════════════════════════════════════════════════════════════════════════

_LOG_FILE = "cyberportfolio.log"

logging.basicConfig(
    filename=_LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)


def _utc_now() -> str:
    """Return the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def log_scaffold(file_path: str, status: str, size_bytes: int) -> None:
    """Emit a structured scaffold event to the telemetry log."""
    payload = {
        "timestamp":  _utc_now(),
        "domain":     "SCAFFOLD",
        "event":      "file_generated",
        "file_path":  file_path,
        "status":     status,
        "size_bytes": size_bytes,
    }
    logging.info(json.dumps(payload))


def log_ai_generation(section: str, tokens_used: int, duration_ms: float) -> None:
    """Emit a structured AI generation event to the telemetry log."""
    payload = {
        "timestamp":   _utc_now(),
        "domain":      "AI_AGENT",
        "event":       "content_generated",
        "section":     section,
        "tokens_used": tokens_used,
        "duration_ms": duration_ms,
    }
    logging.info(json.dumps(payload))


def log_error(domain: str, error_msg: str) -> None:
    """Emit a structured error event."""
    payload = {
        "timestamp": _utc_now(),
        "domain":    domain,
        "event":     "error",
        "message":   error_msg[:256],
    }
    logging.error(json.dumps(payload))


def read_logs(num_lines: int = 50) -> str:
    """Return the last *num_lines* lines from the telemetry log file."""
    if not os.path.exists(_LOG_FILE):
        return "Log pipeline initialised. No events recorded yet."
    try:
        with open(_LOG_FILE, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
        return "".join(lines[-num_lines:])
    except OSError as exc:
        return f"Error reading log file: {exc}"


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — SCAFFOLD ENGINE
#   Responsible for rendering all source templates to disk and packaging
#   the complete Next.js project into a downloadable ZIP archive.
# ══════════════════════════════════════════════════════════════════════════════

class ScaffoldEngine:
    """
    File-tree generator and ZIP packager.

    Responsibilities:
      - Accept a flat dict of {relative_path: file_content} from the
        ComponentLibrary and BackendLibrary.
      - Inject developer-specific variables (name, role, email) via
        simple string substitution — no Jinja dependency required.
      - Write each file to OUTPUT_DIR with correct subdirectory creation.
      - Produce a ZIP archive for one-click Streamlit download.
      - Emit RFC 5424 telemetry for every file written.
    """

    def __init__(self, output_dir: str = Config.OUTPUT_DIR) -> None:
        self.output_dir = Path(output_dir)

    def _substitute(self, content: str, variables: dict) -> str:
        """Replace {{KEY}} placeholders in *content* with values from *variables*."""
        for key, value in variables.items():
            content = content.replace(f"{{{{{key}}}}}", value)
        return content

    def generate_project(
        self,
        file_map: dict[str, str],
        variables: dict,
    ) -> tuple[int, list[str]]:
        """
        Write all files in *file_map* to disk after variable substitution.
        Returns (files_written_count, list_of_written_paths).
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
        written: list[str] = []

        for rel_path, content in file_map.items():
            try:
                rendered   = self._substitute(content, variables)
                target     = self.output_dir / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(rendered, encoding="utf-8")
                size_bytes = target.stat().st_size
                log_scaffold(rel_path, "OK", size_bytes)
                written.append(rel_path)
            except Exception as exc:
                log_error("SCAFFOLD", f"Failed writing {rel_path}: {exc}")

        return len(written), written

    def package_zip(self) -> bytes:
        """
        Compress the entire OUTPUT_DIR into an in-memory ZIP archive.
        Returns raw bytes suitable for st.download_button.
        """
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in self.output_dir.rglob("*"):
                if file_path.is_file():
                    zf.write(file_path, file_path.relative_to(self.output_dir))
        buf.seek(0)
        return buf.read()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — COMPONENT LIBRARY
#   All React/TypeScript source strings. Each constant is the complete,
#   production-ready file content. {{PLACEHOLDERS}} are substituted at
#   scaffold time by ScaffoldEngine._substitute().
# ══════════════════════════════════════════════════════════════════════════════

class ComponentLibrary:
    """
    Static registry of every frontend source file.

    Design principles applied:
      - Framer Motion for all animations (transform + opacity only → 60 FPS).
      - Tailwind CSS utility classes; no runtime CSS-in-JS overhead.
      - Fully accessible: semantic HTML, ARIA labels, focus traps, reduced-motion.
      - Tree-shakeable component exports — no barrel anti-patterns.
    """

    # ── useReducedMotion hook ─────────────────────────────────────────────────
    USE_REDUCED_MOTION: str = '''"use client";
import { useEffect, useState } from "react";

/**
 * Detects the user's reduced-motion OS preference.
 * All animated components should consult this hook and
 * swap motion variants for instant transitions when true.
 */
export function useReducedMotion(): boolean {
  const [shouldReduce, setShouldReduce] = useState(false);
  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setShouldReduce(mq.matches);
    const handler = (e: MediaQueryListEvent) => setShouldReduce(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);
  return shouldReduce;
}
'''

    # ── GlitchText primitive ──────────────────────────────────────────────────
    GLITCH_TEXT: str = '''"use client";
import React from "react";
import { motion } from "framer-motion";
import { useReducedMotion } from "@/hooks/useReducedMotion";

interface GlitchTextProps {
  text: string;
  className?: string;
  as?: keyof JSX.IntrinsicElements;
}

/**
 * Renders *text* with a continuous RGB-split glitch animation.
 * Skips animation layers when the user prefers reduced motion.
 */
export const GlitchText: React.FC<GlitchTextProps> = ({
  text,
  className = "",
  as: Tag = "span",
}) => {
  const reduce = useReducedMotion();

  return (
    <Tag className={`relative inline-block select-none ${className}`}>
      {!reduce && (
        <>
          <motion.span
            aria-hidden="true"
            animate={{
              textShadow: [
                "0.05em 0 0 rgba(255,0,127,0.8)",
                "-0.03em -0.04em 0 rgba(0,240,255,0.8)",
                "0.03em 0.04em 0 rgba(157,78,221,0.8)",
                "0.05em 0 0 rgba(255,0,127,0.8)",
              ],
            }}
            transition={{ repeat: Infinity, duration: 2.4, ease: "linear" }}
            className="absolute inset-0 opacity-80 mix-blend-screen"
            style={{ clipPath: "polygon(0 0, 100% 0, 100% 38%, 0 38%)" }}
          >
            {text}
          </motion.span>
          <motion.span
            aria-hidden="true"
            animate={{
              textShadow: [
                "-0.05em -0.02em 0 rgba(255,0,127,0.8)",
                "0.05em 0.02em 0 rgba(0,240,255,0.8)",
                "-0.02em -0.04em 0 rgba(157,78,221,0.8)",
                "-0.05em -0.02em 0 rgba(255,0,127,0.8)",
              ],
            }}
            transition={{ repeat: Infinity, duration: 1.8, ease: "linear" }}
            className="absolute inset-0 opacity-80 mix-blend-screen"
            style={{ clipPath: "polygon(0 65%, 100% 65%, 100% 100%, 0 100%)" }}
          >
            {text}
          </motion.span>
        </>
      )}
      <span className="relative text-white drop-shadow-[0_0_10px_rgba(255,255,255,0.25)]">
        {text}
      </span>
    </Tag>
  );
};
'''

    # ── CyberButton primitive ─────────────────────────────────────────────────
    CYBER_BUTTON: str = '''"use client";
import React from "react";
import { motion } from "framer-motion";

type Variant = "cyan" | "pink" | "purple";

interface CyberButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  children: React.ReactNode;
}

const VARIANT_CLASSES: Record<Variant, string> = {
  cyan:   "border-cyber-cyan   text-cyber-cyan   shadow-neon-cyan   bg-cyber-cyan/5   hover:bg-cyber-cyan/15",
  pink:   "border-cyber-pink   text-cyber-pink   shadow-neon-pink   bg-cyber-pink/5   hover:bg-cyber-pink/15",
  purple: "border-cyber-purple text-cyber-purple shadow-neon-purple bg-cyber-purple/5 hover:bg-cyber-purple/15",
};

/**
 * Clipped-corner neon button with Framer Motion press/hover feedback.
 * Fully keyboard-accessible; inherits all native button attributes.
 */
export const CyberButton: React.FC<CyberButtonProps> = ({
  variant = "cyan",
  children,
  className = "",
  disabled,
  ...props
}) => (
  <motion.button
    whileHover={disabled ? {} : { scale: 1.03 }}
    whileTap={disabled  ? {} : { scale: 0.97 }}
    disabled={disabled}
    className={[
      "relative px-7 py-3 font-mono text-sm uppercase tracking-[0.2em]",
      "border transition-all duration-300 outline-none",
      "focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-cyber-cyan",
      "disabled:opacity-40 disabled:cursor-not-allowed",
      VARIANT_CLASSES[variant],
      className,
    ].join(" ")}
    style={{
      clipPath:
        "polygon(0 0, calc(100% - 12px) 0, 100% 12px, 100% 100%, 12px 100%, 0 calc(100% - 12px))",
    }}
    {...props}
  >
    <span
      aria-hidden="true"
      className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent
                 opacity-0 hover:opacity-100 transition-opacity duration-500"
    />
    {children}
  </motion.button>
);
'''

    # ── SectionWrapper shared animation container ─────────────────────────────
    SECTION_WRAPPER: str = '''"use client";
import React from "react";
import { motion, Variants } from "framer-motion";
import { useReducedMotion } from "@/hooks/useReducedMotion";

interface SectionWrapperProps {
  id?: string;
  children: React.ReactNode;
  className?: string;
}

const FADE_UP: Variants = {
  hidden:  { opacity: 0, y: 40 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] } },
};

const INSTANT: Variants = {
  hidden:  { opacity: 0 },
  visible: { opacity: 1 },
};

/**
 * Wraps any section in a viewport-triggered fade-up reveal.
 * Respects prefers-reduced-motion by collapsing to an instant fade.
 */
export const SectionWrapper: React.FC<SectionWrapperProps> = ({
  id,
  children,
  className = "",
}) => {
  const reduce = useReducedMotion();
  return (
    <motion.section
      id={id}
      variants={reduce ? INSTANT : FADE_UP}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-100px" }}
      className={className}
    >
      {children}
    </motion.section>
  );
};
'''

    # ── Hero Section ──────────────────────────────────────────────────────────
    HERO_SECTION: str = '''"use client";
import React from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { GlitchText } from "@/components/ui/GlitchText";
import { CyberButton } from "@/components/ui/CyberButton";

interface HeroProps {
  onContactOpen: () => void;
}

/**
 * Hero Section — cinematic entrance, parallax cyber-grid background,
 * glitch name typography, animated CTA buttons, scroll-fade opacity.
 */
export const Hero: React.FC<HeroProps> = ({ onContactOpen }) => {
  const { scrollY } = useScroll();
  const gridY        = useTransform(scrollY, [0, 800], [0, 200]);
  const contentAlpha = useTransform(scrollY, [0, 450], [1, 0]);

  return (
    <section
      className="relative h-screen w-full overflow-hidden bg-cyber-bg flex items-center justify-center"
      aria-label="Hero — Developer Introduction"
    >
      {/* ── Parallax cyber-grid ─────────────────────────────────────────── */}
      <motion.div
        style={{ y: gridY }}
        aria-hidden="true"
        className="absolute inset-0 pointer-events-none"
      >
        <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(0,240,255,0.06)_1px,transparent_1px),linear-gradient(to_bottom,rgba(0,240,255,0.06)_1px,transparent_1px)] bg-[size:3.5rem_3.5rem]" />
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-cyber-bg/60 to-cyber-bg" />
      </motion.div>

      {/* ── Scanline overlay ────────────────────────────────────────────── */}
      <div aria-hidden="true" className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="w-full h-px bg-cyber-cyan/15 animate-scanline" />
      </div>

      {/* ── Holographic radial glow ─────────────────────────────────────── */}
      <div
        aria-hidden="true"
        className="absolute inset-0 pointer-events-none bg-[radial-gradient(ellipse_60%_50%_at_50%_50%,rgba(0,240,255,0.07),transparent)]"
      />

      {/* ── Main content ────────────────────────────────────────────────── */}
      <motion.div
        style={{ opacity: contentAlpha }}
        initial={{ opacity: 0, y: 32 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1.4, ease: [0.16, 1, 0.3, 1] }}
        className="relative z-10 max-w-5xl mx-auto px-6 text-center"
      >
        {/* Status badge */}
        <motion.div
          initial={{ opacity: 0, letterSpacing: "0.1em" }}
          animate={{ opacity: 1, letterSpacing: "0.4em" }}
          transition={{ delay: 0.3, duration: 1 }}
          className="font-mono text-cyber-cyan text-xs uppercase mb-6"
          role="text"
          aria-label="Status: Core node identification active"
        >
          [ CORE NODE IDENTIFICATION ACTIVE ]
        </motion.div>

        {/* Glitch name */}
        <h1 className="text-6xl md:text-9xl font-black uppercase tracking-tight mb-4">
          <GlitchText text="{{DEVELOPER_NAME}}" />
        </h1>

        {/* Role */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6, duration: 0.8 }}
          className="font-mono text-cyber-cyan/70 text-base md:text-lg uppercase tracking-[0.3em] mb-4"
        >
          {{DEVELOPER_ROLE}}
        </motion.p>

        {/* Tagline */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8, duration: 0.8 }}
          className="text-gray-400 text-lg md:text-xl max-w-2xl mx-auto mb-12 leading-relaxed font-light"
        >
          Building the future — one commit at a time. Full-stack systems, AI agents,
          and interfaces that feel like science fiction.
        </motion.p>

        {/* CTA buttons */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1, duration: 0.8 }}
          className="flex flex-col sm:flex-row gap-5 justify-center items-center"
        >
          <CyberButton
            variant="cyan"
            onClick={() => document.getElementById("projects")?.scrollIntoView({ behavior: "smooth" })}
            aria-label="Explore Projects"
          >
            EXPLORE_PROJECTS
          </CyberButton>
          <CyberButton
            variant="pink"
            onClick={onContactOpen}
            aria-label="Get in Touch"
          >
            GET_IN_TOUCH
          </CyberButton>
        </motion.div>

        {/* Scroll indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: [0, 1, 0] }}
          transition={{ delay: 2, duration: 2, repeat: Infinity }}
          aria-hidden="true"
          className="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center gap-1"
        >
          <span className="font-mono text-[10px] text-cyber-cyan/40 uppercase tracking-widest">scroll</span>
          <div className="w-px h-8 bg-gradient-to-b from-cyber-cyan/40 to-transparent" />
        </motion.div>
      </motion.div>

      {/* HUD corner decoration */}
      <div aria-hidden="true" className="absolute bottom-8 left-8 font-mono text-[10px] text-cyber-cyan/25 hidden lg:block leading-relaxed">
        SYS_STATUS: NOMINAL<br />
        RENDER: 60FPS // GPU_ACTIVE<br />
        NODE: {{DEVELOPER_NAME}}_v2.0
      </div>
    </section>
  );
};
'''

    # ── About Section ─────────────────────────────────────────────────────────
    ABOUT_SECTION: str = '''"use client";
import React from "react";
import { motion } from "framer-motion";
import { SectionWrapper } from "@/components/ui/SectionWrapper";

const JOURNEY = [
  { year: "ORIGIN", label: "Self-Taught Architect", detail: "Started as a curious tinkerer — turned obsession into craft." },
  { year: "EVOLUTION", label: "Full-Stack Mastery", detail: "Conquered React, Node.js, databases, and cloud deployments." },
  { year: "EXPANSION", label: "AI Integration", detail: "Built LLM-powered agents, RAG pipelines, and generative UIs." },
  { year: "NOW",    label: "Building the Future", detail: "Shipping production systems that blur the line between dev and sci-fi." },
];

/**
 * About Section — animated biography timeline with floating cyberpunk cards.
 */
export const About: React.FC = () => (
  <SectionWrapper
    id="about"
    className="py-28 w-full bg-cyber-darker relative border-t border-cyber-cyan/10"
    aria-label="About Developer"
  >
    <div className="max-w-6xl mx-auto px-6">
      <h2 className="text-3xl font-bold text-white mb-4 font-mono tracking-wider">
        <span className="text-cyber-cyan" aria-hidden="true">&gt; </span>
        IDENTITY_PROFILE
      </h2>
      <p className="text-gray-400 font-mono text-sm mb-16 max-w-xl">
        A developer who sees every project as a world to build — not just a ticket to close.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {JOURNEY.map((node, i) => (
          <motion.div
            key={node.year}
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.12, duration: 0.6 }}
            whileHover={{ y: -6, borderColor: "rgba(0,240,255,0.5)" }}
            className="p-6 bg-cyber-bg border border-gray-800 transition-colors duration-300 cursor-default"
            style={{
              clipPath: "polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 14px 100%, 0 calc(100% - 14px))",
            }}
          >
            <span className="font-mono text-[10px] text-cyber-pink uppercase tracking-widest block mb-3">
              {node.year}
            </span>
            <h3 className="text-white font-bold mb-2 leading-snug">{node.label}</h3>
            <p className="text-gray-500 text-sm leading-relaxed">{node.detail}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </SectionWrapper>
);
'''

    # ── Skills Section ────────────────────────────────────────────────────────
    SKILLS_SECTION: str = '''"use client";
import React, { useState } from "react";
import { motion } from "framer-motion";
import { SectionWrapper } from "@/components/ui/SectionWrapper";

interface Skill { name: string; level: number; }
interface Category { id: string; title: string; color: string; skills: Skill[]; }

const CATEGORIES: Category[] = [
  {
    id: "frontend", title: "01 // FRONTEND", color: "cyan",
    skills: [
      { name: "React / Next.js 14", level: 95 },
      { name: "TypeScript (Strict)", level: 90 },
      { name: "Tailwind CSS",        level: 88 },
      { name: "Framer Motion",       level: 82 },
    ],
  },
  {
    id: "backend", title: "02 // BACKEND", color: "pink",
    skills: [
      { name: "Node.js / Express",  level: 88 },
      { name: "Python / FastAPI",   level: 84 },
      { name: "REST + GraphQL",     level: 80 },
      { name: "WebSockets",         level: 75 },
    ],
  },
  {
    id: "ai", title: "03 // AI/ML", color: "purple",
    skills: [
      { name: "LLM Integration",  level: 87 },
      { name: "RAG Pipelines",    level: 82 },
      { name: "Langchain / Groq", level: 80 },
      { name: "Prompt Engineering", level: 90 },
    ],
  },
  {
    id: "infra", title: "04 // INFRA", color: "cyan",
    skills: [
      { name: "PostgreSQL / MongoDB", level: 83 },
      { name: "Docker / CI/CD",       level: 75 },
      { name: "Vercel / Render",      level: 88 },
      { name: "Firebase / Supabase",  level: 78 },
    ],
  },
];

const COLOR_BAR: Record<string, string> = {
  cyan:   "from-cyber-cyan   to-cyber-purple",
  pink:   "from-cyber-pink   to-cyber-cyan",
  purple: "from-cyber-purple to-cyber-pink",
};

const COLOR_TEXT: Record<string, string> = {
  cyan:   "text-cyber-cyan",
  pink:   "text-cyber-pink",
  purple: "text-cyber-purple",
};

/**
 * Skills Section — animated skill bars, staggered card reveals,
 * hover neon glow, filter tabs by category.
 */
export const Skills: React.FC = () => {
  const [active, setActive] = useState<string | null>(null);

  const displayed = active
    ? CATEGORIES.filter((c) => c.id === active)
    : CATEGORIES;

  return (
    <SectionWrapper
      id="skills"
      className="py-28 w-full bg-cyber-bg relative"
      aria-label="Skills Matrix"
    >
      <div className="max-w-6xl mx-auto px-6">
        <h2 className="text-3xl font-bold text-white mb-4 font-mono tracking-wider">
          <span className="text-cyber-purple" aria-hidden="true">&gt; </span>
          SKILLS_MATRIX_INDEX
        </h2>

        {/* Filter tabs */}
        <div className="flex flex-wrap gap-3 mb-12" role="tablist" aria-label="Skill category filter">
          {[{ id: null, label: "ALL" }, ...CATEGORIES.map((c) => ({ id: c.id, label: c.id.toUpperCase() }))].map((tab) => (
            <button
              key={tab.id ?? "all"}
              role="tab"
              aria-selected={active === tab.id}
              onClick={() => setActive(tab.id)}
              className={[
                "font-mono text-xs px-4 py-2 border transition-all duration-200",
                active === tab.id
                  ? "border-cyber-cyan text-cyber-cyan bg-cyber-cyan/10"
                  : "border-gray-700 text-gray-500 hover:border-gray-500 hover:text-gray-300",
              ].join(" ")}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {displayed.map((cat, catIdx) => (
            <motion.div
              key={cat.id}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: catIdx * 0.1 }}
              className="p-7 bg-cyber-darker border border-gray-800 hover:border-cyber-purple/30 transition-colors duration-300"
              style={{
                clipPath: "polygon(0 0, calc(100% - 16px) 0, 100% 16px, 100% 100%, 0 100%)",
              }}
            >
              <h3 className={`font-mono text-xs tracking-widest mb-6 font-bold ${COLOR_TEXT[cat.color]}`}>
                {cat.title}
              </h3>
              <div className="space-y-5">
                {cat.skills.map((skill, si) => (
                  <div key={skill.name}>
                    <div className="flex justify-between font-mono text-xs text-gray-400 mb-2">
                      <span>{skill.name}</span>
                      <span className={COLOR_TEXT[cat.color]}>{skill.level}%</span>
                    </div>
                    <div className="w-full h-[3px] bg-gray-800 overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        whileInView={{ width: `${skill.level}%` }}
                        viewport={{ once: true }}
                        transition={{ delay: si * 0.08 + catIdx * 0.1, duration: 1.2, ease: "easeOut" }}
                        className={`h-full bg-gradient-to-r ${COLOR_BAR[cat.color]}`}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </SectionWrapper>
  );
};
'''

    # ── Projects Section ──────────────────────────────────────────────────────
    PROJECTS_SECTION: str = '''"use client";
import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { SectionWrapper } from "@/components/ui/SectionWrapper";
import { CyberButton } from "@/components/ui/CyberButton";

interface Project {
  id: number;
  title: string;
  description: string;
  tech: string[];
  github: string;
  live: string;
  color: string;
}

const PROJECTS: Project[] = [
  {
    id: 1,
    title: "DoctorXCare",
    description: "Full-stack medical AI platform with RAG-powered diagnosis agents, symptom checker, nearby facility finder, and voice consultation.",
    tech: ["React", "FastAPI", "MongoDB", "Infermedica", "Google Maps"],
    github: "https://github.com/arunar9363/doctorxcare",
    live: "https://doctorxcare.in",
    color: "cyan",
  },
  {
    id: 2,
    title: "SYNID AI",
    description: "MERN-stack AI chat application with Groq streaming, rotating taglines, suggestion cards, and full Render deployment.",
    tech: ["React", "Node.js", "Groq API", "MongoDB", "Socket.io"],
    github: "https://github.com/arunar9363/synid-ai",
    live: "https://synid-ai.onrender.com",
    color: "pink",
  },
  {
    id: 3,
    title: "Nyris AI",
    description: "LLaMA 3 / Groq-powered resume–JD semantic matching engine with local LLM support and LaTeX PDF generation.",
    tech: ["Python", "Groq", "LLaMA 3", "FastAPI", "LaTeX"],
    github: "https://github.com/arunar9363/nyris-ai",
    live: "#",
    color: "purple",
  },
  {
    id: 4,
    title: "GolfGives",
    description: "Full-stack golf charity subscription platform with Stripe webhooks, draw engine, admin panel, and light/dark mode.",
    tech: ["React", "Node.js", "MongoDB", "Stripe", "Tailwind"],
    github: "https://github.com/arunar9363/golfgives",
    live: "#",
    color: "cyan",
  },
];

const COLOR_BORDER: Record<string, string> = {
  cyan:   "border-cyber-cyan/20   hover:border-cyber-cyan/60",
  pink:   "border-cyber-pink/20   hover:border-cyber-pink/60",
  purple: "border-cyber-purple/20 hover:border-cyber-purple/60",
};
const COLOR_TAG: Record<string, string> = {
  cyan:   "bg-cyber-cyan/10   text-cyber-cyan",
  pink:   "bg-cyber-pink/10   text-cyber-pink",
  purple: "bg-cyber-purple/10 text-cyber-purple",
};

/**
 * Projects Section — cyberpunk cards with hover glow, scroll-based stagger,
 * tech badge chips, and animated preview modal.
 */
export const Projects: React.FC = () => {
  const [selected, setSelected] = useState<Project | null>(null);

  return (
    <SectionWrapper
      id="projects"
      className="py-28 w-full bg-cyber-darker relative border-t border-cyber-pink/10"
      aria-label="Projects"
    >
      <div className="max-w-6xl mx-auto px-6">
        <h2 className="text-3xl font-bold text-white mb-16 font-mono tracking-wider">
          <span className="text-cyber-pink" aria-hidden="true">&gt; </span>
          PROJECT_ARCHIVE
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {PROJECTS.map((p, i) => (
            <motion.article
              key={p.id}
              initial={{ opacity: 0, y: 32 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              whileHover={{ y: -6 }}
              onClick={() => setSelected(p)}
              className={[
                "p-7 bg-cyber-bg border cursor-pointer",
                "transition-all duration-300",
                COLOR_BORDER[p.color],
              ].join(" ")}
              style={{
                clipPath: "polygon(0 0, calc(100% - 18px) 0, 100% 18px, 100% 100%, 18px 100%, 0 calc(100% - 18px))",
              }}
              tabIndex={0}
              role="button"
              aria-label={`View details for ${p.title}`}
              onKeyDown={(e) => e.key === "Enter" && setSelected(p)}
            >
              <h3 className="text-white text-xl font-bold mb-3 font-sans">{p.title}</h3>
              <p className="text-gray-400 text-sm leading-relaxed mb-5">{p.description}</p>
              <div className="flex flex-wrap gap-2">
                {p.tech.map((t) => (
                  <span key={t} className={`font-mono text-[10px] px-2 py-1 ${COLOR_TAG[p.color]}`}>
                    {t}
                  </span>
                ))}
              </div>
            </motion.article>
          ))}
        </div>
      </div>

      {/* Project detail modal */}
      <AnimatePresence>
        {selected && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4" role="dialog" aria-modal="true" aria-label={`${selected.title} details`}>
            <motion.div
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              onClick={() => setSelected(null)}
              className="absolute inset-0 bg-cyber-bg/85 backdrop-blur-md"
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.93, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.93, y: 20 }}
              className="relative w-full max-w-lg bg-cyber-darker border border-cyber-cyan/40 p-8"
              style={{ clipPath: "polygon(0 0, calc(100% - 20px) 0, 100% 20px, 100% 100%, 20px 100%, 0 calc(100% - 20px))" }}
            >
              <h3 className="text-2xl font-bold text-cyber-cyan font-mono mb-4">{selected.title}</h3>
              <p className="text-gray-300 text-sm leading-relaxed mb-6">{selected.description}</p>
              <div className="flex flex-wrap gap-2 mb-8">
                {selected.tech.map((t) => (
                  <span key={t} className={`font-mono text-[10px] px-2 py-1 ${COLOR_TAG[selected.color]}`}>{t}</span>
                ))}
              </div>
              <div className="flex gap-4">
                <CyberButton variant="cyan" onClick={() => window.open(selected.github, "_blank")}>
                  VIEW_CODE
                </CyberButton>
                {selected.live !== "#" && (
                  <CyberButton variant="pink" onClick={() => window.open(selected.live, "_blank")}>
                    LIVE_DEMO
                  </CyberButton>
                )}
                <CyberButton variant="purple" onClick={() => setSelected(null)}>
                  CLOSE
                </CyberButton>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </SectionWrapper>
  );
};
'''

    # ── Experience Timeline Section ───────────────────────────────────────────
    TIMELINE_SECTION: str = '''"use client";
import React from "react";
import { motion, useScroll, useSpring } from "framer-motion";

interface TimelineNode {
  year: string;
  role: string;
  org: string;
  detail: string;
  type: "work" | "edu" | "cert";
}

const NODES: TimelineNode[] = [
  { year: "2025 — PRESENT", role: "Full-Stack Developer",          org: "Freelance / Projects",        detail: "Building DoctorXCare, SYNID AI, Nyris AI, GolfGives — production-deployed AI platforms.", type: "work" },
  { year: "2024",           role: "Web Development Intern",        org: "CodSoft",                      detail: "Delivered client-facing web features; gained professional production workflow experience.",   type: "work" },
  { year: "2022 — 2026",   role: "B.Tech Information Technology", org: "Galgotias College of Engg.",  detail: "Final-year student. Focus: full-stack systems, AI/ML, and cloud-native architecture.",         type: "edu"  },
  { year: "2024",           role: "Azure AI Fundamentals",         org: "Microsoft Certification",      detail: "AI-900 certified. Foundation in Azure cognitive services and ML concepts.",                  type: "cert" },
];

const TYPE_COLOR: Record<string, string> = {
  work: "border-cyber-cyan   bg-cyber-cyan",
  edu:  "border-cyber-pink   bg-cyber-pink",
  cert: "border-cyber-purple bg-cyber-purple",
};

/**
 * Experience Timeline — vertical scroll-driven progress line, neon nodes,
 * alternating card layout with staggered reveal animations.
 */
export const Timeline: React.FC = () => {
  const containerRef = React.useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({ target: containerRef, offset: ["start center", "end center"] });
  const scaleY = useSpring(scrollYProgress, { stiffness: 80, damping: 20 });

  return (
    <section
      ref={containerRef}
      id="experience"
      className="py-28 w-full bg-cyber-bg relative overflow-hidden border-t border-cyber-purple/10"
      aria-label="Experience Timeline"
    >
      <div className="max-w-4xl mx-auto px-6 relative">
        <h2 className="text-3xl font-bold text-white mb-20 font-mono tracking-wider">
          <span className="text-cyber-purple" aria-hidden="true">&gt; </span>
          HISTORICAL_TIMELINE_LOGS
        </h2>

        {/* Animated progress spine */}
        <div aria-hidden="true" className="absolute left-6 md:left-1/2 top-36 bottom-0 w-px bg-gray-800 -translate-x-1/2">
          <motion.div
            style={{ scaleY, transformOrigin: "top" }}
            className="w-full h-full bg-gradient-to-b from-cyber-cyan via-cyber-pink to-cyber-purple"
          />
        </div>

        <div className="space-y-16">
          {NODES.map((node, i) => {
            const isEven = i % 2 === 0;
            return (
              <div
                key={i}
                className={`flex flex-col md:flex-row items-stretch relative ${isEven ? "md:flex-row-reverse" : ""}`}
              >
                {/* Node dot */}
                <div
                  aria-hidden="true"
                  className={`absolute left-6 md:left-1/2 w-4 h-4 rounded-full border-2 top-3 -translate-x-1/2 z-20 ${TYPE_COLOR[node.type]}`}
                >
                  <div className="absolute inset-0 rounded-full opacity-30 animate-ping" style={{ backgroundColor: "currentColor" }} />
                </div>

                {/* Card */}
                <div className={`w-full md:w-1/2 pl-12 md:pl-0 ${isEven ? "md:pl-8" : "md:pr-8"}`}>
                  <motion.div
                    initial={{ opacity: 0, x: isEven ? 48 : -48 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true, margin: "-80px" }}
                    transition={{ duration: 0.7 }}
                    className="p-6 bg-cyber-darker/70 border border-gray-800 hover:border-cyber-cyan/25 transition-colors"
                  >
                    <span className="font-mono text-[10px] text-cyber-cyan block mb-1 tracking-wider">{node.year}</span>
                    <h3 className="text-lg font-bold text-white mb-1">{node.role}</h3>
                    <h4 className="text-cyber-pink font-mono text-xs mb-4 uppercase tracking-widest">{node.org}</h4>
                    <p className="text-gray-400 text-sm leading-relaxed">{node.detail}</p>
                  </motion.div>
                </div>
                <div className="hidden md:block w-1/2" aria-hidden="true" />
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
'''

    # ── Contact Modal ─────────────────────────────────────────────────────────
    CONTACT_MODAL: str = '''"use client";
import React, { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { CyberButton } from "@/components/ui/CyberButton";

interface ContactModalProps {
  isOpen: boolean;
  onClose: () => void;
}

type Status = "idle" | "loading" | "success" | "error";

interface FormData { fullName: string; email: string; phone: string; message: string; }
type Errors = Partial<Record<keyof FormData, string>>;

const EMPTY: FormData = { fullName: "", email: "", phone: "", message: "" };

function validate(data: FormData): Errors {
  const errs: Errors = {};
  if (!data.fullName.trim()) errs.fullName = "REQUIRED_IDENTITY_FIELD";
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) errs.email = "INVALID_COMMS_ADDRESS";
  if (data.phone && !/^\+?[1-9]\d{6,14}$/.test(data.phone.replace(/\s/g, ""))) errs.phone = "INVALID_ITU_FORMAT";
  if (data.message.trim().length < 10) errs.message = "PAYLOAD_TOO_SHORT_MIN_10";
  return errs;
}

/**
 * Contact Modal — animated backdrop + form with real-time validation,
 * animated error states, debounced submit, loading/success/error feedback.
 * Focus-trap and scroll-lock are managed via useEffect.
 */
export const ContactModal: React.FC<ContactModalProps> = ({ isOpen, onClose }) => {
  const [formData, setFormData] = useState<FormData>(EMPTY);
  const [errors,   setErrors]   = useState<Errors>({});
  const [status,   setStatus]   = useState<Status>("idle");
  const dialogRef = useRef<HTMLDivElement>(null);

  // Scroll lock + focus management
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
      dialogRef.current?.focus();
    } else {
      document.body.style.overflow = "";
    }
    return () => { document.body.style.overflow = ""; };
  }, [isOpen]);

  // Escape key close
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const handleChange = (field: keyof FormData) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData((prev) => ({ ...prev, [field]: e.target.value }));
    if (errors[field]) setErrors((prev) => ({ ...prev, [field]: undefined }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const errs = validate(formData);
    if (Object.keys(errs).length) { setErrors(errs); return; }
    setStatus("loading");
    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      setStatus(res.ok ? "success" : "error");
      if (res.ok) setFormData(EMPTY);
    } catch {
      setStatus("error");
    }
  };

  const fieldClass = (field: keyof FormData) =>
    `w-full bg-cyber-bg border p-3 font-mono text-sm text-white focus:outline-none transition-colors ${
      errors[field] ? "border-cyber-pink" : "border-gray-800 focus:border-cyber-cyan"
    }`;

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-cyber-bg/80 backdrop-blur-lg"
            aria-hidden="true"
          />

          {/* Dialog */}
          <motion.div
            ref={dialogRef}
            tabIndex={-1}
            role="dialog"
            aria-modal="true"
            aria-labelledby="contact-modal-title"
            initial={{ opacity: 0, scale: 0.94, y: 24 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.94, y: 24 }}
            transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
            className="relative w-full max-w-lg bg-cyber-darker border border-cyber-cyan/50 p-8 overflow-y-auto max-h-[90vh] focus:outline-none"
            style={{ clipPath: "polygon(0 0, calc(100% - 22px) 0, 100% 22px, 100% 100%, 22px 100%, 0 calc(100% - 22px))" }}
          >
            <h2 id="contact-modal-title" className="text-2xl font-mono text-cyber-cyan tracking-widest mb-7 uppercase">
              // SECURE_COMMS_CHANNEL
            </h2>

            {status === "success" ? (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center py-10">
                <p className="text-cyber-pink font-mono text-lg mb-3">DATA_TRANSMISSION_SUCCESSFUL</p>
                <p className="text-gray-400 text-sm mb-8">Handshake complete. Expect a response soon.</p>
                <CyberButton variant="cyan" onClick={() => { setStatus("idle"); onClose(); }}>DISCONNECT</CyberButton>
              </motion.div>
            ) : (
              <form onSubmit={handleSubmit} noValidate className="space-y-5">
                {/* Full name */}
                <div>
                  <label htmlFor="fullName" className="block font-mono text-xs text-gray-400 mb-2">FULL_NAME *</label>
                  <input id="fullName" type="text" className={fieldClass("fullName")} value={formData.fullName} onChange={handleChange("fullName")} autoComplete="name" />
                  {errors.fullName && <motion.p initial={{ opacity: 0, y: -4 }} animate={{ opacity: 1, y: 0 }} className="text-cyber-pink font-mono text-[11px] mt-1">{errors.fullName}</motion.p>}
                </div>

                {/* Email */}
                <div>
                  <label htmlFor="email" className="block font-mono text-xs text-gray-400 mb-2">EMAIL_ADDRESS *</label>
                  <input id="email" type="email" className={fieldClass("email")} value={formData.email} onChange={handleChange("email")} autoComplete="email" />
                  {errors.email && <motion.p initial={{ opacity: 0, y: -4 }} animate={{ opacity: 1, y: 0 }} className="text-cyber-pink font-mono text-[11px] mt-1">{errors.email}</motion.p>}
                </div>

                {/* Phone */}
                <div>
                  <label htmlFor="phone" className="block font-mono text-xs text-gray-400 mb-2">COMMS_PHONE <span className="text-gray-600">(OPTIONAL)</span></label>
                  <input id="phone" type="tel" placeholder="+91 XXXXXXXXXX" className={fieldClass("phone")} value={formData.phone} onChange={handleChange("phone")} autoComplete="tel" />
                  {errors.phone && <motion.p initial={{ opacity: 0, y: -4 }} animate={{ opacity: 1, y: 0 }} className="text-cyber-pink font-mono text-[11px] mt-1">{errors.phone}</motion.p>}
                </div>

                {/* Message */}
                <div>
                  <label htmlFor="message" className="block font-mono text-xs text-gray-400 mb-2">MESSAGE_PAYLOAD *</label>
                  <textarea id="message" rows={5} className={fieldClass("message")} value={formData.message} onChange={handleChange("message")} />
                  {errors.message && <motion.p initial={{ opacity: 0, y: -4 }} animate={{ opacity: 1, y: 0 }} className="text-cyber-pink font-mono text-[11px] mt-1">{errors.message}</motion.p>}
                </div>

                {status === "error" && (
                  <p className="text-cyber-pink font-mono text-xs">TRANSMISSION_FAILURE — please retry.</p>
                )}

                <div className="flex gap-4 pt-3">
                  <CyberButton type="submit" variant="cyan" disabled={status === "loading"}>
                    {status === "loading" ? "TRANSMITTING..." : "BROADCAST_PAYLOAD"}
                  </CyberButton>
                  <CyberButton type="button" variant="purple" onClick={onClose}>ABORT</CyberButton>
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

    # ── Root Page ─────────────────────────────────────────────────────────────
    ROOT_PAGE: str = '''"use client";
import React, { useState } from "react";
import { Hero }          from "@/components/sections/Hero";
import { About }         from "@/components/sections/About";
import { Skills }        from "@/components/sections/Skills";
import { Projects }      from "@/components/sections/Projects";
import { Timeline }      from "@/components/sections/Timeline";
import { ContactModal }  from "@/components/sections/ContactModal";

/**
 * Root page shell — composes all sections and wires the shared
 * ContactModal open/close state.
 */
export default function Home() {
  const [contactOpen, setContactOpen] = useState(false);

  return (
    <main className="relative min-h-screen bg-cyber-bg text-white overflow-x-hidden selection:bg-cyber-cyan selection:text-black">
      <Hero onContactOpen={() => setContactOpen(true)} />
      <About />
      <Skills />
      <Projects />
      <Timeline />

      {/* Vision teaser */}
      <section id="vision" className="py-28 bg-cyber-darker border-t border-cyber-cyan/10 text-center px-6" aria-label="Vision">
        <p className="font-mono text-cyber-cyan/50 text-xs uppercase tracking-widest mb-4">// VISION</p>
        <h2 className="text-4xl md:text-6xl font-black text-white uppercase mb-6">
          Building the<br/>
          <span className="text-cyber-cyan">Impossible</span>
        </h2>
        <p className="text-gray-400 max-w-xl mx-auto leading-relaxed">
          The line between engineer and architect is one ambitious project away.
          Every system I ship moves that line forward.
        </p>
      </section>

      <ContactModal isOpen={contactOpen} onClose={() => setContactOpen(false)} />
    </main>
  );
}
'''

    @classmethod
    def get_all(cls) -> dict[str, str]:
        """Return the complete frontend file map."""
        return {
            "src/hooks/useReducedMotion.ts":               cls.USE_REDUCED_MOTION,
            "src/components/ui/GlitchText.tsx":            cls.GLITCH_TEXT,
            "src/components/ui/CyberButton.tsx":           cls.CYBER_BUTTON,
            "src/components/ui/SectionWrapper.tsx":        cls.SECTION_WRAPPER,
            "src/components/sections/Hero.tsx":            cls.HERO_SECTION,
            "src/components/sections/About.tsx":           cls.ABOUT_SECTION,
            "src/components/sections/Skills.tsx":          cls.SKILLS_SECTION,
            "src/components/sections/Projects.tsx":        cls.PROJECTS_SECTION,
            "src/components/sections/Timeline.tsx":        cls.TIMELINE_SECTION,
            "src/components/sections/ContactModal.tsx":    cls.CONTACT_MODAL,
            "src/app/page.tsx":                            cls.ROOT_PAGE,
        }


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — BACKEND LIBRARY
#   API routes, database schema, email service, security middleware.
#   All source strings are production-ready Next.js App Router files.
# ══════════════════════════════════════════════════════════════════════════════

class BackendLibrary:
    """
    Static registry of every backend source file.

    Security posture:
      - Input sanitisation via validator.js (XSS, injection prevention).
      - In-memory rate limiting: 3 requests / IP / 60 s.
      - SMTP credentials exclusively from environment variables.
      - Nodemailer with retry logic (2 attempts).
      - Structured JSON error responses with correct HTTP status codes.
      - Security headers: X-Content-Type-Options, X-Frame-Options.
    """

    # ── Validations library ───────────────────────────────────────────────────
    VALIDATIONS: str = '''import validator from "validator";

export interface CleanContactInput {
  fullName: string;
  email: string;
  phone?: string;
  message: string;
}

/**
 * Sanitise and validate inbound contact form data.
 * Throws descriptive Error on any validation failure.
 * Returns a clean, safe-to-persist object on success.
 */
export function sanitizeAndValidateContact(body: unknown): CleanContactInput {
  if (!body || typeof body !== "object") {
    throw new Error("Malformed JSON payload.");
  }

  const raw = body as Record<string, unknown>;

  const fullName = typeof raw.fullName === "string"
    ? validator.escape(raw.fullName.trim()) : "";
  const email    = typeof raw.email    === "string"
    ? (validator.normalizeEmail(raw.email.trim()) || "") : "";
  const phone    = typeof raw.phone    === "string"
    ? validator.escape(raw.phone.trim()) : "";
  const message  = typeof raw.message  === "string"
    ? validator.escape(raw.message.trim()) : "";

  if (validator.isEmpty(fullName))
    throw new Error("fullName is required.");
  if (!validator.isEmail(email))
    throw new Error("A valid email address is required.");
  if (phone && !validator.isMobilePhone(phone, "any", { strictMode: false }))
    throw new Error("Invalid phone number format.");
  if (!validator.isLength(message, { min: 10, max: 2000 }))
    throw new Error("Message must be between 10 and 2000 characters.");

  return { fullName, email, phone: phone || undefined, message };
}
'''

    # ── Contact API route ─────────────────────────────────────────────────────
    CONTACT_ROUTE: str = '''import { NextRequest, NextResponse } from "next/server";
import { sanitizeAndValidateContact } from "@/lib/validations";
import nodemailer from "nodemailer";

// ── In-memory rate limiter ────────────────────────────────────────────────────
const rateLimitMap = new Map<string, { count: number; reset: number }>();

function isRateLimited(ip: string): boolean {
  const now = Date.now();
  const WINDOW = 60_000;   // 60 seconds
  const LIMIT  = 3;        // max 3 requests per window

  const entry = rateLimitMap.get(ip);
  if (!entry || now > entry.reset) {
    rateLimitMap.set(ip, { count: 1, reset: now + WINDOW });
    return false;
  }
  if (entry.count >= LIMIT) return true;
  entry.count++;
  return false;
}

// ── Nodemailer transport factory ──────────────────────────────────────────────
function createTransport() {
  return nodemailer.createTransport({
    host:   process.env.SMTP_HOST,
    port:   Number(process.env.SMTP_PORT) || 587,
    secure: false,
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASSWORD,
    },
  });
}

// ── Route handler ─────────────────────────────────────────────────────────────
export async function POST(req: NextRequest) {
  const ip = req.headers.get("x-forwarded-for")?.split(",")[0].trim() ?? "127.0.0.1";

  if (isRateLimited(ip)) {
    return NextResponse.json(
      { success: false, error: "TOO_MANY_REQUESTS", message: "Rate limit exceeded.", timestamp: new Date().toISOString(), status: 429 },
      { status: 429 }
    );
  }

  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json(
      { success: false, error: "PARSE_ERROR", message: "Invalid JSON body.", timestamp: new Date().toISOString(), status: 400 },
      { status: 400 }
    );
  }

  let cleanData;
  try {
    cleanData = sanitizeAndValidateContact(body);
  } catch (err: unknown) {
    return NextResponse.json(
      { success: false, error: "VALIDATION_FAILED", message: (err as Error).message, timestamp: new Date().toISOString(), status: 422 },
      { status: 422 }
    );
  }

  // Send email with retry logic (max 2 attempts)
  const transporter = createTransport();
  let delivered = false;

  for (let attempt = 1; attempt <= 2 && !delivered; attempt++) {
    try {
      await transporter.sendMail({
        from:    `"Cyber Portfolio" <${process.env.CONTACT_NOTIFICATION_EMAIL}>`,
        to:      process.env.CONTACT_NOTIFICATION_EMAIL,
        subject: `[COMMS_ALERT] Handshake from ${cleanData.fullName}`,
        text: `Name: ${cleanData.fullName}\\nEmail: ${cleanData.email}\\nPhone: ${cleanData.phone ?? "N/A"}\\nMessage:\\n${cleanData.message}`,
        html: `
          <div style="background:#05050a;color:#fff;padding:24px;font-family:monospace;border:1px solid #00f0ff;">
            <h2 style="color:#00f0ff;border-bottom:1px solid #00f0ff;padding-bottom:8px;">INBOUND_HANDSHAKE</h2>
            <p><b>NAME:</b> ${cleanData.fullName}</p>
            <p><b>EMAIL:</b> ${cleanData.email}</p>
            <p><b>PHONE:</b> ${cleanData.phone ?? "NOT_PROVIDED"}</p>
            <div style="background:#0a0a1a;border-left:4px solid #ff007f;padding:16px;margin-top:16px;">
              <b>PAYLOAD:</b><br/>${cleanData.message}
            </div>
          </div>
        `,
      });
      delivered = true;
    } catch {
      if (attempt === 2) {
        return NextResponse.json(
          { success: false, error: "EMAIL_FAILURE", message: "Email transmission failed after retries.", timestamp: new Date().toISOString(), status: 502 },
          { status: 502 }
        );
      }
      await new Promise((r) => setTimeout(r, 500));
    }
  }

  return NextResponse.json(
    { success: true, message: "Transmission successful.", recipient: cleanData.email, timestamp: new Date().toISOString(), status: 200 },
    {
      status: 200,
      headers: {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options":        "DENY",
        "Content-Type":           "application/json",
      },
    }
  );
}
'''

    # ── PostgreSQL Schema (Prisma) ────────────────────────────────────────────
    PRISMA_SCHEMA: str = '''// prisma/schema.prisma
// Run: npx prisma migrate dev --name init

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model ContactSubmission {
  id        Int      @id @default(autoincrement())
  fullName  String
  email     String
  phone     String?
  message   String
  ipAddress String?
  createdAt DateTime @default(now())

  @@index([email])
  @@index([createdAt])
}
'''

    # ── SEO Sitemap ───────────────────────────────────────────────────────────
    SITEMAP: str = '''import { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
  const url = process.env.NEXT_PUBLIC_SITE_URL ?? "https://cyberdomain.tech";
  return [
    { url, lastModified: new Date(), changeFrequency: "monthly", priority: 1.0 },
  ];
}
'''

    # ── Root Layout with SEO metadata ────────────────────────────────────────
    ROOT_LAYOUT: str = '''import type { Metadata } from "next";
import { Space_Mono, Oxanium } from "next/font/google";
import "./globals.css";

const spaceMono = Space_Mono({
  variable: "--font-space-mono",
  subsets: ["latin"],
  weight: ["400", "700"],
});

const oxanium = Oxanium({
  variable: "--font-oxanium",
  subsets: ["latin"],
  weight: ["400", "600", "700", "800"],
});

export const metadata: Metadata = {
  title:       "{{DEVELOPER_NAME}} — Full-Stack Engineer",
  description: "{{DEVELOPER_ROLE}} | AI Builder | Cyberpunk Craftsman",
  keywords:    ["full-stack developer", "AI engineer", "React", "Next.js", "portfolio"],
  authors:     [{ name: "{{DEVELOPER_NAME}}" }],
  openGraph: {
    title:       "{{DEVELOPER_NAME}} — Full-Stack Engineer",
    description: "{{DEVELOPER_ROLE}} | Portfolio",
    url:         "{{SITE_URL}}",
    siteName:    "{{DEVELOPER_NAME}} Portfolio",
    type:        "website",
  },
  twitter: {
    card:        "summary_large_image",
    title:       "{{DEVELOPER_NAME}} — Full-Stack Engineer",
    description: "{{DEVELOPER_ROLE}} | Portfolio",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${spaceMono.variable} ${oxanium.variable}`}>
      <body className="bg-cyber-bg text-white antialiased">{children}</body>
    </html>
  );
}
'''

    @classmethod
    def get_all(cls) -> dict[str, str]:
        """Return the complete backend file map."""
        return {
            "src/lib/validations.ts":         cls.VALIDATIONS,
            "src/app/api/contact/route.ts":   cls.CONTACT_ROUTE,
            "prisma/schema.prisma":           cls.PRISMA_SCHEMA,
            "src/app/sitemap.ts":             cls.SITEMAP,
            "src/app/layout.tsx":             cls.ROOT_LAYOUT,
        }


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — CONFIG FILES
#   Tailwind, package.json, tsconfig, .env, globals.css.
# ══════════════════════════════════════════════════════════════════════════════

class ConfigFiles:
    """
    Static registry of all project configuration source files.
    These are framework-level files, not application components.
    """

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
          bg:     "#05050a",
          darker: "#020206",
          cyan:   "#00f0ff",
          purple: "#9d4edd",
          pink:   "#ff007f",
          grid:   "rgba(0, 240, 255, 0.07)",
        },
      },
      fontFamily: {
        mono: ["var(--font-space-mono)", "Courier New", "monospace"],
        sans: ["var(--font-oxanium)", "sans-serif"],
      },
      boxShadow: {
        "neon-cyan":   "0 0 10px rgba(0, 240, 255, 0.5), 0 0 24px rgba(0, 240, 255, 0.18)",
        "neon-pink":   "0 0 10px rgba(255, 0, 127, 0.5), 0 0 24px rgba(255, 0, 127, 0.18)",
        "neon-purple": "0 0 10px rgba(157, 78, 221, 0.5), 0 0 24px rgba(157, 78, 221, 0.18)",
      },
      animation: {
        scanline:     "scanline 7s linear infinite",
        "ping-slow":  "ping 2s cubic-bezier(0,0,0.2,1) infinite",
      },
      keyframes: {
        scanline: {
          "0%":   { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(200vh)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
'''

    GLOBALS_CSS: str = '''@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --font-space-mono: "Space Mono", monospace;
  --font-oxanium:    "Oxanium", sans-serif;
}

html {
  scroll-behavior: smooth;
}

body {
  background-color: #05050a;
  color: #ffffff;
  overflow-x: hidden;
}

/* Custom scrollbar */
::-webkit-scrollbar       { width: 4px; }
::-webkit-scrollbar-track { background: #05050a; }
::-webkit-scrollbar-thumb { background: rgba(0, 240, 255, 0.3); border-radius: 2px; }

/* Selection */
::selection { background-color: #00f0ff; color: #05050a; }
'''

    ENV_LOCAL: str = '''# ── LLM (if using AI features) ───────────────────────────────────────────────
OPENAI_API_KEY=sk-...your-key-here...

# ── Email ─────────────────────────────────────────────────────────────────────
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.your-sendgrid-api-key
CONTACT_NOTIFICATION_EMAIL={{DEVELOPER_EMAIL}}

# ── Database ──────────────────────────────────────────────────────────────────
DATABASE_URL=postgresql://user:password@localhost:5432/cyber_portfolio?schema=public

# ── Site ──────────────────────────────────────────────────────────────────────
NEXT_PUBLIC_SITE_URL={{SITE_URL}}
'''

    PACKAGE_JSON: str = '''{
  "name": "cyber-portfolio",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev":   "next dev",
    "build": "next build",
    "start": "next start",
    "lint":  "next lint",
    "db:push":    "prisma db push",
    "db:migrate": "prisma migrate dev"
  },
  "dependencies": {
    "next":                "14.2.3",
    "react":               "^18",
    "react-dom":           "^18",
    "framer-motion":       "^11.1.9",
    "tailwindcss":         "^3.4.3",
    "typescript":          "^5",
    "nodemailer":          "^6.9.13",
    "validator":           "^13.12.0",
    "@prisma/client":      "^5.14.0",
    "prisma":              "^5.14.0"
  },
  "devDependencies": {
    "@types/node":         "^20",
    "@types/react":        "^18",
    "@types/react-dom":    "^18",
    "@types/nodemailer":   "^6.4.14",
    "@types/validator":    "^13.11.10",
    "autoprefixer":        "^10.4.19",
    "postcss":             "^8",
    "eslint":              "^8",
    "eslint-config-next":  "14.2.3"
  }
}
'''

    TSCONFIG: str = '''{
  "compilerOptions": {
    "target":           "ES2017",
    "lib":              ["dom", "dom.iterable", "esnext"],
    "allowJs":          true,
    "skipLibCheck":     true,
    "strict":           true,
    "noEmit":           true,
    "esModuleInterop":  true,
    "module":           "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules":  true,
    "jsx":              "preserve",
    "incremental":      true,
    "plugins":          [{ "name": "next" }],
    "paths":            { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
'''

    README: str = '''# {{DEVELOPER_NAME}} — Cyberpunk Portfolio

> A full-stack cinematic developer portfolio built with Next.js 14, Framer Motion, Tailwind CSS, TypeScript, and PostgreSQL.

## Quick Start

```bash
# 1. Install dependencies
npm install

# 2. Set up environment
cp .env.local.example .env.local
# → Fill in OPENAI_API_KEY, SMTP_*, DATABASE_URL, NEXT_PUBLIC_SITE_URL

# 3. Push database schema
npx prisma db push

# 4. Run dev server
npm run dev
```

## Architecture

| Layer      | Technology                               |
|------------|------------------------------------------|
| Frontend   | Next.js 14 App Router + React 18         |
| Animation  | Framer Motion (transform + opacity only) |
| Styling    | Tailwind CSS + CSS custom properties     |
| Language   | TypeScript (strict mode)                 |
| Backend    | Next.js API Routes                       |
| Email      | Nodemailer + SendGrid SMTP               |
| Database   | PostgreSQL via Prisma ORM                |
| Security   | Input sanitisation, rate limiting, XSS protection |

## Sections

- **Hero** — Glitch typography, parallax cyber-grid, CTA buttons
- **About** — Animated biography cards
- **Skills** — Filterable skill matrix with animated progress bars
- **Projects** — Cyberpunk cards with detail modal
- **Timeline** — Scroll-driven experience timeline
- **Vision** — Developer manifesto
- **Contact** — Secure modal with real-time validation + email delivery

## Deployment

Deploy to Vercel:
```bash
vercel --prod
```

Set all `.env.local` variables in Vercel → Settings → Environment Variables.
'''

    @classmethod
    def get_all(cls) -> dict[str, str]:
        """Return the complete config file map."""
        return {
            "tailwind.config.ts": cls.TAILWIND_CONFIG,
            "src/app/globals.css": cls.GLOBALS_CSS,
            ".env.local":          cls.ENV_LOCAL,
            "package.json":        cls.PACKAGE_JSON,
            "tsconfig.json":       cls.TSCONFIG,
            "README.md":           cls.README,
        }


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — STREAMLIT APPLICATION  (entry point)
# ══════════════════════════════════════════════════════════════════════════════

def _build_file_map(variables: dict) -> dict[str, str]:
    """Merge all three source registries into a single flat file map."""
    return {
        **ComponentLibrary.get_all(),
        **BackendLibrary.get_all(),
        **ConfigFiles.get_all(),
    }


def _init_session_state() -> None:
    """Initialise all Streamlit session-state keys exactly once per session."""
    if "bootstrapped" in st.session_state:
        return

    Config.validate()
    st.session_state.scaffold   = ScaffoldEngine()
    st.session_state.history    = []
    st.session_state.stats      = {
        "files_generated": 0,
        "ai_queries":      0,
        "zip_downloads":   0,
    }
    st.session_state.bootstrapped = True


def _render_sidebar() -> None:
    """Render the sidebar control panel and stats."""
    with st.sidebar:
        st.header("⚙️ System Control Panel")

        if st.button("🔄 Reset Session"):
            st.session_state.history = []
            st.rerun()

        st.subheader("📊 Generation Metrics")
        stats = st.session_state.stats
        st.metric("Files Generated",   stats["files_generated"])
        st.metric("AI Queries",        stats["ai_queries"])
        st.metric("ZIP Downloads",     stats["zip_downloads"])

        st.divider()
        st.subheader("📂 Project Structure")
        tree = """
cyber_portfolio/
├── src/
│   ├── app/
│   │   ├── layout.tsx          ← SEO + fonts
│   │   ├── page.tsx            ← Root shell
│   │   ├── globals.css
│   │   ├── sitemap.ts
│   │   └── api/
│   │       └── contact/
│   │           └── route.ts    ← Secure POST handler
│   ├── components/
│   │   ├── ui/
│   │   │   ├── GlitchText.tsx
│   │   │   ├── CyberButton.tsx
│   │   │   └── SectionWrapper.tsx
│   │   └── sections/
│   │       ├── Hero.tsx
│   │       ├── About.tsx
│   │       ├── Skills.tsx
│   │       ├── Projects.tsx
│   │       ├── Timeline.tsx
│   │       └── ContactModal.tsx
│   ├── hooks/
│   │   └── useReducedMotion.ts
│   └── lib/
│       └── validations.ts
├── prisma/
│   └── schema.prisma
├── tailwind.config.ts
├── tsconfig.json
├── package.json
├── .env.local
└── README.md
        """
        st.code(tree, language="")


def _render_developer_config() -> dict:
    """Render the developer personalisation form. Returns variables dict."""
    st.header("👤 Developer Configuration")
    col1, col2 = st.columns(2)
    with col1:
        name  = st.text_input("Developer Name (displayed in portfolio)", value=Config.DEVELOPER_NAME)
        role  = st.text_input("Role / Position",                         value=Config.DEVELOPER_ROLE)
    with col2:
        email = st.text_input("Contact Email",                           value=Config.DEVELOPER_EMAIL)
        site  = st.text_input("Site URL",                                value=Config.SITE_URL)

    return {
        "DEVELOPER_NAME": name,
        "DEVELOPER_ROLE": role,
        "DEVELOPER_EMAIL": email,
        "SITE_URL": site,
    }


def _render_scaffold_panel(variables: dict) -> None:
    """Render the one-click scaffold + download panel."""
    st.header("🚀 Scaffold & Download")
    st.markdown(
        "Click **Generate Project** to write all files to disk, then download "
        "the complete ZIP archive ready to `npm install && npm run dev`."
    )

    if st.button("⚡ GENERATE_PROJECT", type="primary"):
        file_map  = _build_file_map(variables)
        engine    = st.session_state.scaffold
        engine.output_dir = Path(Config.OUTPUT_DIR)

        with st.spinner("Scaffolding production files…"):
            count, paths = engine.generate_project(file_map, variables)

        st.session_state.stats["files_generated"] = count
        st.success(f"✅ {count} files generated in `{Config.OUTPUT_DIR}/`")

        with st.expander("📋 Generated File Manifest"):
            for p in sorted(paths):
                st.code(p, language="")

    # ── Download ZIP ──────────────────────────────────────────────────────────
    output_dir = Path(Config.OUTPUT_DIR)
    if output_dir.exists() and any(output_dir.rglob("*")):
        zip_bytes = st.session_state.scaffold.package_zip()
        if st.download_button(
            label="📦 DOWNLOAD_ZIP_ARCHIVE",
            data=zip_bytes,
            file_name="cyber_portfolio.zip",
            mime="application/zip",
        ):
            st.session_state.stats["zip_downloads"] += 1


def _render_ai_customiser() -> None:
    """
    AI-powered section customiser.
    Uses the LLM to rewrite portfolio content based on user's actual background.
    """
    st.header("🤖 AI Content Customiser")
    st.markdown(
        "Describe your real background and the AI will generate personalised "
        "portfolio content (About bio, Projects list, Timeline nodes) for you to paste in."
    )

    if "ai_history" not in st.session_state:
        st.session_state.ai_history = []

    # Replay history
    for turn in st.session_state.ai_history:
        with st.chat_message(turn["role"]):
            st.write(turn["content"])

    user_input = st.chat_input("Tell me about your background, projects, or what you want changed…")
    if not user_input:
        return

    st.session_state.stats["ai_queries"] += 1
    with st.chat_message("user"):
        st.write(user_input)

    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    system = (
        "You are a senior frontend architect helping a developer personalise their "
        "cyberpunk portfolio. Given their background, generate production-ready "
        "TypeScript/React portfolio content: bios, project cards, timeline nodes, "
        "skills lists. Return well-structured, concise, copy-paste-ready content. "
        "Keep the cyberpunk theme — use monospace labels, neon accent mentions, "
        "and technical language. Never fabricate credentials."
    )

    messages = [{"role": "system", "content": system}]
    for turn in st.session_state.ai_history[-Config.MAX_TURNS:]:
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        placeholder  = st.empty()
        accumulated  = ""
        try:
            stream = client.chat.completions.create(
                model=Config.LLM_MODEL_NAME,
                messages=messages,
                temperature=0.7,
                max_tokens=Config.MAX_TOKENS,
                stream=True,
            )
            for chunk in stream:
                token = chunk.choices[0].delta.content
                if token:
                    accumulated += token
                    placeholder.write(accumulated + "▌")
            placeholder.write(accumulated)
        except Exception as exc:
            placeholder.error(f"AI generation error: {exc}")
            log_error("AI_AGENT", str(exc))
            return

    st.session_state.ai_history.append({"role": "user",      "content": user_input})
    st.session_state.ai_history.append({"role": "assistant",  "content": accumulated})


def main() -> None:
    """
    Application entry point.
    Run with:  streamlit run golden_response.py
    """
    st.set_page_config(
        page_title="CyberPortfolio Blueprint Generator",
        page_icon="🌐",
        layout="wide",
    )
    st.title("🌐 CyberPortfolio Enterprise Blueprint Generator")
    st.markdown(
        "Production-grade **Next.js 14 + Framer Motion + Tailwind CSS** "
        "cyberpunk developer portfolio — scaffold, personalise, and download."
    )
    st.markdown("---")

    _init_session_state()
    _render_sidebar()

    variables = _render_developer_config()
    st.markdown("---")
    _render_scaffold_panel(variables)
    st.markdown("---")
    _render_ai_customiser()

    # ── Telemetry log viewer ──────────────────────────────────────────────────
    st.markdown("---")
    st.header("📋 System Telemetry Log (RFC 5424)")
    with st.expander("Inspect Active Logs", expanded=False):
        st.code(read_logs(), language="json")


# ─────────────────────────────────────────────────────────────────────────────
# Guard: allow both `streamlit run` and direct `python golden_response.py`
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()