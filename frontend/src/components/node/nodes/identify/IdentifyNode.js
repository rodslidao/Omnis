import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class IdentifyNode extends Node {
  type = 'IdentifyNode';
  // twoColumn = true;

  name = 'Identificação';

  constructor() {
    super();

    this.addInputInterface('Matriz', undefined, undefined, {
      description: 'Costuma receber uma matriz de imagens ja tratadas com filtros',
    });

    this.addOutputInterface('MatrizOut', {
      description:
        'Sai uma matriz com a imagem cortada de cada pedacinho com as informações de identificação dos filtros configurados',
      alias: 'Matriz',
    });

    this.addOption('filters', 'IdentifyDialog', null);

    this.addOption('color', undefined, '#ff3900');
    this.addOption('running', undefined, true);
  }
}
