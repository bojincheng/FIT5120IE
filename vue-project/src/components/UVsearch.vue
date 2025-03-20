<script setup>
import { ref, onMounted, computed, watch } from "vue";
import backgroundVideo from "@/assets/aussie_beach.mp4";
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

// Setting up our reactive state variables
const locationInput = ref("");
const currentUV = ref(null);
const cityName = ref("");
const errorMessage = ref(null);
const recommendation = ref("");
const lastUpdated = ref(null);
const isLoading = ref(false);
const isVisible = ref(false); // For that  slide-up animation
const activeTab = ref("uv"); // Default tab is UV index, other option is "cancer"

// Coordinates and suburb data
const longitude = ref(null);
const latitude = ref(null);
const suburbName = ref("");

// Historical UV data for charts
const historicalUVData = ref([]);
const historicalDates = ref([]);

// Australia bounding box coordinates
// These define the geographical boundaries of Australia
const AUS_BOUNDS = {
  south: -43.6345972634, // Tasmania's southern point
  north: -10.6681857235, // Cape York's northern point
  west: 113.15930688, // Western Australia's western point
  east: 153.63925859 // Eastern point
};

// Cancer research data for the new tab
// This is mock data - in a real app, we'd fetch this from an API
const cancerData = ref({
  diagnoses: {
    labels: ["2000", "2002", "2004", "2006", "2008", "2010", "2012", "2014", "2016", "2018", "2020", "2022"],
    data: [8400, 9100, 9800, 10500, 11300, 12100, 12800, 13600, 14500, 15400, 16200, 17100],
    title: "Skin Cancer Diagnoses in Australia (Per Year)"
  },
  deaths: {
    labels: ["2000", "2002", "2004", "2006", "2008", "2010", "2012", "2014", "2016", "2018", "2020", "2022"],
    data: [1200, 1280, 1350, 1430, 1520, 1610, 1680, 1750, 1830, 1920, 2010, 2100],
    title: "Skin Cancer Deaths in Australia (Per Year)"
  },
  uvExposure: {
    labels: ["Very Low", "Low", "Moderate", "High", "Very High", "Extreme"],
    data: [5, 15, 25, 30, 20, 5],
    title: "Population UV Exposure Distribution (%)"
  }
});

// Compute UV risk level for visual indicators
const uvRiskLevel = computed(() => {
  if (currentUV.value === null) return null;
  
  if (currentUV.value < 3) return { level: 'Low', color: '#3CB371' };
  if (currentUV.value < 6) return { level: 'Moderate', color: '#FFD700' };
  if (currentUV.value < 8) return { level: 'High', color: '#FFA500' };
  if (currentUV.value < 11) return { level: 'Very High', color: '#FF4500' };
  return { level: 'Extreme', color: '#800080' };
});

// Check if coordinates are within Australia
const isLocationInAustralia = (lat, lon) => {
  // Check if the coordinates fall within Australia's bounding box
  return (
    lat >= AUS_BOUNDS.south &&
    lat <= AUS_BOUNDS.north &&
    lon >= AUS_BOUNDS.west &&
    lon <= AUS_BOUNDS.east
  );
};

