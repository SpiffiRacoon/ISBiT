<template>
    <div class="chart-container">
      <ScatterChart ref="chartRef" :data="scatterData" :options="chartOptions" @click="onClick"></ScatterChart>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { Chart as ChartJS, registerables } from 'chart.js';
  import { Scatter } from 'vue-chartjs';
  
  ChartJS.register(...registerables);
  
  export default defineComponent({
    components: {
      ScatterChart: Scatter,
    },
    setup() {
      const chartRef = ref(null);
  
      const scatterData = ref({
        datasets: [
          {
            label: 'Cluster 1',
            data: [
              { x: 18, y: 20, tooltip: 'Point A'},
              { x: 15, y: 10, tooltip: 'Point B' },
              { x: 20, y: 30, tooltip: 'Point C' },
            ],
            backgroundColor: 'blue',
            showLine: false, 
            pointRadius: 5,
          },
          {
            label: 'Cluster 2',
            data: [
              { x: 10, y: 10, tooltip: 'Point D' },
              { x: 14, y: 0, tooltip: 'Point E' },
              { x: 12, y: 10, tooltip: 'Point F' },
            ],
            backgroundColor: 'red',
            showLine: false, 
            pointRadius: 5,
          },
        ],
      });
  
      const chartOptions = ref({
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
        backgroundColor: 'transparent', 
      });
  
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
            const clickedPoint = scatterData.value.datasets[datasetIndex].data[dataIndex];
  
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
  