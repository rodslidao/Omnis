import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class OrNode extends Node {
  type = 'OrNode';
  // twoColumn = true;

  name = 'Condicional OU';

  inputList = [{ name: 'A' }, { name: 'B' }];

  constructor() {
    super();

    this.inputList.forEach((input) => {
      this.addInputInterface(input.name);
    });

    this.addOutputInterface('Saida', {
      description: 'Sai uma das duas entradas',
    });

    this.addOption('color', undefined, '#ff3900');
    this.addOption('running', undefined, true);
  }
}