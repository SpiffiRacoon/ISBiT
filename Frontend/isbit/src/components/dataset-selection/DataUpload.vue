<template>
  <div class="file-uploader">
    <h1>Ladda upp ett dataset</h1>
    <form @submit.prevent="uploadFiles">
      <div>
        <label for="fileName">Namn:</label>
        <input type="text" id="fileName" v-model="fileName" placeholder="Ange datasetets namn" />
      </div>
      <div>
        <label for="dataFile">Datafil:</label>
        <input type="file" id="dataFile" @change="handleFileChange('dataFile', $event)" />
      </div>

      <div>
        <label> Vill du ladda upp en Infofil eller fylla i informationen själv? </label>
        <div class="option-toggle">
          <label>
            <input type="radio" v-model="useCustomInfo" :value="false" />
            Ladda upp Infofil
          </label>
          <label>
            <input type="radio" v-model="useCustomInfo" :value="true" />
            Fyll i informationen själv
          </label>
        </div>
      </div>

      <div v-if="!useCustomInfo">
        <label for="infoFile">Infofil:</label>
        <input type="file" id="infoFile" @change="handleFileChange('infoFile', $event)" />
      </div>

      <div v-else class="info-fields">
        <label for="labels">Labels ex: a, b, c:</label>
        <input
          type="text"
          id="labels"
          v-model="infoData.labels"
          placeholder="Ange labels (ex: LOC, HUM, DESC)"
        />

        <label for="description">Beskrivning:</label>
        <textarea
          id="description"
          v-model="infoData.description"
          placeholder="Ange en beskrivning"
        ></textarea>
      </div>

      <button
        type="submit"
        :disabled="
          !fileName ||
          !dataFile ||
          (!useCustomInfo && !infoFile) ||
          (useCustomInfo && (!infoData.labels || !infoData.description))
        "
      >
        Ladda upp filer
      </button>
    </form>

    <div v-if="uploading">Uploading files...</div>
    <div v-if="successMessage">{{ successMessage }}</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'FileUploader',
  data() {
    return {
      fileName: '',
      dataFile: null,
      infoFile: null,
      infoData: {
        labels: '',
        description: ''
      },
      useCustomInfo: false,
      uploading: false,
      successMessage: '',
      errorMessage: ''
    }
  },
  methods: {
    handleFileChange(type, event) {
      const file = event.target.files[0]
      if (type === 'dataFile') {
        this.dataFile = file
      } else if (type === 'infoFile') {
        this.infoFile = file
      }
    },
    async uploadFiles() {
      if (
        !this.fileName ||
        !this.dataFile ||
        (!this.useCustomInfo && !this.infoFile) ||
        (this.useCustomInfo && (!this.infoData.labels || !this.infoData.description))
      ) {
        this.errorMessage = 'Alla fält är nödvändiga'
        return
      }

      const formData = new FormData()
      formData.append('uploaded_file', this.dataFile)

      if (this.useCustomInfo) {
        const infoFileContent = JSON.stringify({
          labels: this.infoData.labels.split(',').map((label) => label.trim()),
          description: this.infoData.description
        })
        const blob = new Blob([infoFileContent], { type: 'application/json' })
        formData.append('uploaded_info_file', blob, 'info.json')
      } else {
        formData.append('uploaded_info_file', this.infoFile)
      }

      this.uploading = true
      this.successMessage = ''
      this.errorMessage = ''

      try {
        const response = await axios.post(
          `http://localhost:8000/V1/dataset/?filename=${this.fileName}&delimiter=%2C`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        )
        this.successMessage = 'Filer uppladdade.'
        console.log(response.data)
      } catch (error) {
        this.errorMessage = 'Ett fel uppstod.'
        console.error(error)
      } finally {
        this.uploading = false
      }
    }
  }
}
</script>

<style>
.file-uploader {
  max-width: 600px;
  min-width: 450px;
  margin: 50px auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
  color: #333;
}

.file-uploader h1 {
  font-size: 1.8rem;
  margin-bottom: 20px;
  text-align: center;
  color: #444;
  font-weight: 700;
}

.file-uploader form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.file-uploader label {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 5px;
  color: #555;
}

.file-uploader input[type='text'],
.file-uploader input[type='file'],
.file-uploader textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.file-uploader input[type='text']:focus,
.file-uploader input[type='file']:focus,
.file-uploader textarea:focus {
  border-color: #007bff;
  outline: none;
}

.file-uploader textarea {
  resize: none;
  height: 100px;
}

.option-toggle {
  display: flex;
  justify-content: space-between;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 6px;
}

.option-toggle label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
}

.option-toggle input[type='radio'] {
  transform: scale(1.2);
  margin: 0;
}

.file-uploader button {
  padding: 12px 20px;
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
  background-color: #007bff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition:
    background-color 0.3s ease,
    transform 0.2s ease;
}

.file-uploader button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
  transform: none;
}

.file-uploader button:hover:not(:disabled) {
  background-color: #0056b3;
  transform: translateY(-2px);
}

.file-uploader .error {
  color: #d9534f;
  font-weight: 600;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 6px;
  padding: 10px;
  text-align: center;
}

.file-uploader div.uploading {
  font-size: 1rem;
  color: #6c757d;
  text-align: center;
}

.file-uploader div.success {
  color: #28a745;
  font-weight: 600;
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
  border-radius: 6px;
  padding: 10px;
  text-align: center;
}

.info-fields {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.info-fields input,
.info-fields textarea {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.info-fields input:focus,
.info-fields textarea:focus {
  border-color: #007bff;
  outline: none;
}
</style>
