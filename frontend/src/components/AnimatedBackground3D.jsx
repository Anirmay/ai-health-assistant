import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

export const AnimatedBackground3D = ({ isDark }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Scene setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(isDark ? 0x0a0e27 : 0xf3f7ff, 1);
    containerRef.current.appendChild(renderer.domElement);

    camera.position.z = 5;

    // Create particle system
    const particleCount = 100;
    const particles = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const velocities = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount * 3; i += 3) {
      positions[i] = (Math.random() - 0.5) * 20;
      positions[i + 1] = (Math.random() - 0.5) * 20;
      positions[i + 2] = (Math.random() - 0.5) * 20;

      velocities[i] = (Math.random() - 0.5) * 0.1;
      velocities[i + 1] = (Math.random() - 0.5) * 0.1;
      velocities[i + 2] = (Math.random() - 0.5) * 0.1;
    }

    particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    const material = new THREE.PointsMaterial({
      color: isDark ? 0x0ff0ff : 0x2563eb,
      size: 0.1,
      sizeAttenuation: true,
      transparent: true,
      opacity: 0.6,
    });

    const particleSystem = new THREE.Points(particles, material);
    scene.add(particleSystem);

    // Create floating geometric shapes
    const geometries = [
      new THREE.IcosahedronGeometry(1, 3),
      new THREE.OctahedronGeometry(1),
      new THREE.TetrahedronGeometry(1),
    ];

    const shapes = [];
    geometries.forEach((geo, idx) => {
      const mesh = new THREE.Mesh(
        geo,
        new THREE.MeshPhongMaterial({
          color: [0x00ffff, 0xff00ff, 0x00ff88][idx],
          emissive: [0x00ffff, 0xff00ff, 0x00ff88][idx],
          emissiveIntensity: 0.3,
          wireframe: true,
        })
      );
      mesh.position.x = (idx - 1) * 4;
      mesh.position.y = Math.sin(idx) * 3;
      mesh.rotation.set(idx, idx, idx);
      scene.add(mesh);
      shapes.push({ mesh, speedX: 0.002 + idx * 0.001, speedY: 0.003 - idx * 0.001 });
    });

    // Lighting
    const light1 = new THREE.PointLight(0x00ffff, 1, 100);
    light1.position.set(10, 10, 10);
    scene.add(light1);

    const light2 = new THREE.PointLight(0xff00ff, 1, 100);
    light2.position.set(-10, -10, 10);
    scene.add(light2);

    // Mouse interactivity for parallax effect
    let mouseX = 0;
    let mouseY = 0;
    const handleMouseMove = (event) => {
      mouseX = (event.clientX / window.innerWidth) * 2 - 1;
      mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
    };
    window.addEventListener('mousemove', handleMouseMove);

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);

      // Update particles
      const pos = particles.attributes.position.array;
      for (let i = 0; i < particleCount * 3; i += 3) {
        pos[i] += velocities[i];
        pos[i + 1] += velocities[i + 1];
        pos[i + 2] += velocities[i + 2];

        if (pos[i] > 10 || pos[i] < -10) velocities[i] *= -1;
        if (pos[i + 1] > 10 || pos[i + 1] < -10) velocities[i + 1] *= -1;
        if (pos[i + 2] > 10 || pos[i + 2] < -10) velocities[i + 2] *= -1;
      }
      particles.attributes.position.needsUpdate = true;

      // Camera parallax effect
      camera.position.x += (mouseX * 2 - camera.position.x) * 0.05;
      camera.position.y += (mouseY * 2 - camera.position.y) * 0.05;
      camera.lookAt(scene.position);

      // Rotate shapes
      shapes.forEach((shape) => {
        shape.mesh.rotation.x += shape.speedX;
        shape.mesh.rotation.y += shape.speedY;
      });

      renderer.render(scene, camera);
    };

    animate();

    // Handle resize
    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      renderer.dispose();
      containerRef.current?.removeChild(renderer.domElement);
    };
  }, [isDark]);

  return <div ref={containerRef} className="fixed top-0 left-0 w-full h-full -z-10" />;
};
