<template>
  <div class="main-container">
    <!-- Add Top Header with Logo -->
    <header class="top-header">
      <h1 class="main-title">
        <span class="title-text">
          Sun<span class="highlight">Sense</span>
          <span class="sun-icon">☀️</span>
        </span>
      </h1>
    </header>
    
    <main class="main-box">
      <router-view></router-view> <!-- Loads pages dynamically -->
    </main>
    
    <!-- Bottom Bar Menu -->
    <BHeader />
    
    <!-- Sun Cursor -->
    <SunCursor />
  </div>
</template>

<script setup>
import BHeader from './components/BHeader.vue';
import SunCursor from './components/sun-cursor.vue';
</script>

<style>
/* Global Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  overflow-x: hidden;
}

.main-container {
  min-height: 100vh;
}

.main-box {
  padding-top: 70px; /* Add padding for the top header */
  padding-bottom: 70px; /* Match the height of the bottom nav */
}

/* Logo styling */
.top-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
  padding: 10px 20px;
  z-index: 100;
  display: flex;
  justify-content: center;
}

.main-title {
  display: flex;
  justify-content: center;
  margin: 0;
}

.title-text {
  font-size: 2rem;
  font-weight: 300;
  color: white;
  letter-spacing: 0.2em;
  text-shadow: 2px 2px 15px rgba(0, 0, 0, 0.6);
  font-family: 'Times New Roman', serif;
  position: relative;
  display: inline-flex;
  align-items: center;
}

.sun-icon {
  font-size: 1.2rem;
  margin-left: 0.5rem;
  filter: drop-shadow(0 0 10px rgba(255, 204, 0, 0.7));
  position: relative;
  top: -0.5rem;
}

.highlight {
  background: linear-gradient(90deg, #ffcc00, #ff9500);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 400;
}

@media (max-width: 480px) {
  .main-box {
    padding-top: 60px; /* Responsive padding for top header */
    padding-bottom: 60px; /* Match the responsive height of the bottom nav */
  }
  
  .title-text {
    font-size: 1.5rem;
  }
  
  .sun-icon {
    font-size: 1rem;
  }
}
</style>