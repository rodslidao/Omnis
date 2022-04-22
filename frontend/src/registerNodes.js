// import EventButtonOption from "@/options/EventButtonOption";
// import { MoveNode } from '@/components/nodes/MoveNode';
import EventButtonOption from '@/components/nodes/options/EventButtonOption.vue';

// ButtonNode
import ButtonNode from '@/components/nodes/ButtonNode';

// TextNode
import TextTemplateDialog from '@/components/nodes/text/TextTemplateDialog.vue';
import TextTemplateNode from '@/components/nodes/text/TextTemplateNode';

// MoveNode
import MoveAxisDialog from '@/components/nodes/move/MoveAxisDialog.vue';
import MoveAxisNode from '@/components/nodes/move/MoveAxisNode';

export function registerOptions(viewPlugin) {
  viewPlugin.registerOption('EventButtonOption', EventButtonOption);
  viewPlugin.registerOption('TextTemplateDialog', TextTemplateDialog);
  viewPlugin.registerOption('MoveAxisDialog', MoveAxisDialog);
}

export function registerNodes(editorInstance) {
  // editorInstance.registerNodeType('MoveNode', MoveNode);

  // User input
  editorInstance.registerNodeType('button', ButtonNode, 'Input');

  editorInstance.registerNodeType('text-template', TextTemplateNode, 'Text');

  editorInstance.registerNodeType('move-axis', MoveAxisNode, 'Move');
}