// Function to fetch UV Index from backend (by suburb/postcode)
// Using the API endpoint from the second file
const fetchUVData = async () => {
  if (!locationInput.value.trim()) {
    errorMessage.value = "Please enter a location or postcode.";
    return;
  }

  // Check for special characters before sending request
  const regex = /^[a-zA-Z0-9\s-]+$/;
  if (!regex.test(locationInput.value)) {
    errorMessage.value = "Invalid location name. Please avoid special characters.";
    resetData();
    return;
  }

  isLoading.value = true;
  errorMessage.value = null;

  try {
    // Using the API endpoint from the second file
    const response = await fetch(
      `https://fit5120ie-2.onrender.com/get-uv-index?location=${encodeURIComponent(locationInput.value)}`
    );

    const data = await response.json();
    if (response.ok) {
      // Check if the location is in Australia
      if (!isLocationInAustralia(data.lat, data.lon)) {
        errorMessage.value = "SunSense is only available for Australian locations. Please enter an Australian suburb or postcode.";
        resetData();
        isLoading.value = false;
        return;
      }
      
      currentUV.value = data.uv_index;
      longitude.value = data.lon;
      latitude.value = data.lat;
      suburbName.value = data.suburb;
      cityName.value = data.suburb; // For consistency with the UI
      recommendation.value = getUVRecommendation(data.uv_index);
      lastUpdated.value = new Date().toLocaleTimeString();
      errorMessage.value = null;
      
      // Generate mock historical data based on current UV
      generateMockHistoricalData(data.suburb);
    } else {
      errorMessage.value = data.error || "No UV data found.";
      resetData();
    }
  } catch (error) {
    console.error("Error fetching UV data:", error);
    errorMessage.value = "Error fetching UV data. Please check your connection and try again.";
    resetData();
  } finally {
    isLoading.value = false;
  }
};

// Function to fetch UV Index using GPS
const fetchUVByGPS = () => {
  if (!navigator.geolocation) {
    errorMessage.value = "Geolocation is not supported by your browser.";
    return;
  }

  isLoading.value = true;
  errorMessage.value = null;

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const userLat = position.coords.latitude;
      const userLon = position.coords.longitude;
      
      // Check if the user's location is in Australia before making the API call
      if (!isLocationInAustralia(userLat, userLon)) {
        errorMessage.value = "SunSense is only available for Australian locations. Your current location appears to be outside Australia.";
        isLoading.value = false;
        return;
      }

      try {
        // Using the API endpoint from the second file
        const response = await fetch(
          `https://fit5120ie-2.onrender.com/get-uv-index?lat=${userLat}&lon=${userLon}`
        );
        const data = await response.json();

        if (response.ok) {
          currentUV.value = data.uv_index;
          longitude.value = userLon;
          latitude.value = userLat;
          suburbName.value = data.suburb;
          cityName.value = data.suburb; // For consistency with the UI
          recommendation.value = getUVRecommendation(data.uv_index);
          lastUpdated.value = new Date().toLocaleTimeString();
          errorMessage.value = null;
          
          // Generate mock historical data based on current location
          generateMockHistoricalData(data.suburb);
        } else {
          errorMessage.value = data.error || "No UV data found.";
          resetData();
        }
      } catch (error) {
        console.error("Error fetching UV data by GPS:", error);
        errorMessage.value = "Error fetching UV data. Please check your connection and try again.";
        resetData();
      } finally {
        isLoading.value = false;
      }
    },
    (error) => {
      console.error("Geolocation error:", error);
      errorMessage.value = "Location access denied. Please enter a location manually.";
      isLoading.value = false;
    },
    { 
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0
    }
  );
};

// Generate mock historical UV data based on location
// In a real app, we'd fetch this from an API
const generateMockHistoricalData = (location) => {
  // Create dates for the past 7 days
  const dates = [];
  const data = [];
  const today = new Date();
  
  // Base UV value on current UV with some randomness
  const baseUV = currentUV.value || 5;
  
  for (let i = 6; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(today.getDate() - i);
    dates.push(date.toLocaleDateString('en-AU', { month: 'short', day: 'numeric' }));
    
    // Generate a value that's somewhat close to the current UV
    // but with some daily variation
    const variation = (Math.random() * 4) - 2; // -2 to +2
    let value = baseUV + variation;
    value = Math.max(0, Math.min(12, value)); // Clamp between 0 and 12
    data.push(value.toFixed(1));
  }
  
  historicalDates.value = dates;
  historicalUVData.value = data;
  
  // Update the chart
  updateUVChart();
};

// Get UV protection recommendation based on index
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

// Reset all our data fields when we need a clean slate
const resetData = () => {
  currentUV.value = null;
  longitude.value = null;
  latitude.value = null;
  suburbName.value = "";
  recommendation.value = "";
  lastUpdated.value = "";
};

