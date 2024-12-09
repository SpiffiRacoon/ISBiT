<script setup lang="ts">
import LabelBox from './LabelBox.vue'
import TextBox from './TextBox.vue'
import MultiplePointText from './MultiplePointText.vue'
import ClusterPlot from './ClusterPlot.vue'
import { useRoute } from 'vue-router'
</script>

<template>
  <div id="label-menu">
    <div class="block">
      <h2>Dataset: {{ dataset }}</h2>
      <ClusterPlot
        @point-click="(point) => receivePoint(point)"
        @points-marked="(points) => receivePoints(points)"
        :multiple-marking="multipleMarking"
        :active-point="activePoint"
        :active-points="activePoints"
      />
    </div>
    <div id="text-and-labels">
      <h4>Märk Upp Datapunkt</h4>
      <MultiplePointText
        @remove-point="handleRemovePoint"
        v-if="multipleMarking"
        :points="activePoints"
      />
      <TextBox v-else :text="activePoint.text" />

      <LabelBox
        :alternatives="['LOC', 'HUM', 'DESC', 'ENTY', 'ABBR', 'NUM']"
        @mark-point="(category) => categorizeNode(category)"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import type { CustomPoint } from './ClusterPlot.vue'
import axios from 'axios'

export default defineComponent({
  props: {
    text: String
  },
  data() {
    return {
      apiData: { t: String },
      activePoint: { text: 'Välj en punkt i plotten.' } as CustomPoint,
      activePoints: [] as CustomPoint[],
      multipleMarking: false,
      dataset: ''
    }
  },
  created() {
    const route = useRoute()
    this.dataset = route.query.dataset as string
  },
  methods: {
    receivePoint(point: CustomPoint) {
      if (point == null) {
        return
      }
      this.activePoint = point
      this.multipleMarking = false
    },
    receivePoints(points: CustomPoint[]) {
      const pointsArray = points
      if (pointsArray.length >= 1) {
        this.activePoints = points
        this.multipleMarking = true
      }
    },
    handleRemovePoint(id: string) {
      console.log('remove point with id: ', id)
      this.activePoints = this.activePoints.filter((point) => point.id !== id)
    },
    categorizeNode(category: string) {
      try {
        axios.post(
          `http://localhost:8000/V1/data/categorize?node_id=${this.activePoint.id}&category=${category}&dataset_name=${this.dataset}`
        )
        window.location.reload()
      } catch (err) {
        console.error(err)
      }
    }
  }
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
