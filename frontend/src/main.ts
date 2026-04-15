import './assets/main.css'
import { createApp } from "vue";
import App from "./App.vue";

const app = createApp(App)
//app.config.globalProperties["$BASE_URL"] = "https://eda-archives.com/";
app.config.globalProperties["$BASE_URL"] = "http://127.0.0.1/";
app.mount("#app");