// Chart instances - need to keep references so we can destroy them
// before creating new ones
let uvChart = null;
let melanomaChart = null;
let nonMelanomaChart = null;
let uvExposureChart = null;

// Update the UV history chart
const updateUVChart = () => {
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
          borderColor: "orange",
          backgroundColor: "rgba(255, 165, 0, 0.2)",
          borderWidth: 2,
          tension: 0.2,
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
          suggestedMax: 12,
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

// Initialize cancer research charts
const initCancerCharts = () => {
  // Only initialize if we're on the cancer tab
  if (activeTab.value !== 'cancer') return;
  
  // Wait for DOM to be ready
  setTimeout(() => {
    // Diagnoses chart (formerly melanoma chart)
    const diagnosesCtx = document.getElementById("diagnosesChart");
    if (diagnosesCtx && melanomaChart === null) {
      melanomaChart = new Chart(diagnosesCtx, {
        type: "line",
        data: {
          labels: cancerData.value.diagnoses.labels,
          datasets: [
            {
              label: "Number of Diagnoses",
              data: cancerData.value.diagnoses.data,
              borderColor: "#E74C3C",
              backgroundColor: "rgba(231, 76, 60, 0.2)",
              borderWidth: 2,
              tension: 0.2,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: cancerData.value.diagnoses.title,
              font: {
                size: 16
              }
            },
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: false,
              grid: {
                color: "rgba(0,0,0,0.1)"
              }
            },
            x: {
              grid: {
                color: "rgba(0,0,0,0.1)"
              }
            }
          }
        },
      });
    }
    
    // Deaths chart (formerly non-melanoma chart)
    const deathsCtx = document.getElementById("deathsChart");
    if (deathsCtx && nonMelanomaChart === null) {
      nonMelanomaChart = new Chart(deathsCtx, {
        type: "line",
        data: {
          labels: cancerData.value.deaths.labels,
          datasets: [
            {
              label: "Number of Deaths",
              data: cancerData.value.deaths.data,
              borderColor: "#3498DB",
              backgroundColor: "rgba(52, 152, 219, 0.2)",
              borderWidth: 2,
              tension: 0.2,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: cancerData.value.deaths.title,
              font: {
                size: 16
              }
            },
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: false,
              grid: {
                color: "rgba(0,0,0,0.1)"
              }
            },
            x: {
              grid: {
                color: "rgba(0,0,0,0.1)"
              }
            }
          }
        },
      });
    }
    
    // UV exposure distribution chart (unchanged)
    const uvExposureCtx = document.getElementById("uvExposureChart");
    if (uvExposureCtx && uvExposureChart === null) {
      uvExposureChart = new Chart(uvExposureCtx, {
        type: "bar",
        data: {
          labels: cancerData.value.uvExposure.labels,
          datasets: [
            {
              label: "Population Percentage",
              data: cancerData.value.uvExposure.data,
              backgroundColor: [
                'rgba(60, 179, 113, 0.7)',
                'rgba(255, 215, 0, 0.7)',
                'rgba(255, 165, 0, 0.7)',
                'rgba(255, 69, 0, 0.7)',
                'rgba(255, 0, 0, 0.7)',
                'rgba(128, 0, 128, 0.7)'
              ],
              borderColor: [
                'rgb(60, 179, 113)',
                'rgb(255, 215, 0)',
                'rgb(255, 165, 0)',
                'rgb(255, 69, 0)',
                'rgb(255, 0, 0)',
                'rgb(128, 0, 128)'
              ],
              borderWidth: 1
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: cancerData.value.uvExposure.title,
              font: {
                size: 16
              }
            },
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: "rgba(0,0,0,0.1)"
              }
            },
            x: {
              grid: {
                color: "rgba(0,0,0,0.1)"
              }
            }
          }
        },
      });
    }
  }, 300);
};

