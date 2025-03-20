<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

// Track the cursor position with reactive refs
// I love using refs for this - makes the template so clean!
const cursorX = ref(0);
const cursorY = ref(0);
const isVisible = ref(false);
const isClicking = ref(false);

// Track mouse position - the heart of our custom cursor
// This was tricky to get right with the offset calculations
const updateCursorPosition = (e) => {
  cursorX.value = e.clientX;
  cursorY.value = e.clientY;
  
  // Show cursor after first movement - this prevents that awkward flash at page load
  // Took me forever to figure out why the cursor was jumping around at first!
  if (!isVisible.value) {
    isVisible.value = true;
  }
};

// Track mouse clicks - gives that satisfying "squish" effect
// Users love these little details that make the app feel alive
const handleMouseDown = () => {
  isClicking.value = true;
};

const handleMouseUp = () => {
  isClicking.value = false;
};

// Setup and cleanup event listeners
// Always clean up your listeners - learned that the hard way with memory leaks!
onMounted(() => {
  document.addEventListener('mousemove', updateCursorPosition);
  document.addEventListener('mousedown', handleMouseDown);
  document.addEventListener('mouseup', handleMouseUp);
  
  // Hide default cursor - this was a "duh" moment when I realized I needed this
  // Otherwise you get both cursors showing at once - not a good look!
  document.body.style.cursor = 'none';
});

onUnmounted(() => {
  // Clean up all our listeners when component is destroyed
  // This prevents memory leaks - so important for performance
  document.removeEventListener('mousemove', updateCursorPosition);
  document.removeEventListener('mousedown', handleMouseDown);
  document.removeEventListener('mouseup', handleMouseUp);
  
  // Restore default cursor - don't want to leave users cursor-less!
  document.body.style.cursor = 'auto';
});
</script>

<template>
  <div 
    class="sun-cursor" 
    :class="{ 'visible': isVisible, 'clicking': isClicking }"
    :style="{ 
      left: `${cursorX}px`, 
      top: `${cursorY}px` 
    }"
  >
    <!-- Sun rays - these rotate around to create that sunny effect -->
    <!-- I spent way too long getting these rays to look just right! -->
    <div class="rays">
      <div class="ray ray-1"></div>
      <div class="ray ray-2"></div>
      <div class="ray ray-3"></div>
      <div class="ray ray-4"></div>
      <div class="ray ray-5"></div>
      <div class="ray ray-6"></div>
      <div class="ray ray-7"></div>
      <div class="ray ray-8"></div>
    </div>
    
    <!-- Sun core - the main circle of our sun cursor -->
    <!-- The glow effect really makes it pop against any background -->
    <div class="sun-core"></div>
  </div>
</template>

<style scoped>
/* Main cursor container - follows the mouse around */
/* Using fixed positioning with transform for perfect centering */
.sun-cursor {
  position: fixed;
  pointer-events: none; /* Super important! Otherwise it blocks clicks on elements beneath */
  z-index: 9999; /* Keep it above everything else */
  transform: translate(-50%, -50%); /* Center the cursor on the actual pointer position */
  transition: opacity 0.3s ease;
  opacity: 0;
}

/* Only show cursor after first mouse movement - prevents that awkward flash on page load */
.sun-cursor.visible {
  opacity: 1;
}

/* The center of our sun - a bright yellow circle with glow */
/* I tried different sizes and settled on 20px - looks good without being too distracting */
.sun-core {
  width: 20px;
  height: 20px;
  background: #ffcc00; /* Sunny yellow! */
  border-radius: 50%;
  box-shadow: 0 0 15px rgba(255, 204, 0, 0.8); /* This glow effect took some tweaking */
  position: relative;
  z-index: 2; /* Keep the core above the rays */
}

/* Container for all the sun rays - this is what rotates */
/* Using absolute positioning to center it perfectly */
.rays {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  animation: rotate 8s linear infinite; /* Smooth, continuous rotation */
}

/* Individual sun rays - positioned around the core */
/* I tried different lengths and widths before settling on these values */
.ray {
  position: absolute;
  background: #ffcc00;
  width: 4px;
  height: 16px;
  border-radius: 2px; /* Slightly rounded edges look nicer than sharp ones */
  left: 8px; /* Center horizontally */
  top: -14px; /* Position above the core */
  transform-origin: center 24px; /* This is the magic that makes them rotate around the center */
}

/* Position each ray at 45-degree intervals */
/* Could have used a loop in SCSS, but keeping it simple with CSS */
.ray-1 { transform: rotate(0deg); }
.ray-2 { transform: rotate(45deg); }
.ray-3 { transform: rotate(90deg); }
.ray-4 { transform: rotate(135deg); }
.ray-5 { transform: rotate(180deg); }
.ray-6 { transform: rotate(225deg); }
.ray-7 { transform: rotate(270deg); }
.ray-8 { transform: rotate(315deg); }

/* Animation for rays rotation - smooth and continuous */
/* I tried different speeds - 8s feels right, not too fast or slow */
@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); } /* Full circle rotation */
}

/* Click effect - sun gets smaller and changes color when clicking */
/* This gives great visual feedback to the user - feels so satisfying! */
.sun-cursor.clicking .sun-core {
  transform: scale(0.8); /* Shrink slightly */
  background: #ff9900; /* Darker orange when clicking */
  box-shadow: 0 0 20px rgba(255, 153, 0, 0.9); /* Stronger glow */
}

/* Speed up the rotation when clicking - adds to the energy */
.sun-cursor.clicking .rays {
  animation-duration: 4s; /* Twice as fast when clicking */
}
</style>