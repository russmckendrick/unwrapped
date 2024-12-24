<template>
  <div class="h-full">
    <canvas ref="chart"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const chart = ref(null)
const chartInstance = ref(null)

const createChart = () => {
  const ctx = chart.value.getContext('2d')
  
  if (chartInstance.value) {
    chartInstance.value.destroy()
  }

  chartInstance.value = new Chart(ctx, {
    type: 'doughnut',
    data: props.data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: {
          right: 100 // Give more space for legend
        }
      },
      plugins: {
        legend: {
          position: 'right',
          align: 'start',
          labels: {
            color: 'rgba(255, 255, 255, 0.7)',
            font: {
              size: 11
            },
            padding: 8,
            usePointStyle: true,
            pointStyle: 'circle',
            boxWidth: 6
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const label = context.label || ''
              const value = context.parsed || 0
              const total = context.dataset.data.reduce((a, b) => a + b, 0)
              const percentage = ((value / total) * 100).toFixed(1)
              return `${label}: ${value} records (${percentage}%)`
            }
          }
        }
      },
      cutout: '75%',
      radius: '95%'
    }
  })
}

onMounted(() => {
  createChart()
})

watch(() => props.data, () => {
  createChart()
}, { deep: true })
</script>
