import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class MatrixNode extends Node {
  type = 'MatrixNode';
  // twoColumn = true;

  name = 'Matriz';

  constructor() {
    super();

    this.addInputInterface('Reset');

    this.addInputInterface('Próximo', undefined, undefined, {
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

    this.addOutputInterface('Matriz', {
      description: 'Sai uma matriz com a imagem cortada de cada pedacinho',
    });
    this.addOutputInterface('XY', {
      description: 'Sai as coordenadas normalmente usadas no nó de "Mover Eixo"',
    });

    this.addOutputInterface('Fim', {
      description: 'Essa saida é ativada quando o ultimo item da matriz é selecionado',
    });
    this.addOutputInterface('Erro', {
      description: 'Quando ele tenta rodar e por algum motivo não deu certo, essa saida recebe o erro',
    });

    this.addOption('matrix', 'MatrixDialog', null);

    this.addOption('color', undefined, '#00ff89');
    this.addOption('running', undefined, true);
  }
}
