<template>
  <div id="app">
    <DataDisplay />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import DataDisplay from '../components/dataset-selection/DataSelection.vue';

export default defineComponent({
  name: 'DataView',
  components: {
    DataDisplay
  }
});
</script>

<style scoped>
#app {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; 
}
</style>
