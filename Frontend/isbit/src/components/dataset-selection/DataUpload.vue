<template>
  <div class="file-uploader">
    <h1>Ladda upp ett dataset</h1>
    <form @submit.prevent="uploadFiles">
      <div>
        <label for="fileName">Filnamn:</label>
        <input
          type="text"
          id="fileName"
          v-model="fileName"
          placeholder="Ange filnamn"
        />
      </div>
      <div>
        <label for="dataFile">Data-fil:</label>
        <input
          type="file"
          id="dataFile"
          @change="handleFileChange('dataFile', $event)"
        />
      </div>
      <div>
        <label for="infoFile">Info-fil:</label>
        <input
          type="file"
          id="infoFile"
          @change="handleFileChange('infoFile', $event)"
        />
      </div>
      <button
        type="submit"
        :disabled="!fileName || !dataFile || !infoFile"
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
import axios from "axios";

export default {
  name: "FileUploader",
  data() {
    return {
      fileName: "",
      dataFile: null,
      infoFile: null,
      uploading: false,
      successMessage: "",
      errorMessage: "",
    };
  },
  methods: {
    handleFileChange(type, event) {
      const file = event.target.files[0];
      if (type === "dataFile") {
        this.dataFile = file;
      } else if (type === "infoFile") {
        this.infoFile = file;
      }
    },
    async uploadFiles() {
      if (!this.fileName || !this.dataFile || !this.infoFile) {
        this.errorMessage = "Alla fält är nödvändiga";
        return;
      }

      const formData = new FormData();
      formData.append("uploaded_file", this.dataFile);
      formData.append("uploaded_info_file", this.infoFile);

      this.uploading = true;
      this.successMessage = "";
      this.errorMessage = "";

      try {
        const response = await axios.post(
          `http://localhost:8000/V1/dataset/?filename=${this.fileName}`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        this.successMessage = "Filer uppladdade.";
        console.log(response.data);
      } catch (error) {
        this.errorMessage = "Ett fel uppstod.";
        console.error(error);
      } finally {
        this.uploading = false;
      }
    },
  },
};
</script>

<style>
.file-uploader {
  min-width: 400px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
  text-align: left;
}

.file-uploader h1 {
  font-size: 1.8em;
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

.file-uploader form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.file-uploader label {
  font-weight: bold;
  margin-bottom: 5px;
  color: #555;
}

.file-uploader input[type="text"],
.file-uploader input[type="file"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1em;
}

.file-uploader button {
  padding: 10px 15px;
  background-color: #007bff;
  color: #fff;
  font-size: 1em;
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.file-uploader button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

.file-uploader button:hover:not(:disabled) {
  background-color: #0056b3;
}

.file-uploader .error {
  color: #d9534f;
  font-weight: bold;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 5px;
  padding: 10px;
  margin-top: 10px;
}

.file-uploader div.uploading {
  font-size: 1em;
  color: #6c757d;
  margin-top: 10px;
}

.file-uploader div.success {
  color: #28a745;
  font-weight: bold;
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
  border-radius: 5px;
  padding: 10px;
  margin-top: 10px;
}

form > div {
  display: flex;
  flex-direction: column;
}
</style>