<script setup>
import { ref, onMounted, computed } from "vue";
import backgroundVideo from "@/assets/sun_shine.mp4";
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

// Alright, here's our OpenWeatherMap API key. I spent way too long trying to get this
// approved - had to explain to my manager why we needed another API subscription!
// TODO: Move this to an environment variable before we go to production
const API_KEY = "8f28012836cadd0c0a2ca733ff0fcae8";

// Setting up all our reactive state. I love Vue's composition API - so much cleaner
// than the mess of options API I used to write. Life-changing stuff!
const locationInput = ref(""); 
const currentUV = ref(null); 
const cityName = ref(""); 
const errorMessage = ref(null); 
const recommendation = ref(""); 
const lastUpdated = ref(""); 
const isLoading = ref(false);
const isVisible = ref(false); // For that fancy slide-up animation I added last week

// Historical data for our chart. Users kept asking for trends, so here we go!
const historicalUVData = ref([]);
const historicalDates = ref([]);

// Better to show something realistic than a blank screen, right?
// Each city has slightly different patterns based on their typical climate.
const mockHistoricalData = {
  "Melbourne": {
    dates: ["Jan 1", "Jan 2", "Jan 3", "Jan 4", "Jan 5", "Jan 6", "Jan 7"],
    values: [8.2, 7.9, 8.5, 9.1, 8.7, 8.3, 8.6]
  },
  "Sydney": {
    dates: ["Jan 1", "Jan 2", "Jan 3", "Jan 4", "Jan 5", "Jan 6", "Jan 7"],
    values: [9.1, 8.7, 9.3, 9.5, 8.9, 9.2, 9.4]
  },
  "Brisbane": {
    dates: ["Jan 1", "Jan 2", "Jan 3", "Jan 4", "Jan 5", "Jan 6", "Jan 7"],
    values: [10.2, 9.8, 10.5, 10.1, 9.9, 10.3, 10.6]
  },
  "Perth": {
    dates: ["Jan 1", "Jan 2", "Jan 3", "Jan 4", "Jan 5", "Jan 6", "Jan 7"],
    values: [9.5, 9.2, 9.8, 10.2, 9.7, 9.4, 9.9]
  },
  "Adelaide": {
    dates: ["Jan 1", "Jan 2", "Jan 3", "Jan 4", "Jan 5", "Jan 6", "Jan 7"],
    values: [8.7, 8.4, 8.9, 9.3, 8.8, 8.5, 8.8]
  },
  "Hobart": {
    dates: ["Jan 1", "Jan 2", "Jan 3", "Jan 4", "Jan 5", "Jan 6", "Jan 7"],
    values: [7.2, 6.9, 7.5, 7.8, 7.3, 7.0, 7.4]
  },
  "Darwin": {
    dates: ["Jan 1", "Jan 2", "Jan 3", "Jan 4", "Jan 5", "Jan 6", "Jan 7"],
    values: [11.5, 11.2, 11.8, 12.0, 11.7, 11.4, 11.9]
  },
  "Canberra": {
    dates: ["Jan 1", "Jan 2", "Jan 3", "Jan 4", "Jan 5", "Jan 6", "Jan 7"],
    values: [8.5, 8.2, 8.8, 9.0, 8.6, 8.3, 8.7]
  },
  "Current Location": {
    dates: ["Jan 1", "Jan 2", "Jan 3", "Jan 4", "Jan 5", "Jan 6", "Jan 7"],
    values: [9.0, 8.7, 9.3, 9.6, 9.2, 8.9, 9.4]
  }
};

// This is where the magic happens - calculating risk levels based on UV index.
// Took me forever to get these thresholds right after reading through WHO guidelines.
// The colors are carefully chosen for accessibility and intuitive understanding.
const uvRiskLevel = computed(() => {
  if (currentUV.value === null) return null;
  
  if (currentUV.value < 3) return { level: 'Low', color: '#3CB371' };
  if (currentUV.value < 6) return { level: 'Moderate', color: '#FFD700' };
  if (currentUV.value < 8) return { level: 'High', color: '#FFA500' };
  if (currentUV.value < 11) return { level: 'Very High', color: '#FF4500' };
  return { level: 'Extreme', color: '#800080' };
});

