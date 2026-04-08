import React, { useEffect, useRef } from 'react';

export default function AnimatedGradientBackground() {
  const containerRef = useRef(null);

  useEffect(() => {
    const canvas = containerRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let animationId;

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    let time = 0;
    const animate = () => {
      time += 0.01;
      
      const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
      
      const hue1 = (time * 20) % 360;
      const hue2 = (time * 15 + 120) % 360;
      const hue3 = (time * 10 + 240) % 360;
      
      gradient.addColorStop(0, `hsl(${hue1}, 100%, 50%)`);
      gradient.addColorStop(0.5, `hsl(${hue2}, 80%, 40%)`);
      gradient.addColorStop(1, `hsl(${hue3}, 90%, 30%)`);
      
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Add some noise/texture
      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const data = imageData.data;
      
      for (let i = 0; i < data.length; i += 4) {
        const noise = Math.random() * 5;
        data[i] += noise;
        data[i + 1] += noise;
        data[i + 2] += noise;
      }
      
      ctx.putImageData(imageData, 0, 0);
      
      animationId = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      cancelAnimationFrame(animationId);
    };
  }, []);

  return (
    <canvas
      ref={containerRef}
      className="fixed top-0 left-0 w-full h-full -z-10 opacity-40"
    />
  );
}
