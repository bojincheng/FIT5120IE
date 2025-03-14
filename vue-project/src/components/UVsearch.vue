<script setup>
import { ref } from "vue";
import backgroundVideo from "@/assets/bg.mp4";

const API_KEY = "8f28012836cadd0c0a2ca733ff0fcae8"; // API Key
const locationInput = ref(""); // Location
const currentUV = ref(null); //  UV Index
const cityName = ref(""); // City name
const errorMessage = ref(null); // error message
const recommendation = ref(""); // UV protection advice

// get UV Index
const fetchUVData = async () => {
  if (!locationInput.value.trim()) {
    errorMessage.value = "Please enter a city or postcode.";
    currentUV.value = null;
    recommendation.value = "UV protection tips unavailable. Check again later.";
    return;
  }

  try {
    // get location
    const geoResponse = await fetch(
      `https://api.openweathermap.org/geo/1.0/direct?q=${encodeURIComponent(locationInput.value)}&limit=1&appid=${API_KEY}`
    );
    const geoData = await geoResponse.json();

    if (!geoData.length) {
      errorMessage.value = "Location not found.";
      return;
    }

    const { lat, lon, name } = geoData[0];
    cityName.value = name;

    // get UV Index
    const uvResponse = await fetch(
      `https://api.openweathermap.org/data/2.5/uvi?lat=${lat}&lon=${lon}&appid=${API_KEY}`
    );
    const uvData = await uvResponse.json();

    if (uvResponse.ok && uvData.value !== undefined) {
      currentUV.value = uvData.value;
      errorMessage.value = null;
      recommendation.value = getUVRecommendation(currentUV.value);
    } else {
      throw new Error("UV data not found.");
    }
  } catch (error) {
    currentUV.value = null;
    errorMessage.value = "Error fetching UV data.";
    recommendation.value = "UV protection tips unavailable. Check again later.";
    console.error("API Error:", error);
  }
};

// colculate UV Index color
const getUVColor = (index) => {
  if (index < 3) return "green";
  if (index < 6) return "yellow";
  if (index < 8) return "orange";
  if (index < 11) return "red";
  return "purple";
};

//  UV protection advice
const getUVRecommendation = (index) => {
  if (index < 3)
    return "✔ Minimal protection needed, but sunscreen recommended for prolonged exposure.";
  if (index < 6)
    return "🕶 Wear sunglasses, use SPF 30+, and seek shade around midday.";
  if (index < 8)
    return "👕 Wear protective clothing, SPF 50+, avoid midday sun (10 AM - 3 PM).";
  if (index < 11)
    return "🌞 Limit outdoor exposure, SPF 50+, wear a wide-brimmed hat and sunglasses.";
  return "🚨 Avoid direct sun exposure, use SPF 50+, reapply sunscreen every 2 hours.";
};
</script>

<template>
  <div class="homepage">
    <!-- Background Video -->
    <video autoplay loop muted playsinline class="background-video">
      <source :src="backgroundVideo" type="video/mp4" />
    </video>

    <!-- Search Bar -->
    <div class="search-container">
      <input v-model="locationInput" placeholder="Enter city or postcode" />
      <button @click="fetchUVData">Search</button>
    </div>

    <!-- UV Data Display -->
    <div class="uv-container">
      <!-- Current UV Index -->
      <div class="uv-card">
        <h2>{{ cityName }}</h2>
        <p class="uv-index" :style="{ color: getUVColor(currentUV) }">
          UV Index: {{ currentUV }}
        </p>
      </div>
    </div>

    <!-- UV Protection Recommendation Box -->
    <div v-if="currentUV !== null" class="recommendation-box">
      <p>{{ recommendation }}</p>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="error-message">
      <p>{{ errorMessage }}</p>
    </div>
  </div>
</template>

<style scoped>
/* Background Video */
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
  background-color: #ff6600;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}

.search-container button:hover {
  background-color: #e65c00;
  transform: scale(1.05);
}

/* UV Data Display */
.uv-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
}

/* Current UV Card */
.uv-card {
  background: rgba(0, 0, 0, 0.6);
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  color: white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

/* UV Index Text */
.uv-index {
  font-size: 22px;
  font-weight: bold;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.5);
}

/* Recommendation Box */
.recommendation-box {
  background: rgba(255, 255, 255, 0.2);
  padding: 15px;
  border-radius: 10px;
  text-align: center;
  color: white;
  margin-top: 20px;
  backdrop-filter: blur(5px);
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  font-size: 16px;
}

/* Error Message */
.error-message {
  text-align: center;
  color: red;
  margin-top: 10px;
  font-size: 16px;
}

/* Responsive Design */
@media screen and (max-width: 600px) {
  .search-container {
    flex-direction: column;
  }

  .search-container input {
    width: 80%;
    margin-bottom: 10px;
  }

  .search-container button {
    width: 50%;
  }

  .recommendation-box {
    font-size: 14px;
    padding: 10px;
  }
}
</style>
