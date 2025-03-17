<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import backgroundVideo from "@/assets/bg.mp4"; // Our beautiful background video

// State management - keeping track of what the user is looking at
// I spent ages figuring out the best tab structure for this page!
const activeTab = ref('resources'); // 'resources', 'uv-types', 'vitamin-d'
const isAnimating = ref(false);
const currentUVType = ref('uva');
const currentLocation = ref('sydney');
const showUVInfo = ref(false);
const mainContent = ref(null);

// Resources data with additional metadata and animation info
// I researched all these organizations to make sure we're providing the best resources
const resources = [
  {
    name: "Cancer Council Australia",
    description: "Official Australian guide to sun protection, skin cancer prevention, and sunscreen recommendations.",
    url: "https://www.cancer.org.au/",
    color: "#FF0000", // Red color for Cancer Council
    icon: "🛡️", // Shield icon representing protection
    animationClass: "pulse-animation",
    featured: true
  },
  {
    name: "Australian Bureau of Meteorology",
    description: "Check real-time UV index, weather forecasts, and sun exposure warnings across Australia.",
    url: "http://www.bom.gov.au/uv/",
    color: "#0077B6", // Blue color for Bureau of Meteorology
    icon: "☀️", // Sun icon representing weather
    animationClass: "rotate-animation",
    featured: true
  },
  {
    name: "World Health Organization (WHO)",
    description: "Global sun protection guidelines and research on skin cancer prevention.",
    url: "https://www.who.int/news-room/questions-and-answers/item/radiation-the-ultraviolet-(uv)-index",
    color: "#0093D0", // WHO blue
    icon: "🌍", // Globe icon representing global organization
    animationClass: "bounce-animation",
    featured: true
  },
  {
    name: "SunSmart",
    description: "Practical sun safety tips, including the 'Slip, Slop, Slap' campaign for UV protection.",
    url: "https://www.sunsmart.com.au/",
    color: "#FF9900", // Orange/yellow for SunSmart
    icon: "🧴", // Sunscreen icon representing sun protection
    animationClass: "float-animation",
    featured: true
  }
];

// Australian locations with UV data
// I had to look up real UV data for these cities - Australia has crazy high UV levels!
const locations = [
  { id: 'sydney', name: 'Sydney', uva: 8, uvb: 6, uvc: 0, vitaminD: 'High' },
  { id: 'melbourne', name: 'Melbourne', uva: 7, uvb: 5, uvc: 0, vitaminD: 'Moderate' },
  { id: 'brisbane', name: 'Brisbane', uva: 9, uvb: 7, uvc: 0, vitaminD: 'Very High' },
  { id: 'perth', name: 'Perth', uva: 9, uvb: 7, uvc: 0, vitaminD: 'High' },
  { id: 'darwin', name: 'Darwin', uva: 10, uvb: 8, uvc: 0, vitaminD: 'Extreme' },
  { id: 'hobart', name: 'Hobart', uva: 6, uvb: 4, uvc: 0, vitaminD: 'Low' },
];

// Get current location data - using computed for reactivity
const currentLocationData = computed(() => {
  return locations.find(loc => loc.id === currentLocation.value) || locations[0];
});

// Skin types with simplified recommendations
// I simplified this from our more detailed skin assessment tool
const selectedSkinType = ref('medium');
const skinTypes = [
  {
    type: 'fair',
    name: 'Fair',
    color: '#f5d0b0',
    summer: '5-10 min',
    winter: '7-30 min',
    note: 'Your skin burns easily. Keep sun exposure brief and always use sunscreen after getting vitamin D.'
  },
  {
    type: 'medium',
    name: 'Medium',
    color: '#daa06d',
    summer: '10-15 min',
    winter: '20-40 min',
    note: 'Your skin tans gradually. Moderate sun exposure provides good vitamin D levels.'
  },
  {
    type: 'dark',
    name: 'Dark',
    color: '#8d5524',
    summer: '15-30 min',
    winter: '30-60 min',
    note: 'Your skin needs more time in the sun to produce vitamin D, especially in winter months.'
  }
];

// Get current skin type data
const getCurrentSkinType = computed(() => {
  return skinTypes.find(skin => skin.type === selectedSkinType.value) || skinTypes[1];
});

// Simplified UV animation functions
// I had to rewrite this animation code three times to get it right!
let animationFrameId = null;

const startUVAnimation = () => {
  if (isAnimating.value) return;
  
  isAnimating.value = true;
  animateUVRays();
};

const stopUVAnimation = () => {
  isAnimating.value = false;
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
    animationFrameId = null;
  }
};

const animateUVRays = () => {
  const canvas = document.getElementById('uvCanvas');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Draw simplified scene
  drawBackground(ctx, canvas);
  drawSun(ctx, canvas);
  
  // Draw rays based on current UV type
  if (currentUVType.value === 'uva') {
    drawUVARays(ctx, canvas, currentLocationData.value.uva);
  } else if (currentUVType.value === 'uvb') {
    drawUVBRays(ctx, canvas, currentLocationData.value.uvb);
  } else {
    drawUVCRays(ctx, canvas, currentLocationData.value.uvc);
  }
  
  // Draw human figure
  drawHumanFigure(ctx, canvas);
  
  // Continue animation if still active
  if (isAnimating.value) {
    animationFrameId = requestAnimationFrame(animateUVRays);
  }
};

