import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class PauseNode extends Node {
  type = 'PauseNode';
  // twoColumn = true;

  name = 'Pausar';

  constructor() {
    super();

    this.addInputInterface('Gatilho', undefined, undefined, {
      description: 'Quando acionado, pausa o processo ',
    });

    this.addOutputInterface('Saida', {
      description:
        'Chama qualquer outro nó quando o botão Iniciar for acionado',
    });

    this.addOption('color', undefined, '#f3ff06');
    this.addOption('running', undefined, true);
  }
}
