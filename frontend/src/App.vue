<template>
  <div class="app">
    <SimpleSpinner v-if="showSpinner" />
    <div class="section">
      <p class="header">EDA Archives</p>
      <p class="slogan1">YOUR STORY STARTED HERE</p>
      <p class="slogan2">Gift Digital Archive: discover what the world was like on the day you were born</p>
      <button onclick="location.href='#section2'">Open the Archive</button>
    </div>

    <div id="section2" class="section">
      <!-- img src="@/assets/main.jpg" width="200px;" -->
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
html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  background-image: url("@/assets/background.jpg");
  color: white;
}

.section {
  height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  scroll-snap-align: start;
  justify-content: center;
  align-items: center;
}

.app {
  height: 200vh;
}

.card {
  background: #ab8d22;
  padding: 30px;
  border-radius: 16px;
  width: 400px;
  position: absolute;
  left: calc(50% - 200px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  text-align: center;
}

.header {
  font-size: 20px;
  font-weight: bolder;
}

.slogan1 {
  font-size: 50px;
  font-weight: bolder;
}

.slogan2 {
  font-size: 30px;
  font-weight: bolder;
}

h1 {
  margin-bottom: 5px;
}

p {
  margin-bottom: 20px;
  color: #ffffff;
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
  background: #403200;
  color: white;
}

input::placeholder {
  color: #ffffff;
}

.dropzone {
  border: 2px dashed #ffffff;
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
  border-radius: 30px;
  background: #ffffff;
  color: black;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}

button:hover {
  background: #4d401d;
}
</style>
