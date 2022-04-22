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

// MoveNode
import CameraDialog from '@/components/nodes/camera/CameraDialog.vue';
import CameraNode from '@/components/nodes/camera/CameraNode';

export function registerOptions(viewPlugin) {
  viewPlugin.registerOption('EventButtonOption', EventButtonOption);
  viewPlugin.registerOption('TextTemplateDialog', TextTemplateDialog);
  viewPlugin.registerOption('MoveAxisDialog', MoveAxisDialog);
  viewPlugin.registerOption('CameraDialog', CameraDialog);
}

export function registerNodes(editorInstance) {
  // editorInstance.registerNodeType('MoveNode', MoveNode);

  // User input
  editorInstance.registerNodeType('button', ButtonNode, 'Input');

  editorInstance.registerNodeType('text-template', TextTemplateNode, 'Text');

  editorInstance.registerNodeType('move-axis', MoveAxisNode, 'Move');

  editorInstance.registerNodeType('camera', CameraNode, 'Output');
}
