import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class RestartNode extends Node {
  type = 'RestartNode';
  // twoColumn = true;

  name = 'Reiniciar';

  constructor() {
    super();

    this.addInputInterface('Gatilho', undefined, undefined, {
      description: 'Quando acionado, reinicia o  processo ',
    });

    this.addOption('color', undefined, '#0080ff');
    this.addOption('running', undefined, true);
  }
}
