import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class Camera extends Node {
  type = 'matrix';
  // twoColumn = true;

  name = 'Matriz';

  constructor() {
    super();

    this.addInputInterface('Reset');

    this.addInputInterface('Proximo', undefined, undefined, {
      description:
        'Toda vez que ele recebe uma informação, ele passa para a proxima posição da matriz ',
    });

    this.addInputInterface('Imagem', undefined, undefined, {
      description:
        'Recebe a imagem da bandeja de ovo caso eu queira verificar se os ovos estão na bandeja',
    });

    this.addOutputInterface('Item', {
      description: 'Passa o item da posição atual da matriz pra frente',
    });

    this.addOutputInterface('Matrix', {
      description: 'Sai uma matriz com a imagem cortada de cada pedacinho',
    });

    this.addOutputInterface('Falha');

    this.addOption('matrix', 'MatrixDialog', null);

    this.addOption('color', undefined, '#00ff89');
    this.addOption('running', undefined, true);
  }
}
