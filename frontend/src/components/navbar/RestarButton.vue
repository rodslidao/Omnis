<template>
  <div>
    <v-btn icon @click="restartDialog = true">
      <v-icon dark>mdi-restart</v-icon>
    </v-btn>
    <dialog-confirmation
      v-if="selectedItem.show"
      :visible="selectedItem.show"
      :title="
        online
          ? loading
            ? $t('dialogs.waitALittle')
            : $t(selectedItem.title)
          : $t(isDisconnected.title)
      "
      :loading="loading"
      :description="
        online
          ? loading && selectedItem.secondsToComplete > 0
            ? $t('dialogs.processWillTake', {
                s: selectedItem.secondsToComplete,
              })
            : $t(selectedItem.description)
          : $t(isDisconnected.title)
      "
      :cancelText="$t('buttons.cancel')"
      :confirmText="online ? $t(selectedItem.button) : isDisconnected.button"
      @cancel-event="cancel()"
      @confirm-event="selectedItem.buttonAction"
      :confirm-disable="loading"
      :cancel-disable="loading"
    >
    </dialog-confirmation>
    <v-menu open-on-hover bottom offset-y>
      <template v-slot:activator="{ on, attrs }">
        <v-btn text icon v-bind="attrs" v-on="on">
          <v-icon>mdi-power</v-icon>
        </v-btn>
      </template>

      <v-list>
        <v-list-item
          link
          v-for="(item, index) in items"
          :key="index"
          @click="(selectedItem = item.dialog), (selectedItem.show = true)"
        >
          <v-list-item-title>{{ $t(item.button) }}</v-list-item-title>
          <!-- <span>
            <v-dialog v-model="item.dialog.show" max-width="400" persistent>
              <v-card :loading="loading" :disabled="loading">
                <v-card-title class="text-h5">
                  {{
                    online ? $t(item.dialog.title) : $t(isDisconnected.title)
                  }}
                </v-card-title>
                <v-card-text>
                  {{
                    online
                      ? $t(item.dialog.description) +
                        (loading && timerCount > 0
                          ? $t('dialogs.processWillTake', { s: timerCount })
                          : '')
                      : $t(isDisconnected.title)
                  }}
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>

                  <v-btn v-if="!online" text @click="restartDialog = false">
                    {{ $t(isDisconnected.button) }}
                  </v-btn>

                  <v-btn v-else text @click="item.dialog.buttonAction">
                    {{ online ? $t(item.dialog.title) : isDisconnected.button }}
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </span> -->
        </v-list-item>
        <!-- <v-divider></v-divider> -->
      </v-list>
    </v-menu>
  </div>
</template>

<script>
import gql from 'graphql-tag';
import DialogConfirmation from '../settings/DialogConfirmation.vue';

const RESTART = gql`
  mutation RESTART {
    restart
  }
`;

