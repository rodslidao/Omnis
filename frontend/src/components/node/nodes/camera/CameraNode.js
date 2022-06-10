import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class CameraNode extends Node {
  type = 'CameraNode';
  // twoColumn = true;

  name = 'Camera';

  board = { name: '', id: '' };

  constructor() {
    super();
    this.addInputInterface('Gatilho');
    this.addOutputInterface('Imagem');

    this.addOption('camera', 'CameraDialog', this.selectedCamera);

    this.addOption('color', undefined, '#cc00ff');
    this.addOption('running', undefined, true);
  }

  calculate() {
    console.log('CameraNode');
    this.getInterface('Imagem').value = 2;
  }
}
