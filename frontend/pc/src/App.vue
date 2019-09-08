<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
body {
  padding: 0;
  margin: 0;
  background-color: #efefef;
}

.outer {
  display: table;
  position: absolute;
  height: 100%;
  width: 100%;
}
.flex-v {
  display: flex;
  flex-direction: row;
}
.card {
  background-color: rgba(255, 255, 255, 0.8);
  padding: 2rem;
  min-width: 30%;
  min-height: 40%;
  overflow: hidden;
  border-radius: 2rem;
  transition: box-shadow 0.5s;
}
@supports (backdrop-filter: blur) {
  .card {
    background-color: rgba(255, 255, 255, 0.6);
    padding: 2rem;
    min-width: 30%;
    min-height: 40%;
    overflow: hidden;
    border-radius: 2rem;
    backdrop-filter: blur(1rem);
    -webkit-backdrop-filter: blur(1rem);
    transition: box-shadow 0.5s;
  }
}

.middle {
  display: table-cell;
  vertical-align: middle;
}
.right-buttom {
  position: absolute;
  bottom: 1rem;
  right: 2rem;
}
.margeTop {
  margin-top: 1rem;
  text-align: start;
}
.margeTopRight {
  margin-top: 1rem;
}
.Stbotton {
  margin-left: 1rem;
  margin-right: 1rem;
}
</style>
