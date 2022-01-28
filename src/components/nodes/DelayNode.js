import { Node } from "@baklavajs/core";

export class DelayNode extends Node {
    twoColumn = true;
    width = 245;

    constructor() {
        super();
        this.type = "DelayNode";
        this.name = "Esperar";
        this.addInputInterface("Entrada", "", 0, { type: "object" });
        
        this.addOption("Tempo(s)", "InputOption")

        this.addOutputInterface("Saida", { type: "object" });
    }
}
