<template>
  <!-- <div class="cartesian-container" :class="cssVars"> -->
  <div class="cartesian-container" :class="cssUpdate">
    <div class="perspective">
      <div class="cube"></div>
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag';

export default {
  data() {
    return {
      receivedData: null,
    };
  },

  computed: {
    cssUpdate() {
      if (this.receivedData) {
        const css = {
          '--position-x': this.receivedData.X ? this.receivedData.X : 0,
          '--position-y': 300,
        };
        return css;
      }
      return '';
    },
  },

  watch: {
    receivedData(newData) {
      console.log('new2', newData.controls.jog_position.X);
    },
  },

  apollo: {
    $subscribe: {
      // When a tag is added
      controls: {
        query: gql`
          subscription {
            controls {
              jog_position
            }
          }
        `,
        // Result hook
        // Don't forget to destructure `data`
        result({ data }) {
          this.receivedData = data.controls.jog_position;
          // cabo a result
        },
      },
    },
  },
};
</script>

<style scoped>
.cartesian-container {
  --color-main: var(--v-primary-base);

  --position-x: 100;
  --position-y: 100;
  --position-z: 20;

  --x-machine: 1000;
  --y-machine: 800;

  --container-height: 15em;
  --scale-factor: calc(var(--container-height) / var(--y-machine));
  --container-width: calc(var(--scale-factor) * var(--x-machine));

  --cube-size: calc(var(--scale-factor) * 70);
}

.perspective {
  border: 2px solid #545454;
  background-color: hsla(0, 0%, 0%, 0.1);
  background-image: linear-gradient(
      hsla(0, 0%, 0%, 0.1) 2.5%,
      transparent 2.5%,
      transparent 97.5%,
      hsla(0, 0%, 0%, 0.1) 97.5%
    ),
    linear-gradient(
      left,
      hsla(0, 0%, 0%, 0.1) 2.5%,
      transparent 2.5%,
      transparent 97.5%,
      hsla(0, 0%, 0%, 0.1) 97.5%
    );
  background-size: 2em 2em;
  box-shadow: 0 0 0 0.1em hsla(0, 0%, 0%, 0.2);
  height: var(--container-height);
  width: var(--container-width);
  left: 50%;
  position: absolute;
  top: 50%;
  transform: rotateX(60deg) rotateY(0deg) rotateZ(45deg);
  transform-style: preserve-3d;
}
.cube,
.cube:after,
.cube:before {
  /* box-shadow: inset 0 0 0 0.25em hsla(0, 72%, 38%, 0.1); */
  content: '';
  float: left;
  height: var(--cube-size);
  position: absolute;
  width: var(--cube-size);
}
/* Top */
.cube {
  background-color: var(--color-main);
  position: relative;
  transform: translateZ(var(--cube-size));
  transform-style: preserve-3d;
  transition: 0.25s;
}
/* Left */
.cube:after {
  background-color: var(--color-main);
  filter: brightness(70%);
  transform: rotateX(-90deg) translateY(var(--cube-size));
  transform-origin: 100% 100%;
}
/* Right */
.cube:before {
  background-color: var(--color-main);
  filter: brightness(90%);
  transform: rotateY(90deg) translateX(var(--cube-size));
  transform-origin: 100% 0;
}
/* Alternate Colour */
.cube:nth-child(even) {
  background-color: rgb(20, 229, 9);
}
/* .cube:nth-child(even):after {
    background-color: #eb5;
}
.cube:nth-child(even):before {
    background-color: #da4;
} */
/* Animation */
@keyframes wave {
  50% {
    transform: translateZ(4.5em);
  }
}
.cube:nth-child(1) {
  /*     animation: wave 2s ease-in-out infinite; */
  transform: translateZ(
      calc(var(--cube-size) + var(--scale-factor) * var(--position-z))
    )
    translateX(calc(var(--scale-factor) * var(--position-x)))
    translateY(calc(var(--scale-factor) * var(--position-y)));
}
</style>
