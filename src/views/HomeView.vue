<template>
  <div class="relative min-h-screen">
    <div id="bg-canvas" class="fixed inset-0 -z-10"></div>
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-6xl font-bold text-center mb-4">
        <span class="bg-gradient-to-r from-spotify-green to-blue-400 inline-block text-transparent bg-clip-text">Vinyl Unwrapped</span>
      </h1>
      <p class="text-vinyl-light text-center mb-16">Select a Year to View My Vinyl Journey</p>
      
      <div class="flex justify-center">
        <div class="relative w-full max-w-xl">
          <!-- Timeline line -->
          <div class="absolute left-1/2 w-0.5 top-0 bottom-0 transform -translate-x-1/2">
            <div class="h-full bg-gradient-to-b from-spotify-green via-blue-400 to-spotify-green motion-safe:animate-pulse"></div>
          </div>
          
          <!-- Years -->
          <div class="relative py-12 space-y-32">
            <template v-for="year in years" :key="year">
              <router-link 
                :to="{ name: 'year', params: { year }}"
                class="group block relative"
              >
                <!-- Year node -->
                <div class="absolute left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10">
                  <div class="w-4 h-4 rounded-full bg-gradient-to-br from-spotify-green to-blue-400 group-hover:from-blue-400 group-hover:to-spotify-green transition-all duration-500 ease-in-out 
                            motion-safe:group-hover:scale-150 group-hover:shadow-lg group-hover:shadow-blue-400/50
                            border border-white/10 group-hover:border-white/20"></div>
                </div>
                
                <!-- Year content -->
                <div class="ml-16 relative">
                  <!-- Connecting line -->
                  <div class="absolute left-0 top-1/2 h-0.5 w-8 bg-gradient-to-r from-spotify-green to-blue-400 
                            group-hover:from-blue-400 group-hover:to-spotify-green transform -translate-y-1/2 
                            motion-safe:group-hover:w-12 transition-all duration-500
                            motion-safe:group-hover:scale-y-150"></div>
                  
                  <!-- Year card -->
                  <div class="bg-black/20 backdrop-blur-xl rounded-xl p-8 
                            group-hover:bg-black/30 transition-all duration-500 ease-in-out 
                            transform motion-safe:group-hover:translate-x-4 
                            group-hover:shadow-xl group-hover:shadow-spotify-green/10
                            border border-white/5 group-hover:border-white/10
                            motion-safe:hover:scale-105">
                    <div class="flex items-center justify-between">
                      <!-- Left side - Year -->
                      <div class="flex items-center space-x-8">
                        <div class="text-6xl font-bold bg-gradient-to-br from-white to-white/70 bg-clip-text text-transparent 
                                  transition-all duration-500 group-hover:from-spotify-green group-hover:to-blue-400
                                  motion-safe:group-hover:scale-110">
                          {{ year }}
                        </div>
                        <div class="h-16 w-px bg-gradient-to-b from-spotify-green/20 to-blue-400/20 
                                  group-hover:from-spotify-green/40 group-hover:to-blue-400/40 transition-all duration-500"></div>
                      </div>
                      
                      <!-- Right side - Stats -->
                      <div class="text-right">
                        <div class="text-5xl font-bold bg-gradient-to-br from-white/90 to-white/70 bg-clip-text text-transparent
                                  group-hover:from-spotify-green group-hover:to-blue-400 transition-all duration-500">
                          {{ yearData[year]?.length || 0 }}
                        </div>
                        <div class="text-sm text-vinyl-light/60 group-hover:text-vinyl-light/90 transition-colors duration-500">
                          Additions
                        </div>
                      </div>
                    </div>
                    
                    <!-- Additional year stats -->
                    <div class="mt-4 flex items-center justify-end text-sm">
                      <div class="flex items-center space-x-3 text-vinyl-light/60 group-hover:text-vinyl-light/90 transition-colors duration-500
                                px-4 py-2 rounded-lg bg-black/20 group-hover:bg-black/30 backdrop-blur-sm">
                        <span>{{ formatDate(yearData[year]?.[0]?.date_added) }}</span>
                        <span>→</span>
                        <span>{{ formatDate(yearData[year]?.[yearData[year]?.length - 1]?.date_added) }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'
import * as THREE from 'three'

// Order years from newest to oldest for vertical timeline
const years = ['2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015']
const yearData = ref({})

// Load data for each year
onMounted(async () => {
  try {
    for (const year of years) {
      const response = await fetch(`/collection_${year}.json`)
      const data = await response.json()
      yearData.value[year] = data.sort((a, b) => new Date(a.date_added) - new Date(b.date_added))
    }
  } catch (error) {
    console.error('Error loading year data:', error)
  }
})

// Format date to DD/MM
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getDate().toString().padStart(2, '0')}/${(date.getMonth() + 1).toString().padStart(2, '0')}`
}

let scene, camera, renderer, waves = []

onMounted(() => {
  initThree()
  animate()
  window.addEventListener('resize', onWindowResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', onWindowResize)
  if (renderer) {
    renderer.dispose()
    const container = document.getElementById('bg-canvas')
    if (container && container.firstChild) {
      container.removeChild(container.firstChild)
    }
  }
})

function initThree() {
  const container = document.getElementById('bg-canvas')
  if (!container) return

  scene = new THREE.Scene()
  camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000)
  
  renderer = new THREE.WebGLRenderer({ 
    antialias: true,
    alpha: true 
  })
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setClearColor(0x000000, 0)
  container.appendChild(renderer.domElement)

  // Create multiple wave lines
  const numLines = 60
  const points = 150
  const lineSpacing = 0.12
  
  for (let i = 0; i < numLines; i++) {
    const lineGeometry = new THREE.BufferGeometry()
    const linePositions = new Float32Array(points * 3)
    
    for (let j = 0; j < points; j++) {
      const x = (j - points/2) * 0.15
      const y = (i - numLines/2) * lineSpacing
      const z = 0
      
      linePositions[j * 3] = x
      linePositions[j * 3 + 1] = y
      linePositions[j * 3 + 2] = z
    }
    
    lineGeometry.setAttribute('position', new THREE.BufferAttribute(linePositions, 3))
    
    const lineMaterial = new THREE.LineBasicMaterial({ 
      color: 0x2ed573,
      transparent: true,
      opacity: 0.5
    })
    
    const line = new THREE.Line(lineGeometry, lineMaterial)
    waves.push({
      line,
      positions: linePositions,
      offset: i * 0.1
    })
    scene.add(line)
  }

  camera.position.z = 8
}

function animate() {
  requestAnimationFrame(animate)
  
  const time = Date.now() * 0.001
  
  waves.forEach((wave, waveIndex) => {
    const positions = wave.positions
    const points = positions.length / 3
    
    for (let i = 0; i < points; i++) {
      const x = positions[i * 3]
      
      // Create the mountain-like peaks
      const baseY = positions[i * 3 + 1]
      const peakHeight = Math.sin(x * 0.5 + time + wave.offset) * 0.3
      const noise = Math.sin(x * 2 + time * 2) * 0.05
      
      // Add more variation for the mountain effect
      const mountainEffect = Math.exp(-Math.abs(x * 0.5)) * 0.8
      const finalY = baseY + peakHeight * mountainEffect + noise
      
      positions[i * 3 + 1] = finalY
    }
    
    wave.line.geometry.attributes.position.needsUpdate = true
  })
  
  renderer.render(scene, camera)
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
}
</script>

<style scoped>
.container {
  max-width: 1200px;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Custom animation for the timeline line */
@keyframes glow {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 0.8; }
}

.animate-pulse {
  animation: glow 3s ease-in-out infinite;
}
</style>
