import { Node } from '@baklavajs/core';
// import { store } from '../../main';

export default class MoveAxis extends Node {
  type = 'move-axis';
  twoColumn = true;

  height = 800;

  name = 'Mover Eixo';

  axisList = ['X', 'Y', 'Z'];

  constructor() {
    super();
    // const axisList = ["X", "Y", "Z"];
    // this.addInputInterface('X');
    // this.addInputInterface('Y');
    // this.addInputInterface('Z');
    this.addInputInterface('Trigger');
    this.addOutputInterface('onSuccess');
    this.addOutputInterface('onFailure');
    this.axisList.forEach((axis) => {
      this.addOption(axis, 'CheckboxOption');
    });

    // this.addOption("+ Opções", "ButtonOption", () => ({ testtext: "any" }), "MySidebarOption");
    // this.setOptionValue("+ Opções", "Arduino Nano");

    this.events.update.addListener(this, (event) => {
      // console.log(this.interfaces.entries());
       console.log('axis');
      const item = this.axisList.find((axis) => axis == event.name);
      console.log(item);
      console.log(event.name);
      if (event.name === item) {
        if (this.getOptionValue(item)) {
          this.addInputInterface(`${item} `);
        } else {
          this.removeInterface(`${item} `);
        }
      }
    });

    this.addInputInterface('Velocidade', 'NumberOption', 10000);

    this.addOption('settings', 'MoveAxisDialog', {
      template: 'Hello, my name is {name}',
      allowUndefined: false,
      velocity: 10000,
    });

    this.addOption('color', undefined, '#607565');
    this.addOption('running', undefined, true);
  }
}
