<script setup>
import { ref } from "vue";
import backgroundVideo from "@/assets/bg.mp4";

// Skin types
const skinTones = ref([
  { color: "#F2E2DF", label: "Very Fair", advice: "Use SPF 50+, avoid midday sun." },
  { color: "#E6DCCA", label: "Fair", advice: "Use SPF 50+, reapply every 2 hours." },
  { color: "#E8D597", label: "Light", advice: "Use SPF 30+, wear sunglasses." },
  { color: "#E2B8A1", label: "Medium", advice: "SPF 30+, seek shade during peak hours." },
  { color: "#B49068", label: "Tan", advice: "SPF 30, wear a hat and sunglasses." },
  { color: "#3E3633", label: "Dark", advice: "SPF 15+, avoid prolonged exposure." }
]);

// The skin color of the current mouseover
const hoveredSkin = ref(null);
</script>

<template>
  <div class="homepage">
    <!-- Background Video -->
    <video autoplay loop muted playsinline class="background-video">
      <source :src="backgroundVideo" type="video/mp4" />
    </video>

    <!-- Title -->
    <h2 class="title">Which color is more close to your skin?</h2>

    <!-- Skin Tone Selection -->
    <div class="skin-tone-container">
      <div
        v-for="(tone, index) in skinTones"
        :key="index"
        class="skin-circle"
        :style="{ backgroundColor: tone.color }"
        @mouseenter="hoveredSkin = tone"
        @mouseleave="hoveredSkin = null"
      >
        <!-- Tooltip below the color -->
        <div v-if="hoveredSkin === tone" class="tooltip">
          <strong>{{ tone.label }}</strong><br />
          {{ tone.advice }}
        </div>
      </div>
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

/* Centered Container */
.homepage {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  position: relative;
  z-index: 10;
}

/* Title Styling */
.title {
  font-size: 22px;
  font-weight: bold;
  color: white;
  margin-bottom: 15px;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.7);
}

/* Skin Tone Circles */
.skin-tone-container {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.skin-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.3s ease-in-out;
  position: relative;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.4);
}

.skin-circle:hover {
  transform: scale(1.2);
}

/* Tooltip BELOW the skin tone */
.tooltip {
  position: absolute;
  top: 60px; /* Moves tooltip below the circle */
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  white-space: nowrap;
  font-size: 14px;
  text-align: center;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
  pointer-events: none;
}

.skin-circle:hover .tooltip {
  opacity: 1;
}

/* Responsive Design */
@media screen and (max-width: 600px) {
  .skin-tone-container {
    gap: 12px;
  }

  .skin-circle {
    width: 40px;
    height: 40px;
  }

  .tooltip {
    font-size: 12px;
    padding: 6px 10px;
    top: 50px; /* Adjust for smaller screens */
  }
}
</style>
