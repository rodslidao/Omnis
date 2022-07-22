<template>
  <div>
    <v-btn icon @click="restartDialog = true">
      <v-icon dark>mdi-restart</v-icon>
    </v-btn>

    <v-dialog v-model="restartDialog" max-width="400">
      <v-card :loading='loading' :disabled='loading'>
        <v-card-title class="text-h5">
          {{ online ? dilogText.title : isDisconected.title }}
        </v-card-title>

        <v-card-text>
          {{ online ? dilogText.description + (loading && timerCount>0? `Esse processo levará cerca de ${timerCount}s.` : '') : isDisconected.description }}
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn text @click="restartDialog = false">
            {{ online ? dilogText.button : isDisconected.button }}
          </v-btn>

          <v-btn v-if="online" color="red darken-1" text v-on:click="restart()">
            reiniciar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import gql from 'graphql-tag';
const RESTART = gql`
  mutation RESTART {
    restart
  }
`;

export default {
  name: 'RestartButton',

  data: () => ({
    restartDialog: false,
    loading: false,
    timerCount:60,
    dilogText: {
      title: 'Tem certeza que quer reiniciar o sistema?',
      description:
        'Isso pode ajudar a resolver alguns problemas! ',
      button: 'cancelar',
    },

    isDisconected: {
      title: 'Tablet desconectado!',
      description:
        'Não foi possível acessar o servidor! Caso queira reiniciar, faça a operação manualmente. Desligando e e religando no botão físico na maquina!',
      button: 'entendi',
    },
  }),

  watch: {

    timerCount: {
        handler(value) {

            if (value > 0) {
                setTimeout(() => {
                    this.timerCount--;
                }, 1000);
            }

        },
        // immediate: true // This ensures the watcher is triggered upon creation
    }

},

  props: {
    online: Boolean,
  },

  methods: {
    request() {
      fetch(
        `http://${process.env.VUE_APP_URL_API_IP}:${process.env.VUE_APP_URL_API_PORT}`
      ).then(()=>{
        this.$alertFeedback(this.$t('alerts.restart_ok'), 'success');
        this.restartDialog = false;
      })
      .catch(()=>{
        this.$alertFeedback(this.$t('alerts.restart_fail'), 'error');
      })
    },
    async restart() {
      this.loading=true;
      await this.$apollo
        .mutate({
          mutation: RESTART,
        })
        .then(({data})=>{
          this.timerCount=data.restart
          setTimeout(() => {
          this.loading=false;
          this.request();
          }, data.restart*1000);
        })
        .catch(() => {
           this.$alertFeedback(this.$t('alerts.restart_fail'), 'error');
        });
    },
  },
};
</script>

<style>
</style>
