import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class Camera extends Node {
  type = 'camera';
  // twoColumn = true;


  name = 'Camera';

  selectedCamera = null;

  constructor() {
    super();
    this.addInputInterface('Trigger');
    this.addOutputInterface('Imagem');

    this.addOption('selectedCamera', 'CameraDialog', this.selectedCamera);

    this.addOption('color', undefined, '#FF9800');
    this.addOption('running', undefined, true);
  }
}
