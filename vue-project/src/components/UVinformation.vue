<script setup>
import backgroundVideo from "@/assets/bg.mp4";

const resources = [
  {
    name: "Cancer Council Australia",
    description: "Official Australian guide to sun protection, skin cancer prevention, and sunscreen recommendations.",
    url: "https://www.cancer.org.au/",
    logo: "https://www.cancer.org.au/assets/img/logo.svg"
  },
  {
    name: "Australian Bureau of Meteorology",
    description: "Check real-time UV index, weather forecasts, and sun exposure warnings across Australia.",
    url: "http://www.bom.gov.au/uv/",
    logo: "https://www.bom.gov.au/images/bom-logo.svg"
  },
  {
    name: "World Health Organization (WHO)",
    description: "Global sun protection guidelines and research on skin cancer prevention.",
    url: "https://www.who.int/news-room/questions-and-answers/item/radiation-the-ultraviolet-(uv)-index",
    logo: "https://www.who.int/Images/Logo.svg"
  },
  {
    name: "SunSmart",
    description: "Practical sun safety tips, including the 'Slip, Slop, Slap' campaign for UV protection.",
    url: "https://www.sunsmart.com.au/",
    logo: "https://www.sunsmart.com.au/images/logo.png"
  }
];
</script>

<template>
  <div class="resources-page">
    <!-- Background Video -->
    <video autoplay loop muted playsinline class="background-video">
      <source :src="backgroundVideo" type="video/mp4" />
    </video>

    <!-- Overlay for better readability -->
    <div class="overlay"></div>

    <!-- Content -->
    <div class="content">
      <h2 class="title">🌞 Sun Protection Resources</h2>
      <p class="subtitle">Here are some trusted websites that provide essential sun safety guidelines:</p>

      <div class="resources-container">
        <div v-for="resource in resources" :key="resource.name" class="resource-card">
          <img :src="resource.logo" :alt="resource.name" class="resource-logo" />
          <h3>{{ resource.name }}</h3>
          <p>{{ resource.description }}</p>
          <a :href="resource.url" target="_blank" class="visit-button">Visit Website</a>
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
}

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

/* Overlay to improve text visibility */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* Semi-transparent dark overlay */
  z-index: -1;
}

/* Main content area */
.content {
  position: relative;
  z-index: 1;
  max-width: 1000px;
}

/* Title & Subtitle */
.title {
  font-size: 26px;
  font-weight: bold;
  margin-bottom: 10px;
  color: white;
}

.subtitle {
  font-size: 18px;
  color: #ddd;
  margin-bottom: 30px;
}

/* Resource Cards */
.resources-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}

.resource-card {
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
  width: 280px;
  transition: transform 0.3s ease-in-out;
}

.resource-card:hover {
  transform: scale(1.05);
}

/* Logo */
.resource-logo {
  width: 80px;
  height: auto;
  margin-bottom: 15px;
}

/* Visit Button */
.visit-button {
  display: inline-block;
  margin-top: 10px;
  padding: 10px 15px;
  background: #0077cc;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: bold;
  transition: background 0.3s ease-in-out;
}

.visit-button:hover {
  background: #005fa3;
}

/* Mobile Responsive */
@media screen and (max-width: 600px) {
  .resources-container {
    flex-direction: column;
    align-items: center;
  }
}
</style>
