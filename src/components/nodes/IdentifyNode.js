import { Node } from "@baklavajs/core";

export class IdentifyNode extends Node {
    twoColumn = true;
    width = 245;

    constructor() {
        super();
        this.type = "IdentifyNode";
        this.name = "Identificar";
        this.addInputInterface("Entrada", "", 0, { type: "object" });

        this.addOption(
            "Cameras",
            "SelectOption",
            "Selecione uma Camera",
            undefined,
            {
                items: ["Camera Superior", "Camera Inferior"],
            }
        );
        this.addOption(
            "Filtros",
            "SelectOption",
            "Selecione um filtro",
            undefined,
            {
                items: ["Small Blue", "Small Red", "Small Green", "Small Yellow"],
            }
        );
        this.addOption("VideoStreming", "VideoStreming", "VideoStreming");
        this.addOutputInterface("Saida", { type: "object" });
    }

    calculate() {

        // this.addInputInterface("X", "NumberOption", 0);
        // this.getOptionValue("X").events.updated.emit()

        // let moveOutput = {
        //     hardware: this.getOptionValue("Hardware").value,
        //     axisList:
        //         [
        //             // {
        //             //     "axis": "X",
        //             //     "coordinate": this.getInterface("X").value,
        //             //     "channel": 0,
        //             //     "await": false
        //             // },
        //             {
        //                 "axis": "Y",
        //                 "coordinate": this.getInterface("Y").value,
        //                 "channel": 0,
        //                 "await": false
        //             },
        //             {
        //                 "axis": "Z",
        //                 "coordinate": this.getInterface("Z").value,
        //                 "channel": 0,
        //                 "await": false
        //             },
        //             {
        //                 "axis": "A",
        //                 "coordinate": this.getInterface("A").value,
        //                 "channel": 0,
        //                 "await": false
        //             },
        //             {
        //                 "axis": "B",
        //                 "coordinate": this.getInterface("B").value,
        //                 "channel": 0,
        //                 "await": false
        //             },
        //             {
        //                 "axis": "C",
        //                 "coordinate": this.getInterface("C").value,
        //                 "channel": 0,
        //                 "await": false
        //             },
        //             {
        //                 "axis": "F",
        //                 "coordinate": this.getInterface("Velocidade").value,
        //                 "channel": 0,
        //                 "await": false
        //             }

        //         ]
        // }
        this.getInterface("Saida").value = this.getOptionValue("Hardware");
    }
}
