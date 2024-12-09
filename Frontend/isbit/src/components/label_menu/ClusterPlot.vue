<template>
  <div
    class="chart-container"
    @mousedown="startSelecting"
    @mousemove="onMouseMove"
    @mouseup="endSelecting"
  >
    <ScatterChart
      ref="chartRef"
      :data="scatterData"
      :options="chartOptions"
      @click="onClick"
    ></ScatterChart>
  </div>

  <div class="zoom-controls">
    <button
      @click="setZoomOption('pan')"
      :class="{ active: zoomOption === 'pan' }"
      class="zoom-btn"
    >
      Drag
    </button>

    <button
      @click="setZoomOption('drag')"
      :class="{ active: zoomOption === 'drag' }"
      class="zoom-btn"
    >
      Markera zoom
    </button>

    <button @click="setZoomOption('')" :class="{ active: zoomOption === '' }" class="zoom-btn">
      Markera flera punkter
    </button>
  </div>

  <button @click="resetZoom" class="reset-zoom-btn">Återställ zoom</button>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from 'vue'
import type { Ref, PropType } from 'vue'
import { Chart as ChartJS, registerables } from 'chart.js'
import zoomPlugin from 'chartjs-plugin-zoom'
import type { ChartData, ChartOptions } from 'chart.js'
import { Scatter } from 'vue-chartjs'
import axios from 'axios'
import { useRoute } from 'vue-router'

ChartJS.register(...registerables, zoomPlugin)

interface CustomPoint {
  x: number
  y: number
  text: string
  id: string
  truth: string
  input_label: string
  predicted_labels: string
  borderColor?: string
  borderWidth?: number
  opacity?: number
  backgroundColor?: string
}
export type { CustomPoint }

