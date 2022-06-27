<template>
  <div class="d-flex justify-center align-center space flex-column">
    <v-btn-toggle
      v-model="toggle_exclusive"
      rounded
      mandatory
      dense
      class="d-flex justify-center align-center"
    >
      <v-btn class="center"> movimento em <v-icon>mdi-alpha-s</v-icon> </v-btn>
      <v-btn>movimento em <v-icon>mdi-alpha-z </v-icon> </v-btn>
    </v-btn-toggle>
    <p v-if="debugMode">
      {{ selected.direction }} - {{ toggle_exclusive }} - {{ selected }}-
      {{ selectedOrderList }}
    </p>
    <div class="wrapper">
      <v-item-group mandatory class="group">
        <div v-for="(button, index) in buttonList" :key="index">
          <v-item v-slot="{ active, toggle }">
            <v-btn
              icon
              dark
              @click="toggle"
              class="button"
              :style="button.style"
            >
              <v-icon
                :color="active ? 'red' : 'grey'"
                large
                :style="'transform: rotate(' + button.rotation + 'deg)'"
                @click="
                  arrowClicked(button.position, button.orderList[selected.type])
                "
              >
                mdi-arrow-up-thick
              </v-icon>
            </v-btn>
          </v-item>
        </div>
      </v-item-group>

      <div class="container d-flex wrap">
        <div
          :class="items[index].toString()"
          v-for="(item, index) in items"
          v-bind:key="index"
          class="item d-flex justify-center align-center"
        >
          <div class="text-h5">{{ index }}</div>
        </div>
      </div>
    </div>
    <span v-show="false" class="text">{{ classes }}</span>
  </div>
</template>

