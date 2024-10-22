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
  text: string;
  id: string;
  truth: string;
}

export default defineComponent({
  components: {
    ScatterChart: Scatter,
  },
  setup() {
    const chartRef: Ref<{ chart: ChartJS } | null> = ref(null);

    // Scatter data state
    const scatterData: Ref<ChartData<'scatter', CustomPoint[]>> = ref<ChartData<'scatter', CustomPoint[]>>({
      datasets: []
    });

    // Function to fetch and process the API data
    async function fetchData() {
  try {
    const response = await axios.get('http://localhost:8000/V1/data/?collection=swe_qaqc_lib_test');
    const incomingData = response.data;

    const clusters: { [key: number]: CustomPoint[] } = {};

    incomingData.forEach((item: any) => {
      const point: CustomPoint = {
        x: item.x,
        y: item.y,
        text: item.text,
        id: item.id,
        truth: item.truth,
      };

      if (!clusters[item.cluster]) {
        clusters[item.cluster] = [];
      }
      clusters[item.cluster].push(point);
    });

    // Generate new datasets array
    const newDatasets = Object.entries(clusters).map(([clusterIndex, points]) => {
      const getRandomColor = () => {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
          color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
      };

      return {
        label: `Cluster ${clusterIndex}`,
        data: points,
        backgroundColor: getRandomColor(), 
        showLine: false,
        pointRadius: 5,
      };
    });

    // Replace scatterData.value with new data to trigger reactivity
    scatterData.value = {
      datasets: newDatasets,
    };

    console.log("Scatter Data Updated:", scatterData.value);
  } catch (err) {
    console.error(err);
  }
}


    onMounted(fetchData);

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
              return `Text: ${point.text} | x: ${point.x}, y: ${point.y} | ID: ${point.id} | Truth: ${point.truth}`;
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

          console.log('Clicked point:', { 
            id: clickedPoint.id, 
            x: clickedPoint.x, 
            y: clickedPoint.y, 
            text: clickedPoint.text,
            truth: clickedPoint.truth 
          });
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
