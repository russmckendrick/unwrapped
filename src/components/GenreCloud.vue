<template>
  <div ref="cloudContainer" class="h-[300px] w-full bg-opacity-20 rounded-lg"></div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import * as d3 from 'd3'
import cloud from 'd3-cloud'

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  }
})

const cloudContainer = ref(null)

const words = computed(() => {
  if (!props.data || props.data.length === 0) {
    return []
  }
  const total = props.data.reduce((acc, item) => acc + item.value, 0)
  return props.data.map(item => ({
    text: item.text,
    value: item.value,
    size: Math.max(20, 14 + (item.value / total) * 80),
    weight: Math.min(900, Math.floor((item.value / total) * 900) + 500)
  }))
})

const colors = [
  '#1DB954', // Spotify green
  '#60A5FA', // Blue
  '#F472B6', // Pink
  '#34D399', // Emerald
  '#A78BFA', // Purple
  '#FBBF24', // Amber
]

const getColor = (word, index) => {
  return colors[index % colors.length]
}

const clearCloud = () => {
  if (cloudContainer.value) {
    d3.select(cloudContainer.value).selectAll("*").remove()
  }
}

const drawWordCloud = async () => {
  if (!cloudContainer.value) return
  
  // Clear previous content
  clearCloud()
  
  // If no words, don't proceed
  if (words.value.length === 0) return

  // Wait for the next tick to ensure the container is ready
  await nextTick()
  
  // Get container dimensions
  const width = cloudContainer.value.offsetWidth || 600
  const height = cloudContainer.value.offsetHeight || 300

  // Create layout
  const layout = cloud()
    .size([width, height])
    .words(words.value)
    .padding(10)
    .rotate(() => 0)
    .font("Inter")
    .fontSize(d => d.size)
    .spiral("rectangular")
    .on("end", draw)

  // Start layout calculation
  layout.start()

  function draw(words) {
    if (!cloudContainer.value) return

    const svg = d3.select(cloudContainer.value)
      .append("svg")
      .attr("width", "100%")
      .attr("height", "100%")
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("preserveAspectRatio", "xMidYMid meet")

    const group = svg.append("g")
      .attr("transform", `translate(${width/2},${height/2})`)
      .attr("class", "word-cloud-group")

    // Add background rectangles
    group.selectAll("rect")
      .data(words)
      .enter()
      .append("rect")
      .attr("x", d => d.x - (d.width || 0) / 2 - 12)
      .attr("y", d => d.y - (d.height || 0) / 2 - 6)
      .attr("width", d => (d.width || 0) + 24)
      .attr("height", d => (d.height || 0) + 12)
      .attr("rx", 6)
      .attr("ry", 6)
      .attr("fill", "transparent")
      .attr("class", "word-bg")

    // Add text elements
    group.selectAll("text")
      .data(words)
      .enter()
      .append("text")
      .style("font-size", d => `${d.size}px`)
      .style("font-family", "Inter")
      .style("font-weight", d => d.weight)
      .style("fill", (d, i) => getColor(d, i))
      .attr("text-anchor", "middle")
      .attr("transform", d => `translate(${d.x},${d.y})`)
      .text(d => d.text)
      .on("mouseover", function() {
        d3.select(this)
          .transition()
          .duration(200)
          .style("fill", "#1DB954")
        
        d3.select(this.previousSibling)
          .transition()
          .duration(200)
          .attr("fill", "rgba(0, 0, 0, 0.2)")
      })
      .on("mouseout", function(event, d) {
        d3.select(this)
          .transition()
          .duration(200)
          .style("fill", (d, i) => getColor(d, i))
        
        d3.select(this.previousSibling)
          .transition()
          .duration(200)
          .attr("fill", "transparent")
      })
  }
}

const cleanup = () => {
  if (cloudContainer.value) {
    window.removeEventListener('resize', drawWordCloud)
    clearCloud()
  }
}

onMounted(() => {
  drawWordCloud()
  window.addEventListener('resize', drawWordCloud)
})

onUnmounted(() => {
  cleanup()
})

// Watch for changes in the data and redraw
watch(() => props.data, (newData) => {
  if (newData) {
    nextTick(() => {
      drawWordCloud()
    })
  } else {
    clearCloud()
  }
}, { deep: true, immediate: true })
</script>

<style scoped>
.word-cloud-group text {
  cursor: pointer;
  transition: all 0.2s ease;
}

.word-bg {
  transition: all 0.2s ease;
}
</style>
