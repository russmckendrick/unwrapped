<template>
  <div class="w-full h-[300px]" ref="chartContainer"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as d3 from 'd3'

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  }
})

const emit = defineEmits(['month-click'])

const chartContainer = ref(null)

const colors = [
  '#1DB954', // Spotify green
  '#60A5FA', // Blue
  '#F472B6', // Pink
  '#34D399', // Emerald
  '#A78BFA', // Purple
  '#FBBF24', // Amber
]

const clearChart = () => {
  if (chartContainer.value) {
    d3.select(chartContainer.value).selectAll('*').remove()
  }
}

const drawChart = () => {
  if (!chartContainer.value || !props.data.length) return

  clearChart()

  const margin = { top: 20, right: 20, bottom: 40, left: 40 }
  const width = chartContainer.value.offsetWidth - margin.left - margin.right
  const height = chartContainer.value.offsetHeight - margin.top - margin.bottom

  const svg = d3.select(chartContainer.value)
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // X scale
  const x = d3.scaleBand()
    .range([0, width])
    .domain(props.data.map(d => d.month))
    .padding(0.2)

  // Y scale
  const y = d3.scaleLinear()
    .range([height, 0])
    .domain([0, d3.max(props.data, d => d.count)])

  // Add X axis
  svg.append('g')
    .attr('transform', `translate(0,${height})`)
    .call(d3.axisBottom(x))
    .selectAll('text')
    .attr('transform', 'translate(-10,0)rotate(-45)')
    .style('text-anchor', 'end')
    .style('fill', '#fff')

  // Add Y axis
  svg.append('g')
    .call(d3.axisLeft(y).ticks(5))
    .selectAll('text')
    .style('fill', '#fff')

  // Add the bars with different colors and interactivity
  svg.selectAll('rect')
    .data(props.data)
    .join('rect')
    .attr('x', d => x(d.month))
    .attr('width', x.bandwidth())
    .attr('y', d => y(d.count))
    .attr('height', d => height - y(d.count))
    .attr('fill', (_, i) => colors[i % colors.length])
    .attr('rx', 4)
    .attr('ry', 4)
    .style('cursor', 'pointer')
    .on('mouseover', function(event, d) {
      d3.select(this)
        .transition()
        .duration(200)
        .attr('filter', 'brightness(1.2)')
        .attr('transform', `translate(0, -5)`)
    })
    .on('mouseout', function(event, d) {
      d3.select(this)
        .transition()
        .duration(200)
        .attr('filter', null)
        .attr('transform', null)
    })
    .on('click', function(event, d) {
      console.log('MonthlyChart: Click event triggered', { month: d.month })
      
      // Prevent any default behavior
      if (event) {
        event.preventDefault()
        event.stopPropagation()
      }

      try {
        // Ensure we have valid data
        if (!d || !d.month) {
          console.error('MonthlyChart: Invalid click data', d)
          return
        }

        // Force the event to be synchronous
        setTimeout(() => {
          console.log('MonthlyChart: Emitting month-click event', { month: d.month })
          emit('month-click', d.month)
        }, 0)
      } catch (error) {
        console.error('MonthlyChart: Error in click handler', error)
      }
    })

  // Add count labels on top of bars
  svg.selectAll('.count-label')
    .data(props.data)
    .join('text')
    .attr('class', 'count-label')
    .attr('x', d => x(d.month) + x.bandwidth() / 2)
    .attr('y', d => y(d.count) - 5)
    .attr('text-anchor', 'middle')
    .style('fill', '#fff')
    .style('font-size', '12px')
    .text(d => d.count > 0 ? d.count : '')
}

onMounted(() => {
  drawChart()
  window.addEventListener('resize', drawChart)
})

onUnmounted(() => {
  window.removeEventListener('resize', drawChart)
})

watch(() => props.data, () => {
  drawChart()
}, { deep: true })
</script>

<style scoped>
:deep(line) {
  stroke: rgba(255, 255, 255, 0.2);
}

:deep(path) {
  stroke: rgba(255, 255, 255, 0.2);
}
</style>
