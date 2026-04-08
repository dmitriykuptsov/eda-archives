<template>
  <div class="app">
    <SimpleSpinner v-if="showSpinner" />
    <div class="card">
      <h1>EDA-Archives</h1>
      <p>Create your personalized historical report</p>

      <form @submit.prevent="submitForm" class="form">
        <input type="text" v-model="name" placeholder="Full Name" required />

        <input type="email" v-model="email" placeholder="Email Address" required />

        <input type="date" v-model="datetime" required />

        <input type="text" v-model="location" placeholder="Birth Location" required />

        <div
          class="dropzone"
          @dragover.prevent
          @drop.prevent="handleDrop"
          @click="triggerFile"
        >
          <p v-if="!file">Drag & Drop your photo or click to upload</p>
          <p v-else>{{ file.name }}</p>
          <p v-if="missingFile">File is missing</p>
          <input
            type="file"
            ref="fileInput"
            @change="handleFile"
            hidden
            accept="image/*"
          />
        </div>
        <div class="badge badge-danger" v-if="showMessage">{{message}}</div>
        <button type="submit">Generate Report</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import SimpleSpinner from "./components/SimpleSpinner.vue";

export default {
  data() {
    return {
      name: "",
      email: "",
      datetime: "",
      location: "",
      file: null,
      missingFile: false,
      showMessage: true,
      message: "",
      showSpinner: false
    };
  },
  methods: {
    formatDate(date) {
      if (!date) {
        return;
      }
      if (date.getDate() < 10) {
        var day = "0" + date.getDate();
      } else {
        var day = date.getDate();
      }
      if (date.getMonth() + 1 < 10) {
        var month = "0" + (date.getMonth() + 1);
      } else {
        var month = (date.getMonth() + 1);
      }
      return day + "." + month + "." + date.getFullYear();
    },
    handleFile(event) {
      this.file = event.target.files[0];
    },
    handleDrop(event) {
      this.file = event.dataTransfer.files[0];
    },
    triggerFile() {
      this.$refs.fileInput.click();
    },
    submitForm() {
      if (!this.file) {
        this.showMessage = true;
        this.message = "File is missing";
        return;
      }
      this.missingFile = false;
      const formData = new FormData();
      formData.append("file", this.file);
      formData.append("name", this.name);
      formData.append("date", this.formatDate(new Date(this.datetime)));
      formData.append("location", this.location);
      formData.append("email", this.email);

      const url = this.$BASE_URL + "api/order_without_payment";
      this.showSpinner = true;
      axios.post(url, formData).then((response) => {
        this.showSpinner = false;
        this.showMessage = true;
        if (response.data.success) {
          this.message = "Please check your email inbox (" + this.email + "). We will send you link for the report download shortly...";
        } else {
          this.message = response.data.reason;
        }
      });
    },
  },
  components: {
    SimpleSpinner,
  }
};
</script>

<style>
body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  background: linear-gradient(135deg, #1e293b, #0f172a);
  color: white;
}

.app {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100%;
}

.card {
  background: #111827;
  padding: 30px;
  border-radius: 16px;
  width: 400px;
  position: absolute;
  left: calc(50% - 200px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  text-align: center;
}

h1 {
  margin-bottom: 5px;
}

p {
  margin-bottom: 20px;
  color: #9ca3af;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

input {
  padding: 12px;
  border-radius: 10px;
  border: none;
  background: #1f2937;
  color: white;
}

input::placeholder {
  color: #6b7280;
}

.dropzone {
  border: 2px dashed #38bdf8;
  padding: 20px;
  border-radius: 12px;
  cursor: pointer;
  transition: 0.3s;
}

.dropzone:hover {
  background: rgba(56, 189, 248, 0.1);
}

button {
  margin-top: 10px;
  padding: 12px;
  border: none;
  border-radius: 10px;
  background: #38bdf8;
  color: black;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}

button:hover {
  background: #0ea5e9;
}
</style>
