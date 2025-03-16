<script setup>
import backgroundVideo from "@/assets/Front_Page.mp4"; // Import video
import { useRouter } from "vue-router";

const router = useRouter();

// Navigate to specific pages
const goToUVSearch = () => {
  router.push("/UVSearch");
};

const goToSkinSearch = () => {
  router.push("/SkinSearch");
};
</script>

<template>
  <div class="homepage">
    <!-- Background Video -->
    <video autoplay loop muted class="background-video">
      <source :src="backgroundVideo" type="video/mp4" />
    </video>

    <!-- Website Title -->
    <h1 class="fade-in">Welcome to SunSense</h1>

    <!-- UV Search Section -->
    <div class="section-container">
      <div class="section-content">
        <h2>Searching for the UV Index Level</h2>
        <p>Find out the UV levels in your location and get recommendations to protect your skin.</p>
        <button @click="goToUVSearch">Search now!</button>
      </div>
      <img src="@/assets/uv-search.jpeg" alt="UV Search" class="section-image" />
    </div>

    <!-- Skin Search Section -->
    <div class="section-container reverse">
      <img src="@/assets/skin-search.jpeg" alt="Skin Search" class="section-image" />
      <div class="section-content">
        <h2>Personalized Sun Safety Plan</h2>
        <p>Discover how your skin type affects sun sensitivity and get a personalized protection plan.</p>
        <button @click="goToSkinSearch">Get your personalized sun safety plan</button>
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

/* Page Layout */
.homepage {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  position: relative;
  z-index: 10;
}

/* Website Title */
.fade-in {
  font-size: 2.5rem;
  color: white;
  text-align: center;
  margin-top: 10vh;
  opacity: 0;
  animation: fadeIn 3s ease-in-out forwards;
  text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.7);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Section Styling */
.section-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.85);
  padding: 20px;
  border-radius: 10px;
  max-width: 800px;
  width: 100%;
  margin: 20px 0;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.reverse {
  flex-direction: row-reverse;
}

/* Section Content */
.section-content {
  flex: 1;
  text-align: left;
  padding: 20px;
}

.section-content h2 {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}

.section-content p {
  font-size: 16px;
  color: #555;
  margin-bottom: 15px;
}

/* Buttons */
button {
  padding: 10px 15px;
  font-size: 16px;
  background-color: black;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease-in-out;
}

button:hover {
  background: #333;
}

/* Section Image */
.section-image {
  width: 200px;
  height: auto;
  border-radius: 10px;
}

/* Responsive Design */
@media screen and (max-width: 600px) {
  .section-container {
    flex-direction: column;
    text-align: center;
    padding: 15px;
  }

  .reverse {
    flex-direction: column;
  }

  .section-content {
    padding: 10px;
  }

  .section-image {
    width: 100%;
    max-width: 300px;
  }
}
</style>
