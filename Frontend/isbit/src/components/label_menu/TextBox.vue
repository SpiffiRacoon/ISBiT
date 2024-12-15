<template>
  <div class="point-item">
    <p class="">
      {{ point.text }}
    </p>
    <b v-if="point.predicted_labels"> Förslag: {{ point.predicted_labels }}</b>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import type { CustomPoint } from './ClusterPlot.vue'
export default defineComponent({
  props: {
    point: {
      type: Object as PropType<CustomPoint>,
      required: true
    }
  }
})
</script>

<style scoped>
.label-text {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.point-item {
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f9f9f9;
  margin-bottom: 10px;
}
</style>