// Watch for tab changes to initialize charts
watch(activeTab, (newTab) => {
  if (newTab === 'cancer') {
    // Reset chart instances so they can be recreated
    melanomaChart = null;
    nonMelanomaChart = null;
    uvExposureChart = null;
    
    // Initialize cancer charts
    initCancerCharts();
  }
});

// Set everything up when the component mounts
onMounted(() => {
  // Set default city
  cityName.value = "Melbourne";
  
  // Generate a mock UV index for initial display
  currentUV.value = 5.2;
  recommendation.value = getUVRecommendation(currentUV.value);
  lastUpdated.value = new Date().toLocaleTimeString() + " (Estimated)";
  
  // Generate mock historical data
  generateMockHistoricalData("Melbourne");
  
  // Trigger the slide-up animation after a short delay
  setTimeout(() => {
    isVisible.value = true;
  }, 300);
});
</script>

<template>
  <div class="homepage">
    <!-- Background video -->
    <video autoplay loop muted playsinline class="background-video">
      <source :src="backgroundVideo" type="video/mp4" />
    </video>
    
    <!-- Slide-up container -->
    <div class="slide-up-container" :class="{ 'visible': isVisible }">
      <div class="content-container">
        <div class="header">
          <h1>SunSense UV Tracker</h1>
          <p class="tagline">Real-time UV protection for Australians</p>
        </div>

        <!-- Tab Navigation -->
        <div class="tab-navigation">
          <button 
            :class="{ 'active': activeTab === 'uv' }" 
            @click="activeTab = 'uv'"
          >
            UV Index
          </button>
          <button 
            :class="{ 'active': activeTab === 'cancer' }" 
            @click="activeTab = 'cancer'"
          >
            Skin Cancer Research
          </button>
        </div>

        <!-- UV Index Tab Content -->
        <div v-if="activeTab === 'uv'" class="tab-content">
          <!-- Search & GPS -->
          <div class="search-container">
            <div class="input-wrapper">
              <input 
                v-model="locationInput" 
                placeholder="Enter Australian suburb or postcode" 
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
              <span v-if="!isLoading">📍 Use My Location</span>
              <span v-else>
                <span class="loading-spinner">⟳</span> Getting Location...
              </span>
            </button>
            
            <!-- Australia-only notice -->
            <div class="australia-notice">
              <span class="australia-icon">🇦🇺</span>
              <span>SunSense is available for Australian locations only</span>
            </div>
          </div>

          <!-- Error message -->
          <div v-if="errorMessage" class="error-message">
            <p>{{ errorMessage }}</p>
          </div>

          <!-- UV data display -->
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

          <!-- UV protection advice -->
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

          <!-- Historical UV data visualization -->
          <div v-if="historicalUVData.length" class="chart-container">
            <h3>Historical UV Index for {{ cityName }}</h3>
            <div class="chart-wrapper">
              <canvas id="uvChart"></canvas>
            </div>
          </div>
          
          <!-- Info box -->
          <div class="info-box">
            <div class="info-icon">ℹ️</div>
            <p>
              Knowing your local UV index helps you understand your specific sun exposure risks and protection needs.
            </p>
          </div>
        </div>

        <!-- Cancer Research Tab Content -->
        <div v-if="activeTab === 'cancer'" class="tab-content">
          <div class="cancer-research-intro">
            <h2>Skin Cancer & UV Exposure Research</h2>
            <p>
              Australia has one of the highest rates of skin cancer in the world. 
              Two in three Australians will be diagnosed with skin cancer by the age of 70.
              The main cause is exposure to UV radiation from the sun.
            </p>
          </div>

          <div class="chart-grid">
            <!-- Diagnoses Chart (formerly Melanoma Chart) -->
            <div class="chart-container">
              <div class="chart-wrapper">
                <canvas id="diagnosesChart"></canvas>
              </div>
            </div>

            <!-- Deaths Chart (formerly Non-Melanoma Chart) -->
            <div class="chart-container">
              <div class="chart-wrapper">
                <canvas id="deathsChart"></canvas>
              </div>
            </div>

            <!-- UV Exposure Distribution Chart (unchanged) -->
            <div class="chart-container full-width">
              <div class="chart-wrapper">
                <canvas id="uvExposureChart"></canvas>
              </div>
            </div>
          </div>

          <div class="cancer-research-facts">
            <h3>Key Facts</h3>
            <ul>
              <li>Skin cancer is the most common cancer diagnosed in Australia</li>
              <li>More than 2,000 Australians die from skin cancer each year</li>
              <li>Australia has one of the highest rates of skin cancer in the world</li>
              <li>The majority of skin cancers are caused by exposure to UV radiation</li>
              <li>Regular use of sunscreen can reduce melanoma risk by up to 50%</li>
              <li>Skin cancer is one of the most preventable cancers</li>
            </ul>
          </div>

          <div class="info-box warning">
            <div class="info-icon">⚠️</div>
            <p>
              Early detection is crucial for successful treatment of skin cancer. 
              Regular skin checks by a healthcare professional are recommended, especially for high-risk individuals.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Base Styles */
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