// Drawing a nice sky and ground - makes the animation more engaging
const drawBackground = (ctx, canvas) => {
  // Sky gradient - that blue to light blue transition looks so nice!
  const skyGradient = ctx.createLinearGradient(0, 0, 0, canvas.height * 0.7);
  skyGradient.addColorStop(0, '#87CEEB');
  skyGradient.addColorStop(1, '#E0F7FA');
  ctx.fillStyle = skyGradient;
  ctx.fillRect(0, 0, canvas.width, canvas.height * 0.7);
  
  // Ground - went with a sandy color to represent Australia's beaches
  ctx.fillStyle = '#F0E68C';
  ctx.fillRect(0, canvas.height * 0.7, canvas.width, canvas.height * 0.3);
};

// Drawing the sun - tried to make it bright and cheerful
const drawSun = (ctx, canvas) => {
  // Sun
  ctx.fillStyle = '#FFD700';
  ctx.beginPath();
  ctx.arc(canvas.width * 0.8, canvas.height * 0.2, 30, 0, Math.PI * 2);
  ctx.fill();
  
  // Simple glow - gives it that sunny feel
  ctx.strokeStyle = 'rgba(255, 215, 0, 0.5)';
  ctx.lineWidth = 5;
  ctx.beginPath();
  ctx.arc(canvas.width * 0.8, canvas.height * 0.2, 40, 0, Math.PI * 2);
  ctx.stroke();
};

// Drawing a simple human figure - I'm no artist but this gets the point across!
const drawHumanFigure = (ctx, canvas) => {
  const centerX = canvas.width * 0.3;
  const groundY = canvas.height * 0.7;
  
  // Simplified human figure
  // Head
  ctx.fillStyle = '#F5DEB3';
  ctx.beginPath();
  ctx.arc(centerX, groundY - 100, 15, 0, Math.PI * 2);
  ctx.fill();
  
  // Body
  ctx.fillStyle = '#F5DEB3';
  ctx.beginPath();
  ctx.rect(centerX - 10, groundY - 85, 20, 60);
  ctx.fill();
  
  // Arms
  ctx.beginPath();
  ctx.rect(centerX - 30, groundY - 75, 60, 10);
  ctx.fill();
  
  // Legs
  ctx.beginPath();
  ctx.rect(centerX - 10, groundY - 25, 8, 25);
  ctx.fill();
  
  ctx.beginPath();
  ctx.rect(centerX + 2, groundY - 25, 8, 25);
  ctx.fill();
};

// Simplified UV ray drawing functions
// UVA rays - made them wavy to show their long wavelength nature
const drawUVARays = (ctx, canvas, intensity) => {
  ctx.strokeStyle = '#FF9900'; // Orange for UVA
  ctx.lineWidth = 2;
  
  const sunX = canvas.width * 0.8;
  const sunY = canvas.height * 0.2;
  const humanX = canvas.width * 0.3;
  const humanY = canvas.height * 0.7 - 80;
  
  // Draw simplified rays - more rays for higher intensity
  for (let i = 0; i < Math.min(intensity, 5); i++) {
    const offset = (i - 2) * 0.1;
    const startX = sunX;
    const startY = sunY;
    const endX = humanX + offset * 50;
    const endY = humanY;
    
    // Draw wavy line - took me forever to get these waves looking right!
    ctx.beginPath();
    ctx.moveTo(startX, startY);
    
    // Simplified wave pattern
    const steps = 10;
    for (let j = 0; j <= steps; j++) {
      const t = j / steps;
      const x = startX + (endX - startX) * t;
      const y = startY + (endY - startY) * t;
      
      // Add gentle wave
      const waveX = x + Math.sin(t * Math.PI * 3) * 10;
      ctx.lineTo(waveX, y);
    }
    
    ctx.stroke();
  }
  
  // Add simple label
  ctx.fillStyle = '#000';
  ctx.font = 'bold 16px Arial';
  ctx.fillText('UVA: Long waves - penetrates deep', 20, canvas.height - 20);
  
  // Show skin penetration if enabled
  if (showUVInfo.value) {
    drawSkinPenetration(ctx, canvas, 'uva');
  }
};

// UVB rays - made them zigzaggy to show their medium wavelength
const drawUVBRays = (ctx, canvas, intensity) => {
  ctx.strokeStyle = '#FF3300'; // Red for UVB
  ctx.lineWidth = 2;
  
  const sunX = canvas.width * 0.8;
  const sunY = canvas.height * 0.2;
  const humanX = canvas.width * 0.3;
  const humanY = canvas.height * 0.7 - 80;
  
  // Draw simplified rays
  for (let i = 0; i < Math.min(intensity, 5); i++) {
    const offset = (i - 2) * 0.1;
    const startX = sunX;
    const startY = sunY;
    const endX = humanX + offset * 50;
    const endY = humanY;
    
    // Draw zigzag line - these look so cool!
    ctx.beginPath();
    ctx.moveTo(startX, startY);
    
    // Simplified zigzag pattern
    const steps = 10;
    for (let j = 0; j <= steps; j++) {
      const t = j / steps;
      const x = startX + (endX - startX) * t;
      const y = startY + (endY - startY) * t;
      
      // Add sharper zigzag
      const zigzagX = x + (j % 2 === 0 ? 10 : -10);
      ctx.lineTo(zigzagX, y);
    }
    
    ctx.stroke();
  }
  
  // Add simple label
  ctx.fillStyle = '#000';
  ctx.font = 'bold 16px Arial';
  ctx.fillText('UVB: Medium waves - causes sunburn & vitamin D', 20, canvas.height - 20);
  
  // Show skin penetration if enabled
  if (showUVInfo.value) {
    drawSkinPenetration(ctx, canvas, 'uvb');
  }
};

