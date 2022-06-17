<template>
  <!-- <div class="cartesian-container" :class="cssVars"> -->
  <div
    class="cartesian-container"
    :style="cssVars"
    @click="isometric = !isometric"
  >
    <!-- <v-btn icon color="primary" @click="isometric = !isometric">
      <v-icon>mdi-{{!isometric ? 'square' : 'cube'}}</v-icon>
    </v-btn> -->
    <div class="perspective" :style="isometric ? 'transform: none' : ''">
      <div class="cube">
        <div class="shadow"></div>
      </div>
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag';

export default {
  data() {
    return {
      isometric: true,
      receivedData: null,
      cssVars: {
        // '--position-x': this.receivedData.X ? this.receivedData.X : 0,
        '--position-x': 0,
        '--position-y': 0,
        '--position-z': 40,
        '--aaaaaaaaaaaaaaa': 2,
      },
    };
  },

  mounted() {
    // this.generate();
  },

  methods: {
    generate() {
      setInterval(() => {
        this.cssVars['--position-x'] = Math.floor(Math.random() * 1000);
        this.cssVars['--position-y'] = Math.floor(Math.random() * 800);
        this.cssVars['--position-z'] = Math.floor(Math.random() * 200);
      }, 2000);
    },
  },

  computed: {
    cssUpdate(x, y, z) {
      // sort random number each 2 seconds
      console.log(x, y, z);
      return {
        // '--position-x': this.receivedData.X ? this.receivedData.X : 0,
        '--position-x': x,
        '--position-y': y,
        '--position-z': y,
        '--aaaaaaaaaaaaaaa': 2,
      };
    },
  },

  watch: {
    receivedData(newData) {
      console.log('dataaa', newData.controls.jog_position.x);
      if (newData.controls.jog_position) {
        const pos = newData.controls.jog_position;
        // this.cssUpdate(pos.X, pos.Y, pos.Z);0
        this.cssVars['--position-x'] = pos.X;
        this.cssVars['--position-y'] = pos.Y;
        this.cssVars['--position-z'] = pos.Z;
      }
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
          this.receivedData = data;
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

  /* --position-x: 100;
  /* --position-y: 0; */
  /* --position-z: 20; */

  --x-machine: 1000;
  --y-machine: 800;
  --z-machine: 200;

  --container-height: 8em;
  --scale-factor: calc(var(--container-height) / var(--y-machine));
  --container-width: calc(var(--scale-factor) * var(--x-machine));

  --cube-size: calc(var(--scale-factor) * 70);
}

.perspective {
  background-color: hsla(0, 0%, 100%, 0.185);
  box-shadow: 0 0 0 0.1em hsla(0, 0%, 0%, 0.2);
  height: calc(var(--container-height) + var(--cube-size));
  width: calc(var(--container-width) + var(--cube-size));
  left: 50%;
  content: '';
  display: block;
  position: absolute;
  top: 50%;
  transform: rotateX(60deg) rotateY(0deg) rotateZ(45deg);
  transform-style: preserve-3d;
  border-top: 2px solid;
  border-image: linear-gradient(to right, rgb(0, 255, 81), rgba(0, 0, 0, 0)) 1 5%;
}
.perspective:after{
  content: '';
  display: block;
  height: calc(var(--scale-factor) * var(--z-machine));
  width: var(--cube-size);
  position: absolute;
  transform: rotateX(90deg);
  transform-origin: 0% 0%;
  border-left: 2px solid;
  border-image: linear-gradient(to bottom, rgb(0, 119, 255), rgba(0, 0, 0, 0)) 1 100%;
}
.perspective:before {
  content: '';
  display: block;
  position: absolute;
  /* background: red; */
  height: calc(var(--container-height) + var(--cube-size));
  width: calc(var(--container-width) + var(--cube-size));
  border-left: 2px solid;
  border-image: linear-gradient(to bottom, red, rgba(0, 0, 0, 0)) 1 100%;
}
.cube,
.shadow,
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

.shadow {
  background-color: #00000065;
  filter: blur(5px);
  transform: translateZ(
    calc(-1 * (var(--cube-size) + var(--scale-factor) * var(--position-z)))
  );
  transition: 0.25s;
}

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
