<script setup>
import backgroundVideo from "../assets/Front_Page.mp4"; // Background video for that eye-catching first impression
import { ref, onMounted } from 'vue';

// Animation state variables - keeping track of what's visible when
const titleVisible = ref(false);
const subtitleVisible = ref(false);
const sloganVisible = ref(false);

// Trigger animations sequentially - creates a nice cascading effect when the page loads
// I love how this staggers the animations rather than having everything appear at once
onMounted(() => {
  // Wait a bit before showing the title - gives the video a moment to start playing
  setTimeout(() => {
    titleVisible.value = true;
    
    // Once the title is visible, wait a bit then show the subtitle
    // This creates a nice flow of information for the user
    setTimeout(() => {
      subtitleVisible.value = true;
      
      // Finally, show the slogan at the bottom
      // The delay here is shorter since the user's attention is already engaged
      setTimeout(() => {
        sloganVisible.value = true;
      }, 800); // Quick enough to not feel like waiting, but slow enough to notice
    }, 600);
  }, 300); // Just enough delay to feel intentional but not slow
});
</script>

<template>
  <div class="homepage">
    <!-- Background Video - sets the mood and grabs attention immediately -->
    <video autoplay loop muted playsinline class="background-video">
      <source :src="backgroundVideo" type="video/mp4" />
    </video>

    <!-- Overlay - makes the text readable against any background video content -->
    <!-- The gradient helps emphasize different parts of the page -->
    <div class="overlay"></div>

    <!-- Main Content - everything the user actually sees and interacts with -->
    <div class="content-container">
      <!-- Title Section - the main focal point when users first arrive -->
      <div class="title-container">
        <h1 
          class="main-title" 
          :class="{ 'visible': titleVisible }"
        >
          <!-- I like how we highlight just the "Sense" part - makes the brand name pop! -->
          <span class="title-text">Sun<span class="highlight">Sense</span></span>
        </h1>
        
        <p 
          class="subtitle" 
          :class="{ 'visible': subtitleVisible }"
        >
          Your personal UV protection companion
        </p>
      </div>
      
      <!-- Slogan at Bottom - reinforces the brand message as users explore -->
      <!-- This appears last to complete the page's story -->
      <div 
        class="slogan-container"
        :class="{ 'visible': sloganVisible }"
      >
        <!-- These decorative lines add a touch of elegance to the slogan -->
        <div class="slogan-line"></div>
        <p class="slogan">Protecting your skin today, for a healthier tomorrow</p>
        <div class="slogan-line"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Background Video - fills the entire viewport for maximum impact */
/* Full-screen video backgrounds really help create an immersive experience */
.background-video {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover; /* This ensures the video covers the whole screen without distortion */
  z-index: -2; /* Behind everything else */
}

/* Overlay for better readability - crucial for text visibility */
/* I spent ages tweaking this gradient to get it just right! */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, 
    rgba(0, 0, 0, 0.5) 0%, /* Darker at top for the title */
    rgba(0, 0, 0, 0.3) 50%, /* Lighter in the middle to see more of the video */
    rgba(0, 0, 0, 0.6) 100% /* Darker at bottom for the slogan */
  );
  z-index: -1; /* Just above the video but below the content */
}

/* Content Layout - organizes everything vertically */
/* Using the full viewport height and spacing things out nicely */
.content-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Pushes title to top and slogan to bottom */
  align-items: center;
  padding: 0 20px 100px; /* Extra bottom padding accounts for the navigation bar */
}

/* Title Section - where the user's eye goes first */
.title-container {
  margin-top: 30vh; /* Positions title about a third of the way down - felt right visually */
  text-align: center;
}

/* Main title with animation - the star of the show */
.main-title {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2.5rem;
  opacity: 0; /* Starts invisible */
  transform: translateY(-30px); /* Starts slightly above final position */
  transition: opacity 1s ease, transform 1s ease; /* Smooth fade and movement */
}

/* When title becomes visible - triggered by JavaScript */
.main-title.visible {
  opacity: 1;
  transform: translateY(0); /* Moves to final position */
}

/* Sun icon - considered adding this but went with text-only for now */
.sun-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  filter: drop-shadow(0 0 10px rgba(255, 204, 0, 0.7)); /* Gives a subtle glow effect */
  animation: pulse 3s infinite alternate; /* Gentle pulsing animation */
}

/* The actual title text - big and bold */
.title-text {
  font-size: 5rem;
  font-weight: 300; /* Lighter weight for elegance */
  color: white;
  letter-spacing: 0.2em; /* Spaced out letters look more premium */
  text-shadow: 2px 2px 15px rgba(0, 0, 0, 0.6); /* Helps text stand out against video */
  font-family: 'Times New Roman', serif; /* Classic font for a trustworthy feel */
}

/* The highlighted part of the title - "Sense" */
/* This gradient text effect took forever to get right but looks so good! */
.highlight {
  background: linear-gradient(90deg, #ffcc00, #ff9500); /* Sunny yellow-orange gradient */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 400; /* Slightly bolder than the rest of the title */
}

/* Subtitle text - provides context about the app */
.subtitle {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.9); /* Slightly transparent white */
  max-width: 600px;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.6);
  opacity: 0;
  transform: translateY(20px); /* Starts below final position */
  transition: opacity 1s ease, transform 1s ease;
}

/* When subtitle becomes visible */
.subtitle.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Slogan Section - reinforces the brand message */
/* I like how this sits at the bottom of the screen - last thing users see */
.slogan-container {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 5%; /* Space from bottom of screen */
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 1s ease, transform 1s ease;
}

/* When slogan becomes visible */
.slogan-container.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Decorative lines on either side of the slogan */
/* These little details make such a difference to the overall polish */
.slogan-line {
  height: 1px;
  width: 60px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.7), transparent);
}

/* The slogan text itself */
.slogan {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.2rem;
  font-style: italic; /* Adds a touch of sophistication */
  text-align: center;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.6);
  letter-spacing: 0.05em; /* Slightly spaced for readability */
}

/* Animations - brings the page to life */
@keyframes pulse {
  0% { transform: scale(1); opacity: 0.8; }
  100% { transform: scale(1.1); opacity: 1; } /* Subtle size increase and opacity change */
}

/* Responsive Design - looks good on all devices */
/* Tablets and smaller laptops */
@media (max-width: 768px) {
  .title-text {
    font-size: 3.5rem; /* Smaller title on medium screens */
  }
  
  .sun-icon {
    font-size: 3rem;
  }
  
  .subtitle {
    font-size: 1.2rem;
  }
  
  .slogan {
    font-size: 1rem;
  }
  
  .slogan-line {
    width: 40px; /* Shorter decorative lines */
  }
}

/* Mobile phones */
@media (max-width: 480px) {
  .title-text {
    font-size: 2.5rem; /* Even smaller title on phones */
  }
  
  .sun-icon {
    font-size: 2.5rem;
  }
  
  .subtitle {
    font-size: 1rem; /* Readable text size for small screens */
  }
}
</style>