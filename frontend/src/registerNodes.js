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

// ifNode
import IfDialog from '@/components/nodes/if/IfDialog.vue';
import IfNode from '@/components/nodes/if/IfNode';

// MatrixNode
import MatrixDialog from '@/components/nodes/matrix/MatrixDialog.vue';
import MatrixNode from '@/components/nodes/matrix/MatrixNode';

// HsvFilterNode
import HsvFilterDialog from '@/components/nodes/filters/hsv/HsvFilterDialog.vue';
import HsvFilterNode from '@/components/nodes/filters/hsv/HsvFilterNode';

// IdentifyNode
import IdentifyDialog from '@/components/nodes/identify/IdentifyDialog.vue';
import IdentifyNode from '@/components/nodes/identify/IdentifyNode';

export function registerOptions(viewPlugin) {
  viewPlugin.registerOption('EventButtonOption', EventButtonOption);
  viewPlugin.registerOption('TextTemplateDialog', TextTemplateDialog);
  viewPlugin.registerOption('MoveAxisDialog', MoveAxisDialog);
  viewPlugin.registerOption('CameraDialog', CameraDialog);
  viewPlugin.registerOption('IfDialog', IfDialog);
  viewPlugin.registerOption('MatrixDialog', MatrixDialog);
  viewPlugin.registerOption('HsvFilterDialog', HsvFilterDialog);
  viewPlugin.registerOption('IdentifyDialog', IdentifyDialog);
}

export function registerNodes(editorInstance) {
  // editorInstance.registerNodeType('MoveNode', MoveNode);

  // User input
  editorInstance.registerNodeType('ButtonNode', ButtonNode, 'Input');

  editorInstance.registerNodeType('TextTemplateNode', TextTemplateNode, 'Text');

  editorInstance.registerNodeType('MoveAxisNode', MoveAxisNode, 'Move');

  editorInstance.registerNodeType('CameraNode', CameraNode, 'Img');

  editorInstance.registerNodeType('IfNode', IfNode, 'Output');

  editorInstance.registerNodeType('MatrixNode', MatrixNode, 'Matrix');

  editorInstance.registerNodeType('HsvFilterNode', HsvFilterNode, 'Hsv');

  editorInstance.registerNodeType('IdentifyNode', IdentifyNode, 'Matrix');
}