export default defineComponent({
  components: {
    ScatterChart: Scatter
  },
  props: {
    activePoint: {
      type: Object as PropType<CustomPoint | null>,
      default: null
    },
    activePoints: {
      type: Array as PropType<CustomPoint[]>,
      default: () => []
    }
  },
  setup(props, { emit }) {
    const route = useRoute()
    const dataset = route.query.dataset as string
    const chartRef: Ref<{ chart: ChartJS } | null> = ref(null)
    const error: Ref<string | null> = ref(null)

    const zoomOption = ref('pan')
    const selectionRect = ref<{
      startX: number
      startY: number
      endX: number
      endY: number
    } | null>(null)

    const selectedPoints: Ref<CustomPoint[]> = ref([])

    const scatterData: Ref<ChartData<'scatter', CustomPoint[]>> = ref({
      datasets: []
    })

    const chartOptions: Ref<ChartOptions<'scatter'>> = ref({
      scales: {
        x: {
          type: 'linear',
          position: 'bottom',
          grid: { display: false },
          ticks: { display: false },
          border: { display: false }
        },
        y: {
          beginAtZero: true,
          grid: { display: false },
          ticks: { display: false },
          border: { display: false }
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
              const datasetIndex = context.datasetIndex
              const dataIndex = context.dataIndex
              const point = scatterData.value.datasets[datasetIndex].data[dataIndex] as CustomPoint

              return `Text: ${point.text}, Sanning: ${point.input_label || 'Omarkerad'}`
            }
          }
        },
        zoom: {
          zoom: {
            wheel: { enabled: true },
            drag: { enabled: zoomOption.value === 'drag' },
            pinch: { enabled: true },
            mode: 'xy'
          },
          pan: {
            enabled: zoomOption.value === 'pan',
            mode: 'xy'
          }
        }
      },
      backgroundColor: 'transparent'
    })

    function adjustColorOpacity(color: string, opacity: number): string {
      if (color.startsWith('hsl(')) {
        return color.replace('hsl(', 'hsla(').replace(')', `, ${opacity})`)
      } else if (color.startsWith('rgb(')) {
        return color.replace('rgb(', 'rgba(').replace(')', `, ${opacity})`)
      } else if (color.startsWith('#')) {
        const hex = color.substring(1)
        const bigint = parseInt(hex, 16)
        const r = (bigint >> 16) & 255
        const g = (bigint >> 8) & 255
        const b = bigint & 255
        return `rgba(${r}, ${g}, ${b}, ${opacity})`
      } else if (color === 'black') {
        return `rgba(0, 0, 0, ${opacity})`
      }
      return color
    }

    async function fetchData() {
      try {
        const response = await axios.get(`http://localhost:8000/V1/data/?collection=${dataset}`)
        const incomingData = response.data

        const categories: { [key: string]: CustomPoint[] } = {}

        incomingData.forEach((item: any) => {
          const labelKey = item.input_label ?? 'Omarkerad'

          if (!categories[labelKey]) {
            categories[labelKey] = []
          }

          const point: CustomPoint = {
            x: item.x,
            y: item.y,
            text: item.text,
            id: item.id,
            truth: item.truth,
            input_label: item.input_label,
            predicted_labels: item.predicted_labels,
            opacity: 1
          }

          categories[labelKey].push(point)
        })

        const categoryEntries = Object.entries(categories)

        const newDatasets = categoryEntries.map(([clusterIndex, points], index) => {
          let color: string

          if (clusterIndex === 'Omarkerad') {
            color = 'black'
          } else {
            const getDistinctColor = (index: number) => {
              const hue = (index * 360) / (categoryEntries.length - 1 || 1)
              return `hsl(${hue}, 70%, 50%)`
            }
            color = getDistinctColor(index)
          }

          points.forEach((point) => {
            point.backgroundColor = color
          })

          return {
            label: clusterIndex,
            data: points,
            backgroundColor: color,
            showLine: false,
            pointRadius: 8,
            pointHoverRadius: 8,
            pointBorderColor: (context: any) => {
              const dataPoint = context.raw as CustomPoint
              return dataPoint.borderColor || 'transparent'
            },
            pointBorderWidth: (context: any) => {
              const dataPoint = context.raw as CustomPoint
              return dataPoint.borderWidth || 0
            },
            pointBackgroundColor: (context: any) => {
              const dataPoint = context.raw as CustomPoint
              let bgColor = dataPoint.backgroundColor || color
              if (dataPoint.opacity !== undefined) {
                bgColor = adjustColorOpacity(bgColor, dataPoint.opacity)
              }
              return bgColor
            }
          }
        })

        scatterData.value = { datasets: newDatasets }
      } catch (err) {
        console.error('Error fetching data:', err)
      }
    }

    onMounted(() => {
      if (dataset) {
        fetchData()
      } else {
        error.value = 'No dataset provided in the query'
      }
    })

    watch(zoomOption, () => {
      const chartInstance = chartRef.value?.chart

      if (chartInstance && chartInstance.options?.plugins?.zoom) {
        const zoomPlugin = chartInstance.options.plugins.zoom

        if (zoomPlugin.zoom?.drag && zoomPlugin.pan) {
          zoomPlugin.zoom.drag.enabled = zoomOption.value === 'drag'
          zoomPlugin.pan.enabled = zoomOption.value === 'pan'
        }

        chartInstance.update()
      }
    })

    watch(
      () => props.activePoint,
      (newVal) => {
        if (newVal) {
          markPointInChart(newVal.id)
        }
      }
    )

    watch(
      () => props.activePoints,
      (newVal) => {
        if (newVal.length > 0) {
          markPointsInChart(newVal)
        }
      }
    )

    const markPointInChart = (pointId: string) => {
      const chartInstance = chartRef.value?.chart
      if (chartInstance) {
        scatterData.value.datasets.forEach((dataset) => {
          dataset.data.forEach((point: CustomPoint) => {
            if (point.id === pointId) {
              point.borderColor = 'green'
              point.borderWidth = 3
              point.opacity = 1
            } else {
              point.borderColor = undefined
              point.borderWidth = undefined
              point.opacity = 0.5
            }
          })
        })
        chartInstance.update()
      }
    }

    const markPointsInChart = (points: CustomPoint[]) => {
      const chartInstance = chartRef.value?.chart
      if (chartInstance) {
        const pointIds = points.map((p) => p.id)
        scatterData.value.datasets.forEach((dataset) => {
          dataset.data.forEach((point: CustomPoint) => {
            if (pointIds.includes(point.id)) {
              point.borderColor = 'green'
              point.borderWidth = 3
              point.opacity = 1
            } else {
              point.borderColor = undefined
              point.borderWidth = undefined
              point.opacity = 0.5
            }
          })
        })
        chartInstance.update()
      }
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

        if (points.length) {
          const point = points[0]
          const dataIndex = point.index
          const datasetIndex = point.datasetIndex
          const clickedPoint = scatterData.value.datasets[datasetIndex].data[
            dataIndex
          ] as CustomPoint

          emit('point-click', clickedPoint)
        } else {
          emit('point-click', null)
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

    const setZoomOption = (option: string) => {
      zoomOption.value = option
    }

    const startSelecting = (event: MouseEvent) => {
      const chartInstance = chartRef.value?.chart
      if (chartInstance) {
        const { offsetX, offsetY } = event
        const chartX = chartInstance.scales.x.getValueForPixel(offsetX) ?? 0
        const chartY = chartInstance.scales.y.getValueForPixel(offsetY) ?? 0

        selectionRect.value = {
          startX: chartX,
          startY: chartY,
          endX: chartX,
          endY: chartY
        }
      }
    }

    const onMouseMove = (event: MouseEvent) => {
      if (selectionRect.value) {
        const chartInstance = chartRef.value?.chart
        if (chartInstance) {
          const { offsetX, offsetY } = event
          const chartX = chartInstance.scales.x.getValueForPixel(offsetX) ?? 0
          const chartY = chartInstance.scales.y.getValueForPixel(offsetY) ?? 0

          selectionRect.value.endX = chartX
          selectionRect.value.endY = chartY
        }
      }
    }

    const endSelecting = () => {
      if (selectionRect.value) {
        const { startX, startY, endX, endY } = selectionRect.value
        const selectedPointsArray = scatterData.value.datasets.flatMap((dataset) =>
          dataset.data.filter((point: CustomPoint) => {
            return (
              point.x >= Math.min(startX, endX) &&
              point.x <= Math.max(startX, endX) &&
              point.y >= Math.min(startY, endY) &&
              point.y <= Math.max(startY, endY)
            )
          })
        )

        selectedPoints.value = selectedPointsArray

        if (zoomOption.value === '') {
          emit('points-marked', selectedPoints.value)
        }

        selectionRect.value = null
      }
    }

    return {
      scatterData,
      chartOptions,
      onClick,
      chartRef,
      dataset,
      error,
      resetZoom,
      setZoomOption,
      startSelecting,
      onMouseMove,
      endSelecting,
      zoomOption
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

.zoom-controls {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.zoom-btn {
  padding: 10px 15px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition:
    background-color 0.3s,
    color 0.3s;
}

.zoom-btn.active {
  background-color: #007bff;
  color: white;
}

.reset-zoom-btn {
  padding: 10px 15px;
  background-color: #ff6347;
  border: 1px solid #e53e3e;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  color: white;
}

.reset-zoom-btn:hover {
  background-color: #e53e3e;
}
</style>