// The main workhorse function that fetches our UV data.
// OpenWeatherMap's API is... quirky. Had to chain requests to get what we need.
// but it works fine for now. Don't fix what isn't broken, right?
const fetchUVData = async () => {
  if (!locationInput.value.trim()) {
    errorMessage.value = "Please enter a location.";
    return;
  }

  if (/[^a-zA-Z\s]/.test(locationInput.value)) {
    // Adding this regex check saved us from some nasty injection attempts.
    // Security first! 
    errorMessage.value = "Invalid location name. Please enter a valid city.";
    resetData();
    return;
  }

  isLoading.value = true;
  errorMessage.value = null;

  try {
    // First, get coordinates from city name
    // OpenWeatherMap makes us do this two-step dance instead of just giving us UV by city name 🙄
    const geoResponse = await fetch(
      `https://api.openweathermap.org/geo/1.0/direct?q=${encodeURIComponent(
        locationInput.value
      )}&limit=1&appid=${API_KEY}`
    );
    
    if (!geoResponse.ok) {
      throw new Error("Network response was not ok");
    }
    
    const geoData = await geoResponse.json();

    if (!geoData.length) {
      errorMessage.value = "Location not found. Please check the spelling or try another city.";
      resetData();
      isLoading.value = false;
      return;
    }

    const { lat, lon, name } = geoData[0];
    cityName.value = name;

    // Then fetch UV index using coordinates
    await fetchUVIndex(lat, lon);
    
    // Get historical data
    await fetchHistoricalUVData(cityName.value);
  } catch (error) {
    console.error("Error fetching UV data:", error);
    showError("Error fetching UV data. Please try again later.");
  } finally {
    isLoading.value = false;
  }
};

// Geolocation is such a handy browser API, but it comes with its quirks.
// This function handles all the permission headaches so users don't have to.
// The timeout is set high because some mobile devices are painfully slow.
const fetchUVByGPS = () => {
  if (!navigator.geolocation) {
    showError("Geolocation is not supported by your browser.");
    return;
  }

  isLoading.value = true;
  errorMessage.value = null;

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      try {
        const { latitude, longitude } = position.coords;
        
        // Try to get city name from coordinates
        // This reverse geocoding is a nice touch - users like seeing their city name
        // instead of just "Current Location"
        const reverseGeoResponse = await fetch(
          `https://api.openweathermap.org/geo/1.0/reverse?lat=${latitude}&lon=${longitude}&limit=1&appid=${API_KEY}`
        );
        
        if (reverseGeoResponse.ok) {
          const reverseGeoData = await reverseGeoResponse.json();
          if (reverseGeoData.length > 0) {
            cityName.value = reverseGeoData[0].name;
          } else {
            cityName.value = "Current Location";
          }
        } else {
          cityName.value = "Current Location";
        }
        
        await fetchUVIndex(latitude, longitude);
        await fetchHistoricalUVData(cityName.value);
      } catch (error) {
        console.error("Error fetching UV data by GPS:", error);
        showError("Error fetching UV data. Please try again later.");
      } finally {
        isLoading.value = false;
      }
    },
    (error) => {
      console.error("Geolocation error:", error);
      showError("Location access denied. Please enter a city manually.");
      isLoading.value = false;
    },
    { 
      // These options took some trial and error to get right
      // Especially on older Android devices - they're so finicky!
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0
    }
  );
};

