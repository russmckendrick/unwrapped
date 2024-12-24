<template>
  <div class="min-h-screen bg-gradient-to-b from-vinyl-black to-vinyl-dark text-white">
    <!-- Year Navigation -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-vinyl-black/80 backdrop-blur-sm border-b border-white/10">
      <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <div class="flex justify-center items-center space-x-4 mb-8">
          <router-link 
            v-if="currentYear === '2015'"
            :to="{ name: 'year', params: { year: '2016' }}"
            class="px-3 py-1 text-sm rounded-full bg-black/20 hover:bg-black/30 
                   text-vinyl-light hover:text-spotify-green transition-all duration-300
                   border border-spotify-green/10 hover:border-blue-400/20">
            ← 2016
          </router-link>
          <router-link 
            v-else-if="currentYear === '2024'"
            to="/"
            class="px-3 py-1 text-sm rounded-full bg-black/20 hover:bg-black/30 
                   text-vinyl-light hover:text-spotify-green transition-all duration-300
                   border border-spotify-green/10 hover:border-blue-400/20">
            ← Home
          </router-link>
          <router-link 
            v-else
            :to="{ name: 'year', params: { year: String(Number(currentYear) + 1) }}"
            class="px-3 py-1 text-sm rounded-full bg-black/20 hover:bg-black/30 
                   text-vinyl-light hover:text-spotify-green transition-all duration-300
                   border border-spotify-green/10 hover:border-blue-400/20">
            ← {{ Number(currentYear) + 1 }}
          </router-link>
        </div>
        <div class="flex space-x-4 items-center">
          <RouterLink 
            v-for="year in availableYears"
            :key="year"
            :to="'/' + year"
            class="px-2 py-1 rounded transition-colors"
            :class="year === currentYear ? 'bg-spotify-green text-white' : 'text-vinyl-light hover:text-white'">
            {{ year }}
          </RouterLink>
        </div>
        <div class="flex justify-center items-center space-x-4 mb-8">
          <router-link 
            v-if="currentYear === '2015'"
            to="/"
            class="px-3 py-1 text-sm rounded-full bg-black/20 hover:bg-black/30 
                   text-vinyl-light hover:text-spotify-green transition-all duration-300
                   border border-spotify-green/10 hover:border-blue-400/20">
            Home →
          </router-link>
          <router-link 
            v-else-if="currentYear === '2024'"
            :to="{ name: 'year', params: { year: '2023' }}"
            class="px-3 py-1 text-sm rounded-full bg-black/20 hover:bg-black/30 
                   text-vinyl-light hover:text-spotify-green transition-all duration-300
                   border border-spotify-green/10 hover:border-blue-400/20">
            2023 →
          </router-link>
          <router-link 
            v-else
            :to="{ name: 'year', params: { year: String(Number(currentYear) - 1) }}"
            class="px-3 py-1 text-sm rounded-full bg-black/20 hover:bg-black/30 
                   text-vinyl-light hover:text-spotify-green transition-all duration-300
                   border border-spotify-green/10 hover:border-blue-400/20">
            {{ Number(currentYear) - 1 }} →
          </router-link>
        </div>
      </div>
    </nav>

    <main class="pt-20"> 
      <div class="max-w-7xl mx-auto px-4 py-8">
        <!-- Title -->
        <h1 class="text-6xl font-bold text-center mb-2 bg-gradient-to-r from-spotify-green to-purple-400 inline-block w-full text-transparent bg-clip-text">
          Vinyl Unwrapped {{ currentYear }}
        </h1>
        <p class="text-center text-vinyl-light mb-12">
          Updates to my collection in {{ currentYear }}
        </p>

        <!-- Stats -->
        <section class="mb-12">
          <h2 class="text-4xl font-bold mb-8 text-center bg-gradient-to-r from-spotify-green to-blue-400 inline-block text-transparent bg-clip-text">
            {{ currentYear }} in Numbers
          </h2>
          
          <div class="grid grid-cols-3 gap-8 text-center">
            <div>
              <div class="text-5xl font-bold text-spotify-green mb-2">{{ collectionStats.totalRecords }}</div>
              <div class="text-sm text-vinyl-light">Records Added</div>
            </div>
            <div>
              <div class="text-5xl font-bold text-spotify-green mb-2">{{ collectionStats.topGenre }}</div>
              <div class="text-sm text-vinyl-light">Most Common Genre</div>
            </div>
            <div>
              <div class="text-5xl font-bold text-spotify-green mb-2">{{ collectionStats.avgPerMonth }}</div>
              <div class="text-sm text-vinyl-light">Avg Records/Month</div>
            </div>
          </div>
        </section>

        <!-- Charts Section -->
        <section class="grid md:grid-cols-2 gap-8 mb-12">
          <div>
            <h3 class="text-xl font-semibold mb-4">Genre Distribution</h3>
            <GenreCloud :data="genreData" />
          </div>
          <div>
            <h3 class="text-xl font-semibold mb-4">Records Added by Month</h3>
            <p class="text-sm text-vinyl-light mb-4">Click on a month to view its additions</p>
            <MonthlyChart :data="monthlyChartData" @month-click="scrollToMonth" />
          </div>
        </section>

      <!-- Top Artists -->
      <section class="mb-12">
        <TopArtists :albums="collection" :year="currentYear" />
      </section>

        <!-- Monthly Additions -->
        <section class="animate-fade-in">
          <h2 class="text-4xl font-bold mb-8 text-center bg-gradient-to-r from-spotify-green to-blue-400 inline-block text-transparent bg-clip-text">
            Additions to my collection in {{ currentYear }}
          </h2>
          
          <div class="relative space-y-12 before:absolute before:left-1/2 before:-translate-x-1/2 before:h-full before:w-0.5 before:bg-vinyl-light/20">
            <div v-for="month in monthlyCollections" 
                 :key="month.key" 
                 class="relative bg-black/20 rounded-lg p-6 before:absolute before:left-1/2 before:-translate-x-1/2 before:-top-3 before:w-6 before:h-6 before:rounded-full before:border-4 before:border-vinyl-light/20 before:bg-vinyl-black" 
                 :data-month="month.key">
              <div class="flex items-baseline mb-4">
                <h3 class="text-2xl font-semibold">{{ month.name }}</h3>
                <span class="ml-3 text-sm text-vinyl-light">{{ month.albums.length }} records added</span>
              </div>
              <AlbumSlider :albums="month.albums" />
            </div>
          </div>
        </section>
      </div>
    </main>

    <footer class="max-w-7xl mx-auto px-4 py-8 text-center">
      <div class="flex justify-center space-x-4 mb-4">
        <RouterLink 
          v-if="nextYear"
          :to="'/' + nextYear" 
          class="text-sm font-medium text-vinyl-light hover:text-white transition-colors">
          ← {{ nextYear }}
        </RouterLink>
        <RouterLink 
          v-if="previousYear"
          :to="'/' + previousYear" 
          class="text-sm font-medium text-vinyl-light hover:text-white transition-colors">
          {{ previousYear }} →
        </RouterLink>
      </div>
      <p class="text-sm text-vinyl-light">Data from my vinyl collection</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import AlbumSlider from '../components/AlbumSlider.vue'
