import { createApp } from 'vue'
import App from './App.vue'

import router from './router'
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.bundle.js";

import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';

const app = createApp(App);
app.use(PrimeVue,{
    theme:{
        preset:Aura
    }
})
app.use(router)

app.mount('#app')

//createApp(App).mount('#app')