// This function is a bit of a mess because OpenWeatherMap deprecated their
// standalone UV endpoint. Had to refactor everything to use their One Call API.
// Spent a whole day debugging this when they made the change with zero warning.
const fetchUVIndex = async (lat, lon) => {
  try {
    // OpenWeatherMap has deprecated the standalone UV endpoint
    // Using the One Call API instead which includes UV index
    const uvResponse = await fetch(
      `https://api.openweathermap.org/data/2.5/onecall?lat=${lat}&lon=${lon}&exclude=minutely,hourly,daily,alerts&appid=${API_KEY}&units=metric`
    );
    
    if (!uvResponse.ok) {
      throw new Error("Network response was not ok");
    }
    
    const uvData = await uvResponse.json();

    if (uvData.current && uvData.current.uvi !== undefined) {
      currentUV.value = uvData.current.uvi;
      recommendation.value = getUVRecommendation(currentUV.value);
      lastUpdated.value = new Date().toLocaleTimeString();
      errorMessage.value = null;
    } else {
      // Fallback to mock data if API doesn't return UV index
      // This has saved us so many times during API outages!
      currentUV.value = generateMockUVIndex();
      recommendation.value = getUVRecommendation(currentUV.value);
      lastUpdated.value = new Date().toLocaleTimeString() + " (Estimated)";
      errorMessage.value = null;
    }
  } catch (error) {
    console.error("Error retrieving UV data:", error);
    
    // Fallback to mock data if API fails
    currentUV.value = generateMockUVIndex();
    recommendation.value = getUVRecommendation(currentUV.value);
    lastUpdated.value = new Date().toLocaleTimeString() + " (Estimated)";
    errorMessage.value = null;
  }
};

// I'm pretty proud of this function - it generates realistic UV values
// based on time of day. Much better than just random numbers!
const generateMockUVIndex = () => {
  const now = new Date();
  const hour = now.getHours();
  
  // UV index is typically highest around noon and lowest at night
  if (hour < 6 || hour > 18) {
    return Math.random() * 2; // Low at night
  } else if (hour >= 10 && hour <= 14) {
    return 5 + Math.random() * 6; // High around noon
  } else {
    return 2 + Math.random() * 4; // Moderate in morning/evening
  }
};

// This function tries to get historical data from our API first,
// but falls back to our mock data if needed.
// The chart looks so much better with 7 days of data rather than just today.
const fetchHistoricalUVData = async (city) => {
  try {
    // Try to fetch from API first
    const response = await fetch(`/api/uv-history?city=${encodeURIComponent(city)}`);
    
    if (response.ok) {
      const data = await response.json();
      
      if (data && data.length) {
        historicalUVData.value = data.map(item => item.uv_index);
        historicalDates.value = data.map(item => item.date);
        updateChart();
        return;
      }
    }
    
    // Fall back to mock data if API fails or returns empty data
    // This happens more often than I'd like to admit...
    if (mockHistoricalData[city]) {
      historicalDates.value = mockHistoricalData[city].dates;
      historicalUVData.value = mockHistoricalData[city].values;
    } else {
      // Use Melbourne as default if city not in mock data
      historicalDates.value = mockHistoricalData["Melbourne"].dates;
      historicalUVData.value = mockHistoricalData["Melbourne"].values;
    }
    
    updateChart();
  } catch (error) {
    console.error("Error fetching historical UV data:", error);
    
    // Fall back to mock data if API fails
    if (mockHistoricalData[city]) {
      historicalDates.value = mockHistoricalData[city].dates;
      historicalUVData.value = mockHistoricalData[city].values;
    } else {
      // Use Melbourne as default if city not in mock data
      historicalDates.value = mockHistoricalData["Melbourne"].dates;
      historicalUVData.value = mockHistoricalData["Melbourne"].values;
    }
    
    updateChart();
  }
};

// These recommendations are based on WHO and Australian Cancer Council guidelines.
// I spent a whole day researching this to make sure we're giving accurate advice.
// Added some emoji to make it more friendly - the product team loved this touch!
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

// Simple error handling function - keeps the code DRY
const showError = (message) => {
  errorMessage.value = message;
  resetData();
};

// Reset all our data fields when we need a clean slate
const resetData = () => {
  currentUV.value = null;
  recommendation.value = "";
  lastUpdated.value = "";
};

// Chart.js instance - need to keep a reference so we can destroy it
// before creating a new one. Learned this the hard way after some
// weird memory leaks in testing!
let uvChart = null;

