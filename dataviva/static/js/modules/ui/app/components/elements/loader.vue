<template>
  <div>
    <img
      src="../../assets/img/dataviva-logo.png" >
  </div>
</template>

<script>
export default {
  name: "Loader",
};
</script>

<style scoped>
img {
  position: absolute;
  top: calc(50% - 50px);
  left: calc(50% - 50px);
  height: 100px;
  width: 100px;
  animation: fade-in-out 1s steps(12) infinite;
}

@keyframes fade-in-out {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>
