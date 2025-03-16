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
        <li class="nav-item">
          <router-link to="/UVinformation" class="nav-link">UVinformation</router-link>
        </li>
      </ul>
    </header>
  </div>
</template>

<style scoped>

.header {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 90%;
  max-width: 1200px;
  background: rgba(0, 0, 0, 0.5); 
  padding: 14px 24px;
  border-radius: 30px;
  backdrop-filter: blur(20px); 
  z-index: 1000;
}


.nav {
  display: flex;
  justify-content: center;
  gap: 40px;
  list-style: none;
  padding: 0;
  margin: 0;
}


.nav-link {
  color: white;
  text-decoration: none;
  font-weight: bold;
  padding: 12px 20px;
  border-radius: 12px;
  transition: all 0.3s ease-in-out;
  position: relative;
  font-size: 1.2rem;
}


.nav-link:hover,
.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
  text-shadow: 0px 0px 10px rgba(255, 255, 255, 0.9);
}
</style>
