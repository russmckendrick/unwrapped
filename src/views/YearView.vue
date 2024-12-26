<template>
  <div class="min-h-screen bg-gradient-to-b from-vinyl-black to-vinyl-dark text-white">
    <!-- Year Navigation -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-vinyl-black/80 backdrop-blur-sm border-b border-white/10">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <!-- Left side - Home link -->
          <router-link 
            to="/"
            class="text-vinyl-light hover:text-spotify-green transition-all duration-300 text-lg font-medium">
            Vinyl Unwrapped
          </router-link>

          <!-- Center - Desktop Years -->
          <div class="hidden md:flex space-x-2">
            <RouterLink 
              v-for="year in availableYears"
              :key="year"
              :to="'/' + year"
              class="px-3 py-1.5 rounded-full transition-all duration-300 text-center text-sm font-medium"
              :class="[
                year === currentYear 
                  ? 'bg-spotify-green text-white' 
                  : 'text-vinyl-light hover:text-white hover:bg-vinyl-light/10'
              ]">
              {{ year }}
            </RouterLink>
          </div>

          <!-- Right side - Mobile Menu Button -->
          <button 
            @click="isMenuOpen = !isMenuOpen"
            class="md:hidden p-2 text-vinyl-light hover:text-spotify-green focus:outline-none"
            aria-label="Toggle menu">
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              class="h-6 w-6" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor">
              <path 
                v-if="!isMenuOpen"
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="2" 
                d="M4 6h16M4 12h16M4 18h16" />
              <path 
                v-else
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="2" 
                d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Mobile Menu -->
        <transition
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="transform -translate-y-2 opacity-0"
          enter-to-class="transform translate-y-0 opacity-100"
          leave-active-class="transition duration-150 ease-in"
          leave-from-class="transform translate-y-0 opacity-100"
          leave-to-class="transform -translate-y-2 opacity-0">
          <div 
            v-show="isMenuOpen"
            class="md:hidden mt-4">
            <div class="grid grid-cols-3 gap-2">
              <RouterLink 
                v-for="year in availableYears"
                :key="year"
                :to="'/' + year"
                class="px-2 py-2 rounded-lg transition-all duration-300 text-center text-sm font-medium"
                :class="[
                  year === currentYear 
                    ? 'bg-spotify-green text-white' 
                    : 'text-vinyl-light hover:text-white hover:bg-vinyl-light/10'
                ]"
                @click="isMenuOpen = false">
                {{ year }}
              </RouterLink>
            </div>
          </div>
        </transition>
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
          
          <div class="grid grid-cols-2 md:grid-cols-3 gap-4 md:gap-8 text-center">
            <!-- Most Common Style - Full width on mobile -->
            <div class="col-span-2 md:col-span-1 md:order-2 mb-4 md:mb-0">
              <div class="text-4xl md:text-5xl font-bold text-spotify-green mb-2">{{ collectionStats.topStyle }}</div>
              <div class="text-sm text-vinyl-light">Most Common Style</div>
            </div>
            
            <!-- Records Added -->
            <div class="md:order-1">
              <div class="text-4xl md:text-5xl font-bold text-spotify-green mb-2">{{ collectionStats.totalRecords }}</div>
              <div class="text-sm text-vinyl-light">Records Added</div>
            </div>
            
            <!-- Average Records per Month -->
            <div class="md:order-3">
              <div class="text-4xl md:text-5xl font-bold text-spotify-green mb-2">{{ collectionStats.avgPerMonth }}</div>
              <div class="text-sm text-vinyl-light">Avg Records/Month</div>
            </div>
          </div>
        </section>

        <!-- Charts Section -->
        <section class="space-y-12 mb-12">
          <div class="w-full">
            <h3 class="text-xl font-semibold mb-4">Style Distribution</h3>
            <div class="h-[600px]">
              <StyleCloud :data="styleData" />
            </div>
          </div>
          <div class="w-full">
            <h3 class="text-xl font-semibold mb-4">Records Added by Month</h3>
            <div class="h-[300px]">
              <MonthlyChart :data="monthlyChartData" @month-click="scrollToMonth" />
            </div>
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
import StyleCloud from '../components/StyleCloud.vue'
import TopArtists from '../components/TopArtists.vue'
import dayjs from 'dayjs'

