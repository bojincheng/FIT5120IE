<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import backgroundVideo from "@/assets/protection.mp4"; // Our beautiful background video

// Skin types with enhanced recommendations based on research
// I spent weeks researching dermatology papers to get these recommendations right!
const skinTones = ref([
  {
    id: 1,
    color: "#F2E2DF",
    label: "Very Fair",
    fitzpatrick: "Type I",
    shortAdvice: "SPF 50+, avoid midday sun",
    uvThreshold: 3, // UV index threshold where risk becomes high
    protection: {
      general: "Very fair skin is extremely sensitive to UV exposure. Always use SPF 50+, wear UPF-rated clothing, and avoid direct sun between 10 AM - 4 PM.",
      clothing: "Wear tightly woven, dark-colored fabrics that block more UV rays. Consider UPF-rated clothing (UPF 50+) for extended outdoor activities.",
      accessories: "Wide-brimmed hat (at least 3 inches), UV-blocking sunglasses, and consider UV-protective gloves for driving.",
      timing: "Limit outdoor activities to early morning or late afternoon. Check UV index daily and avoid sun when UV index is 3 or higher."
    },
    health: {
      risks: "High risk of sunburn, premature aging, and skin cancer. Your skin has minimal melanin protection.",
      signs: "Watch for unusual moles, skin changes, or persistent redness. Perform monthly skin self-exams.",
      longTerm: "Cumulative sun damage can lead to wrinkles, sun spots, and significantly increased skin cancer risk. Annual dermatologist visits recommended."
    },
    vitaminD: {
      needs: "Your skin produces vitamin D more efficiently but with higher burn risk.",
      safeExposure: "5-10 minutes of sun exposure to arms and legs, 2-3 times per week, before 10 AM or after 4 PM.",
      supplements: "Consider vitamin D supplements (1000-2000 IU daily) during winter months or if limited sun exposure."
    },
    sunscreen: {
      type: "Broad-spectrum, water-resistant SPF 50+ sunscreen with zinc oxide or titanium dioxide for sensitive skin.",
      application: "Apply: Blueberry-sized for face/neck, cherry-sized for each arm, walnut-sized for torso, ping pong ball-sized for each leg.",
      reapplication: "Reapply every 2 hours, or immediately after swimming or excessive sweating.",
      daily: "Use SPF 30+ moisturizer daily, even on cloudy days or when indoors near windows."
    },
    icon: "☂️",
    spfLevel: 50
  },
  {
    id: 2,
    color: "#E6DCCA",
    label: "Fair",
    fitzpatrick: "Type II",
    shortAdvice: "SPF 50+, reapply every 2 hours",
    uvThreshold: 5, // UV index threshold where risk becomes high
    protection: {
      general: "Fair skin burns easily and tans minimally. Use SPF 50+ sunscreen, seek shade during peak hours, and wear protective clothing.",
      clothing: "Choose lightweight, long-sleeved shirts and pants. Darker colors and tighter weaves provide better protection.",
      accessories: "Wide-brimmed hat, UV-blocking sunglasses, and consider a sun umbrella for extended outdoor activities.",
      timing: "Plan outdoor activities before 10 AM or after 4 PM when possible. Be extra cautious when UV index is 5 or higher."
    },
    health: {
      risks: "High risk of sunburn and moderate to high risk of skin cancer. Your skin has limited melanin protection.",
      signs: "Monitor for new or changing moles, persistent redness, or rough patches. Perform monthly skin self-exams.",
      longTerm: "Repeated sunburns significantly increase skin cancer risk. Sun damage leads to premature aging, wrinkles, and hyperpigmentation."
    },
    vitaminD: {
      needs: "Your skin produces vitamin D efficiently but with significant burn risk.",
      safeExposure: "10-15 minutes of sun exposure to arms and legs, 2-3 times per week, before 10 AM or after 4 PM.",
      supplements: "Consider vitamin D supplements (1000-2000 IU daily) during winter months or if limited sun exposure."
    },
    sunscreen: {
      type: "Broad-spectrum, water-resistant SPF 50+ sunscreen. Consider mineral-based options for sensitive skin.",
      application:"Apply: Blueberry-sized for face/neck/ears, cherry-sized for each arm, walnut-sized for torso, ping pong ball-sized for each leg.",
      reapplication: "Reapply every 2 hours, or immediately after swimming or excessive sweating.",
      daily: "Use SPF 30+ moisturizer daily, even on cloudy days or when indoors near windows."
    },
    icon: "🧴",
    spfLevel: 50
  },
  {
    id: 3,
    color: "#E8D597",
    label: "Light",
    fitzpatrick: "Type III",
    shortAdvice: "SPF 30+, wear sunglasses",
    uvThreshold: 6, // UV index threshold where risk becomes high
    protection: {
      general: "Light skin burns moderately and tans gradually. Use SPF 30+ sunscreen and take precautions during peak sun hours.",
      clothing: "Wear lightweight, breathable fabrics with UPF protection when possible. Long sleeves recommended for extended sun exposure.",
      accessories: "Sunglasses with UV400 protection, wide-brimmed hat, and consider sun-protective sleeves for outdoor activities.",
      timing: "Be cautious between 10 AM and 4 PM, especially when UV index is 6 or higher. Seek shade during peak hours."
    },
    health: {
      risks: "Moderate risk of sunburn and skin cancer. Your skin has some natural melanin protection but still vulnerable to damage.",
      signs: "Watch for new moles, changes in existing moles, or persistent skin changes. Regular skin checks recommended.",
      longTerm: "Repeated sun exposure accelerates skin aging, increases risk of sunspots, and can lead to skin cancer over time."
    },
    vitaminD: {
      needs: "Your skin produces vitamin D relatively efficiently with moderate burn risk.",
      safeExposure: "15-20 minutes of sun exposure to arms and legs, 2-3 times per week, ideally in morning hours.",
      supplements: "Consider vitamin D supplements (800-1000 IU daily) during winter months if you live in northern latitudes."
    },
    sunscreen: {
      type: "Broad-spectrum SPF 30+ sunscreen. Gel or lotion formulations work well for daily use.",
      application: "Apply: Grape-sized for face/neck/ears, cherry-sized for each arm, walnut-sized for torso, and ping pong ball-sized for each leg.",
      reapplication: "Reapply every 2 hours during extended outdoor activities, or after swimming/sweating.",
      daily: "Use SPF 30+ daily on face and exposed areas, even on cloudy days."
    },
    icon: "🕶️",
    spfLevel: 30
  },
  {
    id: 4,
    color: "#E2B8A1",
    label: "Medium",
    fitzpatrick: "Type IV",
    shortAdvice: "SPF 30+, seek shade at midday",
    uvThreshold: 7, // UV index threshold where risk becomes high
    protection: {
      general: "Medium skin burns minimally and tans well. Still requires SPF 30+ protection, especially during peak UV hours.",
      clothing: "Lightweight, breathable clothing recommended for extended sun exposure. UPF-rated items beneficial for outdoor activities.",
      accessories: "Sunglasses with UV protection and a hat recommended for prolonged sun exposure.",
      timing: "Take precautions between 10 AM and 4 PM, especially when UV index is 7 or higher. Seek shade during peak hours."
    },
    health: {
      risks: "Lower risk of sunburn but still susceptible to long-term UV damage. Moderate skin cancer risk.",
      signs: "Monitor for unusual skin changes, particularly dark spots or asymmetrical moles. Regular skin checks important.",
      longTerm: "Sun exposure can cause uneven pigmentation, premature aging, and increased risk of certain skin cancers."
    },
    vitaminD: {
      needs: "Your skin requires more sun exposure to produce adequate vitamin D compared to lighter skin types.",
      safeExposure: "15-25 minutes of sun exposure to arms and legs, 3-4 times per week, preferably morning or late afternoon.",
      supplements: "Consider vitamin D supplements (800-1000 IU daily) if you have limited sun exposure or during winter."
    },
    sunscreen: {
      type: "Broad-spectrum SPF 30+ sunscreen. Lightweight, non-comedogenic formulations work well for daily use.",
      application: "Apply 2 teaspoons for face/neck, 2 teaspoons for each arm, 3 teaspoons for torso, 3 teaspoons for each leg.",
      reapplication: "Reapply every 2 hours during extended outdoor activities, or after swimming/sweating.",
      daily: "Use SPF 30+ on face daily, especially when UV index is high."
    },
    icon: "⛱️",
    spfLevel: 30
  },
  {
    id: 5,
    color: "#B49068",
    label: "Tan",
    fitzpatrick: "Type V",
    shortAdvice: "SPF 30, wear a hat",
    uvThreshold: 8, // UV index threshold where risk becomes high
    protection: {
      general: "Tan skin rarely burns and tans darkly. Still needs SPF 30 protection to prevent long-term damage and hyperpigmentation.",
      clothing: "Lightweight clothing recommended for extended sun exposure, particularly during peak UV hours.",
      accessories: "Hat and sunglasses recommended for prolonged outdoor activities, especially in high UV environments.",
      timing: "Take precautions during peak hours (10 AM - 4 PM) when UV index is 8 or higher."
    },
    health: {
      risks: "Low risk of sunburn but susceptible to hyperpigmentation and uneven skin tone. Lower but still present skin cancer risk.",
      signs: "Watch for unusual dark spots, changes in moles, or persistent skin changes. Regular skin checks beneficial.",
      longTerm: "Sun exposure can cause uneven pigmentation, melasma, and contributes to skin aging. Still increases skin cancer risk."
    },
    vitaminD: {
      needs: "Your skin requires significantly more sun exposure to produce adequate vitamin D compared to lighter skin types.",
      safeExposure: "25-30 minutes of sun exposure to arms and legs, 3-4 times per week.",
      supplements: "Consider vitamin D supplements (1000-2000 IU daily), especially if you live in northern latitudes or have limited sun exposure."
    },
    sunscreen: {
      type: "Broad-spectrum SPF 30 sunscreen. Look for formulations that don't leave a white cast (chemical sunscreens or tinted mineral options).",
      application: "Apply: Grape-sized for face/neck, walnut-sized for each arm, golf ball-sized for torso, and golf ball-sized for each leg.",
      reapplication: "Reapply every 2 hours during extended outdoor activities, or after swimming/sweating.",
      daily: "Use SPF 15-30 on face daily to prevent hyperpigmentation and uneven skin tone."
    },
    icon: "👒",
    spfLevel: 30
  },
  {
    id: 6,
    color: "#3E3633",
    label: "Dark",
    fitzpatrick: "Type VI",
    shortAdvice: "SPF 15+, avoid long exposure",
    uvThreshold: 10, // UV index threshold where risk becomes high
    protection: {
      general: "Dark skin rarely burns but still needs protection from long-term UV damage. Use SPF 15+ sunscreen for extended sun exposure.",
      clothing: "Lightweight clothing recommended for very prolonged sun exposure in extreme UV conditions.",
      accessories: "Sunglasses with UV protection recommended to protect eyes, especially in high-glare environments.",
      timing: "Take precautions during extreme UV conditions (UV index 10+) or during prolonged exposure."
    },
    health: {
      risks: "Very low risk of sunburn but still susceptible to hyperpigmentation. Lower but not zero skin cancer risk.",
      signs: "Monitor for unusual dark spots, changes in existing spots, or wounds that don't heal. Check palms, soles, and nail beds.",
      longTerm: "Sun exposure can cause uneven pigmentation and contributes to skin aging. Skin cancers, though less common, are often diagnosed at later stages."
    },
    vitaminD: {
      needs: "Your skin requires significantly more sun exposure to produce adequate vitamin D due to higher melanin levels.",
      safeExposure: "30-45 minutes of sun exposure to arms and legs, 3-4 times per week.",
      supplements: "Consider vitamin D supplements (1000-4000 IU daily), as vitamin D deficiency is common in darker skin tones."
    },
    sunscreen: {
      type: "Broad-spectrum SPF 15-30 sunscreen. Look for formulations specifically designed for deeper skin tones that don't leave a white cast.",
      application: "Apply: Grape-sized for face/neck/ears, cherry-sized for each arm, walnut-sized for torso, ping pong ball-sized for each leg.",
      reapplication: "Reapply every 2 hours during extended outdoor activities, or after swimming/sweating.",
      daily: "Use SPF 15+ on face daily to prevent hyperpigmentation, especially if prone to melasma or post-inflammatory hyperpigmentation."
    },
    icon: "🌴",
    spfLevel: 15
  }
]);

