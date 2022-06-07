<template>
  <v-row justify="center">
    <v-dialog :dark="dark" v-model="dialog" :persistent="persistent" max-width="400">
      <template v-slot:activator="{ on, attrs }">
        <div v-bind="attrs" v-on="on">
          <slot></slot>
        </div>
      </template>
      <v-card>
        <v-card-title class="text-h5">
          {{ title ? title : 'Tem certeza que quer excluir?' }}
        </v-card-title>
        <v-card-text>{{
          description
            ? description
            : 'Esse arquivo será excluído permanentemente, tem certeza que deseja exclui-lo?'
        }}
        <slot name="description"></slot>
        </v-card-text>
        <v-card-actions v-if="!del">
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="$emit('cancel-event')">
            {{ cancelText ? cancelText : 'Cancelar' }}
          </v-btn>
          <v-btn text @click="$emit('confirm-event')">
            {{ confirmText ? confirmText : 'Confirmar' }}
          </v-btn>
        </v-card-actions>
        <v-card-actions v-else>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="$emit('cancel-event')">
            Cancelar
          </v-btn>
          <v-btn text @click=" $emit('confirm-event')">
            Confirmar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  props: {
    confirmText: String,
    cancelText: String,
    title: String,
    description: String,
    del: Boolean,
    persistent: Boolean,
    dark: Boolean,
  },

  data() {
    return {
      dialog: true,
    };
  },
  methods: {
    confirm() {
      this.dialog = true;
    },
  },
};
</script>