/* Background Video */
.background-video {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: -2;
}

/* Slide-up Container */
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

/* Header */
.header {
  text-align: center;
  margin-bottom: 20px;
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

/* Tab Navigation */
.tab-navigation {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
  border-bottom: 1px solid #ddd;
}

.tab-navigation button {
  padding: 12px 25px;
  font-size: 1.1rem;
  background: transparent;
  color: #666;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  margin: 0 10px;
}

.tab-navigation button:hover {
  color: #FF8C00;
}

.tab-navigation button.active {
  color: #FF8C00;
  border-bottom: 3px solid #FF8C00;
  font-weight: 600;
}

/* Tab Content */
.tab-content {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Search Container */
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

/* Australia-only notice */
.australia-notice {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 0.9rem;
  color: #666;
  margin-top: 5px;
}

.australia-icon {
  font-size: 1.2rem;
}

/* Loading Spinner */
.loading-spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* UV Data Display */
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

/* Recommendation Box */
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

/* Chart Container */
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

/* Info Box */
.info-box {
  margin-top: 30px;
  padding: 20px;
  background: #e6f2f7;
  border-radius: 10px;
  display: flex;
  align-items: center;
  border-left: 4px solid #0099cc;
}

.info-box.warning {
  background: #fff3e0;
  border-left: 4px solid #ff9800;
}

.info-icon {
  font-size: 1.5rem;
  margin-right: 15px;
  color: #0099cc;
}

.info-box.warning .info-icon {
  color: #ff9800;
}

.info-box p {
  margin: 0;
  color: #444;
  line-height: 1.5;
}

/* Error Message */
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

/* Cancer Research Tab Styles */
.cancer-research-intro {
  text-align: center;
  margin-bottom: 30px;
}

.cancer-research-intro h2 {
  font-size: 1.8rem;
  margin-bottom: 15px;
  color: #444;
}

.cancer-research-intro p {
  color: #555;
  line-height: 1.6;
}

.chart-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

@media (min-width: 768px) {
  .chart-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.chart-grid .full-width {
  grid-column: 1 / -1;
}

.cancer-research-facts {
  background: white;
  padding: 25px;
  border-radius: 15px;
  margin: 20px 0;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.cancer-research-facts h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.3rem;
  color: #FF8C00;
}

.cancer-research-facts ul {
  margin: 0;
  padding-left: 20px;
}

.cancer-research-facts li {
  margin-bottom: 10px;
  color: #555;
  line-height: 1.5;
}

/* Responsive Adjustments */
@media (max-width: 600px) {
  .content-container {
    padding: 25px;
    width: 100%;
    border-radius: 20px 20px 0 0;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .tab-navigation button {
    padding: 10px 15px;
    font-size: 0.9rem;
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