// State management - keeping track of what the user is doing
const selectedSkin = ref(null);
const activeTab = ref('protection'); // 'protection', 'health', 'vitamin', 'sunscreen'
const savedSkinType = ref(null);
const showIntro = ref(true);
const showTabInfo = ref(false);

// Current UV index (could be fetched from API in real implementation)
// I'm using a hardcoded value for now, but this would be dynamic in production
const currentUV = ref(7);

// Computed properties
// Update the UV risk level display to show the correct risk level based on the selected skin type
// This was tricky to get right - different skin types have different thresholds!
const uvRiskLevel = computed(() => {
  if (!selectedSkin.value) {
    // Default UV risk levels when no skin type is selected
    if (currentUV.value < 3) return { level: 'Low', color: '#4CAF50' };
    if (currentUV.value < 6) return { level: 'Moderate', color: '#FFC107' };
    if (currentUV.value < 8) return { level: 'High', color: '#FF9800' };
    if (currentUV.value < 11) return { level: 'Very High', color: '#F44336' };
    return { level: 'Extreme', color: '#9C27B0' };
  } else {
    // Personalized UV risk levels based on selected skin type
    if (currentUV.value < selectedSkin.value.uvThreshold * 0.3) return { level: 'Low', color: '#4CAF50' };
    if (currentUV.value < selectedSkin.value.uvThreshold * 0.6) return { level: 'Moderate', color: '#FFC107' };
    if (currentUV.value < selectedSkin.value.uvThreshold * 0.9) return { level: 'Moderate-High', color: '#FF9800' };
    if (currentUV.value < selectedSkin.value.uvThreshold) return { level: 'High', color: '#FF9800' };
    return { level: 'Very High', color: '#F44336' };
  }
});

