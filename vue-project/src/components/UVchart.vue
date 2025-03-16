<script setup>
import { ref, onMounted } from "vue";
import backgroundVideo from "@/assets/sun_shine.mp4";
import { Chart, registerables } from "chart.js";
//import { onMounted, onUnmounted } from "vue";
Chart.register(...registerables);

const API_KEY = "8f28012836cadd0c0a2ca733ff0fcae8";
const locationInput = ref(""); 
const currentUV = ref(null); 
const cityName = ref(""); 
const errorMessage = ref(null); 
const recommendation = ref(""); 
const lastUpdated = ref(""); 

// save history UV data
const historicalUVData = ref([]);
const historicalDates = ref([]);

// get UV index
const fetchUVData = async () => {
  if (!locationInput.value.trim() || /[^a-zA-Z\s]/.test(locationInput.value)) {
    errorMessage.value = "Invalid location name. Please enter a valid city.";
    resetData();
    return;
  }

  try {
    const geoResponse = await fetch(
      `https://api.openweathermap.org/geo/1.0/direct?q=${encodeURIComponent(
        locationInput.value
      )}&limit=1&appid=${API_KEY}`
    );
    const geoData = await geoResponse.json();

    if (!geoData.length) {
      errorMessage.value = "Location not found.";
      resetData();
      return;
    }

    const { lat, lon, name } = geoData[0];
    cityName.value = name;

    await fetchUVIndex(lat, lon);
    await fetchHistoricalUVData(cityName.value);
  } catch (error) {
    showError("Error fetching UV data.");
  }
};

// get UV index from GPS
const fetchUVByGPS = () => {
  if (!navigator.geolocation) {
    showError("Geolocation is not supported by your browser.");
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const { latitude, longitude } = position.coords;
      cityName.value = "Current Location";
      await fetchUVIndex(latitude, longitude);
      await fetchHistoricalUVData(cityName.value);
    },
    () => {
      showError("Location access denied. Please enter a city manually.");
    }
  );
};

// get current UV index
const fetchUVIndex = async (lat, lon) => {
  try {
    const uvResponse = await fetch(
      `https://api.openweathermap.org/data/2.5/uvi?lat=${lat}&lon=${lon}&appid=${API_KEY}`
    );
    const uvData = await uvResponse.json();

    if (uvResponse.ok && uvData.value !== undefined) {
      currentUV.value = uvData.value;
      recommendation.value = getUVRecommendation(currentUV.value);
      lastUpdated.value = new Date().toLocaleTimeString();
      errorMessage.value = null;
    } else {
      throw new Error("UV data not found.");
    }
  } catch (error) {
    showError("Error retrieving UV data.");
  }
};

// for PostgreSQL API
const fetchHistoricalUVData = async (city) => {
  try {
    const response = await fetch(`/api/uv-history?city=${encodeURIComponent(city)}`);
    const data = await response.json();

    if (data.length) {
      historicalUVData.value = data.map(item => item.uv_index);
      historicalDates.value = data.map(item => item.date);
      updateChart();
    }
  } catch (error) {
    console.error("Error fetching historical UV data:", error);
  }
};

// UV protection advice
const getUVRecommendation = (index) => {
  if (index < 3)
    return "✔ Minimal protection needed. Sunscreen recommended for prolonged exposure. ☀️ Consider getting 15-30 minutes of midday sunlight for Vitamin D synthesis.";
  
  if (index < 6)
    return "🕶 Moderate risk: Wear sunglasses, use SPF 30+, and seek shade around midday.";

  if (index < 8)
    return "👕 High risk: Wear protective clothing, SPF 50+, and avoid midday sun (10 AM - 3 PM).";

  if (index < 11)
    return "🌞 Very High risk: Limit outdoor exposure, SPF 50+, wear a wide-brimmed hat and sunglasses.";

  return "🚨 Extreme risk! Avoid direct sun exposure, use SPF 50+, reapply sunscreen every 2 hours.";
};

// error message
const showError = (message) => {
  errorMessage.value = message;
  resetData();
};

// reset UV data
const resetData = () => {
  currentUV.value = null;
  recommendation.value = "UV protection tips unavailable. Check again later.";
  lastUpdated.value = "";
};

// create table for UV history
let uvChart = null;
const updateChart = () => {
  if (uvChart) {
    uvChart.destroy();
  }
  
  const ctx = document.getElementById("uvChart").getContext("2d");
  uvChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: historicalDates.value,
      datasets: [
        {
          label: "Historical UV Index",
          data: historicalUVData.value,
          borderColor: "orange",
          backgroundColor: "rgba(255, 165, 0, 0.2)",
          borderWidth: 2,
          tension: 0.2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          suggestedMax: 12,
        },
      },
    },
  });
};

onMounted(() => {
  fetchHistoricalUVData("Melbourne");
});
</script>

<template>
  <div class="homepage">
    <!-- Background vedio -->
    <video autoplay loop muted playsinline class="background-video">
      <source :src="backgroundVideo" type="video/mp4" />
    </video>

    <!-- Searching & GPS -->
    <div class="search-container">
      <input v-model="locationInput" placeholder="Enter city or postcode" />
      <button @click="fetchUVData">Search</button>
      <button class="gps-btn" @click="fetchUVByGPS">Use Current Location</button>
    </div>

    <!-- show UV data -->
    <div class="uv-container">
      <div v-if="currentUV !== null" class="uv-card">
        <h2>{{ cityName }}</h2>
        <p class="uv-index">{{ currentUV }}</p>
        <p class="last-updated">Last updated: {{ lastUpdated }}</p>
      </div>
    </div>

    <!-- UV protection advice -->
    <div v-if="currentUV !== null" class="recommendation-box">
      <p>{{ recommendation }}</p>
    </div>

    <!--  history UV data visualization -->
    <div v-if="historicalUVData.length" class="chart-container">
      <h3>Historical UV Index for {{ cityName }}</h3>
      <canvas id="uvChart"></canvas>
    </div>

    <!-- error message -->
    <div v-if="errorMessage" class="error-message">
      <p>{{ errorMessage }}</p>
    </div>
  </div>
</template>

<style scoped>
.chart-container {
  width: 80%;
  max-width: 600px;
  margin: 20px auto;
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
}

.background-video {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: -1;
}

/* Search Container */
.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 10px;
}

.search-container input {
  padding: 12px;
  font-size: 16px;
  border-radius: 8px;
  border: none;
  width: 250px;
  outline: none;
}

.search-container button {
  padding: 12px 18px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}

.search-container button:hover {
  transform: scale(1.05);
}

.gps-btn {
  background-color: #0077cc;
  color: white;
}

.gps-btn:hover {
  background-color: #005fa3;
}

/* UV Data */
.uv-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
}

.uv-card {
  background: rgba(0, 0, 0, 0.6);
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  color: white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.uv-index {
  font-size: 22px;
  font-weight: bold;
}

.last-updated {
  font-size: 14px;
  margin-top: 5px;
  color: lightgray;
}

/* UV advice */
.recommendation-box {
  background: rgba(255, 255, 255, 0.2);
  padding: 15px;
  border-radius: 10px;
  text-align: center;
  color: rgb(0, 92, 12);
  margin-top: 20px;
  font-size: 20px; 
  font-weight: bold; 
}


/* Error Message */
.error-message {
  text-align: center;
  color: red;
  margin-top: 10px;
  font-size: 16px;
}
</style>
