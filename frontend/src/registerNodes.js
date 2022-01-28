// import EventButtonOption from "@/options/EventButtonOption";
import { MoveNode } from "../components/nodes/MoveNode";

export function registerOptions(viewPlugin) {
    // viewPlugin.registerOption("EventButtonOption", EventButtonOption);
}

export function registerNodes(editorInstance) {
    editorInstance.registerNodeType("MoveNode", MoveNode);
}
