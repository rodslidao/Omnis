<template>
  <div class="d-flex justify-center align-center space flex-column">
    <v-btn-toggle
      v-model="toggle_exclusive"
      rounded
      mandatory
      dense
      class="d-flex justify-center align-center"
    >
      movimento em S
      <v-btn class="center">
        <v-icon>mdi-swap-horizontal-variant</v-icon>
      </v-btn>
      <v-btn> <v-icon>mdi-alpha-z </v-icon> </v-btn>
      movimento em Z
    </v-btn-toggle>
    <p>{{ selected.direction }} - {{ toggle_exclusive }}</p>
    <div class="wrapper">
      <v-item-group mandatory class="group">
        <v-div v-for="button in buttonList" :key="button">
          <v-item v-slot="{ active, toggle }">
            <v-btn
              icon
              dark
              @click="
                toggle,
                  arrowClicked(button.position, button.OrderList[selected.type])
              "
              class="button"
              :style="button.style"
            >
              <v-icon
                :color="active ? 'red' : 'blue'"
                large
                :style="'transform: rotate(' + button.rotation + 'deg)'"
              >
                mdi-arrow-up-thick
              </v-icon>
            </v-btn>
          </v-item>
        </v-div>
      </v-item-group>

      <div class="container d-flex wrap">
        <div
          :class="items[index].toString()"
          v-for="(item, index) in items"
          v-bind:key="item"
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
      items: [],
      defaultOrderList: [0, 1, 2, 5, 4, 3, 6, 7, 8],
      selectedOrderList: [],
      counter: 0,
      indexToFlash: 0,
      offsetMarginArrows: '40px',
      selected: {
        direction: '',
        type: '',
      },
    };
  },

  watch: {
    toggle_exclusive(newValue) {
      console.log('toggle_exclusive', newValue);
      this.selected.type = newValue === 0 ? 's' : 'z';
      this.counter = 0;
    },

    selectedOrderList() {
      console.log('selectedOrderList', this.selectedOrderList);
      this.counter = 0;
      this.flash();
    },
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
        },
        {
          rotation: 180,
          position: 'TRB',
          style: {
            top: this.offsetMarginArrows,
            right: '0px',
          },
        },
        {
          rotation: 0,
          position: 'BRT',
          style: {
            bottom: this.offsetMarginArrows,
            right: '0px',
          },
        },
        {
          rotation: 270,
          position: 'BRL',
          style: {
            bottom: 0,
            right: this.offsetMarginArrows,
          },
        },
        {
          rotation: 360,
          position: 'BLT',
          style: {
            left: 0,
            bottom: this.offsetMarginArrows,
          },
        },
        {
          rotation: 90,
          position: 'BLR',
          style: {
            left: this.offsetMarginArrows,
            bottom: 0,
          },
        },
      ];
      return btnList;
    },
  },

  created() {
    for (let i = 0; i < this.totalElements; i += 1) {
      this.items[i] = false;
    }
    console.log(this.items);
    this.flash();
    this.selected.direction = 'TLR';
    this.selected.selectedOrderList = this.defaultOrderList;
  },

  methods: {
    arrowClicked(direction, orderList) {
      console.log('awdad', orderList);
      this.selected.direction = direction;
      this.selected.selectedOrderList = orderList;
    },

    flash() {
      setInterval(() => {
        if (this.counter <= this.items.length - 1) {
          this.items[this.selected.selectedOrderList[this.counter]] = true;
          if (this.counter >= 1) {
            this.items[
              this.selected.selectedOrderList[this.counter - 1]
            ] = false;
          }
          if (this.counter === 0) {
            this.items[this.items.length - 1] = false;
          }
          // console.log('conta', this.counter, this.items.length);
          this.counter += 1;
          // console.log(this.items);
          if (this.counter === this.items.length) {
            this.counter = 0;
          }
        }
      }, 800);
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
      color: white;
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
        border: 4px solid;
        opacity: 1;
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