<script>
export default {
  data() {
    return {
      toggle_exclusive: undefined,
      totalElements: 9,
      debugMode: false,
      items: [],
      defaultOrderList: [0, 1, 2, 3, 4, 5, 6, 7, 8],
      selectedOrderList: [],
      counter: 0,
      indexToFlash: 0,
      offsetMarginArrows: '40px',
      selected: {
        direction: '',
        type: 's',
      },
    };
  },

  watch: {
    toggle_exclusive(newValue) {
      console.log('toggle_exclusive', newValue);
      this.selected.type = newValue === 0 ? 's' : 'z';
      const getItem = this.buttonList.find(
        (item) => item.position === this.selected.direction
      );

      console.log('getItem', getItem);

      this.selectedOrderList = getItem.orderList[this.selected.type];
      this.counter = 0;
      this.resetList();
    },

    selectedOrderList() {
      this.counter = 0;
      this.resetList();
    },
  },

  created() {
    for (let i = 0; i < this.totalElements; i += 1) {
      this.items[i] = false;
    }
    this.flash();
    this.selected.direction = 'TLR';
    this.selectedOrderList = this.defaultOrderList;
  },

  computed: {
    // just to update the DOM, will need to refactor
    classes() {
      return this.items[this.counter];
    },

    buttonList() {
      const btnList = [
        {
          rotation: 90,
          // (T)top and (L)left point to (R)right
          position: 'TLR',
          style: {
            left: this.offsetMarginArrows,
          },
          orderList: {
            s: [0, 1, 2, 5, 4, 3, 6, 7, 8],
            z: this.defaultOrderList,
          },
        },
        {
          rotation: 180,
          position: 'TLB',
          style: {
            top: this.offsetMarginArrows,
          },
          orderList: {
            s: [0, 3, 6, 7, 4, 1, 2, 5, 8],
            z: [0, 3, 6, 1, 4, 7, 2, 5, 8],
          },
        },
        {
          rotation: 270,
          position: 'TRL',
          style: {
            right: this.offsetMarginArrows,
          },
          orderList: {
            s: [2, 1, 0, 3, 4, 5, 8, 7, 6],
            z: [2, 1, 0, 5, 4, 3, 8, 7, 6],
          },
        },
        {
          rotation: 180,
          position: 'TRB',
          style: {
            top: this.offsetMarginArrows,
            right: '0px',
          },
          orderList: {
            s: [2, 5, 8, 7, 4, 1, 0, 3, 6],
            z: [2, 5, 8, 1, 4, 7, 0, 3, 6],
          },
        },
        {
          rotation: 0,
          position: 'BRT',
          style: {
            bottom: this.offsetMarginArrows,
            right: '0px',
          },
          orderList: {
            s: [8, 5, 2, 1, 4, 7, 6, 3, 0],
            z: [8, 5, 2, 7, 4, 1, 6, 3, 0],
          },
        },
        {
          rotation: 270,
          position: 'BRL',
          style: {
            bottom: 0,
            right: this.offsetMarginArrows,
          },
          orderList: {
            s: [8, 7, 6, 3, 4, 5, 2, 1, 0],
            z: [8, 7, 6, 5, 4, 3, 2, 1, 0],
          },
        },
        {
          rotation: 360,
          position: 'BLT',
          style: {
            left: 0,
            bottom: this.offsetMarginArrows,
          },
          orderList: {
            s: [6, 3, 0, 1, 4, 7, 8, 5, 2],
            z: [6, 3, 0, 7, 4, 1, 8, 5, 2],
          },
        },
        {
          rotation: 90,
          position: 'BLR',
          style: {
            left: this.offsetMarginArrows,
            bottom: 0,
          },
          orderList: {
            s: [6, 7, 8, 5, 4, 3, 0, 1, 2],
            z: [6, 7, 8, 1, 4, 3, 0, 5, 2],
          },
        },
      ];
      return btnList;
    },
  },

  methods: {
    arrowClicked(direction, orderList) {
      this.selected.direction = direction;
      this.selectedOrderList = orderList;
    },

    resetList() {
      this.selectedOrderList.forEach((item) => {
        this.items[item] = false;
      });
    },

    flash() {
      setInterval(() => {
        if (this.counter <= this.items.length) {
          this.items[this.selectedOrderList[this.counter]] = true;

          if (this.counter >= 0) {
            this.items[this.selectedOrderList[this.counter - 1]] = false;
          }
          if (this.counter === 0) {
            this.items[this.selectedOrderList[8]] = false;
          }
          // console.log('conta', this.counter, this.items.length);
          this.counter += 1;
          // console.log(this.items);
          if (this.counter === this.items.length) {
            this.counter = 0;
          }
        }
      }, 500);
    },
  },
};
</script>

<style lang="scss" scoped>
.space {
  height: 100%;
  width: 100%;

  .wrapper {
    height: fit-content;
    width: fit-content;
    position: relative;
  }

  .group {
    position: absolute;
    width: 100%;
    height: 100%;
    .button {
      position: absolute;
    }
  }

  .container {
    margin: 2.5rem;
    border-radius: 0.5rem;
    box-shadow: 0 0 9px 6px rgb(0 0 0 / 18%);
    background-image: linear-gradient(
      to right top,
      #a1ffff,
      #80ecfc,
      #65d8f9,
      #54c2f4,
      #53acec,
      #509bde,
      #4f8acf,
      #4e79bf,
      #3e6bab,
      #2f5c97,
      #1e4e84,
      #0b4171
    );
    position: relative;
    height: 300px;
    width: 300px;
    flex-wrap: wrap;

    .item {
      color: rgb(100, 100, 100);
      flex: 0 0 30%;
      margin: 0.2rem;
      width: 30%;
      height: 30%;
      border-radius: 0.5rem;
      clip: rect(10px, 100px, 100px, 10px);
      background-color: #1e1e1e;
      box-shadow: inset 0 0 17px 2px rgb(0 0 0 / 18%);
      animation-name: fadeInOpacity;
      animation-timing-function: ease-out;
      animation-duration: 2s;

      &.true {
        border: 4px solid #f9f9f9;
        opacity: 1;
        color: white;
      }
      &.false {
      }
    }
  }

  @keyframes fadeInOpacity {
    0% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }
}

.arrow {
}
</style>