import MonthlyChart from '../components/MonthlyChart.vue'
import GenreCloud from '../components/GenreCloud.vue'
import TopArtists from '../components/TopArtists.vue'
import dayjs from 'dayjs'

const route = useRoute()
const props = defineProps({
  year: {
    type: String,
    required: true
  }
})

const collection = ref([])
const currentYear = computed(() => props.year)

// Get available years from the route params
const availableYears = ref(['2024', '2023', '2022', '2021', '2020',
  '2019', '2018', '2017', '2016', '2015'].sort((a, b) => b - a))

const previousYear = computed(() => {
  const idx = availableYears.value.indexOf(currentYear.value)
  return idx < availableYears.value.length - 1 ? availableYears.value[idx + 1] : null
})

const nextYear = computed(() => {
  const idx = availableYears.value.indexOf(currentYear.value)
  return idx > 0 ? availableYears.value[idx - 1] : null
})

// Function to load data for a specific year
const loadYearData = async (year) => {
  try {
    // Reset data first
    collection.value = []
    
    const response = await fetch(`/collection_${year}.json`)
    
    if (!response.ok) {
      throw new Error('Failed to fetch collection data')
    }
    
    // Update collection data
    collection.value = await response.json()
  } catch (error) {
    console.error('Error loading data:', error)
    collection.value = []
  }
}

