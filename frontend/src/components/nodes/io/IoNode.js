import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class IoNode extends Node {
  type = 'IoNode';
  // twoColumn = true;

  name = 'Portas I/O';

  constructor() {
    super();

    this.addInputInterface('Gatilho', undefined, undefined, {
      description:
        "Entrada que fará o acionamento do nó' ",
    });

    this.addOutputInterface('Saida', {
      description: 'Se tudo der certo sai por aqui ',
    });

    this.addOption('port', 'IoDialog', null);

    this.addOption('color', undefined, '#ff3800');
    this.addOption('running', undefined, true);
  }
}