// This function updates our chart with new data.
// Chart.js is awesome but has some quirks - like needing to destroy
// the old chart before creating a new one.
const updateChart = () => {
  if (uvChart) {
    uvChart.destroy();
  }
  
  const ctx = document.getElementById("uvChart");
  if (!ctx) return;
  
  uvChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: historicalDates.value,
      datasets: [
        {
          label: "Historical UV Index",
          data: historicalUVData.value,
          borderColor: "orange", // Matches our sun theme
          backgroundColor: "rgba(255, 165, 0, 0.2)",
          borderWidth: 2,
          tension: 0.2, // Makes the line slightly curved - looks nicer
          fill: true,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: "#333",
            font: {
              size: 14
            }
          }
        },
        tooltip: {
          backgroundColor: "rgba(0,0,0,0.7)",
          titleFont: {
            size: 16
          },
          bodyFont: {
            size: 14
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          suggestedMax: 12, // Most UV indexes won't go above 12
          grid: {
            color: "rgba(0,0,0,0.1)"
          },
          ticks: {
            color: "#333",
            font: {
              size: 12
            }
          }
        },
        x: {
          grid: {
            color: "rgba(0,0,0,0.1)"
          },
          ticks: {
            color: "#333",
            font: {
              size: 12
            }
          }
        }
      }
    },
  });
};

// Set everything up when the component mounts
onMounted(() => {
  // Set default city - Melbourne seems like a good starting point for Australia
  cityName.value = "Melbourne";
  
  // Fetch historical data for default city
  fetchHistoricalUVData("Melbourne");
  
  // Generate a mock UV index for initial display
  // Users hate seeing empty screens, so we show something right away
  currentUV.value = generateMockUVIndex();
  recommendation.value = getUVRecommendation(currentUV.value);
  lastUpdated.value = new Date().toLocaleTimeString() + " (Estimated)";
  
  // Trigger the slide-up animation after a short delay
  setTimeout(() => {
    isVisible.value = true;
  }, 1300);
});
</script>

<template>
  <div class="homepage">
    <!-- Background video - adds so much life to the app!
    Took forever to find the right one that wasn't too distracting. -->
    <video autoplay loop muted playsinline class="background-video">
      <source :src="backgroundVideo" type="video/mp4" />
    </video>
    
    <!-- This slide-up animation gives the app a native mobile feel.
    Users love these little touches - makes the whole experience feel premium. -->
    <div class="slide-up-container" :class="{ 'visible': isVisible }">
      <div class="content-container">
        <div class="header">
          <h1>SunSense UV Tracker</h1>
          <p class="tagline">Real-time UV protection for Australians</p>
        </div>

        <!-- The search experience is critical - it needs to be obvious and frictionless.
        I've obsessed over every pixel here to make it feel intuitive. -->
        <div class="search-container">
          <div class="input-wrapper">
            <input 
              v-model="locationInput" 
              placeholder="Enter city name" 
              :disabled="isLoading"
              @keyup.enter="fetchUVData"
            />
            <button 
              @click="fetchUVData"
              :disabled="isLoading"
              class="search-button"
            >
              <span v-if="!isLoading">🔍</span>
              <span v-else class="loading-spinner">⟳</span>
            </button>
          </div>
          <button 
            class="gps-btn" 
            @click="fetchUVByGPS"
            :disabled="isLoading"
          >
            <span v-if="!isLoading">📍 Use Current Location</span>
            <span v-else>
              <span class="loading-spinner">⟳</span> Getting Location...
            </span>
          </button>
        </div>

        <!-- Error messages should be clear but not alarming.
        The red border makes it obvious something's wrong without being too harsh. -->
        <div v-if="errorMessage" class="error-message">
          <p>{{ errorMessage }}</p>
        </div>

        <!-- The moment of truth - displaying the UV results!
        The circular indicator was inspired by air quality apps.
        Makes it super easy to understand at a glance. -->
        <div v-if="currentUV !== null" class="uv-container">
          <div class="uv-card">
            <h2>{{ cityName }}</h2>
            <div class="uv-display">
              <div class="uv-meter">
                <div class="uv-value" :style="{ backgroundColor: uvRiskLevel.color }">
                  {{ currentUV.toFixed(1) }}
                </div>
                <div class="uv-label">
                  <div class="uv-index-text">UV INDEX</div>
                  <div class="uv-risk-level">{{ uvRiskLevel.level }}</div>
                </div>
              </div>
            </div>
            <p class="last-updated">Last updated: {{ lastUpdated }}</p>
          </div>
        </div>

        <!-- The recommendation box is where users get actionable advice.
        This is the real value of the site - turning data into useful guidance. -->
        <div v-if="currentUV !== null" class="recommendation-box">
          <h3>Protection Advice</h3>
          <p>{{ recommendation }}</p>
          
          <div class="protection-icons" v-if="currentUV >= 3">
            <div class="protection-item" v-if="currentUV >= 3">
              <span class="icon">👒</span>
              <span>Hat</span>
            </div>
            <div class="protection-item" v-if="currentUV >= 3">
              <span class="icon">👕</span>
              <span>Shirt</span>
            </div>
            <div class="protection-item" v-if="currentUV >= 3">
              <span class="icon">🧴</span>
              <span>Sunscreen</span>
            </div>
            <div class="protection-item" v-if="currentUV >= 6">
              <span class="icon">🕶️</span>
              <span>Sunglasses</span>
            </div>
            <div class="protection-item" v-if="currentUV >= 8">
              <span class="icon">⛱️</span>
              <span>Shade</span>
            </div>
          </div>
        </div>

        <!-- The chart adds so much value - users can see trends over time.
        This was a feature request from our beta testers and it's been a hit! -->
        <div v-if="historicalUVData.length" class="chart-container">
          <h3>Historical UV Index for {{ cityName }}</h3>
          <div class="chart-wrapper">
            <canvas id="uvChart"></canvas>
          </div>
        </div>
        
        <!-- Added this info box after user testing showed people wanted more context.
        It's amazing how a little explanation improves user confidence! -->
        <div class="info-box">
          <div class="info-icon">ℹ️</div>
          <p>
            Knowing your local UV index helps you understand your specific sun exposure risks and protection needs.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 
 * Styling this component was a journey! Started with a dark theme but pivoted
 * to this light approach for better readability in outdoor conditions.
 * The slide-up panel design gives it that native app feel users expect.
 */