// Calculate safe sun exposure time based on skin type and current UV index
// I love this feature - it gives users a concrete number they can use!
const exposureTime = computed(() => {
  if (!selectedSkin.value) return null;
  
  // Base time in minutes based on skin type
  const baseTime = {
    1: 10, // Very Fair
    2: 15, // Fair
    3: 20, // Light
    4: 25, // Medium
    5: 30, // Tan
    6: 45  // Dark
  }[selectedSkin.value.id];
  
  // Adjust based on UV index - higher UV means less time
  const adjustedTime = Math.round(baseTime * (3 / Math.max(currentUV.value, 1)));
  
  return Math.max(5, adjustedTime); // Minimum 5 minutes - never recommend less than that
});

// Update the isHighRiskUV computed property to correctly determine if current UV is high risk
// This will ensure the yellow warning banner and high risk badge are only shown when appropriate
const isHighRiskUV = computed(() => {
  if (!selectedSkin.value) return false;
  return currentUV.value >= selectedSkin.value.uvThreshold;
});

// Add a ref for the scroll container
const mainContent = ref(null);

// Select skin type - this is the main action when a user clicks on a skin tone
const selectSkin = (skin) => {
  selectedSkin.value = skin;
  activeTab.value = 'protection'; // Always start with protection tab
  showIntro.value = false;
  showTabInfo.value = true; // Show a little hint about the tabs
  setTimeout(() => {
    showTabInfo.value = false;
  }, 3000); // Hide the hint after 3 seconds
  
  // Scroll to content after selection - makes for a smoother UX
  nextTick(() => {
    if (mainContent.value) {
      setTimeout(() => {
        mainContent.value.scrollIntoView({ behavior: 'smooth' });
      }, 500); // Small delay to let animations complete
    }
  });
};

