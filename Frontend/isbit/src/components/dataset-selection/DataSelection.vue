<template>
  <div class="container">
    <h1 class="header">Dataset Information</h1>
    <div v-if="error" class="error">{{ error }}</div>
    <div class="card" v-for="(item, index) in combinedDataList" :key="index">
      <div class="card-content">
        <h2 class="card-title">{{ item.dataset }}</h2>
        <div class="card-details">
          <div class="label-group">
            <p v-if="isDataAvailable(item.dataset)" class="label">
              <i class="icon assignment-icon"></i>
              <strong>Uppgift:</strong> {{ item.assignment }}
            </p>
            <p v-if="isDataAvailable(item.dataset)" class="label">
              <i class="icon datatype-icon"></i>
              <strong>Typ av data:</strong> {{ item.datatype }}
            </p>
            <p class="availability">
              <strong>Tillgänglighet:</strong>
              {{ isDataAvailable(item.dataset) ? 'Tillgänglig' : 'Ej tillgänglig' }}
            </p>
          </div>

          <div class="button-container">
            <button 
              v-if="isDataAvailable(item.dataset)" 
              @click="redirectToDetails(item.dataset)"
              class="btn primary-btn"
            >
              Uppmärk Data
            </button>
            <button
            v-if="isDataAvailable(item.dataset)" 
              @click="removeDataset(item.dataset)"
              class="btn third-btn"
            >
              Ta bort dataset
            </button>
          </div>

          <button
            @click="runModel(item.dataset, index)"
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
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'DataDisplay',
  setup() {
    const dataList = ref<any[]>([]);
    const availableDatasets = ref<any[]>([]);
    const combinedDataList = ref<any[]>([]);
    const error = ref<string | null>(null);
    const loading = ref<boolean>(false); 

    const fetchData = async () => {
      try {
        const filesResponse = await axios.get('http://localhost:8000/V1/dataset/files');
        console.log('Data files fetched:', filesResponse.data);
        dataList.value = filesResponse.data.dataList;

        const availableDataResponse = await axios.get('http://localhost:8000/V1/dataset');
        console.log('Data availability fetched:', availableDataResponse.data);
        availableDatasets.value = availableDataResponse.data.dataList;

        combineData();
      } catch (err) {
        error.value = 'Error fetching data';
        console.error(err);
      }
    };

    const combineData = () => {
      combinedDataList.value = dataList.value.map(file => {
        const availableData = availableDatasets.value.find(item => item.dataset === file.dataset);
        return {
          ...file,
          assignment: availableData ? availableData.assignment : null,
          datatype: availableData ? availableData.datatype : null,
          loading: false
        };
      });
    };


    const isDataAvailable = (dataset: string): boolean => {
      return availableDatasets.value.some(item => item.dataset === dataset);
    };

    onMounted(fetchData);

    return {
      combinedDataList,
      error,
      isDataAvailable,
      fetchData,
      loading 
    };
  },
  methods: {
    redirectToDetails(dataset: string) {
      this.$router.push({ path: '/label', query: { dataset: dataset } });
    },
    async runModel(file: string, index: number) {
      try {
          this.combinedDataList[index].loading = true;
          await axios.get('http://localhost:8000/V1/run_ml/?model_name=qaqc_main&file=' + file + '&dim_red_method=COMBO');
          console.log(`Model run for dataset ${file}`);
          this.fetchData();
      } catch (err) {
        this.error = 'Error running model';
        console.error(err);
      } finally {
        this.combinedDataList[index].loading = false; 
      }
    },
    async removeDataset(dataset: string) {
      try {
        await axios.delete('http://localhost:8000/V1/dataset/?dataset=' + dataset);
        console.log(`Dataset ${dataset} removed`);
        this.fetchData();
      } catch (err) {
        this.error = 'Error removing dataset';
        console.error(err);
      }

    }
  }
});
</script>


<style scoped>
.container {
  padding: 20px;
}

.header {
  font-size: 2em;
  margin-bottom: 20px;
}

.card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  padding: 15px;
  transition: transform 0.2s;
}

.card:hover {
  transform: scale(1.02);
}

.card-title {
  font-size: 1.5em;
  color: #2c3e50;
}

.label-group {
  margin-bottom: 15px;
}

.label {
  font-size: 1.1em;
  color: #34495e;
}

.availability {
  font-weight: bold;
}

.btn {
  padding: 2px 5px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 10px;
}
.button-container {
  display: flex;
  align-items: center; 
}

.primary-btn {
  background-color: #3498db;
  color: #fff;
  margin-bottom: 5px;
}

.secondary-btn {
  background-color: #e67e22;
  color: #fff;
}

.third-btn {
  background-color: #e74c3c;
  color: #fff;
  margin-bottom: 5px;
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
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>