<template>
    <div id="app">
      <FileUploader />
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue'
  import FileUploader from '../components/dataset-selection/DataUpload.vue'
  
  export default defineComponent({
    name: 'UploadView',
    components: {
        FileUploader
    }
  })
  </script>
  
  <style scoped>
  #app {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
  </style>
  