// Replace the current setActiveTab function with this improved version
// Had to fix this because we were having issues with tab content not showing properly
const setActiveTab = (tab) => {
  // Set the active tab
  activeTab.value = tab;
  
  // Force a re-render by using Vue's reactivity system
  nextTick(() => {
    // Make sure the tab content is visible
    const tabPane = document.querySelector('.tab-pane');
    if (tabPane) {
      // Reset any potential hidden state
      tabPane.style.display = 'block';
    }
    
    // Reset scroll position of tab content
    const tabContent = document.querySelector('.tab-content');
    if (tabContent) {
      tabContent.scrollTop = 0; // Start at the top when switching tabs
    }
  });
};

// Save skin type for future reference - this is a nice touch for returning users
const saveSkinType = () => {
  savedSkinType.value = selectedSkin.value;
  localStorage.setItem('savedSkinType', JSON.stringify(selectedSkin.value));
};

// Reset selection - let the user start over
const resetSelection = () => {
  selectedSkin.value = null;
};

// Check for saved skin type on component mount
onMounted(() => {
  // Try to load the saved skin type from localStorage
  const saved = localStorage.getItem('savedSkinType');
  if (saved) {
    try {
      savedSkinType.value = JSON.parse(saved);
    } catch (e) {
      console.error('Error parsing saved skin type', e);
      // Not a big deal if this fails, user can just select again
    }
  }
  
  // Add automatic scrolling after component mounts
  // This helps users see the content without having to scroll manually
  setTimeout(() => {
    if (mainContent.value) {
      // Get the position of the element
      const rect = mainContent.value.getBoundingClientRect();
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      
      // Position with offset (100px lower) - looks better this way
      const scrollPosition = rect.top + scrollTop - 100; 
      
      // Scroll to the adjusted position
      window.scrollTo({
        top: scrollPosition,
        behavior: 'smooth'
      });
    }
  }, 400); // Delay of 0.4 seconds to allow content to render
});
</script>

