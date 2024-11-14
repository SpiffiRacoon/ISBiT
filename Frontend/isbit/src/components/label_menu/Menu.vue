<script setup lang="ts">
import LabelBox from './LabelBox.vue'
import ClusterPlot from './ClusterPlot.vue'
</script>

<template>
  <div id="label-menu">
    <div class="block">
      <h2>Dataset: qaqc</h2>
      <ClusterPlot @point-click="(point) => receivePoint(point)"/>
    </div>
    <div id="text-and-labels">
      <h2>Märk Upp Datapunkt</h2>
      <LabelBox :text="activePoint.text" :alternatives="['LOC', 'HUM', 'DESC', 'ENTY', 'ABBR', 'NUM']" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'
import type {CustomPoint} from './ClusterPlot.vue'
export default defineComponent({
  props: {
    text: String
  },
  data() {
    return {
      activePoint: {text: "Välj en punkt i plotten."} as CustomPoint,
    }
  },
  methods: {
    receivePoint(point: CustomPoint) {
      this.activePoint=point
    }
  },
})
</script>

<style scoped>
#label-menu {
  display: flex;
}

#text-and-labels {
  margin: 20px;
  display: block;
  width: 300px;
}

.block {
  display: block;
}
</style>
