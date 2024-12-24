<template>
  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router'
import { ref, computed, onMounted } from 'vue'
import AlbumSlider from './components/AlbumSlider.vue'
import MonthlyChart from './components/MonthlyChart.vue'
import GenreCloud from './components/GenreCloud.vue'
import TopArtists from './components/TopArtists.vue'
import dayjs from 'dayjs'

const collection = ref([])
const lastfmData = ref({})

// Fetch data
onMounted(async () => {
  try {
    const [collectionResponse, lastfmResponse] = await Promise.all([
      fetch('/collection_2024.json'),
      fetch('/lastfm_2024.json')
    ])
    
    collection.value = await collectionResponse.json()
    lastfmData.value = await lastfmResponse.json()
  } catch (error) {
    console.error('Error loading data:', error)
  }
})

// Computed properties
const collectionStats = computed(() => {
  if (!collection.value.length) return { 
    totalRecords: 0, 
    topGenre: '-',
    avgPerMonth: 0
  }
  
  const genres = collection.value.flatMap(record => record.genres)
  const genreCounts = genres.reduce((acc, genre) => {
    acc[genre] = (acc[genre] || 0) + 1
    return acc
  }, {})
  
  const topGenre = Object.entries(genreCounts)
    .sort((a, b) => b[1] - a[1])[0][0]
  
  // Calculate average records per month
  const months = new Set(collection.value.map(record => 
    dayjs(record.date_added).format('YYYY-MM')
  )).size
  
  return {
    totalRecords: collection.value.length,
    topGenre,
    avgPerMonth: Math.round(collection.value.length / months)
  }
})

const topArtists = computed(() => {
  return lastfmData.value.top_artists?.slice(0, 6) || []
})

const monthlyAdditions = computed(() => {
  if (!collection.value.length) return []
  
  const months = {}
  collection.value.forEach(record => {
    const date = dayjs(record.date_added)
    const monthKey = date.format('YYYY-MM')
    const monthName = date.format('MMMM YYYY')
    
    if (!months[monthKey]) {
      months[monthKey] = {
        month: monthKey,
        monthName,
        albums: []
      }
    }
    months[monthKey].albums.push(record)
  })

  // Sort albums within each month by date_added
  Object.values(months).forEach(month => {
    month.albums.sort((a, b) => dayjs(a.date_added).valueOf() - dayjs(b.date_added).valueOf())
  })
  
  // Sort months chronologically (oldest to newest)
  return Object.values(months)
    .sort((a, b) => dayjs(a.month).valueOf() - dayjs(b.month).valueOf())
})

const monthlyChartData = computed(() => {
  if (!monthlyAdditions.value.length) return { labels: [], datasets: [] }
  
  const sortedMonths = monthlyAdditions.value
    .sort((a, b) => dayjs(a.month).valueOf() - dayjs(b.month).valueOf())
  
  const labels = sortedMonths.map(month => month.monthName)
  console.log('Chart labels:', labels)
  
  return {
    labels,
    datasets: [{
      data: sortedMonths.map(month => month.albums.length),
      backgroundColor: [
        '#1DB954', // Spotify green
        '#3B82F6', // Blue
        '#8B5CF6', // Purple
        '#EC4899', // Pink
        '#F59E0B', // Orange
        '#06B6D4', // Cyan
        '#6366F1', // Indigo
        '#D946EF', // Fuchsia
        '#F97316', // Orange
        '#14B8A6', // Teal
        '#A855F7', // Purple
        '#EF4444'  // Red
      ],
      borderRadius: 6,
      hoverBackgroundColor: '#3B82F1'
    }]
  }
})

const genreData = computed(() => {
  if (!collection.value.length) return { labels: [], datasets: [] }
  
  const genres = collection.value.flatMap(record => record.genres)
  const genreCounts = genres.reduce((acc, genre) => {
    acc[genre] = (acc[genre] || 0) + 1
    return acc
  }, {})
  
  const sortedGenres = Object.entries(genreCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
  
  return {
    labels: sortedGenres.map(([genre]) => genre),
    datasets: [{
      label: 'Records',
      data: sortedGenres.map(([, count]) => count),
      backgroundColor: [
        '#1DB954', // Spotify green
        '#3B82F6', // Blue
        '#8B5CF6', // Purple
        '#EC4899', // Pink
        '#F59E0B', // Orange
        '#06B6D4', // Cyan
        '#6366F1', // Indigo
        '#D946EF', // Fuchsia
        '#F97316', // Orange
        '#14B8A6'  // Teal
      ]
    }]
  }
})

// Scroll to month function
const scrollToMonth = (monthName) => {
  console.log('Attempting to scroll to:', monthName)
  const monthId = monthName.toLowerCase()
  console.log('Looking for element with ID:', monthId)
  const element = document.getElementById(monthId)
  
  if (element) {
    console.log('Found element, scrolling to:', element)
    element.scrollIntoView({ 
      behavior: 'smooth', 
      block: 'start',
      inline: 'nearest'
    })
  } else {
    console.warn('Element not found for month:', monthName)
  }
}
</script>