// Watch for route changes
watch(() => route.params.year, async (newYear) => {
  if (newYear) {
    await loadYearData(newYear)
  }
}, { immediate: true })

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
  )).size || 1 // Avoid division by zero
  
  return {
    totalRecords: collection.value.length,
    topGenre,
    avgPerMonth: Math.round(collection.value.length / months)
  }
})

const genreData = computed(() => {
  if (!collection.value.length) return []
  
  const genres = collection.value.flatMap(record => record.genres)
  const genreCounts = genres.reduce((acc, genre) => {
    acc[genre] = (acc[genre] || 0) + 1
    return acc
  }, {})
  
  return Object.entries(genreCounts)
    .map(([text, value]) => ({ text, value }))
    .sort((a, b) => b.value - a.value)
})

const monthlyChartData = computed(() => {
  if (!collection.value.length) return []
  
  const monthCounts = collection.value.reduce((acc, record) => {
    const month = dayjs(record.date_added).format('MMMM')
    acc[month] = (acc[month] || 0) + 1
    return acc
  }, {})
  
  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ]
  
  return months.map(month => ({
    month,
    count: monthCounts[month] || 0
  }))
})

const monthlyCollections = computed(() => {
  if (!collection.value.length) return []
  
  // Create array for all months of the year
  const allMonths = Array.from({ length: 12 }, (_, i) => {
    const date = dayjs(`${currentYear.value}-${i + 1}-01`)
    return {
      key: date.format('YYYY-MM'),
      name: date.format('MMMM YYYY'),
      albums: []
    }
  })

  // Group albums by month
  collection.value.forEach(record => {
    const monthIndex = dayjs(record.date_added).month()
    allMonths[monthIndex].albums.push(record)
  })

  // Sort albums within each month
  allMonths.forEach(month => {
    month.albums.sort((a, b) => 
      dayjs(a.date_added).valueOf() - dayjs(b.date_added).valueOf()
    )
  })

  // Only return months that have albums
  return allMonths.filter(month => month.albums.length > 0)
})

function scrollToMonth(monthName) {
  try {
    console.log('YearView: scrollToMonth called', { monthName })

    // Validate month name
    if (!monthName) {
      console.error('YearView: Invalid month name', { monthName })
      return
    }

    // Map full month names to numbers
    const monthMap = {
      'January': '01', 'February': '02', 'March': '03', 'April': '04',
      'May': '05', 'June': '06', 'July': '07', 'August': '08',
      'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }

    // Get month number
    const monthNumber = monthMap[monthName]
    if (!monthNumber) {
      console.error('YearView: Invalid month name', { monthName })
      return
    }

    // Create the month key directly
    const monthKey = `${currentYear.value}-${monthNumber}`
    console.log('YearView: Generated month key', { monthKey, monthName, currentYear: currentYear.value })
    
    const monthElement = document.querySelector(`[data-month="${monthKey}"]`)
    console.log('YearView: Found month element', { found: !!monthElement, monthKey })
    
    if (monthElement) {
      // Get the element's position relative to the viewport
      const rect = monthElement.getBoundingClientRect()
      const absoluteTop = window.pageYOffset + rect.top - 80 // 80px for header offset
      console.log('YearView: Calculated scroll position', { 
        rectTop: rect.top,
        pageYOffset: window.pageYOffset,
        absoluteTop 
      })
      
      // Use a more basic scrolling approach that works in Safari
      console.log('YearView: Attempting smooth scroll')
      window.scroll({
        top: absoluteTop,
        behavior: 'smooth'
      })
      
      // Fallback for Safari if smooth scroll doesn't work
      const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent)
      console.log('YearView: Browser detection', { isSafari })
      
      if (isSafari) {
        console.log('YearView: Safari detected, using fallback')
        window.scrollTo(0, absoluteTop)
      }
    }
  } catch (error) {
    console.error('YearView: Error in scrollToMonth', error)
  }
}
</script>
