import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class DelayNode extends Node {
  type = 'DelayNode';
  // twoColumn = true;

  name = 'Espera (Delay)';

  constructor() {
    super();

    this.addInputInterface('Gatilho', undefined, undefined, {
      description: "Entrada que fará o acionamento do nó' ",
    });

    this.addOutputInterface('Saida', {
      description: 'Se tudo der certo sai por aqui a mesma informação que entrou',
    });

    this.addOption('delay', 'DelayDialog', null);

    this.addOption('color', undefined, '#ffff00');
    this.addOption('running', undefined, true);
  }
}
