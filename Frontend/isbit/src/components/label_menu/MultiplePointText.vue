<template>
    <div id="label-text">
      <div v-for="(point, index) in points" :key="index" class="point-item">
        <p>{{ point.text }}</p> 
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
  
  .point-item p {
    margin: 0;
    font-size: 14px;
  }
  </style>
  