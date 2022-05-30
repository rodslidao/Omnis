<template>
  <svg>
    <path
      :d="d"
      :class="classes"
      @mouseover.alt="removeConnection"
      style="pointer-events: fill; stroke-width: 2.5px"
    />
  </svg>
</template>

<script>
// import { socketio } from '@/main';
import gql from 'graphql-tag';

export default {
  props: {
    connection: Object,
  },
  data() {
    return {
      d: '',
      count: 0,
      connectionActive: false,
    };
  },
  inject: ['plugin', 'editor'],
  async mounted() {
    await this.$nextTick();
    this.updateCoords();
  },
  watch: {
    'connection.from.parent.position': {
      handler() {
        this.updateCoords();
      },
      deep: true,
    },
    'connection.to.parent.position': {
      handler() {
        this.updateCoords();
      },
      deep: true,
    },
    'plugin.scaling': {
      handler() {
        this.updateCoords();
      },
      deep: true,
    },
    'plugin.panning': {
      handler() {
        this.updateCoords();
      },
      deep: true,
    },
  },
  methods: {
    transform(x, y) {
      const tx = (x + this.plugin.panning.x) * this.plugin.scaling;
      const ty = (y + this.plugin.panning.y) * this.plugin.scaling;
      return [tx, ty];
    },
    updateCoords() {
      const from = this.resolveDom(this.connection.from);
      const to = this.resolveDom(this.connection.to);
      const [x1, y1] = this.getPortCoordinates(from);
      const [x2, y2] = this.getPortCoordinates(to);
      const [tx1, ty1] = this.transform(x1, y1);
      const [tx2, ty2] = this.transform(x2, y2);
      const dx = 0.6 * Math.abs(tx1 - tx2);
      this.d = `M ${tx1} ${ty1} C ${tx1 + dx} ${ty1}, ${
        tx2 - dx
      } ${ty2}, ${tx2} ${ty2}`;
    },
    getPortCoordinates(resolved) {
      if (resolved.node && resolved.interface && resolved.port) {
        return [
          resolved.node.offsetLeft
            + resolved.interface.offsetLeft
            + resolved.port.offsetLeft
            + resolved.port.clientWidth / 2,
          resolved.node.offsetTop
            + resolved.interface.offsetTop
            + resolved.port.offsetTop
            + resolved.port.clientHeight / 2,
        ];
      }
      return [0, 0];
    },
    resolveDom(ni) {
      const nodeDOM = document.getElementById(ni.parent.id);
      const interfaceDOM = document.getElementById(ni.id);
      const portDOM = interfaceDOM?.getElementsByClassName('__port');
      return {
        node: nodeDOM,
        interface: interfaceDOM,
        port: portDOM && portDOM.length > 0 ? portDOM[0] : null,
      };
    },
    removeConnection() {
      this.editor.plugin.editor.removeConnection(this.connection);
    },
  },
  computed: {
    classes() {
      return {
        connection: true,
        active: this.connectionActive,
      };
    },
  },

  apollo: {
    // Subscriptions
    $subscribe: {
      // When a tag is added
      tagAdded: {
        query: gql`
          subscription {
            nodes {
              type
              id
              info{
                message{
                  to
                  from
                }
              }
            }
          }
        `,
        // Result hook
        // Don't forget to destructure `data`
        result({ data }) {
          // console.log('nodes', data.nodes);
          let timeOut = null;
          if (
            data.nodes.info.message.from === this.connection.from.id
            && data.nodes.info.message.to === this.connection.to.id
          ) {
            this.connectionActive = true; // Activate animation
            clearTimeout(timeOut); // Reset timeout if called
            timeOut = setTimeout(() => {
              this.connectionActive = false; // Deactivate animation if method is not called within interval.
            }, 750);
          }
        },
      },
    },
  },

  created() {
    window.addEventListener('resize', () => {
      this.updateCoords();
    });
    // eslint-disable-next-line no-unused-vars
    const timeOut = null;
  },
};
</script>
<style scoped>
.active {
  stroke-dasharray: 15;
  stroke-width: 3px;
  animation: dash 5s linear infinite;
}
@keyframes dash {
  to {
    stroke-dashoffset: -1000;
  }
}
</style>
