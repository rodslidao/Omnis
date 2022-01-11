import { Node } from "@baklavajs/core";

export class MoveNode extends Node {
    twoColumn = true;
    width = 245;

    axisList = ["X", "Y", "Z"];

    constructor() {
        super();
        this.type = "MoveNode";
        this.name = "Movimentar";
        this.addInputInterface("Entrada", "", 0, { type: "object" });

        this.addOption(
            "Hardware",
            "SelectOption",
            "Selecione uma Placa",
            undefined,
            {
                items: ["Arduino Nano", "Octopus V1.1"]
            }
        );
        this.axisList.forEach(axis => { this.addOption(axis, "CheckboxOption") });


        // this.addOption("+ Opções", "ButtonOption", () => ({ testtext: "any" }), "MySidebarOption");
        // this.setOptionValue("+ Opções", "Arduino Nano");

        this.events.update.addListener(this, event => {

            // console.log(this.interfaces.entries()); 
            // console.log(this.options.entries()); 
            const item = this.axisList.find(axis => axis == event.name)
            if (event.name === item) {
                if (this.getOptionValue(item)) {
                    this.addInputInterface(item + " ", "NumberOption", 0);
                } else {
                    this.removeInterface(item + " ");
                }
            }
        });
        this.addInputInterface("Velocidade", "NumberOption", 10000);

        this.addOutputInterface("Saida", { type: "object" });

        // const value = {...this.getInterface("Velocidade").value}
    }

    calculate() {

        console.log("entrouuuuuuuuuuuuuuuuuu");

        this.getInterface("Saida").value = {
            hardware: this.getOptionValue("Hardware").value,
            axisList: this.axisList.filter(axis => this.getOptionValue(axis)).map(axis => {
                return {
                    axis: axis,
                    coordinate: this.getInterface(axis + " ").value,
                    channel: 0,
                    await: false
                }
            }),

        }
    }

        // calculate() {

        //     this.addInputInterface("X", "NumberOption", 0);
        //     // this.getOptionValue("X").events.updated.emit()

        //     // let moveOutput = {
        //     //     hardware: this.getOptionValue("Hardware").value,
        //     //     axisList:
        //     //         [
        //     //             // {
        //     //             //     "axis": "X",
        //     //             //     "coordinate": this.getInterface("X").value,
        //     //             //     "channel": 0,
        //     //             //     "await": false
        //     //             // },
        //     //             {
        //     //                 "axis": "Y",
        //     //                 "coordinate": this.getInterface("Y").value,
        //     //                 "channel": 0,
        //     //                 "await": false
        //     //             },
        //     //             {
        //     //                 "axis": "Z",
        //     //                 "coordinate": this.getInterface("Z").value,
        //     //                 "channel": 0,
        //     //                 "await": false
        //     //             },
        //     //             {
        //     //                 "axis": "A",
        //     //                 "coordinate": this.getInterface("A").value,
        //     //                 "channel": 0,
        //     //                 "await": false
        //     //             },
        //     //             {
        //     //                 "axis": "B",
        //     //                 "coordinate": this.getInterface("B").value,
        //     //                 "channel": 0,
        //     //                 "await": false
        //     //             },
        //     //             {
        //     //                 "axis": "C",
        //     //                 "coordinate": this.getInterface("C").value,
        //     //                 "channel": 0,
        //     //                 "await": false
        //     //             },
        //     //             {
        //     //                 "axis": "F",
        //     //                 "coordinate": this.getInterface("Velocidade").value,
        //     //                 "channel": 0,
        //     //                 "await": false
        //     //             }

        //     //         ]
        //     // }
        // }
    }
