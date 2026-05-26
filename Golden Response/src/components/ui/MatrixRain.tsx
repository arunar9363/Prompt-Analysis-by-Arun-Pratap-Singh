"use client";

import React, { useEffect, useRef } from "react";
import { usePerformance } from "@/hooks/usePerformance";
import { useReducedMotion } from "@/hooks/useReducedMotion";

export const MatrixRain: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const { isLowPerformance } = usePerformance();
  const shouldReduce = useReducedMotion();

  useEffect(() => {
    if (shouldReduce) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let resizeTimer: NodeJS.Timeout;
    const resizeCanvas = () => {
      if (canvas && canvas.parentElement) {
        canvas.width = canvas.parentElement.clientWidth || window.innerWidth;
        canvas.height = canvas.parentElement.clientHeight || window.innerHeight;
      }
    };

    // Debounced resize to avoid layout thrashing
    const handleResize = () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(resizeCanvas, 150);
    };

    resizeCanvas();
    window.addEventListener("resize", handleResize);

    // Character set
    const chars = "010101ABCDEF//[]{}<>_+$#@!%&*()-+=";
    const charArray = chars.split("");

    const fontSize = 15;
    let columns = Math.floor(canvas.width / fontSize);
    let drops: number[] = Array(columns).fill(1);

    // Performance adaptation: reduce draw speed on low performance devices
    const fpsInterval = isLowPerformance ? 1000 / 12 : 1000 / 24;
    let then = performance.now();
    let animationFrameId: number;

    const draw = (now: number) => {
      animationFrameId = requestAnimationFrame(draw);

      const elapsed = now - then;
      if (elapsed < fpsInterval) return;
      then = now - (elapsed % fpsInterval);

      // Black background paint with opacity to leave trails
      ctx.fillStyle = "rgba(5, 5, 10, 0.12)";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.font = `bold ${fontSize}px var(--font-space-mono), monospace`;

      for (let i = 0; i < drops.length; i++) {
        const char = charArray[Math.floor(Math.random() * charArray.length)];

        // Dynamic theme-matching cyberpunk colors
        // Alternate between neon-cyan, electric-purple, and hot-pink
        const colorPalette = ["#00f0ff", "#9d4edd", "#ff007f", "#004bba"];
        ctx.fillStyle = colorPalette[i % colorPalette.length];

        const x = i * fontSize;
        const y = drops[i] * fontSize;

        ctx.fillText(char, x, y);

        // Reset drop state randomly once it hits the bottom
        if (y > canvas.height && Math.random() > 0.982) {
          drops[i] = 0;
        }

        drops[i]++;
      }
    };

    animationFrameId = requestAnimationFrame(draw);

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener("resize", handleResize);
      clearTimeout(resizeTimer);
    };
  }, [isLowPerformance, shouldReduce]);

  if (shouldReduce) return null;

  return (
    <canvas
      ref={canvasRef}
      className="matrix-canvas-layer pointer-events-none absolute inset-0 w-full h-full"
      style={{ mixBlendMode: "screen", opacity: 0.15 }}
      aria-hidden="true"
    />
  );
};
export default MatrixRain;