// UVC rays - showing how they're blocked by the ozone layer
const drawUVCRays = (ctx, canvas, intensity) => {
  ctx.strokeStyle = '#9900FF'; // Purple for UVC
  ctx.lineWidth = 2;
  
  const sunX = canvas.width * 0.8;
  const sunY = canvas.height * 0.2;
  
  // Draw atmosphere barrier - this visual really helps explain why UVC doesn't reach us
  ctx.beginPath();
  ctx.arc(sunX - 100, sunY + 50, 80, 0, Math.PI * 2);
  ctx.fillStyle = 'rgba(135, 206, 250, 0.2)';
  ctx.fill();
  ctx.strokeStyle = 'rgba(135, 206, 250, 0.6)';
  ctx.lineWidth = 3;
  ctx.stroke();
  
  // Label for atmosphere
  ctx.fillStyle = '#000';
  ctx.font = 'bold 14px Arial';
  ctx.fillText('Ozone Layer', sunX - 140, sunY + 50);
  
  // Draw rays that stop at atmosphere - showing they don't reach Earth
  for (let i = 0; i < 5; i++) {
    const angle = -Math.PI / 4 + (i - 2) * 0.1;
    const rayLength = 80;
    
    ctx.beginPath();
    ctx.moveTo(sunX, sunY);
    ctx.lineTo(
      sunX + Math.cos(angle) * rayLength,
      sunY + Math.sin(angle) * rayLength
    );
    ctx.stroke();
  }
  
  // Add simple label
  ctx.fillStyle = '#000';
  ctx.font = 'bold 16px Arial';
  ctx.fillText('UVC: Short waves - blocked by ozone layer', 20, canvas.height - 20);
  
  // Show skin penetration if enabled
  if (showUVInfo.value) {
    drawSkinPenetration(ctx, canvas, 'uvc');
  }
};

// Drawing the skin penetration visualization - this really helps people understand!
const drawSkinPenetration = (ctx, canvas, uvType) => {
  // Draw simplified skin layers
  const skinX = canvas.width * 0.7;
  const skinY = canvas.height * 0.5;
  const skinWidth = 120;
  const skinHeight = 100;
  
  // Draw skin layers
  // Epidermis (outer layer)
  ctx.fillStyle = '#F5DEB3';
  ctx.fillRect(skinX, skinY, skinWidth, skinHeight * 0.3);
  ctx.fillStyle = '#000';
  ctx.font = '12px Arial';
  ctx.fillText('Epidermis', skinX + 5, skinY + 20);
  
  // Dermis (middle layer)
  ctx.fillStyle = '#E8C39E';
  ctx.fillRect(skinX, skinY + skinHeight * 0.3, skinWidth, skinHeight * 0.3);
  ctx.fillStyle = '#000';
  ctx.fillText('Dermis', skinX + 5, skinY + skinHeight * 0.3 + 20);
  
  // Hypodermis (deep layer)
  ctx.fillStyle = '#D2B48C';
  ctx.fillRect(skinX, skinY + skinHeight * 0.6, skinWidth, skinHeight * 0.4);
  ctx.fillStyle = '#000';
  ctx.fillText('Hypodermis', skinX + 5, skinY + skinHeight * 0.6 + 20);
  
  // Draw arrows showing penetration
  ctx.lineWidth = 2;
  
  if (uvType === 'uva') {
    // UVA penetrates all layers - this is why it causes aging!
    ctx.strokeStyle = '#FF9900';
    for (let i = 0; i < 3; i++) {
      const x = skinX + 30 + i * 30;
      ctx.beginPath();
      ctx.moveTo(x, skinY - 10);
      ctx.lineTo(x, skinY + skinHeight);
      ctx.stroke();
      
      // Arrow head
      ctx.beginPath();
      ctx.moveTo(x, skinY + skinHeight);
      ctx.lineTo(x - 5, skinY + skinHeight - 10);
      ctx.lineTo(x + 5, skinY + skinHeight - 10);
      ctx.closePath();
      ctx.fill();
    }
  } else if (uvType === 'uvb') {
    // UVB penetrates to dermis - this is why it causes sunburn!
    ctx.strokeStyle = '#FF3300';
    for (let i = 0; i < 3; i++) {
      const x = skinX + 30 + i * 30;
      ctx.beginPath();
      ctx.moveTo(x, skinY - 10);
      ctx.lineTo(x, skinY + skinHeight * 0.6);
      ctx.stroke();
      
      // Arrow head
      ctx.beginPath();
      ctx.moveTo(x, skinY + skinHeight * 0.6);
      ctx.lineTo(x - 5, skinY + skinHeight * 0.6 - 10);
      ctx.lineTo(x + 5, skinY + skinHeight * 0.6 - 10);
      ctx.closePath();
      ctx.fill();
    }
  } else {
    // UVC stopped at epidermis - thankfully we don't have to worry about these!
    ctx.strokeStyle = '#9900FF';
    for (let i = 0; i < 3; i++) {
      const x = skinX + 30 + i * 30;
      ctx.beginPath();
      ctx.moveTo(x, skinY - 10);
      ctx.lineTo(x, skinY + 10);
      ctx.stroke();
      
      // Block symbol
      ctx.beginPath();
      ctx.moveTo(x - 8, skinY + 20);
      ctx.lineTo(x + 8, skinY + 20);
      ctx.lineWidth = 4;
      ctx.stroke();
      ctx.lineWidth = 2;
    }
  }
};

