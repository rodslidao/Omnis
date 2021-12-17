import { Node } from "@baklavajs/core";

export class MoveNode extends Node {
    constructor() {
        super();
        this.type = "MoveNode";
        this.name = "Movimento";
        this.addInputInterface("X", "NumberOption", 0);
        this.addInputInterface("Y", "NumberOption", 0);
        this.addInputInterface("Z", "NumberOption", 0);
        this.addInputInterface("A", "NumberOption", 0);
        this.addInputInterface("B", "NumberOption", 0);
        this.addInputInterface("C", "NumberOption", 0);
        this.addInputInterface("Velocidade", "NumberOption", 10);
        this.addOption(
            "Hardware",
            "SelectOption",
            "Selecione uma Placa",
            undefined,
            {
                items: ["Arduino Nano", "Octopus V1.1"]
            }
        );
        this.addOutputInterface("");
    }

    calculate() {
        let positionList = [ 
            {
            "axis": "X",
            "coordinate": this.getInterface("X").value,
            "channel": 0,
            "await": false
        },
            {
            "axis": "Y",
            "coordinate": this.getInterface("Y").value,
            "channel": 0,
            "await": false
        },
            {
            "axis": "Z",
            "coordinate": this.getInterface("Z").value,
            "channel": 0,
            "await": false
        },
        {
            "axis": "A",
            "coordinate": this.getInterface("A").value,
            "channel": 0,
            "await": false
        },
        {
            "axis": "B",
            "coordinate": this.getInterface("B").value,
            "channel": 0,
            "await": false
        },
        {
            "axis": "C",
            "coordinate": this.getInterface("C").value,
            "channel": 0,
            "await": false
        },
            {
            "axis": "F",
            "coordinate": this.getInterface("F").value,
            "channel": 0,
            "await": false
        }

    ]; 
        this.getInterface("Cordenadas").value = positionList;
    }
}
