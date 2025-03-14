<script setup>
import { ref } from "vue";
import backgroundVideo from "@/assets/bg.mp4"; // Import video

// Reactive variables
const locationInput = ref("");  // Stores user input (suburb name or postcode)
const uvIndex = ref(null);       // Stores fetched UV Index
const errorMessage = ref(null);  // Stores any error messages

// Function to fetch UV Index from backend
const fetchUVIndex = async () => {
  if (!locationInput.value.trim()) {
    errorMessage.value = "Please enter a location or postcode.";
    uvIndex.value = null;
    return;
  }

  try {
    const response = await fetch(
      `http://localhost:5000/get-uv-data?location=${encodeURIComponent(locationInput.value)}`
    );

    const data = await response.json();

    if (response.ok) {
      uvIndex.value = data.uv_index;
      errorMessage.value = null;
    } else {
      uvIndex.value = null;
      errorMessage.value = data.error || "No UV data found.";
    }
  } catch (error) {
    uvIndex.value = null;
    errorMessage.value = "Error fetching UV data.";
    console.error("Fetch error:", error);
  }
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
      <input v-model="locationInput" placeholder="Enter suburb or postcode" />
      <button @click="fetchUVIndex">Search</button>
    </div>

    <!-- Display UV Index -->
    <div v-if="uvIndex !== null" class="uv-result">
      <p>UV Index for "{{ locationInput }}": <strong>{{ uvIndex }}</strong></p>
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

/* Error Message */
.error-message {
  text-align: center;
  color: red;
  margin-top: 10px;
}
</style>

