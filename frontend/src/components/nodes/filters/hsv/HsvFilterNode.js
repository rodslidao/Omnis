import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class Camera extends Node {
  type = 'hsv-filter';
  // twoColumn = true;

  name = 'Filtro de Cor';

  constructor() {
    super();

    this.addOutputInterface('Imagem');

    this.addInputInterface('Cor 1', undefined, undefined, {
      description:
        'Imagine uma escala do preto(Cor 1) para branco (Cor 2). o filtro ira pegar todos as cores no intervalo entre as duas cores, o cinza por exemplo',
    });

    this.addInputInterface('Cor 2', undefined, undefined, {
      description:
        'Imagine uma escala do preto(Cor 1) para branco (Cor 2). O filtro ira pegar todos as cores no intervalo entre as duas cores, do preto passando pelo cinza até o branco',
    });

    this.addOutputInterface('Imagem', {
      description: 'Sai uma imagem preto e branco, com a cor escolhida em branco e o resto preto',
    });

    this.addOption('lower', 'HsvFilterDialog', this.selectedCamera);
    this.addOption('upper', undefined, this.selectedCamera);

    this.addOption('color', undefined, '#cc00ff');
    this.addOption('running', undefined, true);
  }
}
