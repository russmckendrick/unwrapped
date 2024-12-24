<template>
  <div class="relative group">
    <div class="overflow-x-auto hide-scrollbar">
      <div class="flex space-x-4 p-1">
        <div v-for="album in albums" :key="album.id" 
             class="flex-none w-48">
          <a :href="album.album_uri" 
             target="_blank" 
             class="block group/album relative rounded-lg overflow-hidden bg-vinyl-dark/40">
            <img :src="album.cover_image" 
                 :alt="album.title" 
                 class="w-full aspect-square object-cover transition-transform duration-300 group-hover/album:scale-110">
            <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/50 to-transparent opacity-0 group-hover/album:opacity-100 transition-all duration-300">
              <div class="absolute bottom-3 left-3 right-3">
                <div class="font-medium text-sm line-clamp-2">{{ album.title }}</div>
                <div class="text-vinyl-light text-xs mt-1">{{ album.artist.join(', ') }}</div>
              </div>
            </div>
          </a>
        </div>
      </div>
    </div>
    
    <!-- Scroll Indicators -->
    <div class="absolute left-0 top-0 bottom-0 w-20 bg-gradient-to-r from-vinyl-black to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
    <div class="absolute right-0 top-0 bottom-0 w-20 bg-gradient-to-l from-vinyl-black to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
    
    <!-- Scroll Buttons -->
    <button @click="scroll('left')" 
            class="absolute left-2 top-1/2 -translate-y-1/2 bg-vinyl-dark/90 text-white p-2 rounded-full opacity-0 group-hover:opacity-100 transition-opacity hover:bg-spotify-green/90 focus:outline-none">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    <button @click="scroll('right')" 
            class="absolute right-2 top-1/2 -translate-y-1/2 bg-vinyl-dark/90 text-white p-2 rounded-full opacity-0 group-hover:opacity-100 transition-opacity hover:bg-spotify-green/90 focus:outline-none">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  albums: {
    type: Array,
    required: true
  }
})

const scroll = (direction) => {
  const container = event.currentTarget.closest('.relative').querySelector('.overflow-x-auto')
  const albumWidth = 192 // width of each album (48px * 4)
  const scrollAmount = direction === 'left' ? -(albumWidth * 3) : (albumWidth * 3)
  container.scrollBy({
    left: scrollAmount,
    behavior: 'smooth'
  })
}
</script>

<style scoped>
.hide-scrollbar {
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>
