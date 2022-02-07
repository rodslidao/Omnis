import { Node } from "@baklavajs/core";

export class VariableNode extends Node {
    twoColumn = true;
    width = 245;

    constructor() {
        super();
        this.type = "VariableNode";
        this.name = "Variavel";
        // this.addInputInterface("Entrada", "", 0, { type: "object" });
        
        this.addOption("ValueText", "InputOption", "AA");

        this.addOutputInterface("Saida", { type: "object" });
        this.events.update.addListener(this, () => {
            this.getInterface("Saida").value = this.getOptionValue("ValueText");
        });
        // this.getInterface("Saida").value = this.getInterface("Valor").value;
    }
}
