import { Node } from "@baklavajs/core";

export class IoNode extends Node {
    twoColumn = true;
    width = 245;

    constructor() {
        super();
        this.type = "IoNode";
        this.name = "Acionar Pinos";
        this.addInputInterface("Entrada", "", 0, { type: "object" });

        this.addOption(
            "Pinos",
            "SelectOption",
            "Selecione um pino/IO",
            undefined,
            {
                items: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"],
            }
        );
        this.addOption(
            "Ações",
            "SelectOption",
            "Selecione uma Ação",
            undefined,
            {
                items: ["Ligar, Desligar"],
            }
        );
        this.addOutputInterface("Saida", { type: "object" });
    }
}
