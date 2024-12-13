<template>
  <div @click="runModel()" class="proc-data">
    <button class="btn third-btn">
      Kör modell
      <span v-if="loading" class="loading-indicator">
        <i class="loading-spinner"></i>
      </span>
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: 'DataDisplay',
  props: {
    file: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      loading: false
    }
  },
  methods: {
    async runModel() {
      this.loading = true
      try {
        await axios.post(
          'http://localhost:8000/V1/run_ml/?model_name=QaqcMainModel&file=' + this.file
        )
        console.log(`Model run initiated for dataset ${this.file}`)
        this.startPolling()
      } catch (err) {
        console.error(err)
      }
    },
    async startPolling() {
      const interval = setInterval(async () => {
        const status = await this.getStatus()
        if (status === 'Not running') {
          console.log('Model run completed')
          clearInterval(interval)
          this.loading = false
          window.location.reload()
        }
      }, 500)
    },
    async getStatus() {
      try {
        const response = await axios.get(
          `http://localhost:8000/V1/run_ml/?model_name=QaqcMainModel&file=${this.file}`
        )
        return response.data.status
      } catch (err) {
        console.error('Error fetching status', err)
        return null
      }
    }
  }
})
</script>

<style scoped>
.proc-data {
  margin: 10px;
  padding: 5px 5px;
  background-color: #f0f0f0;
  border: 2px solid green;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition:
    background-color 0.3s,
    color 0.3s;
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
