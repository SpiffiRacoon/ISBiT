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
  id: string;
  truth: string;
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
    {
    "id": "6716971a90ae9e2ea7018fc3",
    "cluster": 0,
    "text": "Hur kan jag hitta en lista över kändisars riktiga namn?",
    "x": -1.582128643989563,
    "y": 2.1271731853485107,
    "truth": "DESC"
  },
  {
    "id": "6716971a90ae9e2ea7018fc4",
    "cluster": 0,
    "text": "Vilken fjäderfä fångar rampljuset efter det kinesiska apans år?",
    "x": -0.5479762554168701,
    "y": -0.04891887679696083,
    "truth": "ENTY"
  },
  {
    "id": "6716971a90ae9e2ea7018fc5",
    "cluster": 3,
    "text": "Vad är den fullständiga formen av .com?",
    "x": 2.4311063289642334,
    "y": 0.8338965773582458,
    "truth": "ABBR"
  },
  {
    "id": "6716971a90ae9e2ea7018fc6",
    "cluster": 1,
    "text": "Vilken föraktlig skurk stal korken från min lunch?",
    "x": -1.2232531309127808,
    "y": -0.9398744702339172,
    "truth": "HUM"
  },
  {
    "id": "6716971a90ae9e2ea7018fc7",
    "cluster": 0,
    "text": "Vilket lag blev basebollens St. Louis Browns?",
    "x": -0.2102341204881668,
    "y": -1.9608551263809204,
    "truth": "HUM"
  },
  {
    "id": "6716971a90ae9e2ea7018fc8",
    "cluster": 3,
    "text": "Vad är det äldsta yrket?",
    "x": 3.835052251815796,
    "y": 1.4481770992279053,
    "truth": "HUM"
  },
  {
    "id": "6716971a90ae9e2ea7018fc9",
    "cluster": 3,
    "text": "Vad är leverenzymer?",
    "x": 3.304880142211914,
    "y": -0.8225280046463013,
    "truth": "DESC"
  },
  {
    "id": "6716971a90ae9e2ea7018fca",
    "cluster": 0,
    "text": "Namnge den ärriga prisjägaren i The Old West.",
    "x": -0.18163913488388062,
    "y": -0.11950625479221344,
    "truth": "HUM"
  },
  {
    "id": "6716971a90ae9e2ea7018fcb",
    "cluster": 0,
    "text": "När föddes Ozzy Osbourne?",
    "x": -0.8736490607261658,
    "y": -1.865033745765686,
    "truth": "NUM"
  },
  {
    "id": "6716971a90ae9e2ea7018fcc",
    "cluster": 0,
    "text": "Varför faller tyngre föremål snabbare nedåt?",
    "x": -0.6079009175300598,
    "y": -1.1007612943649292,
    "truth": "DESC"
  },
  {
    "id": "6716971a90ae9e2ea7018fcd",
    "cluster": 0,
    "text": "Vem var Yankees stolthet?",
    "x": -0.9928578734397888,
    "y": -2.4561874866485596,
    "truth": "HUM"
  },
  {
    "id": "6716971a90ae9e2ea7018fce",
    "cluster": 4,
    "text": "Vem dödade Gandhi?",
    "x": -0.8677371740341187,
    "y": -0.34027373790740967,
    "truth": "HUM"
  },
  {
    "id": "6716971a90ae9e2ea7018fcf",
    "cluster": 0,
    "text": "Vad anses vara den dyraste katastrofen som försäkringsbranschen någonsin har stött på?",
    "x": -0.0989217609167099,
    "y": -0.5378841161727905,
    "truth": "ENTY"
  },
  {
    "id": "6716971a90ae9e2ea7018fd0",
    "cluster": 0,
    "text": "Vilken utbredd amerikansk stat har flest flygplatser?",
    "x": -0.9462676048278809,
    "y": -0.9544591903686523,
    "truth": "LOC"
  },
  {
    "id": "6716971a90ae9e2ea7018fd1",
    "cluster": 0,
    "text": "Vad behandlade den enda upphävda ändringen av USA:s konstitution?",
    "x": 0.9145219326019287,
    "y": -0.41327130794525146,
    "truth": "DESC"
  },
  {
    "id": "6716971a90ae9e2ea7018fd2",
    "cluster": 2,
    "text": "Hur många judar avrättades i koncentrationsläger under andra världskriget?",
    "x": -2.3423988819122314,
    "y": 1.2422314882278442,
    "truth": "NUM"
  },
  {
    "id": "6716971a90ae9e2ea7018fd3",
    "cluster": 3,
    "text": "Vad är \"Nine Inch Nails\"?",
    "x": 2.499086856842041,
    "y": -1.006535291671753,
    "truth": "DESC"
  },
  {
    "id": "6716971a90ae9e2ea7018fd4",
    "cluster": 3,
    "text": "Vad är en antecknad bibliografi?",
    "x": 2.218491792678833,
    "y": 0.865366518497467,
    "truth": "DESC"
  },
  {
    "id": "6716971a90ae9e2ea7018fd5",
    "cluster": 3,
    "text": "Vad är datumet för Boxing Day?",
    "x": 3.4017579555511475,
    "y": 0.7848553657531738,
    "truth": "NUM"
  },
  {
    "id": "6716971a90ae9e2ea7018fd6",
    "cluster": 1,
    "text": "Vilka klädesplagg är poletter i Monopol?",
    "x": -2.0697035789489746,
    "y": -0.05695539340376854,
    "truth": "ENTY"
  },
  {
    "id": "6716971a90ae9e2ea7018fd7",
    "cluster": 0,
    "text": "Namnge 11 berömda martyrer.",
    "x": 0.9512044191360474,
    "y": -2.532208204269409,
    "truth": "HUM"
  },
  {
    "id": "6716971a90ae9e2ea7018fd8",
    "cluster": 0,
    "text": "Vad är det olympiska mottot?",
    "x": 1.2986435890197754,
    "y": 1.183980941772461,
    "truth": "DESC"
  },
  {
    "id": "6716971a90ae9e2ea7018fd9",
    "cluster": 0,
    "text": "Vad är ursprunget till namnet \"Scarlett\"?",
    "x": 1.1348650455474854,
    "y": 0.9663435816764832,
    "truth": "DESC"
  },
  {
    "id": "6716971a90ae9e2ea7018fda",
    "cluster": 0,
    "text": "Vad är den näst mest använda vokalen i engelskan?",
    "x": 1.4371780157089233,
    "y": 1.1585625410079956,
    "truth": "ENTY"
  },
  {
    "id": "6716971a90ae9e2ea7018fdb",
    "cluster": 1,
    "text": "Vem var uppfinnaren av Silly Putty?",
    "x": -0.5312477946281433,
    "y": -1.5152606964111328,
    "truth": "HUM"
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
        id: item.id,
        truth: item.truth,
      };

      if (!clusters[item.cluster]) {
        clusters[item.cluster] = [];
      }
      clusters[item.cluster].push(point);
    });

    Object.entries(clusters).forEach(([clusterIndex, points]) => {

      const getRandomColor = () => {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
          color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
      };

      scatterData.value.datasets.push({
        label: `Cluster ${clusterIndex}`,
        data: points,
        backgroundColor: getRandomColor(), 
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
          return `Text: ${point.tooltip} | x: ${point.x}, y: ${point.y} | ID: ${point.id} | Truth: ${point.truth}`;
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
            tooltip: clickedPoint.tooltip,
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