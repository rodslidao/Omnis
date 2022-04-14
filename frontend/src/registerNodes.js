// import EventButtonOption from "@/options/EventButtonOption";
import { MoveNode } from '@/components/nodes/MoveNode';
import EventButtonOption from "@/components/nodes/options/EventButtonOption";

// ButtonNode
import ButtonNode from '@/components/nodes/ButtonNode';

export function registerOptions(viewPlugin) {
  viewPlugin.registerOption("EventButtonOption", EventButtonOption);
}

export function registerNodes(editorInstance) {
  editorInstance.registerNodeType('MoveNode', MoveNode);

  // User input
  editorInstance.registerNodeType('button', ButtonNode, 'Input');
}
