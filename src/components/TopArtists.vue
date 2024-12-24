<template>
  <section>
    <h2 class="text-4xl font-bold mb-8 text-center bg-gradient-to-r from-spotify-green to-blue-400 inline-block text-transparent bg-clip-text">
      Most added artists in {{ year }}
    </h2>
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div v-for="(artist, index) in topArtists" 
           :key="artist.name" 
           class="relative flex items-center gap-4 rounded-lg bg-black/20 p-4 transition-all hover:bg-black/30">
        <div class="relative h-16 w-16 flex-none">
          <div class="absolute -left-2 -top-2 flex h-8 w-8 items-center justify-center rounded-full bg-spotify-green text-sm font-bold">
            #{{ index + 1 }}
          </div>
          <img v-if="artist.image" 
               :src="artist.image" 
               :alt="artist.displayName"
               class="h-full w-full rounded-full object-cover"
               @error="handleImageError(artist)" />
          <div v-else 
               class="h-full w-full rounded-full bg-vinyl-light/10 flex items-center justify-center text-2xl">
            {{ artist.displayName[0] }}
          </div>
        </div>
        <div class="min-w-0 flex-auto">
          <a :href="artist.url" 
             target="_blank" 
             class="hover:text-spotify-green transition-colors">
            <h3 class="font-semibold truncate">{{ artist.displayName }}</h3>
          </a>
          <p class="mt-1 text-sm text-vinyl-light">{{ artist.count }} records</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  albums: {
    type: Array,
    required: true,
    default: () => []
  },
  year: {
    type: [Number, String],
    required: true
  }
})

function formatArtistName(artists) {
  if (Array.isArray(artists)) {
    // Join multiple artists with " & " and remove numbers in parentheses
    return artists.map(artist => artist.replace(/\s*\(\d+\)$/, '')).join(" & ")
  }
  // Remove numbers in parentheses from single artist
  return artists.replace(/\s*\(\d+\)$/, '')
}

// Compute top artists from the albums
const topArtists = computed(() => {
  const artistCounts = props.albums.reduce((acc, album) => {
    // Skip Various Artists - check both string and array cases
    if (album.artist === "Various" || 
        album.artist === "Various Artists" || 
        (Array.isArray(album.artist) && album.artist.includes("Various")) ||
        (Array.isArray(album.artist) && album.artist.includes("Various Artists"))) {
      return acc
    }

    const artistKey = Array.isArray(album.artist) ? album.artist.join(" & ") : album.artist
    if (!acc[artistKey]) {
      acc[artistKey] = {
        name: artistKey,
        displayName: formatArtistName(album.artist),
        count: 0,
        image: album.artist_image,
        url: album.artist_uri
      }
    }
    acc[artistKey].count++
    return acc
  }, {})

  return Object.values(artistCounts)
    .sort((a, b) => b.count - a.count)
    .slice(0, 16) // Get top 16 artists
})

function handleImageError(artist) {
  // If image fails to load, we'll just show the first letter
  artist.image = null
}
</script>
