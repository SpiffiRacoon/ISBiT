<template>
  <div id="label-text">
    <p class="point-item">
      {{ text }}
    </p>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
export default defineComponent({
  props: {
    text: String
  }
})
</script>

<style scoped>
#label-text {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.point-item {
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f9f9f9;
}
</style>
