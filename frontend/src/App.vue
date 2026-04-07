<template>
  <div class="app">
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
          <input
            type="file"
            ref="fileInput"
            @change="handleFile"
            hidden
            accept="image/*"
          />
        </div>

        <button type="submit">Generate Report</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      name: "",
      email: "",
      datetime: "",
      location: "",
      file: null,
    };
  },
  methods: {
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
      console.log({
        name: this.name,
        email: this.email,
        datetime: this.datetime,
        location: this.location,
        file: this.file,
      });
      this.file = e.target.files[0];
      const formData = new FormData();
      formData.append("file", this.file);
      formData.append("name", this.name);
      formData.append("datetime", this.datetime);
      formData.append("location", this.location);
      formData.append("email", this.email);

      const url = this.$BASE_URL + "/order_without_payment/";

      this.showSpinner = true;
      axios.post(url, formData).then((response) => {
        this.showSpinner = false;
        if (!response.data.auth_fail) {
          this.isAuthenticated = true;
          this.getVersions();
        } else {
          this.isAuthenticated = false;
          this.$router.push("/login/");
        }
      });
    },
  },
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
