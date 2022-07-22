import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class AlertNode extends Node {
  type = 'AlertNode';
  // twoColumn = true;

  name = 'Alerta';

  constructor() {
    super();

    this.addInputInterface('Gatilho', undefined, undefined, {
      description: "Entrada que fará o acionamento do nó' ",
    });

    // this.addOutputInterface('Saida', {
    //   description: 'Se tudo der certo sai por aqui ',
    // });

    this.addOption('level', 'AlertDialog', null);
    this.addOption('title', undefined, null);
    this.addOption('description', undefined, null);
    this.addOption('how2solve', undefined, null);
    this.addOption('buttonText', undefined, null);

    this.addOption('color', undefined, '#ff3800');
    this.addOption('running', undefined, true);
  }
}
