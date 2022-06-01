import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class StartNode extends Node {
  type = 'StartNode';
  // twoColumn = true;

  name = 'Iniciar';

  constructor() {
    super();

    // this.addInputInterface('Matriz', undefined, undefined, {
    //   description: 'Costuma receber uma matriz de imagens ja tratadas com filtros',
    // });

    this.addOutputInterface('Gatilho', {
      description:
        'Chama qualquer outro nó quando o botão Iniciar for acionado'
    });

    this.addOption('color', undefined, '#00a000');
    this.addOption('running', undefined, true);
  }
}
