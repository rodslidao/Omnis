/* eslint-disable object-curly-newline */
import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class PositionAdjustmentNode extends Node {
  type = 'PositionAdjustmentNode';

  twoColumn = true;

  height = 800;

  name = 'Ajuste de posição';

  axisList = [
    { name: 'X', isActive: false, value: 0, homing: false },
    { name: 'Y', isActive: false, value: 0, homing: false },
    { name: 'Z', isActive: false, value: 0, homing: false },
    // { name: 'A', isActive: false, value: 0, homing: false },
    // { name: 'B', isActive: false, value: 0, homing: false },
    // { name: 'C', isActive: false, value: 0, homing: false },
    // { name: 'F', isActive: false, value: 0, homing: false },
  ];

  board = { name: '', id: '' };

  mode = { name: 'Cruz', icon: 'plus', description: '' };

  selectedBoard = null;

  boardCopy = null;

  repetitions = 1;

  invert = { direction: false, axis: false };

  velocity = { isActive: true, value: 0 };

  zStep = 1;

  divider = 1;

  selectedBoard = null;

  axisListDialog = [
    { name: 'X', min: -1, max: 1 },
    { name: 'Y', min: -1, max: 1 },
  ];

  constructor() {
    super();
    // const axisList = ["X", "Y", "Z"];
    // this.addInputInterface('X');
    // this.addInputInterface('Y');
    // this.addInputInterface('Z');
    this.addInputInterface('Gatilho', undefined, undefined, {
      description: 'Entrada que fará o acionamento do nó',
    });
    this.addInputInterface('XY', undefined, undefined, {
      description: 'Recebe uma lista de coordenadas para executar o movimento',
    });
    this.addOutputInterface('Sucesso');
    this.addOutputInterface('Falha');
    this.axisList.forEach((axis) => {
      // if (axis.isActive) {
      if (axis.name === 'F') {
        this.addInputInterface('Velocidade');
      } else {
        this.addInputInterface(axis.name);
        // }
      }
    });

    // this.axisList.forEach((axis) => {
    //   this.addOption(axis[0], 'CheckboxOption');
    // });

    // this.events.update.addListener(this, (event) => {
    // });

    // this.events.update.addListener(this, (event) => {
    //   // console.log(this.interfaces.entries());
    //   console.log('axis');
    //   const item = this.axisList.find((axis) => axis == event.name);
    //   console.log(item);
    //   console.log(event.name);
    //   if (event.name === item) {
    //     if (this.getOptionValue(item)) {
    //       this.addInputInterface(`${item} `);
    //     } else {
    //       this.removeInterface(`${item} `);
    //     }
    //   }
    // });

    this.addOption('axisList', 'PositionAdjustmentDialog', this.axisListDialog);
    this.addOption('mode', undefined, this.mode);
    this.addOption('zStep', undefined, this.zStep);
    this.addOption('repetitions', undefined, this.repetitions);
    this.addOption('invert', undefined, this.invert);
    this.addOption('divider', undefined, this.divider);
    this.addOption('velocity', undefined, this.velocity);

    this.addOption('board', undefined, this.board);
    this.addOption('color', undefined, '#fd7000');
    this.addOption('running', undefined, true);
  }
}
