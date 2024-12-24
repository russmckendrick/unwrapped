<template>
  <div class="style-cloud-container relative w-full h-full overflow-hidden">
    <div ref="cloudContainer" class="style-cloud w-full h-full">
      <div
        v-for="(word, index) in words"
        :key="index"
        class="word absolute transition-all duration-500 cursor-pointer"
        :class="{ 'z-50': word.isActive }"
        :style="{
          left: `${word.x}px`,
          top: `${word.y}px`,
          transform: `translate(-50%, -50%) rotate(${word.rotate}deg) scale(${word.isActive ? 1.5 : 1})`,
          color: word.color,
          opacity: word.opacity
        }"
        @click="handleClick(index)"
      >
        <div class="flex flex-col items-center relative">
          <span class="word-text">{{ word.text }}</span>
          <span 
            v-if="word.isActive" 
            class="count-badge text-sm opacity-90 mt-1"
          >
            {{ word.count }} {{ word.count === 1 ? 'appearance' : 'appearances' }}
          </span>
          
          <!-- Album Preview Card -->
          <div v-if="word.isActive && word.albums" 
               class="album-preview absolute z-50 bg-vinyl-black/95 rounded-lg p-2 shadow-xl"
               :style="{
                 left: '50%',
                 transform: 'translateX(-50%)',
                 top: 'calc(100% + 5px)',
                 width: '400px'
               }"
               @wheel.stop
               @touchmove.stop
               @scroll.stop>
            <div class="flex flex-col gap-1">
              <div class="text-xs text-gray-400 text-center mb-1">
                <span v-if="word.albums.length > 3">Scroll to see all albums ↓</span>
                <span v-else>&nbsp;</span>
              </div>
              <div class="grid gap-2 max-h-[240px] overflow-y-auto custom-scrollbar pr-3"
                   :class="{
                     'grid-cols-1 justify-items-center': word.albums.length === 1,
                     'grid-cols-2 justify-items-center': word.albums.length === 2,
                     'grid-cols-3': word.albums.length >= 3
                   }"
                   style="min-height: 240px;"
                   @wheel.stop
                   @touchmove.stop
                   @scroll.stop>
                <div v-for="album in word.albums" 
                     :key="album.id"
                     class="aspect-square w-full max-w-[110px]">
                  <img :src="album.cover" 
                       :alt="album.title"
                       class="w-full h-full object-cover rounded-md">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as d3 from 'd3'
import cloud from 'd3-cloud'
import dayjs from 'dayjs'

const props = defineProps({
  data: {
    type: Array,
    required: true
  }
})

const cloudContainer = ref(null)
const words = ref([])

const colors = [
  '#1DB954', // Spotify green
  '#FF0080', // Hot pink
  '#00BCD4', // Cyan
  '#FF9800', // Orange
  '#E91E63', // Pink
  '#9C27B0', // Purple
  '#4CAF50', // Green
  '#2196F3'  // Blue
]

const BASE_FONT_SIZE = 32
const PUSH_DISTANCE = 180

function initializeWords() {
  const container = cloudContainer.value
  if (!container) return

  const { width, height } = container.getBoundingClientRect()
  const padding = 2
  
  // Create word objects for the cloud layout
  const wordObjects = props.data.map((word, i) => ({
    text: word.text,
    size: BASE_FONT_SIZE,
    count: word.value,
    color: colors[i % colors.length],
    opacity: 0.9,
    rotate: (~~(Math.random() * 6) - 3) * 15,
    isActive: false,
    albums: word.albums // Include albums data
  }))

  // Create the cloud layout
  const layout = cloud()
    .size([width * 0.95, height * 0.95])
    .words(wordObjects)
    .padding(padding)
    .rotate(d => d.rotate)
    .fontSize(d => d.size)
    .spiral('archimedean')
    .on('end', cloudWords => {
      words.value = cloudWords.map(word => ({
        ...word,
        x: word.x + width / 2,
        y: word.y + height / 2,
        isActive: false,
        albums: word.albums // Preserve albums data
      }))
    })

  layout.start()
}

function handleClick(index) {
  const wasActive = words.value[index].isActive
  const centerX = cloudContainer.value.clientWidth / 2
  const clickedWord = words.value[index]

  // If clicking an active word or clicking a different word, reset all first
  if (wasActive || words.value.some(w => w.isActive && w !== clickedWord)) {
    resetAllWords()
    if (wasActive) return // If clicking active word, just reset all
  }

  // Otherwise, activate the clicked word and move it to the top
  words.value = words.value.map((word, i) => {
    if (i === index) {
      return {
        ...word,
        isActive: true,
        originalX: word.x,
        originalY: word.y,
        originalRotate: word.rotate,
        x: centerX,
        y: 80, // Position near the top
        rotate: 0,
        opacity: 1
      }
    } else {
      // Push other words down and away
      const dx = word.x - clickedWord.x
      const dy = word.y - clickedWord.y
      const distance = Math.sqrt(dx * dx + dy * dy)
      const angle = Math.atan2(dy, dx)
      
      const pushForce = Math.max(0, 1 - distance / (PUSH_DISTANCE * 2))
      const pushX = Math.cos(angle) * PUSH_DISTANCE * pushForce
      const pushY = Math.sin(angle) * PUSH_DISTANCE * pushForce + 100 // Add extra downward push

      return {
        ...word,
        isActive: false,
        originalX: word.x,
        originalY: word.y,
        x: word.x + pushX,
        y: word.y + pushY,
        opacity: 0.3
      }
    }
  })
}

function resetAllWords() {
  words.value = words.value.map(word => ({
    ...word,
    isActive: false,
    x: word.originalX || word.x,
    y: word.originalY || word.y,
    rotate: word.originalRotate || word.rotate,
    opacity: 0.9
  }))
}

function handleClickOutside(event) {
  if (!event.target.closest('.word')) {
    resetAllWords()
  }
}

onMounted(() => {
  initializeWords()
  window.addEventListener('click', handleClickOutside)
  
  const handleResize = () => {
    resetAllWords() // Reset positions before reinitializing
    initializeWords()
  }
  window.addEventListener('resize', handleResize)
  
  onUnmounted(() => {
    window.removeEventListener('click', handleClickOutside)
    window.removeEventListener('resize', handleResize)
  })
})

watch(() => props.data, initializeWords)
</script>

<style scoped>
.style-cloud-container {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
}

.word {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  white-space: nowrap;
  cursor: pointer;
  user-select: none;
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 32px;
  font-weight: 700;
}

.count-badge {
  background: rgba(29, 185, 84, 0.2);
  padding: 1px 6px;
  border-radius: 10px;
  white-space: nowrap;
  font-size: 0.75rem;
}

.album-preview {
  border: 1px solid rgba(29, 185, 84, 0.2);
  backdrop-filter: blur(8px);
}

.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: rgba(29, 185, 84, 0.5) rgba(255, 255, 255, 0.1);
  -webkit-overflow-scrolling: touch;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 8px; /* Slightly wider for easier grabbing */
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  margin: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(29, 185, 84, 0.5);
  border-radius: 4px;
  border: 2px solid rgba(0, 0, 0, 0.2);
  min-height: 40px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(29, 185, 84, 0.7);
}
</style>
