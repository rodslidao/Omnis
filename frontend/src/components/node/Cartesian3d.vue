<template>
  <!-- <div class="cartesian-container" :class="cssVars"> -->
  <div
    class="cartesian-container"
    :style="cssVars"
    @click="lockView ? '' : (isometric = !isometric)"
  >
    <!-- <v-btn icon color="primary" @click="isometric = !isometric">
      <v-icon>mdi-{{!isometric ? 'square' : 'cube'}}</v-icon>
    </v-btn> -->
    <div class="perspective" :style="!isometric ? 'transform: none' : ''">
      <div class="cube">
        <div class="shadow"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  props: {
    lockView: Boolean,
    height: String || Number,
  },

  data() {
    return {
      isometric: true,
      jogPosition: null,
      cssVars: {
        // '--position-x': this.receivedData.X ? this.receivedData.X : 0,
        '--position-x': 0,
        '--position-y': 0,
        '--position-z': 40,
        '--container-height': this.height || '10rem',
      },
    };
  },

  mounted() {
    // this.generate();
  },

  created() {
    this.connectToWebsocket();
    window.addEventListener('beforeunload', this.leaving);
  },

  methods: {
    leaving: function () {
        console.log("Exiting")
        this.WebSocket.close()
    },
    // generate() {
    //   setInterval(() => {
    //     this.cssVars['--position-x'] = Math.floor(Math.random() * 1000);
    //     this.cssVars['--position-y'] = Math.floor(Math.random() * 800);
    //     this.cssVars['--position-z'] = Math.floor(Math.random() * 70);
    //   }, 3000);
    // },

    connectToWebsocket() {
      console.log(this.$t('alerts.wsConnecting'));
      this.WebSocket = new WebSocket(
        `ws://${process.env.VUE_APP_URL_API_IP}:${process.env.VUE_APP_URL_API_PORT}/controls/6244b0ad3a8338aceae46cf1`
      );

      this.WebSocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        // console.log('veio websoket', data);
        this.jogPosition = data.jog_position;
      };

      this.WebSocket.onopen = (event) => {
        // console.log(event);
        console.log(this.$t('alerts.wsConnectSuccess'));
      };

      this.WebSocket.onclose = (event) => {
        console.log(
          'Socket is closed. Reconnect will be attempted in 1 second.',
          event.reason,
        );
        this.WebSocket.close()
        setTimeout(() => this.connectToWebsocket(), Math.floor(Math.random() * 2500));
      };
    },
  },

  computed: {
    ...mapState('node', {
      controls: (state) => state.controls,
    }),
  },

  watch: {
    jogPosition(newData) {
      // console.log('dataaa', newData);
      if (newData) {
        // this.cssUpdate(pos.X, pos.Y, pos.Z);0
        this.cssVars['--position-x'] = newData.X;
        this.cssVars['--position-y'] = newData.Y? newData.Y : -10; // -10 para não ficar sobre o eixo y ! Remover depois
        this.cssVars['--position-z'] = newData.Z;
      }
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
  --z-machine: 70;

  --position: absolute;
  --container-height: 100%;
  --scale-factor: calc(var(--container-height) / var(--y-machine));
  --container-width: calc(var(--scale-factor) * var(--x-machine));

  --cube-size: calc(var(--scale-factor) * 70);
}

.perspective {
  content: '';
  display: block;
  height: calc(var(--container-height) + var(--cube-size));
  width: calc(var(--container-width) + var(--cube-size));
  transform: rotateX(70deg) rotateY(0deg) rotateZ(45deg);
  transform-style: preserve-3d;
  border-top: 2px solid;
  border-image: linear-gradient(to right, red, rgba(0, 0, 0, 0)) 1 5%;
  background-color: hsla(0, 0%, 100%, 0.185);
  box-shadow: 0 0 0 0.1em hsla(0, 0%, 0%, 0.2);
  
}
.perspective:after {
  content: '';
  display: block;
  height: calc(var(--scale-factor) * var(--z-machine));
  width: var(--cube-size);
  position: absolute;
  transform: rotateX(90deg);
  transform-origin: 0% 0%;
  border-left: 2px solid;
  border-image: linear-gradient(to bottom, rgb(0, 119, 255), rgba(0, 0, 0, 0)) 1
    100%;
}
.perspective:before {
  content: '';
  display: block;
  position: absolute;
  /* background: red; */
  height: calc(var(--container-height) + var(--cube-size));
  width: calc(var(--container-width) + var(--cube-size));
  border-left: 2px solid;
  border-image: linear-gradient(to bottom, rgb(0, 255, 81), rgba(0, 0, 0, 0)) 1
    100%;
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
  filter: blur(4px);
  transform: translateZ(
    calc(
      -1 * (var(--cube-size) + var(--scale-factor) *
            (-1 * var(--position-z) + var(--z-machine)))
    )
  );
  color: white;
  content: 'calc(-1*(var(--cube-size) + var(--scale-factor) * var(--position-z)))';
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
      calc(
        var(--cube-size) + var(--scale-factor) *
          (-1 * var(--position-z) + var(--z-machine))
      )
    )
    translateX(calc(var(--scale-factor) * var(--position-x)))
    translateY(calc(var(--scale-factor) * var(--position-y)));
}
</style>