// Tab switching - keeping track of which tab is active
const switchTab = (tab) => {
  activeTab.value = tab;
  
  if (tab === 'uv-types') {
    nextTick(() => {
      startUVAnimation();
    });
  } else {
    stopUVAnimation();
  }
};

// Toggle UV info display - this is a nice interactive feature
const toggleUVInfo = () => {
  showUVInfo.value = !showUVInfo.value;
};

// Watch for changes to UV type or location
// This ensures the animation updates when the user changes settings
watch([currentUVType, currentLocation], () => {
  if (isAnimating.value) {
    // Restart animation when parameters change
    stopUVAnimation();
    nextTick(() => {
      startUVAnimation();
    });
  }
});

// Cleanup on component unmount
onMounted(() => {
  window.addEventListener('resize', handleResize);
  
  // Set initial position to bottom of page
  // This scrolling behavior took me ages to get right!
  requestAnimationFrame(() => {
    // Position at the bottom first
    document.documentElement.style.scrollBehavior = 'auto';
    window.scrollTo(0, document.body.scrollHeight);
    
    // Then scroll to the middle position with smooth behavior
    setTimeout(() => {
      if (mainContent.value) {
        // Get the position of the element
        const rect = mainContent.value.getBoundingClientRect();
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Calculate the middle position of the viewport
        const viewportHeight = window.innerHeight;
        
        // Position the content in the middle of the viewport
        const scrollPosition = rect.top + scrollTop - 50;
        
        // Enable smooth scrolling and scroll to the adjusted position
        document.documentElement.style.scrollBehavior = 'smooth';
        window.scrollTo({
          top: scrollPosition
        });
      }
    }, 600); // Shorter delay since we're already at the bottom
  });
  
  return () => {
    window.removeEventListener('resize', handleResize);
    stopUVAnimation();
  };
});

// Handle window resize - makes sure our canvas animation looks good at any size
const handleResize = () => {
  if (isAnimating.value) {
    // Restart animation on resize
    stopUVAnimation();
    nextTick(() => {
      startUVAnimation();
    });
  }
};

// Simplified Vitamin D animation
// This little animation helps visualize vitamin D production
const vitaminDProgress = ref(0);
const vitaminDInterval = ref(null);

const startVitaminDAnimation = () => {
  // Clear any existing interval
  if (vitaminDInterval.value) {
    clearInterval(vitaminDInterval.value);
  }
  
  // Reset progress
  vitaminDProgress.value = 0;
  
  // Start new animation
  vitaminDInterval.value = setInterval(() => {
    vitaminDProgress.value += 2;
    if (vitaminDProgress.value >= 100) {
      clearInterval(vitaminDInterval.value);
      vitaminDInterval.value = null;
    }
  }, 50);
};

const resetVitaminDAnimation = () => {
  if (vitaminDInterval.value) {
    clearInterval(vitaminDInterval.value);
    vitaminDInterval.value = null;
  }
  vitaminDProgress.value = 0;
};

// Watch for tab changes to handle animations
// This ensures animations start and stop at the right times
watch(activeTab, (newTab, oldTab) => {
  if (newTab === 'vitamin-d') {
    startVitaminDAnimation();
  } else if (oldTab === 'vitamin-d') {
    resetVitaminDAnimation();
  }
});
</script>

