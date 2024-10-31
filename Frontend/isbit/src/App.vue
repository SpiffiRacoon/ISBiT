<script>
import Navbar from './components/navbar/NavBar.vue' 
export default {
  components: {
    Navbar
  }
}
</script>

<template>
  <div id="app">
    <Navbar />
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<style>
.main-color {
  background-color: #246a3c;
}

.highlight-color {
  background-color: #4954b0;
}
</style>

<style scoped>
main {
  margin-top: 60px;
  padding: 20px;
}
</style>
