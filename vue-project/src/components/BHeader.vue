<template>
  <div class="header-container">
    <header class="header">
      <ul class="nav">
        <li class="nav-item">
          <router-link to="/Home" class="nav-link">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/UVsearch" class="nav-link">UVsearch</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/Skinsearch" class="nav-link">Skinsearch</router-link>
        </li>
      </ul>
    </header>
  </div>
</template>

<style scoped>

.header-container {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  display: flex;
  justify-content: center;
  z-index: 1000;
}


.header {
  background: rgba(0, 0, 0, 0.3); 
  padding: 10px 20px;
  border-radius: 12px;
  backdrop-filter: blur(10px); 
}

.nav {
  display: flex;
  gap: 20px;
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  font-size: 1.1rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: bold;
  padding: 8px 15px;
  border-radius: 8px;
  transition: all 0.3s ease-in-out;
}

.nav-link:hover,
.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
  text-shadow: 0px 0px 8px rgba(255, 255, 255, 0.8);
}
</style>
