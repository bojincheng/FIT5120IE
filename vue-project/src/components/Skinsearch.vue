<script setup>
import { ref } from "vue";
import backgroundVideo from "@/assets/protection.mp4";

// Skin types with enhanced recommendations
const skinTones = ref([
  {
    color: "#F2E2DF",
    label: "Very Fair",
    shortAdvice: "SPF 50+, avoid midday sun.",
    fullAdvice: "Very fair skin is extremely sensitive to UV exposure. Always use SPF 50+, wear UPF-rated clothing, and avoid direct sun between 10 AM - 4 PM.",
    healthRisk: "⚠️ High risk of sunburn, premature aging, and skin cancer.",
    vitaminD: "🌞 Requires more Vitamin D synthesis. Safe sun exposure: ~10-15 min before 10 AM or after 3 PM.",
    sunscreenUsage: "💧 Use ~1 teaspoon of SPF 50+ for face and neck, reapply every 2 hours."
  },
  {
    color: "#E6DCCA",
    label: "Fair",
    shortAdvice: "SPF 50+, reapply every 2 hours.",
    fullAdvice: "Fair skin is prone to sunburn. Apply SPF 50+ every 2 hours, wear a hat and sunglasses, and seek shade during peak hours.",
    healthRisk: "⚠️ High risk of sunburn, moderate risk of hyperpigmentation and skin cancer.",
    vitaminD: "🌤️ Safe sun exposure: ~10-15 min in the morning/evening.",
    sunscreenUsage: "💧 Use ~1.5 teaspoons of SPF 50+ for face, neck, and arms."
  },
  {
    color: "#E8D597",
    label: "Light",
    shortAdvice: "SPF 30+, wear sunglasses.",
    fullAdvice: "Light skin requires moderate protection. Apply SPF 30+, wear sunglasses, and limit direct exposure to intense sunlight.",
    healthRisk: "⚠️ Moderate risk of sunburn, sunspots, and wrinkles with frequent unprotected exposure.",
    vitaminD: "🌞 Can generate Vitamin D efficiently. Safe sun exposure: ~15-20 min.",
    sunscreenUsage: "💧 Use ~2 teaspoons of SPF 30+ for upper body protection."
  },
  {
    color: "#E2B8A1",
    label: "Medium",
    shortAdvice: "SPF 30+, seek shade at midday.",
    fullAdvice: "Medium skin tones can tolerate more sunlight but still need SPF 30+, especially around midday when UV levels are high.",
    healthRisk: "⚠️ Lower sunburn risk but prone to uneven pigmentation and premature aging.",
    vitaminD: "🌤️ Safe sun exposure: ~20 min for optimal Vitamin D levels.",
    sunscreenUsage: "💧 Use ~3 teaspoons of SPF 30+ for full upper body coverage."
  },
  {
    color: "#B49068",
    label: "Tan",
    shortAdvice: "SPF 30, wear a hat.",
    fullAdvice: "Tan skin tones have more melanin protection but should still use SPF 30 and protective clothing.",
    healthRisk: "⚠️ Less prone to sunburn but at risk of long-term pigmentation changes and premature aging.",
    vitaminD: "🌞 Requires ~25-30 min of sun exposure for Vitamin D synthesis.",
    sunscreenUsage: "💧 Use ~4 teaspoons of SPF 30+ for full-body protection."
  },
  {
    color: "#3E3633",
    label: "Dark",
    shortAdvice: "SPF 15+, avoid long exposure.",
    fullAdvice: "Dark skin has a lower risk of sunburn but still needs SPF 15+ to prevent long-term damage.",
    healthRisk: "⚠️ Low sunburn risk but at increased risk of Vitamin D deficiency.",
    vitaminD: "🌞 Requires ~30-45 min of sun exposure for adequate Vitamin D synthesis.",
    sunscreenUsage: "💧 Use ~6 teaspoons (2 tablespoons) of SPF 15+ for full-body protection."
  }
]);

const selectedSkin = ref(null);
const showModal = ref(false);

// Show full suggestions in a modal
const openModal = (skin) => {
  selectedSkin.value = skin;
  showModal.value = true;
};

// Close modal
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
        <p><strong>🌞 Sun Protection Advice:</strong> {{ selectedSkin.fullAdvice }}</p>
        <p><strong>⚠️ Health Risks:</strong> {{ selectedSkin.healthRisk }}</p>
        <p><strong>🌤️ Vitamin D Guidance:</strong> {{ selectedSkin.vitaminD }}</p>
        <p><strong>💧 Sunscreen Usage:</strong> {{ selectedSkin.sunscreenUsage }}</p>
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
</style>
