<template>
  <div class="container">
    <div v-if="error" class="error">{{ error }}</div>

    <div class="lists-container">
      <div class="list-column">
        <h2 class="list-title">Bearbetade Dataset</h2>
        <div class="card" v-for="(item, index) in availableDatasets" :key="index">
          <div class="card-content">
            <h3 class="card-title">{{ item.dataset }}</h3>
            <div class="card-details">
              <div class="label-group">
                <p class="label">
                  <i class="icon assignment-icon"></i>
                  <strong>Uppgift:</strong> {{ item.assignment }}
                </p>
                <p class="label">
                  <i class="icon datatype-icon"></i>
                  <strong>Typ av data:</strong> {{ item.datatype }}
                </p>
              </div>

              <div class="button-container">
                <button @click="redirectToDetails(item.dataset)" class="btn primary-btn">
                  Märk upp data
                </button>
                <button @click="removeDataset(item.dataset)" class="btn third-btn">
                  Ta bort dataset
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="list-column">
        <h2 class="list-title">Tillgängliga Dataset</h2>
        <div class="card" v-for="(item, index) in dataList" :key="index">
          <div class="card-content">
            <h3 class="card-title">{{ item.dataset }}</h3>
            <div class="run-container">
              <div class="select-label">
                <p>Välj modell:</p>
                <select v-model="item.dimRedMethod">
                  <option value="PCA">PCA</option>
                  <option value="UMAP">UMAP</option>
                  <option value="TSNE">TSNE</option>
                  <option value="COMBO">COMBO</option>
                </select>
              </div>
              <button
                @click="runModel(item.dataset, index, item.dimRedMethod)"
                class="btn secondary-btn"
              >
                Kör modell
                <span v-if="item.loading" class="loading-indicator">
                  <i class="loading-spinner"></i>
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
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
    async runModel(file: string, index: number, dimRedMethod: string) {
      try {
        this.dataList[index].loading = true
        //TOOD: fix model name
        await axios.post(
          'http://localhost:8000/V1/run_ml/?model_name=QaqcMainModel&file=' +
            file +
            '&dim_red_method=' +
            dimRedMethod
        )
        console.log(`Model run initiated for dataset ${file}`)
        this.startPolling(file, index)
      } catch (err) {
        this.error = 'Error running model'
        console.error(err)
      }
    },
    async startPolling(file: string, index: number) {
      const interval = setInterval(async () => {
        const status = await this.getStatus(file)
        if (status === 'Not running') {
          console.log('Model run completed')
          this.dataList[index].loading = false

          clearInterval(interval)
          this.fetchData()
        }
      }, 500)
    },
    async getStatus(file: string) {
      try {
        const response = await axios.get(
          `http://localhost:8000/V1/run_ml/?model_name=QaqcMainModel&file=${file}`
        )
        return response.data.status
      } catch (err) {
        console.error('Error fetching status', err)
        return null
      }
    },
    async removeDataset(dataset: string) {
      try {
        await axios.delete('http://localhost:8000/V1/dataset/?dataset=' + dataset)
        console.log(`Dataset ${dataset} removed`)
        this.fetchData()
      } catch (err) {
        this.error = 'Error removing dataset'
        console.error(err)
      }
    }
  },
  mounted() {
    this.fetchData()
  }
})
</script>

<style scoped>
.container {
  padding: 20px;
  min-height: 100vh; /* Ensure the container spans the full viewport height */
  box-sizing: border-box; /* Includes padding in total height */
}

.header {
  font-size: 2em;
  margin-bottom: 20px;
}

.lists-container {
  display: flex;
  justify-content: space-between;
  gap: 40px;
  align-items: flex-start;
  position:absolute;
}

.list-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
}

.card {
  background: #fff;
  border-radius: 7px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s;
}

.card-content {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-title {
  font-size: 1.3em;
  color: #2c3e50;
  margin-bottom: 10px;
}

.button-container {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  margin-top: auto;
  padding-top: 10px;
}

.run-container {
  display: flex;
  align-items: center;
}

.select-label {
  margin-bottom: 10px;
}

.primary-btn,
.secondary-btn,
.third-btn {
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.primary-btn {
  background-color: #3498db;
  color: #fff;
}

.secondary-btn {
  background-color: #e67e22;
  color: #fff;
}

.third-btn {
  background-color: #e74c3c;
  color: #fff;
}

.btn:hover {
  opacity: 0.9;
}

.loading-indicator {
  margin-left: 5px;
}

.icon {
  margin-right: 5px;
}

.loading-spinner {
  display: inline-block;
  width: 12px;
  height: 12px;
  border: 2px solid #3498db;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