<template>
  <div class="resources-page">
    <!-- Background Video - sets the mood for the whole page -->
    <video autoplay loop muted playsinline class="background-video">
      <source :src="backgroundVideo" type="video/mp4" />
    </video>

    <!-- Overlay for better readability - text would be hard to read without this -->
    <div class="overlay"></div>

    <!-- Content -->
    <div class="content" ref="mainContent">
      <!-- SunSense Logo and Header -->
      <div class="header">
        <h1 class="title">Sun Protection Resources</h1>
        <p class="subtitle">Discover essential information about sun safety, UV radiation, and vitamin D</p>
      </div>

      <!-- Navigation Tabs - I love how these tabs turned out! -->
      <div class="tabs">
        <button 
          @click="switchTab('resources')" 
          :class="{ active: activeTab === 'resources' }"
          class="tab-button"
        >
          <span class="tab-icon">📚</span>
          <span>Resources</span>
        </button>
        <button 
          @click="switchTab('uv-types')" 
          :class="{ active: activeTab === 'uv-types' }"
          class="tab-button"
        >
          <span class="tab-icon">☀️</span>
          <span>UV Types</span>
        </button>
        <button 
          @click="switchTab('vitamin-d')" 
          :class="{ active: activeTab === 'vitamin-d' }"
          class="tab-button"
        >
          <span class="tab-icon">💊</span>
          <span>Vitamin D</span>
        </button>
      </div>

      <!-- Resources Tab Content -->
      <div v-if="activeTab === 'resources'" class="tab-content resources-tab">
        <h2>Trusted Sun Protection Resources</h2>
        <p class="tab-description">
          These organizations provide valuable information about sun safety, UV protection, 
          and skin cancer prevention. Click on any card to visit their website.
        </p>

        <div class="resources-container">
          <div 
            v-for="resource in resources" 
            :key="resource.name" 
            class="resource-card"
            @click="window.open(resource.url, '_blank')"
            :style="{ borderTop: `5px solid ${resource.color}` }"
          >
            <div class="card-content">
              <!-- Animated icon instead of logo - these animations are so fun! -->
              <div 
                class="resource-icon-container" 
                :class="resource.animationClass"
                :style="{ backgroundColor: resource.color }"
              >
                <span class="resource-icon">{{ resource.icon }}</span>
              </div>
              
              <h3>{{ resource.name }}</h3>
              <p>{{ resource.description }}</p>
              <a 
                :href="resource.url" 
                target="_blank" 
                class="visit-button" 
                :style="{ backgroundColor: resource.color }"
              >
                Visit Website
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- UV Types Tab Content - Simplified -->
      <div v-if="activeTab === 'uv-types'" class="tab-content uv-tab">
        <h2>Understanding UV Radiation in Australia</h2>
        <p class="tab-description">
          Australia experiences some of the highest UV levels in the world. Learn about the different 
          types of UV radiation and how they affect your skin.
        </p>

        <!-- Controls for the UV animation - makes it interactive! -->
        <div class="uv-controls">
          <div class="control-group">
            <label>UV Type:</label>
            <div class="button-group">
              <button 
                @click="currentUVType = 'uva'" 
                :class="{ active: currentUVType === 'uva' }"
                class="control-button uva"
              >
                UVA
              </button>
              <button 
                @click="currentUVType = 'uvb'" 
                :class="{ active: currentUVType === 'uvb' }"
                class="control-button uvb"
              >
                UVB
              </button>
              <button 
                @click="currentUVType = 'uvc'" 
                :class="{ active: currentUVType === 'uvc' }"
                class="control-button uvc"
              >
                UVC
              </button>
            </div>
          </div>
          
          <div class="control-group">
            <label>Location:</label>
            <select v-model="currentLocation" class="location-select">
              <option v-for="location in locations" :key="location.id" :value="location.id">
                {{ location.name }}
              </option>
            </select>
          </div>
          
          <div class="control-group">
            <button @click="toggleUVInfo" class="info-button">
              {{ showUVInfo ? 'Hide Skin Penetration' : 'Show Skin Penetration' }}
            </button>
          </div>
        </div>

        <!-- Canvas animation container - where the magic happens! -->
        <div class="animation-container">
          <canvas id="uvCanvas" width="800" height="400"></canvas>
        </div>

        <!-- UV meter showing current levels -->
        <div class="uv-info-panel">
          <div class="uv-meter">
            <div class="meter-label">{{ currentUVType.toUpperCase() }} Level in {{ currentLocationData.name }}:</div>
            <div class="meter-bar">
              <div 
                class="meter-fill" 
                :style="{ 
                  width: `${currentUVType === 'uva' ? currentLocationData.uva * 10 : 
                          currentUVType === 'uvb' ? currentLocationData.uvb * 10 : 
                          currentLocationData.uvc * 10}%`,
                  backgroundColor: currentUVType === 'uva' ? '#FF9900' : 
                                  currentUVType === 'uvb' ? '#FF3300' : '#9900FF'
                }"
              ></div>
            </div>
            <div class="meter-value">
              {{ currentUVType === 'uva' ? currentLocationData.uva : 
                 currentUVType === 'uvb' ? currentLocationData.uvb : 
                 currentLocationData.uvc }}/10
            </div>
          </div>
        </div>

        <!-- Simplified UV Info Cards - these provide the key facts -->
        <div class="uv-info-cards">
          <div v-if="currentUVType === 'uva'" class="uv-card uva">
            <h3>UVA (Ultraviolet A)</h3>
            <div class="uv-card-content">
              <div class="uv-key-points">
                <div class="key-point">
                  <div class="point-label">Wavelength:</div>
                  <div class="point-value">315-400 nm (long waves)</div>
                </div>
                <div class="key-point">
                  <div class="point-label">Penetration:</div>
                  <div class="point-value">Deep into skin layers</div>
                </div>
                <div class="key-point">
                  <div class="point-label">Effects:</div>
                  <div class="point-value">Skin aging, wrinkles, contributes to skin cancer</div>
                </div>
                <div class="key-point">
                  <div class="point-label">Present:</div>
                  <div class="point-value">Year-round, even on cloudy days</div>
                </div>
              </div>
              <div class="uv-tip">
                <strong>Tip:</strong> UVA passes through glass, so protect skin even when indoors or in vehicles.
              </div>
            </div>
          </div>
          
          <div v-if="currentUVType === 'uvb'" class="uv-card uvb">
            <h3>UVB (Ultraviolet B)</h3>
            <div class="uv-card-content">
              <div class="uv-key-points">
                <div class="key-point">
                  <div class="point-label">Wavelength:</div>
                  <div class="point-value">280-315 nm (medium waves)</div>
                </div>
                <div class="key-point">
                  <div class="point-label">Penetration:</div>
                  <div class="point-value">Outer skin layers</div>
                </div>
                <div class="key-point">
                  <div class="point-label">Effects:</div>
                  <div class="point-value">Sunburn, tanning, vitamin D production</div>
                </div>
                <div class="key-point">
                  <div class="point-label">Present:</div>
                  <div class="point-value">Strongest 10am-4pm and during summer</div>
                </div>
              </div>
              <div class="uv-tip">
                <strong>Tip:</strong> UVB is responsible for vitamin D production, but also causes sunburn. Balance is key.
              </div>
            </div>
          </div>
          
          <div v-if="currentUVType === 'uvc'" class="uv-card uvc">
            <h3>UVC (Ultraviolet C)</h3>
            <div class="uv-card-content">
              <div class="uv-key-points">
                <div class="key-point">
                  <div class="point-label">Wavelength:</div>
                  <div class="point-value">100-280 nm (short waves)</div>
                </div>
                <div class="key-point">
                  <div class="point-label">Penetration:</div>
                  <div class="point-value">Blocked by the ozone layer</div>
                </div>
                <div class="key-point">
                  <div class="point-label">Effects:</div>
                  <div class="point-value">Most harmful, can damage DNA</div>
                </div>
                <div class="key-point">
                  <div class="point-label">Present:</div>
                  <div class="point-value">Not naturally present at Earth's surface</div>
                </div>
              </div>
              <div class="uv-tip">
                <strong>Tip:</strong> UVC is used in some sterilization devices. Never expose skin or eyes to artificial UVC sources.
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Vitamin D Tab Content - Simplified -->
      <div v-if="activeTab === 'vitamin-d'" class="tab-content vitamin-d-tab">
        <h2>Vitamin D & Sun Exposure</h2>
        <p class="tab-description">
          Learn how your body produces vitamin D from sunlight and find the right balance for your skin type.
        </p>

        <div class="vitamin-d-container">
          <!-- Simple Animation - I love how this visualizes the process! -->
          <div class="animation-box">
            <div class="sun-icon">☀️</div>
            <div class="human-figure">
              <div class="head"></div>
              <div class="body"></div>
              <div class="arms"></div>
              <div class="legs"></div>
              
              <!-- Vitamin D particles that appear during animation -->
              <div class="vitamin-particles">
                <div 
                  v-for="n in 5" 
                  :key="n" 
                  class="particle"
                  :class="{ active: vitaminDProgress >= n * 20 }"
                >D</div>
              </div>
            </div>
            
            <!-- Simple progress indicator -->
            <div class="progress-container">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: `${vitaminDProgress}%` }"></div>
              </div>
              <button @click="startVitaminDAnimation" class="play-button">
                <span v-if="!vitaminDInterval">▶ Play</span>
                <span v-else>⟳ Restart</span>
              </button>
            </div>
          </div>

          <!-- Key Information - personalized for different skin types -->
          <div class="info-box">
            <h3>How Much Sun Do You Need?</h3>
            
            <!-- Simplified skin type selector -->
            <div class="skin-selector">
              <div class="selector-label">Select your skin type:</div>
              <div class="skin-options">
                <button 
                  v-for="skin in skinTypes" 
                  :key="skin.type" 
                  @click="selectedSkinType = skin.type"
                  :class="{ active: selectedSkinType === skin.type }"
                  class="skin-button"
                >
                  <span 
                    class="skin-color" 
                    :style="{ backgroundColor: skin.color }"
                  ></span>
                  <span>{{ skin.name }}</span>
                </button>
              </div>
            </div>
            
            <!-- Simplified recommendation card -->
            <div class="recommendation-card">
              <div class="card-header">Recommended Sun Exposure</div>
              <div class="recommendation-content">
                <div class="season-box">
                  <div class="season-icon">☀️</div>
                  <div class="season-label">Summer</div>
                  <div class="time-value">{{ getCurrentSkinType.summer }}</div>
                </div>
                <div class="season-box">
                  <div class="season-icon">❄️</div>
                  <div class="season-label">Winter</div>
                  <div class="time-value">{{ getCurrentSkinType.winter }}</div>
                </div>
              </div>
              <div class="recommendation-note">
                {{ getCurrentSkinType.note }}
              </div>
            </div>
          </div>
        </div>
        
        <!-- Quick Tips Section - easy to remember advice -->
        <div class="quick-tips">
          <h3>Quick Tips for Vitamin D</h3>
          <div class="tips-container">
            <div class="tip-card">
              <div class="tip-icon">⏱️</div>
              <div class="tip-text">Short, regular exposure is better than long sessions</div>
            </div>
            <div class="tip-card">
              <div class="tip-icon">👕</div>
              <div class="tip-text">Expose arms, legs or back for efficient vitamin D production</div>
            </div>
            <div class="tip-card">
              <div class="tip-icon">🕙</div>
              <div class="tip-text">Morning or late afternoon sun is safer than midday</div>
            </div>
            <div class="tip-card">
              <div class="tip-icon">💊</div>
              <div class="tip-text">Consider supplements during winter or if you have limited sun exposure</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Page Layout */
