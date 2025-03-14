<script setup>
import { ref } from "vue";
import backgroundVideo from "@/assets/bg.mp4";

// Skin types
const skinTones = ref([
  { color: "#F2E2DF", label: "Very Fair", shortAdvice: "Use SPF 50+, avoid midday sun.", fullAdvice: "Very fair skin is highly sensitive to UV exposure. Apply SPF 50+ sunscreen, wear long sleeves, and avoid direct sun between 10 AM - 4 PM." },
  { color: "#E6DCCA", label: "Fair", shortAdvice: "Use SPF 50+, reapply every 2 hours.", fullAdvice: "Fair skin is prone to sunburn. Apply SPF 50+ every 2 hours, wear a hat and sunglasses, and seek shade during peak hours." },
  { color: "#E8D597", label: "Light", shortAdvice: "Use SPF 30+, wear sunglasses.", fullAdvice: "Light skin requires moderate protection. Apply SPF 30+, wear sunglasses, and limit direct exposure to intense sunlight." },
  { color: "#E2B8A1", label: "Medium", shortAdvice: "SPF 30+, seek shade at midday.", fullAdvice: "Medium skin tones can tolerate more sunlight but still need SPF 30+, especially around midday when UV levels are high." },
  { color: "#B49068", label: "Tan", shortAdvice: "SPF 30, wear a hat.", fullAdvice: "Tan skin tones have more melanin protection but should still use SPF 30 and protective clothing." },
  { color: "#3E3633", label: "Dark", shortAdvice: "SPF 15+, avoid long exposure.", fullAdvice: "Dark skin has a lower risk of sunburn but still needs SPF 15+ to prevent long-term damage." }
]);

const selectedSkin = ref(null); // get skin type
const showModal = ref(false); // show modal

// Show full suggestions
const openModal = (skin) => {
  selectedSkin.value = skin;
  showModal.value = true;
};

// Close the modal
const closeModal = () => {
  showModal.value = false;
  selectedSkin.value = null;
};
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
        @mouseenter="selectedSkin = tone"
        @mouseleave="selectedSkin = null"
        @click="openModal(tone)"
      >
        <!-- Tooltip below the skin tone -->
        <div v-if="selectedSkin === tone" class="tooltip">
          <strong>{{ tone.label }}</strong><br />
          {{ tone.shortAdvice }}
        </div>
      </div>
    </div>

    <!-- Modal (Popup) for Full Advice -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h3>{{ selectedSkin.label }}</h3>
        <p>{{ selectedSkin.fullAdvice }}</p>
        <button @click="closeModal">Close</button>
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
  top: 60px;
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

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

/* Modal Content */
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  max-width: 400px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
}

.modal-content h3 {
  font-size: 20px;
  margin-bottom: 10px;
}

.modal-content p {
  font-size: 16px;
  margin-bottom: 20px;
}

.modal-content button {
  padding: 10px 15px;
  font-size: 16px;
  background-color: #ff6600;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.modal-content button:hover {
  background-color: #e65c00;
}
</style>
