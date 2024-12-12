<template>
  <div id="label-text">
    <div class="column">
      <h5>Omärkta punkter</h5>
      <div v-for="(point, index) in unmarkedPoints" :key="index" class="point-item">
        <p>{{ point.text }}</p>
        <b v-if="point.predicted_labels">Förslag: {{ point.predicted_labels }}</b>
        <button @click="removePoint(point.id)">avmarkera</button>
      </div>
    </div>
    <div class="column">
      <h5>
        Markerade Punkter
        <button @click="showMarkedPoints = !showMarkedPoints" class="dropdown-button">
          {{ showMarkedPoints ? '-' : '+' }}
        </button>
      </h5>
      <div v-if="showMarkedPoints">
        <div v-for="(point, index) in markedPoints" :key="index" class="point-item">
          <p>{{ point.text }}</p>
          <b>Sanning: {{ point.truth }}</b>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import type { CustomPoint } from './ClusterPlot.vue'

export default defineComponent({
  props: {
    points: {
      type: Array as PropType<CustomPoint[]>,
      required: true
    }
  },
  data() {
    return {
      showMarkedPoints: true
    }
  },
  computed: {
    unmarkedPoints() {
      console.log(this.points)
      return this.points.filter((point) => point.input_label === null)
    },
    markedPoints() {
      return this.points.filter((point) => point.input_label !== null)
    }
  },
  methods: {
    removePoint(id: string) {
      this.$emit('remove-point', id)
    }
  }
})
</script>

<style scoped>
#label-text {
  display: flex;
  gap: 20px;
}

.column {
  flex: 1;
}

.point-item {
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f9f9f9;
  margin-bottom: 10px;
}

.point-item p {
  margin: 0;
  font-size: 14px;
}

.point-item button {
  margin-top: 5px;
  background-color: #e74c3c;
  color: #fff;
  border: none;
  padding: 5px 8px;
  border-radius: 3px;
  cursor: pointer;
}

.point-item button:hover {
  background-color: #c0392b;
}

.dropdown-button {
  border-radius: 3px;
  float: right;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 10px;
  font-size: 14px;
}
</style>