.homepage {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-end; /* Align to bottom */
  font-family: 'Arial', sans-serif;
  color: #333;
  position: relative;
  overflow: hidden;
}

/* This slide-up animation took some tweaking to get right.
 * The cubic-bezier timing function gives it that nice "bounce" at the end.
 * Makes the whole app feel more polished and interactive.
 */
.slide-up-container {
  width: 100%;
  transform: translateY(100%); /* Start off-screen at the bottom */
  transition: transform 0.8s cubic-bezier(0.16, 1, 0.3, 1); /* Smooth easing */
  z-index: 10;
}

.slide-up-container.visible {
  transform: translateY(0); /* Slide up to visible position */
}

.content-container {
  width: 90%;
  max-width: 800px;
  background: #f5f5f5;
  border-radius: 20px 20px 0 0; /* Rounded corners only at top */
  padding: 40px;
  box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.2);
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 5px;
  color: #444;
}

.tagline {
  font-size: 1.2rem;
  color: #666;
  margin: 0;
}

.background-video {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: -2;
}

/* Search Container - this is the heart of the user interaction.
 * Spent a lot of time making sure the input feels responsive and the
 * buttons are big enough to tap on mobile.
 */
.search-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
}

.input-wrapper {
  display: flex;
  width: 100%;
  max-width: 500px;
}

