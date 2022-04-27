import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class Camera extends Node {
  type = 'if';
  // twoColumn = true;

  name = 'Condicional IF';

  inputList = [{ name: 'A' }, { name: 'B' }, { name: 'C' }, { name: 'F' }];

  constructor() {
    super();

    this.inputList.forEach((input) => {
      this.addInputInterface(input.name);
    });

    this.addInputInterface('expressão');

    this.addInputInterface('Verdadeiro');
    this.addInputInterface('Falso');

    this.addOutputInterface('Sucesso');
    this.addOutputInterface('Falha');

    this.addOption('expression', 'ifDialog', null);
    this.addOption('true', undefined, null);
    this.addOption('inputList', undefined, this.inputList);

    this.addOption('color', undefined, '#FF9800');
    this.addOption('running', undefined, true);
  }
}
