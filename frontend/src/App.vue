<template>
  <div id="app">
    <OperadorasSearch />
  </div>
</template>

<script>
import OperadorasSearch from "./components/OperadorasSearch.vue";

export default {
  name: "App",
  components: {
    OperadorasSearch,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>