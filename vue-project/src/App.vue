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
// Stores UV protection suggestion
const uvSuggestion = ref("");   
// Stores error messages
const errorMessage = ref(null);

// Function to fetch UV Index from backend
const fetchUVIndex = async () => {
  if (!locationInput.value.trim()) {
    errorMessage.value = "Please enter a location or postcode.";
    uvIndex.value = null;
    longitude.value = null;
    latitude.value = null;
    uvSuggestion.value = "";
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
      uvSuggestion.value = data.suggestion;
      errorMessage.value = null;
    } else {
      uvIndex.value = null;
      longitude.value = null;
      latitude.value = null;
      uvSuggestion.value = "";
      // If the error is "Location not found in database", show input again and clear the field
      if (data.error === "Location not found in database") {
        isInputVisible.value = true; // Show input field again
        locationInput.value = ""; // Clear the input field
      }
      errorMessage.value = data.error || "No UV data found.";
    }
  } catch (error) {
    uvIndex.value = null;
    longitude.value = null;
    latitude.value = null;
    uvSuggestion.value = "";
    errorMessage.value = "Error fetching UV data.";
    console.error("Fetch error:", error);
  }
};

// Function to reset the input for new location entry
const resetInput = () => {
  locationInput.value = "";
  uvIndex.value = null;
  longitude.value = null;
  latitude.value = null;
  uvSuggestion.value = "";
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
      <!-- Conditionally render input box and search button -->
      <input v-if="isInputVisible" v-model="locationInput" placeholder="Enter suburb or postcode" />
      <button v-if="isInputVisible" @click="fetchUVIndex">Search</button> <!-- Hide after searching -->
    </div>

    <!-- Display UV Index -->
    <div v-if="uvIndex !== null" class="uv-result">
      <p>UV Index for "{{ locationInput }}": <strong>{{ uvIndex }}</strong></p>
      <p><strong>Protection Suggestion:</strong> {{ uvSuggestion }}</p> <!-- Display UV suggestion -->
      <button @click="resetInput">Search New Location</button> <!-- Button for new search -->
    </div>
    
    <!-- Display Error Message -->
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
</style>

