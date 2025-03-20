<template>
  <!-- Only show the header when we're not on the home page -->
  <!-- I debated showing it everywhere, but it looks cleaner this way -->
  <header v-if="!isHomePage" class="top-header">
    <h1 class="main-title">
      <span class="title-text">
        <!-- I love how we split the name to highlight just the "Sense" part -->
        Sun<span class="highlight">Sense</span>
        <!-- This little sun icon adds so much character! -->
        <span class="sun-icon">☀️</span>
      </span>
    </h1>
  </header>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

// Get the current route so we can check if we're on the home page
const route = useRoute();

// Determine if we're on the home page - we don't want the header there
// since the home page already has the big logo front and center
const isHomePage = computed(() => {
  // I'm checking both path and name just to be safe
  // Had a bug once where only checking path didn't work with base URLs
  return route.path === '/' || route.name === 'home';
});
</script>

<style scoped>
/* Fixed header that stays at the top as you scroll */
/* The semi-transparent background looks so much better than solid! */
.top-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: rgba(0, 0, 0, 0.5); /* Just enough opacity to read text over any content */
  padding: 10px 20px;
  z-index: 100; /* Keep it above everything else */
  display: flex;
  justify-content: center;
}

/* Center the title - looks more balanced this way */
.main-title {
  display: flex;
  justify-content: center;
  margin: 0;
}

/* The title text styling - spent ages getting this just right! */
.title-text {
  font-size: 2rem;
  font-weight: 300; /* Lighter weight looks more elegant */
  color: white;
  letter-spacing: 0.2em; /* Spaced out letters for that premium feel */
  text-shadow: 2px 2px 15px rgba(0, 0, 0, 0.6); /* Subtle shadow helps it pop */
  font-family: 'Times New Roman', serif; /* Classic font for a trustworthy feel */
  position: relative;
  display: inline-flex;
  align-items: center;
}

/* The sun icon - small but mighty! */
/* Positioning it slightly up gives it that playful floating look */
.sun-icon {
  font-size: 1.2rem;
  margin-left: 0.5rem;
  filter: drop-shadow(0 0 10px rgba(255, 204, 0, 0.7)); /* Subtle glow effect */
  position: relative;
  top: -0.5rem; /* Nudge it up a bit - looks like it's rising! */
}

/* The gradient text effect for "Sense" - this was tricky to get right! */
/* Had to try several color combinations before finding this perfect sunny gradient */
.highlight {
  background: linear-gradient(90deg, #ffcc00, #ff9500); /* Sunny yellow-orange gradient */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 400; /* Slightly bolder than the rest of the title */
}

/* Mobile adjustments - smaller text on small screens */
/* Always test on mobile! So many people forget this step */
@media (max-width: 480px) {
  .title-text {
    font-size: 1.5rem; /* Smaller but still readable */
  }
  
  .sun-icon {
    font-size: 1rem; /* Keep the sun proportional */
  }
}
</style>