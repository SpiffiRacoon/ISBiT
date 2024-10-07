<template>
  <div class="container">
    <h1>Dataset Information</h1>
    <div v-if="error" class="error">{{ error }}</div> <!-- Error handling -->
    <div class="card" v-for="(item, index) in dataList" :key="index">
      <div class="card-content">
        <h2>{{ item.dataset }}</h2>
        <div class="card-details">
          <div class="label-group">
            <p><strong>Uppgift:</strong> {{ item.assignment }}</p>
            <p><strong>Typ av data:</strong> {{ item.datatype }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import axios from 'axios';

export default defineComponent({
  name: 'DataDisplay',
  setup() {
    const dataList = ref<any[]>([]);
    const error = ref<string | null>(null);

    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/V1/dataset');
        console.log("Data fetched:", response.data);
        dataList.value = response.data.dataList; 
      } catch (err) {
        error.value = 'Error fetching data';
        console.error(err);
      }
    };

    onMounted(fetchData);

    return {
      dataList,
      error,
    };
  },
});
</script>

<style scoped>

.container {
  font-family: Arial, sans-serif;
  padding: 20px;
  max-width: 1100px;
  margin: 0 auto;
  background-color: #f9f9f9;
}

h1 {
  text-align: center;
  font-size: 28px;
  color: #333;
  margin-bottom: 30px;
}

.card {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 0;
  margin: 20px 0;
  padding: 25px 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
  width: 100%;
}

.card:hover {
  transform: scale(1.02);
}

.card-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start; 
  gap: 30px; 
}

.card h2 {
  margin: 0;
  font-size: 22px;
  color: #333;
  flex-shrink: 0; 
}

.card-details {
  display: flex;
  flex-wrap: wrap; 
  align-items: center;
}

.label-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.label-group p {
  margin: 0;
  font-size: 16px;
  color: #666;
  white-space: nowrap; 
}

@media (max-width: 768px) {
  .card-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .card-details {
    flex-direction: column;
  }

  .card h2 {
    font-size: 18px;
  }
}
</style>
