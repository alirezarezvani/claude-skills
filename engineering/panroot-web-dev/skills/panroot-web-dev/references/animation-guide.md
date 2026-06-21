# Animation Guide — Panroot Web Dev

## Decision Tree: Which Animation Library?

| Effect | Library | Reason |
|--------|---------|--------|
| Scroll reveal, entrance, hover | Framer Motion | React-native, declarative |
| Counter, parallax, timeline, scrub | GSAP + ScrollTrigger | Best-in-class scroll performance |
| Hero background, particle field, shaders | Three.js + GLSL | GPU-accelerated, mouse-reactive |
| Pulsing dot, ticker, grid move | CSS @keyframes | Zero JS, prefers-reduced-motion safe |
| Page transitions | Framer Motion AnimatePresence | Route-level, smooth |

## GSAP ScrollTrigger Patterns

```js
// Parallax scrub
gsap.to(element, {
  yPercent: -30,
  ease: 'none',
  scrollTrigger: { trigger: section, scrub: 1, start: 'top bottom', end: 'bottom top' }
})

// Reveal on enter
gsap.from(elements, {
  y: 60, opacity: 0, stagger: 0.15, duration: 0.8, ease: 'power3.out',
  scrollTrigger: { trigger: section, start: 'top 80%', once: true }
})

// Horizontal scroll section
ScrollTrigger.create({
  trigger: panel,
  pin: true,
  scrub: 1,
  start: 'top top',
  end: () => `+=${panels.length * 100}%`,
})
```

## Three.js Hero Setup (React)

```tsx
import { useEffect, useRef } from 'react'
import * as THREE from 'three'

export function HeroCanvas() {
  const mountRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true })
    renderer.setSize(window.innerWidth, window.innerHeight)
    mountRef.current?.appendChild(renderer.domElement)

    const geometry = new THREE.PlaneGeometry(2, 2)
    const material = new THREE.ShaderMaterial({
      uniforms: {
        uTime: { value: 0 },
        uMouse: { value: new THREE.Vector2(0.5, 0.5) },
        uResolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) }
      },
      vertexShader: `varying vec2 vUv; void main() { vUv = uv; gl_Position = vec4(position, 1.0); }`,
      fragmentShader: FRAGMENT_SHADER,
      transparent: true
    })

    const mesh = new THREE.Mesh(geometry, material)
    scene.add(mesh)
    camera.position.z = 1

    // Mouse tracking
    const onMouseMove = (e: MouseEvent) => {
      material.uniforms.uMouse.value.set(e.clientX / window.innerWidth, 1 - e.clientY / window.innerHeight)
    }
    window.addEventListener('mousemove', onMouseMove)

    let raf: number
    const animate = () => {
      raf = requestAnimationFrame(animate)
      material.uniforms.uTime.value += 0.01
      renderer.render(scene, camera)
    }
    animate()

    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener('mousemove', onMouseMove)
      renderer.dispose()
      mountRef.current?.removeChild(renderer.domElement)
    }
  }, [])

  return <div ref={mountRef} className="absolute inset-0 pointer-events-none" />
}

const FRAGMENT_SHADER = `
  uniform float uTime;
  uniform vec2 uMouse;
  uniform vec2 uResolution;
  varying vec2 vUv;

  void main() {
    vec2 grid = fract(vUv * 24.0);
    float lineX = step(0.97, grid.x);
    float lineY = step(0.97, grid.y);
    float lines = lineX + lineY;
    
    float dist = distance(vUv, uMouse);
    float glow = smoothstep(0.5, 0.0, dist);
    
    float pulse = sin(uTime * 0.8 + vUv.x * 8.0 + vUv.y * 6.0) * 0.5 + 0.5;
    
    vec3 gridColor = vec3(0.0, 0.706, 0.847); // accent cyan
    vec3 base = vec3(0.04, 0.087, 0.157);     // primary navy
    
    vec3 color = mix(base, gridColor, lines * (pulse * 0.3 + glow * 0.4));
    float alpha = lines * (0.4 + glow * 0.6);
    
    gl_FragColor = vec4(color, alpha * 0.8);
  }
`
```

## Framer Motion Scroll Reveal — Standard Components

```tsx
// useScrollReveal hook
import { useInView } from 'framer-motion'
import { useRef } from 'react'

export function useScrollReveal(threshold = 0.1) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: '-10% 0px' })
  return { ref, isInView }
}

// Section wrapper
export function RevealSection({ children, delay = 0 }: { children: React.ReactNode, delay?: number }) {
  const { ref, isInView } = useScrollReveal()
  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.7, delay, ease: [0.22, 1, 0.36, 1] }}
    >
      {children}
    </motion.div>
  )
}
```

## Scroll-Driven Counter (Panroot Stats)

```tsx
'use client'
import { useEffect, useRef } from 'react'
import { useInView } from 'framer-motion'
import gsap from 'gsap'

export function AnimatedCounter({ target, suffix = '' }: { target: number, suffix?: string }) {
  const ref = useRef<HTMLSpanElement>(null)
  const isInView = useInView(ref, { once: true })

  useEffect(() => {
    if (!isInView || !ref.current) return
    const obj = { value: 0 }
    gsap.to(obj, {
      value: target,
      duration: 2.5,
      ease: 'power2.out',
      onUpdate: () => {
        if (ref.current) ref.current.textContent = Math.round(obj.value) + suffix
      }
    })
  }, [isInView, target, suffix])

  return <span ref={ref} className="font-mono text-accent">0{suffix}</span>
}
```