export default {
  components: { DialogConfirmation },
  name: 'RestartButton',

  data() {
    return {
      restartDialog: false,
      loading: false,
      timerCount: 60,
      selectedItem: {
        show: false,
        secondsToComplete: 180,
        running: false,
      },
      items: [
        {
          button: 'buttons.fastRestart',
          dialog: {
            title: 'dialogs.fastRestartConfirm.title',
            description: 'dialogs.fastRestartConfirm.description',
            button: 'buttons.fastRestart',
            buttonAction: this.fastRestart,
            secondsToComplete: 15,
            textAfterTime: 'dialogs.fastRestartConfirm.textAfterTime',
            show: true,
          },
        },
        {
          button: 'buttons.shutdown',
          dialog: {
            title: 'dialogs.shutdownConfirm.title',
            description: 'dialogs.shutdownConfirm.description',
            button: 'buttons.shutdown',
            buttonAction: this.shutdown,
            secondsToComplete: 30,
            textAfterTime: 'dialogs.shutdownConfirm.textAfterTime',
            show: true,
          },
        },
        {
          button: 'buttons.restart',
          dialog: {
            title: 'dialogs.restartConfirm.title',
            description: 'dialogs.restartConfirm.description',
            button: 'buttons.restart',
            buttonAction: this.restart,
            secondsToComplete: 60 * 4 + 20,
            show: true,
          },
        }
      ],

      isDisconnected: {
        title: 'dialogs.tabletDisconnected.title',
        description: 'dialogs.tabletDisconnected.description',
        button: 'buttons.gotIt',
        buttonAction: this,
        secondsToComplete: 180,
        show: false,
      },
    };
  },

  props: {
    online: Boolean,
  },

  computed: {},

  watch: {
    selectedItem: {
      handler(value) {
        if (value.secondsToComplete > 0) {
          const timer = setInterval(() => {
            this.selectedItem.secondsToComplete -= 1;
          }, 1000);
        } else {
          clearInterval(timer);
        }
      },
      // immediate: true // This ensures the watcher is triggered upon creation
    },
  },

  methods: {
    async fastRestart() {
      this.loading = true;
      await this.$apollo
        .mutate({
          mutation: RESTART,
        })
        .then(({ data }) => {
          this.timerCount = data.restart;
          setTimeout(() => {
            fetch(
              `http://${process.env.VUE_APP_URL_API_IP}:${process.env.VUE_APP_URL_API_PORT}`
            )
              .then(() => {
                this.$alertFeedback('alerts.restart_ok', 'success');
                this.restartDialog = false;
                this.refreshAfter(2);
              })
              .catch(() => {
                this.$alertFeedback('alerts.restart_fail', 'error');
              })
              .finally((this.loading = false));
          }, data.restart * 1000);
        })
        .catch(() => {
          this.$alertFeedback('alerts.restart_fail', 'error');
          this.loading = false;
        });
    },

    async shutdown() {
      fetch(`http://${process.env.VUE_APP_URL_API_IP}:3000/shutdown`, {
        mode: 'no-cors',
      })
        .then(() => {
          // this.$alertFeedback('alerts.shutdownSuccess', 'success');
          this.loading = true;
          setTimeout(() => {
            fetch(
              `http://${process.env.VUE_APP_URL_API_IP}:${process.env.VUE_APP_URL_API_PORT}`
            )
              .then(() => {
                this.$alertFeedback('alerts.shutdownFail', 'error');
              })
              .catch(() => {
                this.$alertFeedback('alerts.shutdownSuccess', 'success');
              })
              .finally((this.loading = false));
          }, this.selectedItem.secondsToComplete * 1000);
        })
        .catch(() => {
          this.$alertFeedback('alerts.shutdownFail', 'error');
          this.loading = false;
        });
    },

    async restart() {
      fetch(`http://${process.env.VUE_APP_URL_API_IP}:3000/reboot`, {
        mode: 'no-cors',
      })
        .then(() => {
          this.loading = true;
          // Verifica se entrou em processo de restart
          this.isBackendRunningAfter(
            2, // Quantos segundos é pra esperar antes de fazer o check?
            () => {
              // caso esteja rodando (on)
              this.$alertFeedback('alerts.restartFail', 'error');
            },
            () => {
              // caso  esteja desligado (off)
              // Espera até ligar novamente
              setTimeout(() => {
                fetch(
                  // Verifica se ligou
                  `http://${process.env.VUE_APP_URL_API_IP}:${process.env.VUE_APP_URL_API_PORT}`
                )
                  .then(() => {
                    // Avisa que está tudo ok
                    this.$alertFeedback('alerts.restartSuccess', 'success');
                    // Reload na página.
                    this.refreshAfter(2);
                  })
                  .catch(() => {
                    // Avisa que não voltou mais (ainda está desligado.)
                    this.$alertFeedback('alerts.restartFail', 'error');
                  })
                  .finally((this.loading = false));
              }, this.selectedItem.secondsToComplete * 1000); // Definição do tempo pra o segundo check.
            }
          );
        })
        // Não conseguiu nem fazer a requisição para reiniciar
        .catch(() => {
          this.$alertFeedback('alerts.restartFail', 'error');
          this.loading = false;
        });
    },
    refreshAfter(seconds) {
      setTimeout(() => {
        document.location.reload(false);
      }, seconds * 1000);
    },

    isBackendRunningAfter(
      seconds,
      successCallback = console.log,
      failCallback = console.log
    ) {
      setTimeout(() => {
        fetch(
          `http://${process.env.VUE_APP_URL_API_IP}:${process.env.VUE_APP_URL_API_PORT}`
        )
          .then(() => {
            successCallback();
            return true;
          })
          .catch(() => {
            failCallback();
            return false;
          });
      }, seconds * 1000);
    },

    cancel() {
      console.log('cancelar', this.selectedItem.show);
      this.selectedItem.show = false;
    },
  },
};
</script>

<style>
</style>
