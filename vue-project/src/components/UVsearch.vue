<script setup>
import { ref, onMounted } from "vue";
import backgroundVideo from "@/assets/sun_shine.mp4";

const API_KEY = "8f28012836cadd0c0a2ca733ff0fcae8"; // API Key
const locationInput = ref(""); // User input location
const currentUV = ref(null); // UV Index value
const cityName = ref(""); // City name
const errorMessage = ref(null); // Error message
const recommendation = ref(""); // UV protection advice
const lastUpdated = ref(""); // Last updated timestamp

// Get UV Index by manually entering a city or suburb
const fetchUVData = async () => {
  if (!locationInput.value.trim() || /[^a-zA-Z\s]/.test(locationInput.value)) {
    errorMessage.value = "Invalid location name. Please enter a valid city.";
    resetData();
    return;
  }

  try {
    // Get location coordinates
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

    // Get UV Index
    await fetchUVIndex(lat, lon);
  } catch (error) {
    showError("Error fetching UV data.");
  }
};

// Get UV Index using GPS location
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
    },
    () => {
      showError("Location access denied. Please enter a city manually.");
    }
  );
};

// Fetch UV Index Data
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

// Get UV Index color coding
const getUVColor = (index) => {
  if (index < 3) return "green";
  if (index < 6) return "yellow";
  if (index < 8) return "orange";
  if (index < 11) return "red";
  return "purple";
};

// Provide sun protection recommendations
const getUVRecommendation = (index) => {
  if (index < 3)
    return "✔ Minimal protection needed. Sunscreen recommended for prolonged exposure. ☀️ Consider getting 15-30 minutes of midday sunlight for Vitamin D synthesis. Apply ~0.5 teaspoons of SPF 15+ sunscreen for face if exposed for extended periods.";
  
  if (index < 6)
    return "🕶 Moderate risk: Wear sunglasses, use SPF 30+, and seek shade around midday. 🌤️ 10-15 minutes of sun exposure before 10 AM or after 3 PM can help maintain Vitamin D levels. Apply ~1 teaspoon of SPF 30+ sunscreen for face and neck.";

  if (index < 8)
    return "👕 High risk: Wear protective clothing, SPF 50+, and avoid midday sun (10 AM - 3 PM). 🌞 Limited sun exposure in the morning is advised for Vitamin D. Apply ~1.5 teaspoons of SPF 50+ sunscreen for face, neck, and arms.";

  if (index < 11)
    return "🌞 Very High risk: Limit outdoor exposure, SPF 50+, wear a wide-brimmed hat and sunglasses. ☀️ Vitamin D can be maintained through diet and supplements. Apply ~3 teaspoons (1 tablespoon) of SPF 50+ sunscreen for full upper body protection.";

  return "🚨 Extreme risk! Avoid direct sun exposure, use SPF 50+, reapply sunscreen every 2 hours. 🌥️ Vitamin D should be obtained from diet or supplements in such conditions. Apply at least 6 teaspoons (2 tablespoons) of SPF 50+ sunscreen for full body protection.";
};

// Show error messages
const showError = (message) => {
  errorMessage.value = message;
  resetData();
};

// Reset UV data
const resetData = () => {
  currentUV.value = null;
  recommendation.value = "UV protection tips unavailable. Check again later.";
  lastUpdated.value = "";
};

</script>

<template>
  <div class="homepage">
    <!-- Background Video -->
    <video autoplay loop muted playsinline class="background-video">
      <source :src="backgroundVideo" type="video/mp4" />
    </video>

    <!-- Search & GPS Buttons -->
    <div class="search-container">
      <input v-model="locationInput" placeholder="Enter city or postcode" />
      <button @click="fetchUVData">Search</button>
      <button class="gps-btn" @click="fetchUVByGPS">Use Current Location</button>
    </div>

    <!-- UV Data Display -->
    <div class="uv-container">
      <div v-if="currentUV !== null" class="uv-card">
        <h2>{{ cityName }}</h2>
        <p class="uv-index" :style="{ color: getUVColor(currentUV) }">
          UV Index: {{ currentUV }}
        </p>
        <p class="last-updated">Last updated: {{ lastUpdated }}</p>
      </div>
    </div>

    <!-- UV Protection Recommendation -->
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