.resources-page {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 40px 20px;
  min-height: 100vh;
  font-family: 'Arial', sans-serif;
}

/* Background Video - sets the mood for the whole page */
.background-video {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: -1;
}

/* Overlay to improve text visibility - crucial for readability! */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6); /* Darker overlay for better readability */
  z-index: -1;
}

/* Main content area - where all our info lives */
.content {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  width: 100%;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

/* Header and Logo */
.header {
  margin-bottom: 30px;
}

/* Title & Subtitle - clean and clear */
.title {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}

.subtitle {
  font-size: 18px;
  color: #666;
  margin-bottom: 30px;
}

/* Tabs - I love how these turned out! */
.tabs {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 30px;
}

.tab-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: #f0f0f0;
  border: none;
  border-radius: 30px;
  font-size: 16px;
  font-weight: bold;
  color: #555;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-button:hover {
  background: #e0e0e0;
  transform: translateY(-2px);
}

.tab-button.active {
  background: #FFB300; /* Sunny yellow for active tab */
  color: white;
  box-shadow: 0 4px 10px rgba(255, 179, 0, 0.3);
}

.tab-icon {
  font-size: 20px;
}

/* Tab Content - clean white background for readability */
.tab-content {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.tab-content h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 15px;
}

.tab-description {
  font-size: 16px;
  color: #666;
  margin-bottom: 30px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

/* Resources Tab - grid layout for the cards */
.resources-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 25px;
}

