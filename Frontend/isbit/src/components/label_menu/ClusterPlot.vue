<template>
  <div class="chart-container" @mousedown="startSelecting" @mousemove="onMouseMove" @mouseup="endSelecting">
    <ScatterChart
      ref="chartRef"
      :data="scatterData"
      :options="chartOptions"
      @click="onClick"
    ></ScatterChart>
  </div>
  <button @click="resetZoom" class="reset-zoom-btn">Återställ zoom</button>
  <button @click="setZoomOption('pan')" class="reset-zoom-btn">Drag</button>
  <button @click="setZoomOption('drag')" class="reset-zoom">Markera zoom</button>
  <button @click="setZoomOption('')"> Markera område</button>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from 'vue'
import type { Ref } from 'vue'
import { Chart as ChartJS, registerables } from 'chart.js'
import zoomPlugin from 'chartjs-plugin-zoom';
import type { ChartData, ChartOptions } from 'chart.js'
import { Scatter } from 'vue-chartjs'
import axios from 'axios'
import { useRoute } from 'vue-router'
export type {CustomPoint}

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
  emits: ['pointClick'],
  components: {
    ScatterChart: Scatter
  },
  setup(props, context) {
    const route = useRoute()
    const dataset = route.query.dataset as string
    const chartRef: Ref<{ chart: ChartJS } | null> = ref(null)
    const error: Ref<string | null> = ref(null)

    const scatterData: Ref<ChartData<'scatter', CustomPoint[]>> = ref<ChartData<'scatter', CustomPoint[]>>({
      datasets: []
    })

    var zoomOption = ref('pan');
    const selectionRect = ref<{ startX: number, startY: number, endX: number, endY: number } | null>(null);
    const selectedPoints: Ref<CustomPoint[]> = ref([]);

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

    const chartOptions: Ref<ChartOptions<'scatter'>> = ref({
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
              enabled: true,
            },
            drag: {
              enabled: zoomOption.value === 'drag'
            },
            pinch: {
              enabled: true
            },
            mode: 'xy',
          },
          pan: {
            enabled: zoomOption.value === 'pan',
            mode: 'xy'
          },
        }
      },
      backgroundColor: 'transparent'
    })

    watch(zoomOption, () => {
      const chartInstance = chartRef.value?.chart;

      if (chartInstance && chartInstance.options?.plugins?.zoom) {
        const zoomPlugin = chartInstance.options.plugins.zoom;


        if (zoomPlugin.zoom && zoomPlugin.zoom.drag && zoomPlugin.pan) {
          zoomPlugin.zoom.drag.enabled = zoomOption.value === 'drag';
          zoomPlugin.pan.enabled = zoomOption.value === 'pan';
        }

        chartInstance.update(); 
      }
    });

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
          context.emit('pointClick', clickedPoint); // tell parent the point was clicked
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

    const setZoomOption = (option: string) => {
      zoomOption.value = option;
    }

    const startSelecting = (event: MouseEvent) => {
      const chartInstance = chartRef.value?.chart
      if (chartInstance) {
        const { offsetX, offsetY } = event;
        const chartArea = chartInstance.chartArea;
        const chartX = chartInstance.scales.x.getValueForPixel(offsetX) ?? 0;
        const chartY = chartInstance.scales.y.getValueForPixel(offsetY) ?? 0;
        
        selectionRect.value = { startX: chartX, startY: chartY, endX: chartX, endY: chartY };
      }
    };

    const onMouseMove = (event: MouseEvent) => {
      if (selectionRect.value) {
        const chartInstance = chartRef.value?.chart
        if (chartInstance) {
          const { offsetX, offsetY } = event;
          const chartX = chartInstance.scales.x.getValueForPixel(offsetX) ?? 0;
          const chartY = chartInstance.scales.y.getValueForPixel(offsetY) ?? 0;

          selectionRect.value.endX = chartX;
          selectionRect.value.endY = chartY;
        }
      }
    };

    const endSelecting = () => {
      if (selectionRect.value) {
        const { startX, startY, endX, endY } = selectionRect.value;
        const selectedPointsArray = scatterData.value.datasets[0].data.filter((point: CustomPoint) => {
          return (
            point.x >= Math.min(startX, endX) &&
            point.x <= Math.max(startX, endX) &&
            point.y >= Math.min(startY, endY) &&
            point.y <= Math.max(startY, endY)
          );
        });
        
        selectedPoints.value = selectedPointsArray;
        console.log('Selected points:', selectedPointsArray);
        selectionRect.value = null;
      }
    };

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
      endSelecting
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
