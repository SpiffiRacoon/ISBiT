<template>
  <div class="chart-container">
    <ScatterChart ref="chartRef" :data="scatterData" :options="chartOptions" @click="onClick"></ScatterChart>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import type { Ref } from 'vue';
import { Chart as ChartJS, registerables } from 'chart.js';
import type { ChartData, ChartOptions } from 'chart.js';
import { Scatter } from 'vue-chartjs';
import axios from 'axios';

ChartJS.register(...registerables);

interface CustomPoint {
  x: number;
  y: number;
  tooltip: string; 
}

export default defineComponent({
  components: {
    ScatterChart: Scatter,
  },
  setup() {
    const chartRef: Ref<{ chart: ChartJS } | null> = ref(null);

    // Example data 
    var incomingData = [
      {
        "id": "6714f4f41ba92ae7309e1558",
        "cluster": 0,
        "text": "Hur utvecklades träldomen i Ryssland?",
        "x": -1.2356,
        "y": 0.6237,
        "truth": "DESC"
      },
      {
        "id": "6714f4f41ba92ae7309e1559",
        "cluster": 1,
        "text": "Vilka filmer inkluderade karaktären Popeye Doyle?",
        "x": -1.7641,
        "y": -0.6591,
        "truth": "ENTY"
      },

    ];



    const scatterData: Ref<ChartData<'scatter', CustomPoint[]>> = ref<ChartData<'scatter', CustomPoint[]>>({
      datasets: []
    });

    const clusters: { [key: number]: CustomPoint[] } = {};

    incomingData.forEach(item => {
      const point: CustomPoint = {
        x: item.x,
        y: item.y,
        tooltip: item.text,
      };

      if (!clusters[item.cluster]) {
        clusters[item.cluster] = [];
      }
      clusters[item.cluster].push(point);
    });

    Object.entries(clusters).forEach(([clusterIndex, points]) => {
      scatterData.value.datasets.push({
        label: `Cluster ${clusterIndex}`,
        data: points,
        backgroundColor: clusterIndex === '0' ? 'blue' : 'red', 
        showLine: false,
        pointRadius: 5,
      });
    });

    const chartOptions: ChartOptions<'scatter'> = {
      scales: {
        x: {
          type: 'linear',
          position: 'bottom',
          grid: {
            display: false,
          },
          ticks: {
            display: false,
          },
          border: {
            display: false,
          },
        },
        y: {
          beginAtZero: true,
          grid: {
            display: false,
          },
          ticks: {
            display: false,
          },
          border: {
            display: false,
          },
        },
      },
      interaction: {
        mode: 'nearest',
        intersect: true,
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: (context) => {
              const point = scatterData.value.datasets[context.datasetIndex].data[context.dataIndex] as CustomPoint;
              return point.tooltip || `x: ${point.x}, y: ${point.y}`;
            },
          },
        },
      },
      backgroundColor: 'transparent',
    };

    const onClick = (event: MouseEvent) => {
      const chartInstance = chartRef.value?.chart;

      if (chartInstance) {
        const points = chartInstance.getElementsAtEventForMode(
          event,
          'nearest',
          { intersect: true },
          true
        );

        if (points && points.length) {
          const point = points[0];
          const datasetIndex = point.datasetIndex;
          const dataIndex = point.index;
          const clickedPoint = scatterData.value.datasets[datasetIndex].data[dataIndex] as CustomPoint;

          console.log('Clicked point:', { x: clickedPoint.x, y: clickedPoint.y, tooltip: clickedPoint.tooltip });
        } else {
          console.log('No point clicked');
        }
      } else {
        console.error('Chart instance not found');
      }
    };

    return {
      scatterData,
      chartOptions,
      onClick,
      chartRef,
    };
  },
});
</script>

<style scoped>
.chart-container {
  border: 3px solid green;
  padding: 10px;
  border-radius: 8px;
  width: 800px;
  height: 600px;
  position: relative;
}
</style>