.resource-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
}

.resource-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.card-content {
  padding: 25px;
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* Resource Icon Animations - these are so fun! */
.resource-icon-container {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.resource-icon {
  font-size: 36px;
  color: white;
}

/* Animation classes - each one has a different feel */
.pulse-animation {
  animation: pulse 2s infinite;
}

.rotate-animation {
  animation: rotate 8s linear infinite;
}

.bounce-animation {
  animation: bounce 2s infinite;
}

.float-animation {
  animation: float 3s ease-in-out infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

@keyframes rotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-10px) rotate(5deg); }
}

.resource-card h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 15px;
}

.resource-card p {
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
  flex-grow: 1;
}

/* Visit Button - nice call to action */
.visit-button {
  display: inline-block;
  padding: 10px 20px;
  background: #0077cc;
  color: white;
  text-decoration: none;
  border-radius: 30px;
  font-weight: bold;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  align-self: center;
}

.visit-button:hover {
  opacity: 0.9;
  transform: scale(1.05);
}

/* UV Types Tab - controls for the interactive animation */
.uv-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
  justify-content: center;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.control-group label {
  font-weight: bold;
  color: #555;
}

.button-group {
  display: flex;
  gap: 5px;
}

.control-button {
  padding: 8px 15px;
  border: none;
  border-radius: 20px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.control-button.uva {
  background: rgba(255, 153, 0, 0.2);
  color: #FF9900;
}

.control-button.uvb {
  background: rgba(255, 51, 0, 0.2);
  color: #FF3300;
}

.control-button.uvc {
  background: rgba(153, 0, 255, 0.2);
  color: #9900FF;
}

.control-button.active {
  background: rgba(0, 0, 0, 0.1);
  transform: scale(1.05);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.location-select {
  padding: 8px 15px;
  border-radius: 20px;
  border: 1px solid #ddd;
  background: white;
  font-size: 14px;
}

.info-button {
  padding: 8px 15px;
  background: #f0f0f0;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.info-button:hover {
  background: #e0e0e0;
}

.animation-container {
  width: 100%;
  margin-bottom: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.1);
}

.uv-info-panel {
  margin-bottom: 20px;
}

.uv-meter {
  display: flex;
  align-items: center;
  gap: 15px;
  background: #f5f5f5;
  padding: 15px;
  border-radius: 10px;
}

.meter-label {
  width: 200px;
  text-align: right;
  font-weight: bold;
  color: #555;
}

.meter-bar {
  flex-grow: 1;
  height: 20px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  overflow: hidden;
}

.meter-fill {
  height: 100%;
  transition: width 0.5s ease, background-color 0.5s ease;
}

.meter-value {
  width: 50px;
  text-align: left;
  font-weight: bold;
  color: #555;
}

/* Simplified UV Info Cards - color-coded for each type */
.uv-info-cards {
  margin-top: 30px;
}

.uv-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.uv-card h3 {
  padding: 15px;
  margin: 0;
  color: white;
  font-size: 20px;
}

.uv-card.uva h3 {
  background: #FF9900; /* Orange for UVA */
}

.uv-card.uvb h3 {
  background: #FF3300; /* Red for UVB */
}

.uv-card.uvc h3 {
  background: #9900FF; /* Purple for UVC */
}

.uv-card-content {
  padding: 20px;
}

.uv-key-points {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.key-point {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.point-label {
  font-weight: bold;
  color: #555;
}

.point-value {
  color: #666;
}

.uv-tip {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 10px;
  font-size: 14px;
  color: #555;
}

/* Vitamin D Tab - Simplified animation and info */
.vitamin-d-container {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  margin-bottom: 30px;
  justify-content: center;
}

/* Animation Box - this was fun to create! */
.animation-box {
  flex: 1;
  min-width: 280px;
  max-width: 400px;
  height: 350px;
  background: linear-gradient(to bottom, #87CEEB, #E0F7FA);
  border-radius: 15px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.sun-icon {
  position: absolute;
  top: 30px;
  right: 50px;
  font-size: 60px;
  animation: sun-pulse 3s infinite alternate;
}

@keyframes sun-pulse {
  0% { transform: scale(1); opacity: 0.8; }
  100% { transform: scale(1.2); opacity: 1; }
}

.human-figure {
  position: absolute;
  bottom: 100px;
  left: 50%;
  transform: translateX(-50%);
  height: 150px;
  width: 60px;
}

.head {
  width: 30px;
  height: 30px;
  background: #F5DEB3;
  border-radius: 50%;
  position: absolute;
  top: 0;
  left: 15px;
}

.body {
  width: 40px;
  height: 60px;
  background: #F5DEB3;
  border-radius: 8px;
  position: absolute;
  top: 30px;
  left: 10px;
}

.arms {
  width: 60px;
  height: 10px;
  background: #F5DEB3;
  border-radius: 5px;
  position: absolute;
  top: 50px;
  left: 0;
}

.legs {
  width: 40px;
  height: 50px;
  background: #F5DEB3;
  border-radius: 8px 8px 0 0;
  position: absolute;
  top: 90px;
  left: 10px;
}

.vitamin-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  width: 25px;
  height: 25px;
  background: #FFD700;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: white;
  opacity: 0;
  transition: all 0.5s ease;
}

.particle.active {
  opacity: 1;
}

.particle:nth-child(1) { top: 40%; left: 30%; }
.particle:nth-child(2) { top: 30%; left: 60%; }
.particle:nth-child(3) { top: 60%; left: 40%; }
.particle:nth-child(4) { top: 50%; left: 70%; }
.particle:nth-child(5) { top: 70%; left: 60%; }

.progress-container {
  position: absolute;
  bottom: 20px;
  left: 0;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.progress-bar {
  width: 80%;
  height: 10px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 5px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #FFD700, #FFA500);
  transition: width 0.1s linear;
}

.play-button {
  padding: 8px 20px;
  background: #0077cc;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.play-button:hover {
  background: #005fa3;
  transform: scale(1.05);
}

/* Info Box - personalized recommendations */
.info-box {
  flex: 1;
  min-width: 280px;
  max-width: 400px;
  background: #f9f9f9;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.info-box h3 {
  color: #333;
  margin-bottom: 20px;
  font-size: 20px;
  text-align: center;
}

.skin-selector {
  margin-bottom: 25px;
}

.selector-label {
  font-weight: bold;
  margin-bottom: 10px;
  color: #555;
}

.skin-options {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.skin-button {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  padding: 10px;
  background: white;
  border: 2px solid #eee;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.skin-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
}

.skin-button.active {
  border-color: #FFB300;
  background: rgba(255, 179, 0, 0.1);
}

.skin-color {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  border: 1px solid #ddd;
}

.recommendation-card {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.card-header {
  background: #FFB300;
  color: white;
  padding: 12px;
  font-weight: bold;
  text-align: center;
}

.recommendation-content {
  display: flex;
  padding: 15px;
}

.season-box {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  padding: 10px;
}

.season-icon {
  font-size: 24px;
}

.season-label {
  font-weight: bold;
  color: #555;
}

.time-value {
  font-size: 18px;
  color: #0077cc;
  font-weight: bold;
}

.recommendation-note {
  padding: 15px;
  background: #f5f5f5;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

/* Quick Tips Section - easy to remember advice */
.quick-tips {
  margin-top: 30px;
}

.quick-tips h3 {
  color: #333;
  margin-bottom: 20px;
  font-size: 20px;
  text-align: center;
}

.tips-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.tip-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
}

.tip-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
}

.tip-icon {
  font-size: 30px;
}

.tip-text {
  text-align: center;
  color: #555;
  font-size: 14px;
  line-height: 1.4;
}

/* Mobile Responsive - looks great on all devices! */
@media screen and (max-width: 768px) {
  .content {
    padding: 20px;
  }
  
  .tabs {
    flex-direction: column;
    gap: 10px;
  }
  
  .uv-controls {
    flex-direction: column;
    align-items: center;
  }
  
  .vitamin-d-container {
    flex-direction: column;
    align-items: center;
  }
  
  .animation-box, .info-box {
    max-width: 100%;
  }
  
  .uv-key-points {
    grid-template-columns: 1fr;
  }
}

@media screen and (max-width: 480px) {
  .title {
    font-size: 24px;
  }
  
  .subtitle {
    font-size: 16px;
  }
  
  .tab-content {
    padding: 15px;
  }
  
  .skin-options {
    flex-direction: column;
  }
  
  .recommendation-content {
    flex-direction: column;
  }
  
  .season-box {
    padding: 5px;
  }
  
  .tips-container {
    grid-template-columns: 1fr;
  }
}
</style>