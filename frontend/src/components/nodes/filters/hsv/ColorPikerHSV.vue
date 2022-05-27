<template>
  <div>
    <div class="d-flex flex-column justify-center mb-6">
      <div class="total d-flex flex-column justify-center mb-6">
        <div class="wrap d-flex justify-center mb-6">
          <div
            class="right"
            :class="!selectedColor1 ? 'colorName' : 'colorNameSelected'"
          >
            <div class="d-flex align-right mb-6 text-h6 d-flex flex-column">
              Cor 1<br />
              <span v-show="false" class="text-subtitle-2">
                {{ myMessage.a }}</span
              >
              <v-text-field
                v-model="configuration.camera.filters.hole.gradient.color"
                dense
                hide-details
              ></v-text-field>
            </div>
          </div>
          <div
            class="gradient"
            :style="`background: linear-gradient(to right,
           ${configuration.camera.filters[selectedFilter].gradient.color},
           ${configuration.camera.filters[selectedFilter].gradient.color2})
`"
          >
            <div class="d-flex justify-space-between mb-6 circles">
              <v-btn
                class="ma-2 selected"
                fab
                :color="
                  configuration.camera.filters[selectedFilter].gradient.color
                "
                @click="selectedColor1 = true"
              >
              </v-btn>
              <v-btn
                class="ma-2 selected"
                fab
                :color="
                  configuration.camera.filters[selectedFilter].gradient.color2
                "
                @click="selectedColor1 = false"
              >
              </v-btn>
            </div>
          </div>
          <div :class="selectedColor1 ? 'colorName' : 'colorNameSelected'">
            <div class="d-flex mb-6 text-h6 d-flex flex-column">
              Cor 2<br />
              <span v-show="false" class="text-subtitle-2">{{
                myMessage.b
              }}</span>
              <v-text-field
                v-model="configuration.camera.filters.hole.gradient.color2"
                dense
                hide-details
              ></v-text-field>
            </div>
          </div>
        </div>

        <div class="colorPicker">
          <color-picker
            v-model="
              configuration.camera.filters[selectedFilter].gradient.color
            "
            v-if="selectedColor1"
            mode="rgba"
            @update:color="printColor(rgba)"
          ></color-picker>
          <color-picker
            v-model="
              configuration.camera.filters[selectedFilter].gradient.color2
            "
            v-else
          ></color-picker>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ColorPicker from 'vue-color-picker-wheel';

export default {
  name: 'ColorPikerHSV',
  components: {
    ColorPicker,
  },
  props: {
    upper: Object,
    lower: Object,
  },

  data: () => ({
    selected: '',
    selectedColor1: true,
    dialog: false,
    area_max: 1000,
    area_min: 0,
    configuration: {
      camera: {
        process: null,
        filters: {
          hole: {
            name: 'hole',
            area: [10, 20],
            gradient: {
              color: '#ffffff',
              color2: '#ffffff',
            },
            hsv: {
              hue: [2, 50],
              sat: [0, 250],
              val: [30, 50],
            },
          },
        },
      },
    },
    selectedFilter: 'hole',
  }),

  created() {
    this.configuration.camera.filters[this.selectedFilter].gradient.color = this.lower.hex;
    this.configuration.camera.filters[this.selectedFilter].gradient.color2 = this.upper.hex;
  },

  methods: {
    hexToRgb(hex) {
      // Expand shorthand form (e.g. "03F") to full form (e.g. "0033FF")
      const shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
      // eslint-disable-next-line no-param-reassign
      hex = hex.replace(shorthandRegex, (m, r, g, b) => r + r + g + g + b + b);

      const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
      return result
        ? [
          parseInt(result[1], 16),
          parseInt(result[2], 16),
          parseInt(result[3], 16),
        ]
        : null;
    },
  },

  computed: {
    myMessage() {
      const lowerA = this.configuration.camera.filters.hole.gradient.color;
      const upperB = this.configuration.camera.filters.hole.gradient.color2;

      const data = {
        lower: {
          rgb: this.hexToRgb(lowerA),
          hex: lowerA,
        },
        upper: {
          rgb: this.hexToRgb(upperB),
          hex: upperB,
        },
        // rgb: {
        //   lower: this.hexToRgb(lowerA),
        //   upper: this.hexToRgb(upperB),
        // },
        // hex: {
        //   lower: lowerA,
        //   upper: upperB,
        // },
      };

      this.$emit('colors', data);
      return { a: lowerA, b: upperB };
    },
  },
};
</script>
<style lang="scss" scoped>
.total {
  margin: 0 auto;
}

.gradient {
  width: 284px;
  height: 56px;
  border-radius: 56px;
}
.selected {
  border: solid 5px black;
}
.circles {
  position: absolute;
  width: 300px;
  margin-top: -8px;
  margin-left: -7px;
}
.wrap {
  width: 490px;
}

.colorName {
  height: 56px;
  padding: 0 13px;
  width: 90px;

  // font-weight: 600;
}
.colorNameSelected {
  height: 56px;
  padding: 0 13px;
  font-weight: 600;
  width: 90px;
}
.right {
  text-align: end;
}

.colorPicker {
  margin: 0 auto;
}
.slider {
  width: 300px;
  margin: 37px auto 0;
}
</style>
