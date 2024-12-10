<template>
  <nav>
    <RouterLink to="/" class="home-link">ISBiT</RouterLink>
    <RouterLink to="/data">Välj Data </RouterLink>
  </nav>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400&display=swap');

nav {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #246a3c;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  padding: 20px 40px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

nav a {
  font-size: 20px;
  color: white;
  text-decoration: none;
  margin: 0 30px;
  padding: 5px 5px;
}

nav a:hover,
nav a:focus,
nav a:active {
  text-decoration: underline;
  outline: none;
}

.home-link {
  font-size: 30px;
  font-family: 'Orbitron', sans-serif;
}
</style>
