<script setup>
import { ref } from "vue";
// Import background video
import backgroundVideo from "@/assets/bg.mp4"; 

// Stores user input (suburb name or postcode)
const locationInput = ref("");
// Boolean to control whether the input field is visible
const isInputVisible = ref(true); 

// Stores fetched UV Index
const uvIndex = ref(null);   
// Stores longitude
const longitude = ref(null);
// Stores latitude
const latitude = ref(null);
// Stores suburb name
const suburbName = ref(""); 
// Stores UV protection suggestion
const uvSuggestion = ref("");   
// Stores error messages
const errorMessage = ref(null);
// Stores last updated time
const lastUpdated = ref(null);

// Function to fetch UV Index from backend (by suburb/postcode)
const fetchUVIndex = async () => {
  if (!locationInput.value.trim()) {
    errorMessage.value = "Please enter a location or postcode.";
    return;
  }

  // Check for special characters before sending request
  const regex = /^[a-zA-Z0-9\s-]+$/;
  if (!regex.test(locationInput.value)) {
    errorMessage.value = "Invalid location name. Please avoid special characters.";
    return;
  }

  // Hide the input field once search is done
  isInputVisible.value = false;

  try {
    const response = await fetch(
      `http://localhost:5000/get-uv-index?location=${encodeURIComponent(locationInput.value)}`
    );

    const data = await response.json();
    if (response.ok) {
      uvIndex.value = data.uv_index;
      longitude.value = data.lon;
      latitude.value = data.lat;
      suburbName.value = data.suburb;
      uvSuggestion.value = data.suggestion;
      lastUpdated.value = new Date().toLocaleTimeString();
      errorMessage.value = null;
    } else {
      errorMessage.value = data.error || "No UV data found.";
      isInputVisible.value = true; // Show input field again
      locationInput.value = ""; // Clear the input field
    }
  } catch (error) {
    errorMessage.value = "Error fetching UV data.";
    isInputVisible.value = true;
  }
};

// Function to fetch UV Index using GPS
const fetchUVIndexFromGPS = () => {
  if (!navigator.geolocation) {
    errorMessage.value = "Geolocation is not supported by your browser.";
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const userLat = position.coords.latitude;
      const userLon = position.coords.longitude;

      try {
        const response = await fetch(
          `http://localhost:5000/get-uv-index?lat=${userLat}&lon=${userLon}`
        );
        const data = await response.json();

        if (response.ok) {
          uvIndex.value = data.uv_index;
          longitude.value = userLon;
          latitude.value = userLat;
          suburbName.value = data.suburb;
          uvSuggestion.value = data.suggestion;
          lastUpdated.value = new Date().toLocaleTimeString();
          isInputVisible.value = false;
          errorMessage.value = null;
        } else {
          errorMessage.value = data.error || "No UV data found.";
        }
      } catch (error) {
        errorMessage.value = "Error fetching UV data.";
      }
    },
    () => {
      errorMessage.value = "Location access denied. Please enter a location manually.";
    }
  );
};

// Function to reset input
const resetInput = () => {
  locationInput.value = "";
  uvIndex.value = null;
  longitude.value = null;
  latitude.value = null;
  suburbName.value = "";
  uvSuggestion.value = "";
  lastUpdated.value = null;
  errorMessage.value = null;
  isInputVisible.value = true; // Show input field again
};
</script>

<template>
  <div class="homepage">
    <!-- Background Video -->
    <video autoplay loop muted class="background-video">
      <source :src="backgroundVideo" type="video/mp4" />
    </video>

    <!-- Title -->
    <h1 class="fade-in">Welcome to SunSense</h1>

    <!-- Search Box -->
    <div class="search-container">
      <input v-if="isInputVisible" v-model="locationInput" placeholder="Enter suburb or postcode" />
      <button v-if="isInputVisible" @click="fetchUVIndex">Search</button>
      <button v-if="isInputVisible" @click="fetchUVIndexFromGPS">Use My Location</button>
    </div>

    <!-- Display Error Message -->
    <div v-if="errorMessage" class="error-message">
      <p>{{ errorMessage }}</p>
      <button @click="resetInput">Try Again</button>
    </div>

    <!-- Display UV Index -->
    <div v-if="uvIndex !== null" class="uv-result">
      <p>UV Index for "{{ suburbName }}": <strong>{{ uvIndex }}</strong></p>
      <p><strong>Protection Suggestion:</strong> {{ uvSuggestion }}</p>
      <p>Last Updated: <strong>{{ lastUpdated }}</strong></p>
      <button @click="resetInput">Search New Location</button>
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

/* Title */
.fade-in {
  font-size: 2.5rem;
  color: white;
  text-align: center;
  margin-top: 20vh;
  opacity: 0;
  animation: fadeIn 3s ease-in-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Search Container */
.search-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
.search-container input {
  padding: 10px;
  font-size: 16px;
  border-radius: 5px;
  border: none;
  margin-right: 10px;
}
.search-container button {
  padding: 10px 15px;
  font-size: 16px;
  background-color: #ff6600;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.search-container button:hover {
  background-color: #e65c00;
}

/* UV Result */
.uv-result {
  text-align: center;
  margin-top: 20px;
  font-size: 18px;
  color: white;
}
.uv-result button {
  margin-top: 10px;
  padding: 10px 15px;
  background-color: #ff6600;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.uv-result button:hover {
  background-color: #e65c00;
}

/* Error Message */
.error-message {
  text-align: center;
  color: red;
  margin-top: 10px;
}
.error-message button {
  margin-top: 10px;
  padding: 10px 15px;
  background-color: #ff6600;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.error-message button:hover {
  background-color: #e65c00;
}
</style>