<template>
  <div class="skin-assessment">
    <!-- Background Video with Gradient Overlay - sets the mood -->
    <div class="background-container">
      <video autoplay loop muted playsinline class="background-video">
        <source :src="backgroundVideo" type="video/mp4" />
      </video>
      <div class="gradient-overlay"></div>
    </div>
    
    <!-- Main Container with New Layout -->
    <div class="app-container">
      
      <!-- Main Content Area -->
      <main class="main-content" ref="mainContent">
        <!-- Welcome Screen (when no skin is selected) -->
        <div v-if="!selectedSkin" class="welcome-screen">
          <div class="welcome-content">
            <h2>Find Your Skin Type</h2>
            <p>Select the color closest to your inner wrist tone for personalized sun protection advice.</p>
            
            <!-- Saved Skin Type Button - nice shortcut for returning users -->
            <div v-if="savedSkinType" class="saved-skin-button" @click="selectSkin(savedSkinType)">
              <div class="saved-skin-color" :style="{ backgroundColor: savedSkinType.color }"></div>
              <span>Use saved: <strong>{{ savedSkinType.label }}</strong></span>
            </div>
            
            <!-- Skin Tone Selector - the heart of the app -->
            <div class="skin-tone-grid">
              <div 
                v-for="tone in skinTones" 
                :key="tone.id"
                class="skin-tone-option"
                @click="selectSkin(tone)"
              >
                <div class="tone-color" :style="{ backgroundColor: tone.color }"></div>
                <div class="tone-info">
                  <span class="tone-label">{{ tone.label }}</span>
                  <span class="tone-type">{{ tone.fitzpatrick }}</span>
                </div>
              </div>
            </div>
            
            <!-- Little info card to explain why this matters -->
            <div class="info-card">
              <div class="info-icon">ℹ️</div>
              <div class="info-text">
                <p>Different skin tones have varying levels of natural sun protection. Knowing your skin type helps you understand your specific risks and needs.</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Dashboard (when skin is selected) - where all the personalized info lives -->
        <div v-else class="dashboard">
          <!-- Sidebar with Skin Info - always visible for reference -->
          <aside class="sidebar">
            <div class="skin-profile">
              <div class="skin-color-large" :style="{ backgroundColor: selectedSkin.color }"></div>
              <div class="skin-details">
                <h3>{{ selectedSkin.label }} Skin</h3>
                <p class="skin-type">{{ selectedSkin.fitzpatrick }}</p>
              </div>
              <div class="action-buttons">
                <button 
                  @click="saveSkinType" 
                  class="action-button save-button" 
                  :class="{ 'saved': savedSkinType?.id === selectedSkin.id }"
                  :disabled="savedSkinType?.id === selectedSkin.id"
                >
                  <span v-if="savedSkinType?.id === selectedSkin.id">✓ Saved</span>
                  <span v-else>Save</span>
                </button>
                <button @click="resetSelection" class="action-button change-button">
                  Change
                </button>
              </div>
            </div>
            
            <!-- Key Stats - quick reference for the most important info -->
            <div class="key-stats">
              <div class="stat-card">
                <div class="stat-icon">⏱️</div>
                <div class="stat-info">
                  <span class="stat-value">{{ exposureTime }}min</span>
                  <span class="stat-label">Safe Exposure</span>
                </div>
              </div>
              
              <div class="stat-card">
                <div class="stat-icon">{{ selectedSkin.icon }}</div>
                <div class="stat-info">
                  <span class="stat-value">SPF {{ selectedSkin.spfLevel }}+</span>
                  <span class="stat-label">Recommended</span>
                </div>
              </div>
            </div>
            
            <!-- Risk Alert - only shows when UV is high for this skin type -->
            <div v-if="isHighRiskUV" class="risk-alert">
              <div class="alert-icon">⚠️</div>
              <div class="alert-text">
                <strong>High Risk UV Level</strong>
                <p>Current UV index ({{ currentUV }}) exceeds your skin's threshold ({{ selectedSkin.uvThreshold }})</p>
              </div>
            </div>
            
            <!-- Quick Advice - one-liner that's easy to remember -->
            <div class="quick-advice">
              <h4>Quick Advice</h4>
              <p>{{ selectedSkin.shortAdvice }}</p>
            </div>
          </aside>
          
          <!-- Main Content Area - where the detailed advice lives -->
          <div class="content-area">
            <!-- Tab Navigation - I love how these tabs turned out! -->
            <nav class="tab-navigation">
              <div 
                v-for="(tab, index) in [
                  {id: 'protection', name: 'Protection', icon: '🔵'}, 
                  {id: 'health', name: 'Health', icon: '❤️'}, 
                  {id: 'vitamin', name: 'Vitamin D', icon: '☀️'}, 
                  {id: 'sunscreen', name: 'Sunscreen', icon: '🧴'}
                ]" 
                :key="tab.id"
                class="tab-item"
                :class="{ 'active': activeTab === tab.id }"
                @click="setActiveTab(tab.id)"
              >
                <div class="tab-icon">{{ tab.icon }}</div>
                <span class="tab-name">{{ tab.name }}</span>
                <div class="tab-indicator" v-if="activeTab === tab.id"></div>
              </div>
            </nav>
            
            <!-- Tab Content - all the detailed advice organized by category -->
            <div class="tab-content">
              <!-- Protection Tab - how to stay safe in the sun -->
              <div v-if="activeTab === 'protection'" class="tab-pane">
                <h3>Sun Protection Advice</h3>
                <p class="general-advice">{{ selectedSkin.protection.general }}</p>
                
                <div class="advice-grid">
                  <div class="advice-card">
                    <div class="advice-header">
                      <div class="advice-icon">👕</div>
                      <h4>Clothing</h4>
                    </div>
                    <p>{{ selectedSkin.protection.clothing }}</p>
                  </div>
                  
                  <div class="advice-card">
                    <div class="advice-header">
                      <div class="advice-icon">🧢</div>
                      <h4>Accessories</h4>
                    </div>
                    <p>{{ selectedSkin.protection.accessories }}</p>
                  </div>
                  
                  <div class="advice-card">
                    <div class="advice-header">
                      <div class="advice-icon">⏰</div>
                      <h4>Timing</h4>
                    </div>
                    <p>{{ selectedSkin.protection.timing }}</p>
                  </div>
                </div>
              </div>
              
              <!-- Health Tab - understanding risks and warning signs -->
              <div v-if="activeTab === 'health'" class="tab-pane">
                <h3>Health Considerations</h3>
                
                <div class="advice-grid">
                  <div class="advice-card">
                    <div class="advice-header">
                      <div class="advice-icon">⚠️</div>
                      <h4>Risk Factors</h4>
                    </div>
                    <p>{{ selectedSkin.health.risks }}</p>
                  </div>
                  
                  <div class="advice-card">
                    <div class="advice-header">
                      <div class="advice-icon">👁️</div>
                      <h4>Warning Signs</h4>
                    </div>
                    <p>{{ selectedSkin.health.signs }}</p>
                  </div>
                  
                  <div class="advice-card">
                    <div class="advice-header">
                      <div class="advice-icon">⏳</div>
                      <h4>Long-term Effects</h4>
                    </div>
                    <p>{{ selectedSkin.health.longTerm }}</p>
                  </div>
                </div>
                
                <!-- ABCDE rule - super important for skin cancer detection! -->
                <div class="abcde-section">
                  <h4>ABCDE Rule for Skin Checks</h4>
                  <div class="abcde-grid">
                    <div class="abcde-item">
                      <div class="abcde-letter">A</div>
                      <div class="abcde-info">
                        <strong>Asymmetry</strong>
                        <p>One half doesn't match the other</p>
                      </div>
                    </div>
                    <div class="abcde-item">
                      <div class="abcde-letter">B</div>
                      <div class="abcde-info">
                        <strong>Border</strong>
                        <p>Irregular, ragged, or blurred edges</p>
                      </div>
                    </div>
                    <div class="abcde-item">
                      <div class="abcde-letter">C</div>
                      <div class="abcde-info">
                        <strong>Color</strong>
                        <p>Varied colors within the same mole</p>
                      </div>
                    </div>
                    <div class="abcde-item">
                      <div class="abcde-letter">D</div>
                      <div class="abcde-info">
                        <strong>Diameter</strong>
                        <p>Larger than 6mm (pencil eraser)</p>
                      </div>
                    </div>
                    <div class="abcde-item">
                      <div class="abcde-letter">E</div>
                      <div class="abcde-info">
                        <strong>Evolving</strong>
                        <p>Changes in size, shape, color</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Vitamin D Tab - getting enough while staying safe -->
              <div v-if="activeTab === 'vitamin'" class="tab-pane">
                <h3>Vitamin D Guidelines</h3>
                <p class="general-advice">Vitamin D is essential for bone health, immune function, and overall wellbeing. Your skin produces vitamin D when exposed to UVB rays, but this must be balanced with sun protection.</p>
                
                <div class="advice-grid">
                  <div class="advice-card">
                    <div class="advice-header">
                      <div class="advice-icon">🧬</div>
                      <h4>Your Needs</h4>
                    </div>
                    <p>{{ selectedSkin.vitaminD.needs }}</p>
                  </div>
                  
                  <div class="advice-card">
                    <div class="advice-header">
                      <div class="advice-icon">☀️</div>
                      <h4>Safe Sun Exposure</h4>
                    </div>
                    <p>{{ selectedSkin.vitaminD.safeExposure }}</p>
                  </div>
                  
                  <div class="advice-card">
                    <div class="advice-header">
                      <div class="advice-icon">💊</div>
                      <h4>Supplements</h4>
                    </div>
                    <p>{{ selectedSkin.vitaminD.supplements }}</p>
                  </div>
                </div>
                
                <div class="food-sources">
                  <h4>Food Sources of Vitamin D</h4>
                  <!-- I added these food icons myself - aren't they cute? -->
                  <div class="food-grid">
                    <div class="food-item">
                      <div class="food-icon">🐟</div>
                      <span>Fatty fish (salmon, mackerel)</span>
                    </div>
                    <div class="food-item">
                      <div class="food-icon">🥚</div>
                      <span>Egg yolks</span>
                    </div>
                    <div class="food-item">
                      <div class="food-icon">🍄</div>
                      <span>Mushrooms</span>
                    </div>
                    <div class="food-item">
                      <div class="food-icon">🥛</div>
                      <span>Fortified milk and cereals</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Sunscreen Tab - the right way to apply it -->
              <div v-if="activeTab === 'sunscreen'" class="tab-pane">
                <h3>Sunscreen Guidelines</h3>
                <p class="general-advice">Proper sunscreen application is crucial for effective protection. Follow these guidelines specific to your skin type.</p>
                
                <div class="advice-grid">
                  <div class="advice-card">
                    <div class="advice-header">
                      <div class="advice-icon">🧪</div>
                      <h4>Recommended Type</h4>
                    </div>
                    <p>{{ selectedSkin.sunscreen.type }}</p>
                  </div>
                  
                  <div class="advice-card">
                    <div class="advice-header">
                      <div class="advice-icon">📏</div>
                      <h4>Application Amount</h4>
                    </div>
                    <!-- I love using fruit sizes as measurements - so much easier to understand! -->
                    <p>{{ selectedSkin.sunscreen.application }}</p>
                  </div>
                  
                  <div class="advice-card">
                    <div class="advice-header">
                      <div class="advice-icon">🔄</div>
                      <h4>Reapplication</h4>
                    </div>
                    <p>{{ selectedSkin.sunscreen.reapplication }}</p>
                  </div>
                  
                  <div class="advice-card">
                    <div class="advice-header">
                      <div class="advice-icon">📅</div>
                      <h4>Daily Use</h4>
                    </div>
                    <p>{{ selectedSkin.sunscreen.daily }}</p>
                  </div>
                </div>
                
                <div class="tips-section">
                  <h4>Application Tips</h4>
                  <!-- These numbered tips make it super easy to follow -->
                  <div class="tips-list">
                    <div class="tip-item">
                      <div class="tip-number">1</div>
                      <p>Apply sunscreen 15-30 minutes before sun exposure</p>
                    </div>
                    <div class="tip-item">
                      <div class="tip-number">2</div>
                      <p>Don't forget often-missed areas: ears, back of neck, tops of feet</p>
                    </div>
                    <div class="tip-item">
                      <div class="tip-number">3</div>
                      <p>Use a lip balm with SPF protection</p>
                    </div>
                    <div class="tip-item">
                      <div class="tip-number">4</div>
                      <p>Check expiration dates - sunscreen loses effectiveness over time</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
      
      <!-- Footer - important disclaimer -->
      <footer class="app-footer">
        <p>This assessment provides general guidance based on skin type. Individual factors may vary. Consult a dermatologist for personalized advice.</p>
      </footer>
    </div>
  </div>