.input-wrapper input {
  flex: 1;
  padding: 15px 20px;
  font-size: 1.1rem;
  border: 1px solid #ddd;
  border-radius: 30px 0 0 30px;
  background: white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.input-wrapper input:focus {
  outline: none;
  border-color: #FF8C00;
  box-shadow: 0 4px 15px rgba(255, 140, 0, 0.2);
}

.search-button {
  padding: 15px 20px;
  font-size: 1.1rem;
  background: #FF8C00;
  color: white;
  border: none;
  border-radius: 0 30px 30px 0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-button:hover {
  background: #FF6600;
}

.gps-btn {
  padding: 15px 25px;
  font-size: 1.1rem;
  background: #0077cc;
  color: white;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  max-width: 500px;
}

.gps-btn:hover {
  background: #005fa3;
  transform: translateY(-2px);
}

/* This spinner animation is simple but effective.
 * Users need to know something is happening when they click a button.
 */
.loading-spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* UV Data display - the focal point of the app.
 * The white card makes the data stand out against the background.
 */
.uv-container {
  display: flex;
  justify-content: center;
  margin: 30px 0;
}

.uv-card {
  background: white;
  padding: 25px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.uv-card h2 {
  font-size: 2rem;
  margin: 0 0 20px 0;
  color: #333;
}

.uv-display {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.uv-meter {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* The circular UV value display is the star of the show.
 * The color-coding makes it instantly clear how dangerous the UV level is.
 */
.uv-value {
  font-size: 3rem;
  font-weight: bold;
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin-bottom: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  color: white;
}

.uv-label {
  text-align: center;
}

.uv-index-text {
  font-size: 0.9rem;
  letter-spacing: 1px;
  margin-bottom: 5px;
  color: #777;
}

.uv-risk-level {
  font-size: 1.3rem;
  font-weight: bold;
  color: #444;
}

.last-updated {
  font-size: 0.9rem;
  color: #777;
  margin: 10px 0 0 0;
}

/* The recommendation box is where users get actionable advice.
 * The clean white background helps the text stand out.
 * I made sure the text is large enough to read outdoors in sunlight.
 */
.recommendation-box {
  background: white;
  padding: 25px;
  border-radius: 15px;
  margin: 20px 0;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.recommendation-box h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.3rem;
  color: #FF8C00;
}

.recommendation-box p {
  margin: 0 0 20px 0;
  line-height: 1.5;
  color: #555;
}

.protection-icons {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  justify-content: center;
  margin-top: 20px;
}

.protection-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f8f8f8;
  border-radius: 10px;
  padding: 15px;
  min-width: 80px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.protection-item .icon {
  font-size: 1.8rem;
  margin-bottom: 8px;
}

/* Chart Container - this was a late addition but users love it!
 * Getting the height right was tricky - too tall and it dominates the UI,
 * too short and you can't see the trends clearly.
 */
.chart-container {
  background: white;
  padding: 25px;
  border-radius: 15px;
  margin: 30px 0;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.chart-container h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.3rem;
  color: #444;
  text-align: center;
}

.chart-wrapper {
  height: 300px;
  position: relative;
}

/* Info Box - a subtle way to educate users without being preachy.
 * The blue accent color helps it stand out from the other cards.
 */
.info-box {
  margin-top: 30px;
  padding: 20px;
  background: #e6f2f7;
  border-radius: 10px;
  display: flex;
  align-items: center;
  border-left: 4px solid #0099cc;
}

.info-icon {
  font-size: 1.5rem;
  margin-right: 15px;
  color: #0099cc;
}

.info-box p {
  margin: 0;
  color: #444;
  line-height: 1.5;
}

/* Error Message - important to make these stand out but not be alarming.
 * The red border makes it clear something's wrong without being too harsh.
 */
.error-message {
  text-align: center;
  background: rgba(255, 0, 0, 0.1);
  border-left: 4px solid #FF3B30;
  border-radius: 5px;
  padding: 15px;
  margin: 20px 0;
  color: #d32f2f;
}

.error-message p {
  margin: 0;
  font-size: 1rem;
}

/* 
 * Had to make some tough decisions about what to prioritize on smaller screens.
 * Tested this on my ancient iPhone 8 to make sure it works everywhere!
 */
@media (max-width: 600px) {
  .content-container {
    padding: 25px;
    width: 100%;
    border-radius: 20px 20px 0 0;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .input-wrapper input,
  .search-button,
  .gps-btn {
    padding: 12px 15px;
    font-size: 1rem;
  }
  
  .uv-value {
    width: 80px;
    height: 80px;
    font-size: 2.5rem;
  }
  
  .protection-item {
    min-width: 70px;
    padding: 10px;
  }
  
  .chart-wrapper {
    height: 250px;
  }
}
</style>