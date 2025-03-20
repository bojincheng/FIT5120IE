<template>
  <div class="bottom-nav-container">
    <!-- Main navigation bar that stays fixed at the bottom of the screen -->
    <nav class="bottom-nav">
      <!-- Home navigation item -->
      <router-link to="/" class="nav-item" active-class="active">
        <div class="nav-icon">🏠</div>
        <div class="nav-label">Home</div>
      </router-link>
      
      <!-- UV Search navigation item - helps users find UV index in their area -->
      <router-link to="/UVsearch" class="nav-item" active-class="active">
        <div class="nav-icon">🔍</div>
        <div class="nav-label">UV Search</div>
      </router-link>
      
      <!-- Skin Type assessment tool navigation item -->
      <router-link to="/Skinsearch" class="nav-item" active-class="active">
        <div class="nav-icon">👤</div>
        <div class="nav-label">Skin Type</div>
      </router-link>
      
      <!-- Resources and information page navigation item -->
      <router-link to="/UVinformation" class="nav-item" active-class="active">
        <div class="nav-icon">📚</div>
        <div class="nav-label">Resources</div>
      </router-link>
    </nav>
  </div>
</template>

<style scoped>
/* Container that keeps the nav bar fixed at the bottom */
/* Using fixed positioning ensures it stays visible as users scroll */
.bottom-nav-container {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  z-index: 1000; /* High z-index ensures it stays on top of other content */
}

/* The actual navigation bar styling */
/* I'm using a semi-transparent background with blur for a modern look */
.bottom-nav {
  display: flex;
  justify-content: space-around; /* Evenly distributes the nav items */
  align-items: center;
  background: rgba(0, 0, 0, 0.8); /* Dark semi-transparent background */
  backdrop-filter: blur(10px); /* Creates a frosted glass effect - looks great! */
  height: 70px;
  width: 100%;
  border-top: 1px solid rgba(255, 255, 255, 0.1); /* Subtle top border for definition */
}

/* Individual navigation items */
/* Each item is a column with icon on top and label below */
.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.7); /* Slightly dimmed white for inactive items */
  text-decoration: none; /* Removes underline from router-links */
  width: 25%; /* Each item takes up equal space (4 items = 25% each) */
  height: 100%;
  transition: all 0.3s ease; /* Smooth transition for hover/active states */
  position: relative; /* Needed for the active indicator bar */
  overflow: hidden; /* Ensures nothing spills outside the nav item */
}

/* Icon styling - using emoji for simplicity but could be replaced with SVGs */
.nav-icon {
  font-size: 1.5rem;
  margin-bottom: 4px;
  transition: transform 0.3s ease; /* Allows the icon to move slightly when active */
}

/* Text label styling */
.nav-label {
  font-size: 0.8rem;
  font-weight: 500; /* Medium weight for better readability */
  letter-spacing: 0.5px; /* Slightly spaced out text looks more premium */
  transition: opacity 0.3s ease;
}

/* Hover effect - brightens the item and adds a subtle background */
.nav-item:hover {
  color: rgba(255, 255, 255, 0.9); /* Brighter text on hover */
  background: rgba(255, 255, 255, 0.05); /* Very subtle highlight background */
}

/* Active state - when this route is currently active */
.nav-item.active {
  color: white; /* Full white for active item */
}

/* Active indicator - the colored bar at the top of the active item */
/* Using a pseudo-element to create a colorful gradient bar */
.nav-item.active::before {
  content: ''; /* Required for pseudo-elements */
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px; /* Thin bar */
  background: linear-gradient(90deg, #ffcc00, #ff9500); /* Sunny orange gradient - perfect for a sun app! */
}

/* Makes the icon pop up slightly when its nav item is active */
.nav-item.active .nav-icon {
  transform: translateY(-2px); /* Small upward shift creates a nice effect */
}

/* Pressed state - provides tactile feedback when tapped */
.nav-item:active {
  background: rgba(255, 255, 255, 0.1); /* Slightly stronger background when pressed */
}

/* Mobile optimizations - smaller devices get a more compact navigation bar */
@media (max-width: 480px) {
  .nav-icon {
    font-size: 1.3rem; /* Slightly smaller icons on mobile */
  }
  
  .nav-label {
    font-size: 0.7rem; /* Smaller text on mobile */
  }
  
  .bottom-nav {
    height: 60px; /* Shorter nav bar on mobile to save space */
  }
}
</style>