import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class StopNode extends Node {
  type = 'StopNode';
  // twoColumn = true;

  name = 'Encerrar';

  constructor() {
    super();

    this.addInputInterface('Gatilho', undefined, undefined, {
      description: 'Quando acionado, para o processo',
    });

    this.addOption('color', undefined, '#ff0000');
    this.addOption('running', undefined, true);
  }
}