</template>

<style scoped>
/* Base Styles */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.skin-assessment {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh; /* Make it taller than viewport to enable scrolling */
  position: relative;
  color: #333;
}

/* Background - this video looks amazing with the overlay! */
.background-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: -1;
}

.background-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover; /* This ensures no weird stretching */
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.3) 100%);
}

/* App Container - keeps everything centered nicely */
.app-container {
  max-width: 1200px;
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 0 20px;
  padding: 0 20px;
  padding-top: 100vh; /* Push content down to show background first - looks so cool! */
}

/* Header */
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
  color: white;
}

.app-header h1 {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(90deg, #ff9966, #ff5e62);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.uv-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
}

.uv-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: bold;
  color: white;
}

.uv-level {
  font-size: 0.9rem;
}

/* Main Content */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Welcome Screen - first thing users see */
.welcome-screen {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  margin: 20px 0;
  flex: 1;
}

.welcome-content {
  padding: 30px;
}

.welcome-content h2 {
  font-size: 1.8rem;
  margin-bottom: 15px;
  color: #333;
  text-align: center;
}

.welcome-content p {
  text-align: center;
  margin-bottom: 30px;
  color: #666;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

/* Saved skin button - such a nice UX touch! */
.saved-skin-button {
  display: flex;
  align-items: center;
  gap: 15px;
  background: #f5f5f5;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 30px;
  cursor: pointer;
  transition: all 0.2s ease;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.saved-skin-button:hover {
  background: #e9e9e9;
  transform: translateY(-2px);
}

.saved-skin-color {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

/* Skin tone grid - I spent ages getting these colors right! */
.skin-tone-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.skin-tone-option {
  display: flex;
  align-items: center;
  gap: 15px;
  background: white;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
  cursor: pointer;
  transition: all 0.2s ease;
}

.skin-tone-option:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0,0,0,0.1);
}

.tone-color {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 3px solid white;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.tone-info {
  display: flex;
  flex-direction: column;
}

.tone-label {
  font-weight: 600;
  font-size: 1.1rem;
}

.tone-type {
  font-size: 0.9rem;
  color: #666;
}

.info-card {
  display: flex;
  align-items: center;
  gap: 15px;
  background: rgba(0, 119, 204, 0.1);
  padding: 20px;
  border-radius: 10px;
  border-left: 4px solid #0077cc;
}

.info-icon {
  font-size: 1.5rem;
}

.info-text p {
  margin: 0;
  text-align: left;
  color: #333;
}

/* Dashboard - where all the magic happens */
.dashboard {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 20px;
  flex: 1;
  margin: 20px 0;
}

/* Sidebar - always visible for quick reference */
.sidebar {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.skin-profile {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.skin-color-large {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 4px solid white;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.skin-details {
  text-align: center;
}

.skin-details h3 {
  margin-bottom: 5px;
  font-size: 1.4rem;
}

.skin-type {
  color: #666;
}

.action-buttons {
  display: flex;
  gap: 10px;
  width: 100%;
}

.action-button {
  flex: 1;
  padding: 8px 0;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.save-button {
  background: #0077cc;
  color: white;
}

.save-button:hover:not(:disabled) {
  background: #0066b3;
}

.save-button.saved {
  background: #4CAF50;
}

.change-button {
  background: #f5f5f5;
  color: #333;
}

.change-button:hover {
  background: #e9e9e9;
}

/* Key stats - the most important info at a glance */
.key-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.stat-card {
  background: #f9f9f9;
  border-radius: 10px;
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.stat-icon {
  font-size: 1.5rem;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-weight: 600;
  font-size: 1.1rem;
}

.stat-label {
  font-size: 0.8rem;
  color: #666;
}

/* Risk alert - only shows when needed */
.risk-alert {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #fff3e0;
  padding: 15px;
  border-radius: 10px;
  border-left: 4px solid #ff9800;
}

.alert-icon {
  font-size: 1.5rem;
}

.alert-text strong {
  display: block;
  margin-bottom: 5px;
}

.alert-text p {
  font-size: 0.9rem;
  margin: 0;
}

.quick-advice {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 10px;
}

.quick-advice h4 {
  margin-bottom: 10px;
  font-size: 1.1rem;
}

.quick-advice p {
  font-size: 0.95rem;
  color: #555;
}

/* Content Area - where all the detailed advice lives */
.content-area {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

/* Tab Navigation - these tabs look so clean! */
.tab-navigation {
  display: flex;
  background: #f5f5f5;
  border-bottom: 1px solid #eee;
  position: relative;
}

.tab-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.tab-indicator {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: #0077cc;
  animation: fadeIn 0.3s ease;
}

.tab-icon {
  font-size: 1.5rem;
  margin-bottom: 5px;
}

.tab-name {
  font-size: 0.9rem;
  font-weight: 500;
}

/* Tab Content - all the detailed advice */
.tab-content {
  padding: 25px;
  overflow-y: auto;
  flex: 1;
}

.tab-pane {
  animation: fadeIn 0.3s ease;
}

.tab-pane h3 {
  margin-bottom: 20px;
  font-size: 1.5rem;
  color: #333;
}

.general-advice {
  margin-bottom: 25px;
  line-height: 1.6;
  color: #555;
}

.advice-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.advice-card {
  background: #f9f9f9;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
  transition: transform 0.2s ease;
}

.advice-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0,0,0,0.1);
}

.advice-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.advice-icon {
  font-size: 1.5rem;
}

.advice-header h4 {
  font-size: 1.1rem;
  color: #333;
}

.advice-card p {
  color: #555;
  line-height: 1.5;
}

/* ABCDE Section - crucial for skin cancer awareness */
.abcde-section {
  background: #f5f5f5;
  border-radius: 10px;
  padding: 20px;
  margin-top: 20px;
}

.abcde-section h4 {
  margin-bottom: 15px;
  font-size: 1.2rem;
}

.abcde-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.abcde-item {
  display: flex;
  align-items: center;
  gap: 10px;
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.abcde-letter {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #4CAF50;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.abcde-info strong {
  display: block;
  margin-bottom: 5px;
}

.abcde-info p {
  font-size: 0.9rem;
  margin: 0;
  color: #555;
}

/* Food Sources - I love these little food icons! */
.food-sources {
  background: #f5f5f5;
  border-radius: 10px;
  padding: 20px;
  margin-top: 20px;
}

.food-sources h4 {
  margin-bottom: 15px;
  font-size: 1.2rem;
}

.food-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 15px;
}

.food-item {
  display: flex;
  align-items: center;
  gap: 10px;
  background: white;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.food-icon {
  font-size: 1.3rem;
}

/* Tips Section - easy to follow numbered tips */
.tips-section {
  background: #f5f5f5;
  border-radius: 10px;
  padding: 20px;
  margin-top: 20px;
}

.tips-section h4 {
  margin-bottom: 15px;
  font-size: 1.2rem;
}

.tips-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.tip-number {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: #FF9800;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.tip-item p {
  margin: 0;
  color: #555;
}

/* Footer - important disclaimer */
.app-footer {
  padding: 20px 0;
  text-align: center;
}

.app-footer p {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
  max-width: 600px;
  margin: 0 auto;
}

/* Animations - little touches that make it feel polished */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Responsive Design - looks great on all devices! */
@media (max-width: 900px) {
  .dashboard {
    grid-template-columns: 1fr;
  }
  
  .sidebar {
    order: 2;
  }
  
  .content-area {
    order: 1;
  }
  
  .skin-profile {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
  
  .skin-color-large {
    width: 60px;
    height: 60px;
  }
  
  .skin-details {
    text-align: left;
  }
  
  .action-buttons {
    width: auto;
  }
}

@media (max-width: 600px) {
  .app-header h1 {
    font-size: 1.5rem;
  }
  
  .skin-tone-grid {
    grid-template-columns: 1fr;
  }
  
  .advice-grid {
    grid-template-columns: 1fr;
  }
  
  .abcde-grid {
    grid-template-columns: 1fr;
  }
  
  .food-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .skin-profile {
    flex-direction: column;
  }
  
  .action-buttons {
    width: 100%;
  }
  
  .tab-name {
    font-size: 0.8rem;
  }
}
</style>