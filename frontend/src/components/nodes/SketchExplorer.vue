<template>
  <div class="d-flex">
    <v-data-table
      :headers="headers"
      :items="files"
      sort-by="name"
      class="elevation-1"
      @contextmenu:row="contextMenu"
    >
      <template v-slot:item.name="{ item }" class="name">
        {{ item.name }}
        <v-icon v-if="runningFileId == item.id" small color="green"
          >mdi-play-circle</v-icon
        >
      </template>

      <template v-slot:item.lastAccess="{ item }">
        {{ timestampToData(item.lastAccess) }}
      </template>

      <template v-slot:top>
        <v-toolbar flat>
          <!-- <div class="h4">Arquivos</div> -->
          <v-toolbar-title>Arquivos</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <!-- <template v-slot:activator="{ on, attrs }">
            <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
            Criar arquivo
            </v-btn>
          </template> -->
            <v-card>
              <v-card-title>
                <span class="text-h5">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.name"
                        label="Dessert name"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.descrição"
                        label="descrição"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <p class="">Qtd. nó</p>
                      <p class="">{{ editedItem.nodeQtd }}</p>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <p class="">Author</p>
                      <p class="">{{ editedItem.nodeQtd }}</p>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="close">
                  Cancel
                </v-btn>
                <v-btn color="blue darken-1" text @click="save"> Save </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title class="text-h5"
                >Are you sure you want to delete this item?</v-card-title
              >
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeDelete"
                  >Cancel</v-btn
                >
                <v-btn color="blue darken-1" text @click="deleteItemConfirm"
                  >OK</v-btn
                >
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <!-- <v-icon small class="mr-2" @click="editItem(item)"> mdi-pencil </v-icon>
        <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon> -->

        <v-menu v-model="showMenu" offset-y style="max-width: 600px">
          <template v-slot:activator="{ on, attrs }">
            <v-icon small @click="contextMenu()"> mdi-dots-vertical </v-icon>
          </template>

          <v-list>
            <v-list-item v-for="(item, index) in items" :key="index" link>
              <v-list-item-title
                @click="item.function()"
                ><v-icon small class="mr-5">mdi-{{ item.btnIcon }}</v-icon
                >{{ item.title }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
      <template v-slot:no-data>
        <v-btn color="primary" @click="initialize"> Reset </v-btn>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import { actions } from '../../store';
export default {
  data: () => ({
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: 'Nome',
        align: 'start',
        value: 'name',
      },
      { text: 'Descrição', value: 'descrição' },
      { text: 'Qtd. nó', value: 'nodeQtd' },
      { text: 'Autor', value: 'author' },
      { text: 'ID', value: 'id' },
      { text: 'Ultima Alteração', value: 'lastAccess' },
      { text: 'Ações', value: 'actions', sortable: false },
    ],
    files: [],
    runningFileId: 16530682866630,
    editedIndex: -1,
    editedItem: {
      name: '',
      descrição: 0,
      nodeQtd: 0,
      author: '',
      id: '',
    },
    defaultItem: {
      name: '',
      descrição: 0,
      nodeQtd: 0,
      author: '',
      id: '',
    },
    showMenu: false,
    items: [
      {
        title: 'Duplicar',
        btnIcon: 'content-duplicate',
        function: this.duplicate,
        enabled: true,
      },
      {
        title: 'Duplicar',
        btnIcon: 'content-duplicate',
        function: this.edit,
        enabled: true,
      },
      {
        title: 'Duplicar',
        btnIcon: 'content-duplicate',
        function: this.rename,
        enabled: true,
      },
      {
        title: 'Renomear',
        btnIcon: 'form-textbox',
        function: this.delete,
        enabled: true,
      },
    ],
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'New Item' : 'Edit Item';
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      this.files = [
        {
          name: 'Pega de conectores',
          descrição:
            'Rotina Para pega de conectores, no gabarito e a colocação dele nos painéis',
          nodeQtd: 6,
          author: 'Rodrigo Gomes',
          lastAccess: '1653080955',
          id: '16530682866630',
        },
        {
          name: 'Verifica conectores',
          descrição: 'Rotina Para verificação de conectores',
          nodeQtd: 3,
          author: 'Henrique A',
          lastAccess: '1653080155',
          id: '16530682866631',
        },
      ];
    },

    editItem(item) {
      this.editedIndex = this.files.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      this.editedIndex = this.files.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      this.files.splice(this.editedIndex, 1);
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.files[this.editedIndex], this.editedItem);
      } else {
        this.files.push(this.editedItem);
      }
      this.close();
    },

    contextMenu() {
      this.showMenu = true;
      console.log('contextMenu');
    },

    duplicate() {
      console.log('duplicate');
    },

    rename() {
      console.log('rename');
    },

    edit() {
      console.log('edit');
    },

    delete() {
      console.log('delete');
    },

    timestampToData(timestamp) {
      const d = new Date(timestamp * 1000);
      const options = {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        hour12: true,
      };

      return new Intl.DateTimeFormat('pt-BR', options).format(d);
    },
  },
};
</script>
