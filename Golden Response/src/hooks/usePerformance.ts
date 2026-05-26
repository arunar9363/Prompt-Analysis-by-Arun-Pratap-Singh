import { useEffect, useRef, useState } from "react";

export function usePerformance() {
  const [fps, setFps] = useState(60);
  const frameCount = useRef(0);
  const lastTime = useRef(0);

  useEffect(() => {
    if (typeof window === "undefined") return;
    
    lastTime.current = performance.now();
    let animationFrameId: number;

    const tick = () => {
      frameCount.current++;
      const now = performance.now();
      const delta = now - lastTime.current;

      if (delta >= 1000) {
        const currentFps = Math.round((frameCount.current * 1000) / delta);
        setFps(currentFps);
        frameCount.current = 0;
        lastTime.current = now;
      }
      
      animationFrameId = requestAnimationFrame(tick);
    };

    animationFrameId = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(animationFrameId);
  }, []);

  return {
    fps,
    isLowPerformance: fps < 45,
  };
}
export default usePerformance;
