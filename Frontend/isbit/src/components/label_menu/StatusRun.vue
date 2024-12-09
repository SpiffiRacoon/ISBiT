<template>
    <div
    @click="runModel()" 
    class="proc-data"
    >
        <button class="btn third-btn" >
        Processa uppmärkta data punker: 
        </button>
    </div>

    

  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue'
  import axios from 'axios'
  
  export default defineComponent({
    name: 'DataDisplay',
    setup() {
      const dataList = ref<any[]>([])
      const availableDatasets = ref<any[]>([])
      const error = ref<string | null>(null)
      const loading = ref<boolean>(false)
  
      const fetchData = async () => {
        try {
          const filesResponse = await axios.get('http://localhost:8000/V1/dataset/files')
          dataList.value = filesResponse.data.dataList
  
          const availableDataResponse = await axios.get('http://localhost:8000/V1/dataset')
          availableDatasets.value = availableDataResponse.data.dataList
        } catch (err) {
          error.value = 'Error fetching data'
          console.error(err)
        }
      }
  
      return {
        dataList,
        availableDatasets,
        error,
        fetchData,
        loading
      }
    },
    methods: {
      redirectToDetails(dataset: string) {
        this.$router.push({ path: '/label', query: { dataset: dataset } })
      },
      async runModel() {
        try {
          //this.dataList[index].loading = true
          //TOOD: fix model name
          await axios.post(
            'http://localhost:8000/V1/run_ml/?model_name=QaqcMainModel&file=j_test'
              //file
          )
          console.log(`Model run initiated for dataset TESTJACKE`)
          //this.startPolling(file, index)
        } catch (err) {
          this.error = 'Error running model'
          console.error(err)
        }
      },
    },
    mounted() {
      this.fetchData()
    }
  })
  </script>
  
  <style scoped>
  .proc-data {
    margin: 10px;
    padding: 5px 5px;
    background-color: #f0f0f0;
    border: 2px solid;
    border-color: green;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    transition:
        background-color 0.3s,
        color 0.3s;
  }
  </style>
  