<template>
  <div class="chart-container">
    <ScatterChart
      ref="chartRef"
      :data="scatterData"
      :options="chartOptions"
      @click="onClick"
    ></ScatterChart>
  </div>
  <button @click="resetZoom" class="reset-zoom-btn">Reset Zoom</button>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import type { Ref } from 'vue'
import { Chart as ChartJS, registerables } from 'chart.js'
import zoomPlugin from 'chartjs-plugin-zoom'
import type { ChartData, ChartOptions } from 'chart.js'
import { Scatter } from 'vue-chartjs'
import axios from 'axios'
import { useRoute } from 'vue-router'

ChartJS.register(...registerables)
ChartJS.register(zoomPlugin)

interface CustomPoint {
  x: number
  y: number
  text: string
  id: string
  truth: string
}

export default defineComponent({
  components: {
    ScatterChart: Scatter
  },
  setup() {
    const route = useRoute()
    const dataset = route.query.dataset as string
    console.log(dataset)
    const chartRef: Ref<{ chart: ChartJS } | null> = ref(null)
    const error: Ref<string | null> = ref(null)

    const scatterData: Ref<ChartData<'scatter', CustomPoint[]>> = ref<
      ChartData<'scatter', CustomPoint[]>
    >({
      datasets: []
    })

    async function fetchData() {
      try {
        const response = await axios.get('http://localhost:8000/V1/data/?collection=' + dataset)
        const incomingData = response.data

        const points: CustomPoint[] = incomingData.map((item: any) => ({
          x: item.x,
          y: item.y,
          text: item.text,
          id: item.id,
          truth: item.truth
        }))

        const newDataset = {
          label: 'Data Points',
          data: points,
          backgroundColor: 'black',
          showLine: false,
          pointRadius: 5
        }

        scatterData.value = {
          datasets: [newDataset]
        }

        console.log('Scatter Data Updated:', scatterData.value)
      } catch (err) {
        console.error(err)
      }
    }

    onMounted(() => {
      if (dataset) {
        fetchData()
      } else {
        error.value = 'No dataset provided in the query'
      }
    })

    const chartOptions: ChartOptions<'scatter'> = {
      scales: {
        x: {
          type: 'linear',
          position: 'bottom',
          grid: {
            display: false
          },
          ticks: {
            display: false
          },
          border: {
            display: false
          }
        },
        y: {
          beginAtZero: true,
          grid: {
            display: false
          },
          ticks: {
            display: false
          },
          border: {
            display: false
          }
        }
      },
      interaction: {
        mode: 'nearest',
        intersect: true
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: (context) => {
              const point = scatterData.value.datasets[0].data[context.dataIndex] as CustomPoint
              return `Text: ${point.text}, Truth: ${point.truth}`
            }
          }
        },
        zoom: {
          zoom: {
            wheel: {
              enabled: true
            },
            drag: {
              enabled: false
            },
            pinch: {
              enabled: true
            },
            mode: 'xy'
          },
          pan: {
            enabled: true,
            mode: 'xy'
          }
        }
      },
      backgroundColor: 'transparent'
    }

    const onClick = (event: MouseEvent) => {
      const chartInstance = chartRef.value?.chart

      if (chartInstance) {
        const points = chartInstance.getElementsAtEventForMode(
          event,
          'nearest',
          { intersect: true },
          true
        )

        if (points && points.length) {
          const point = points[0]
          const dataIndex = point.index
          const clickedPoint = scatterData.value.datasets[0].data[dataIndex] as CustomPoint

          console.log('Clicked point:', {
            id: clickedPoint.id,
            x: clickedPoint.x,
            y: clickedPoint.y,
            text: clickedPoint.text,
            truth: clickedPoint.truth
          })
        } else {
          console.log('No point clicked')
        }
      } else {
        console.error('Chart instance not found')
      }
    }
    const resetZoom = () => {
      const chartInstance = chartRef.value?.chart
      if (chartInstance) {
        chartInstance.resetZoom()
      }
    }
    return {
      scatterData,
      chartOptions,
      onClick,
      chartRef,
      dataset,
      error,
      resetZoom
    }
  }
})
</script>

<style scoped>
.chart-container {
  border: 3px solid green;
  padding: 10px;
  border-radius: 8px;
  width: 1000px;
  height: 500px;
  position: relative;
}
</style>
