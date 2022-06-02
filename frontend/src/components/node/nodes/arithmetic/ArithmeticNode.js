import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class ArithmeticNode extends Node {
  type = 'ArithmeticNode';
  // twoColumn = true;

  name = 'Calcula';

  inputList = [{ name: 'A' }, { name: 'B' }, { name: 'C' }, { name: 'F' }];

  constructor() {
    super();

    this.inputList.forEach((input) => {
      this.addInputInterface(input.name);
    });

    this.addOutputInterface('Sucesso', {
      description: 'Se tudo der certo sai por aqui ',
    });

    this.addOutputInterface('Falha');

    this.addOption('expression', 'ArithmeticDialog', null);
    this.addOption('ArithmeticSelected', 'ArithmeticOption', null);

    this.addOption('color', undefined, '#2d5ff5');
    this.addOption('running', undefined, true);
  }
}