const route = useRoute()
const props = defineProps({
  year: {
    type: String,
    required: true
  }
})

const yearData = ref(null)
const collection = ref([])
const currentYear = computed(() => props.year)
const isMenuOpen = ref(false)

// Available years will be dynamically loaded from collection files
const availableYears = ref([])

// Load the available years on component mount
onMounted(async () => {
  try {
    // First load the current year's data
    await loadYearData(props.year)
    
    // Then try to load the list of all available years
    const files = await fetch('/collection_2024.json')
      .then(response => {
        if (!response.ok) throw new Error('Failed to fetch collection')
        return response.json()
      })
      .catch(error => {
        console.error('Error fetching collection:', error)
        return []
      })
    
    // Get unique years from the collection files in public directory
    const years = ['2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015']
    availableYears.value = years.sort((a, b) => b - a)
  } catch (error) {
    console.error('Error in onMounted:', error)
    // Fallback to just the current year if there's an error
    availableYears.value = [props.year]
  }
})

// Function to load data for a specific year
async function loadYearData(year) {
  try {
    // Reset data first
    collection.value = []
    yearData.value = null
    
    const response = await fetch(`/collection_${year}.json`)
    if (!response.ok) {
      throw new Error(`Failed to fetch collection for year ${year}`)
    }
    
    const data = await response.json()
    collection.value = data
    yearData.value = data
  } catch (error) {
    console.error('Error loading year data:', error)
    collection.value = []
    yearData.value = null
  }
}

// Watch for route changes
watch(() => route.params.year, async (newYear) => {
  if (newYear) {
    await loadYearData(newYear)
  }
}, { immediate: true })

// Computed properties for statistics
const collectionStats = computed(() => {
  if (!collection.value || collection.value.length === 0) {
    return { 
      totalRecords: 0, 
      topStyle: '-',
      avgPerMonth: 0
    }
  }
  
  const styles = collection.value.flatMap(record => record.styles || [])
  const styleCounts = styles.reduce((acc, style) => {
    acc[style] = (acc[style] || 0) + 1
    return acc
  }, {})
  
  const topStyle = Object.entries(styleCounts)
    .sort((a, b) => b[1] - a[1])[0]?.[0] || '-'
  
  const monthsWithRecords = new Set(
    collection.value
      .filter(record => record.date_added)
      .map(record => dayjs(record.date_added).format('YYYY-MM'))
  )
  
  const avgPerMonth = Math.round(collection.value.length / (monthsWithRecords.size || 1))
  
  return {
    totalRecords: collection.value.length,
    topStyle,
    avgPerMonth
  }
})

const styleData = computed(() => {
  if (!collection.value?.length) return []
  
  const styleMap = new Map()
  
  // First pass to count styles and collect albums
  collection.value.forEach(album => {
    album.styles.forEach(style => {
      if (!styleMap.has(style)) {
        styleMap.set(style, {
          text: style,
          value: 1,
          albums: [{
            id: album.id,
            title: album.title,
            cover: album.cover_image,
            slug: album.slug
          }]
        })
      } else {
        const existing = styleMap.get(style)
        existing.value++
        existing.albums.push({
          id: album.id,
          title: album.title,
          cover: album.cover_image,
          slug: album.slug
        })
      }
    })
  })
  
  return Array.from(styleMap.values())
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

const previousYear = computed(() => {
  const idx = availableYears.value.indexOf(currentYear.value)
  return idx < availableYears.value.length - 1 ? availableYears.value[idx + 1] : null
})

const nextYear = computed(() => {
  const idx = availableYears.value.indexOf(currentYear.value)
  return idx > 0 ? availableYears.value[idx - 1] : null
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
