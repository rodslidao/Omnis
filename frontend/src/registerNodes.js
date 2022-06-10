// import EventButtonOption from "@/options/EventButtonOption";
// import { MoveNode } from '@/components/node/nodes/MoveNode';
import EventButtonOption from '@/components/node/nodes/options/EventButtonOption.vue';

import ArithmeticOption from '@/components/node/nodes/arithmetic/ArithmeticOption.vue';

// TextNode
import TextTemplateDialog from '@/components/node/nodes/text/TextTemplateDialog.vue';
import TextTemplateNode from '@/components/node/nodes/text/TextTemplateNode';

// MoveNode
import MoveAxisDialog from '@/components/node/nodes/move/MoveAxisDialog.vue';
import MoveAxisNode from '@/components/node/nodes/move/MoveAxisNode';

// MoveNode
import CameraDialog from '@/components/node/nodes/camera/CameraDialog.vue';
import CameraNode from '@/components/node/nodes/camera/CameraNode';

// ifNode
import IfDialog from '@/components/node/nodes/if/IfDialog.vue';
import IfNode from '@/components/node/nodes/if/IfNode';

// OrNode
import OrNode from '@/components/node/nodes/or/OrNode';

// MatrixNode
import MatrixDialog from '@/components/node/nodes/matrix/MatrixDialog.vue';
import MatrixNode from '@/components/node/nodes/matrix/MatrixNode';

// DelayNode
import DelayDialog from '@/components/node/nodes/delay/DelayDialog.vue';
import DelayNode from '@/components/node/nodes/delay/DelayNode';

// HsvFilterNode
import HsvFilterDialog from '@/components/node/nodes/filters/hsv/HsvFilterDialog.vue';
import HsvFilterNode from '@/components/node/nodes/filters/hsv/HsvFilterNode';

// IdentifyNode
import IdentifyDialog from '@/components/node/nodes/identify/IdentifyDialog.vue';
import IdentifyNode from '@/components/node/nodes/identify/IdentifyNode';

// IoNode
import IoNode from '@/components/node/nodes/io/IoNode';
import IoDialog from '@/components/node/nodes/io/IoDialog.vue';

// input nodes
import StartNode from '@/components/node/nodes/inputs/StartNode';
import PauseNode from '@/components/node/nodes/inputs/PauseNode';
import StopNode from '@/components/node/nodes/inputs/StopNode';
import RestartNode from '@/components/node/nodes/inputs/RestartNode';

// AlertNode
import AlertNode from '@/components/node/nodes/alert/AlertNode';
import AlertDialog from '@/components/node/nodes/alert/AlertDialog.vue';

// ArithmeticNode
import ArithmeticNode from '@/components/node/nodes/arithmetic/ArithmeticNode';
import ArithmeticDialog from '@/components/node/nodes/arithmetic/ArithmeticDialog.vue';

export function registerOptions(viewPlugin) {
  viewPlugin.registerOption('EventButtonOption', EventButtonOption);
  viewPlugin.registerOption('ArithmeticOption', ArithmeticOption);
  viewPlugin.registerOption('TextTemplateDialog', TextTemplateDialog);
  viewPlugin.registerOption('MoveAxisDialog', MoveAxisDialog);
  viewPlugin.registerOption('CameraDialog', CameraDialog);
  viewPlugin.registerOption('IfDialog', IfDialog);
  viewPlugin.registerOption('MatrixDialog', MatrixDialog);
  viewPlugin.registerOption('HsvFilterDialog', HsvFilterDialog);
  viewPlugin.registerOption('IdentifyDialog', IdentifyDialog);
  viewPlugin.registerOption('IoDialog', IoDialog);
  viewPlugin.registerOption('AlertDialog', AlertDialog);
  viewPlugin.registerOption('DelayDialog', DelayDialog);
  viewPlugin.registerOption('ArithmeticDialog', ArithmeticDialog);
}

export function registerNodes(editorInstance) {
  // editorInstance.registerNodeType('MoveNode', MoveNode);

  // User input

  editorInstance.registerNodeType('TextTemplateNode', TextTemplateNode, 'Text');

  editorInstance.registerNodeType('MoveAxisNode', MoveAxisNode, 'Move');

  editorInstance.registerNodeType('CameraNode', CameraNode, 'Img');

  editorInstance.registerNodeType('IfNode', IfNode, 'Input');

  editorInstance.registerNodeType('OrNode', OrNode, 'Input');

  editorInstance.registerNodeType('MatrixNode', MatrixNode, 'Input');

  editorInstance.registerNodeType('DelayNode', DelayNode, 'Output');

  editorInstance.registerNodeType('HsvFilterNode', HsvFilterNode, 'Hsv');

  editorInstance.registerNodeType('IdentifyNode', IdentifyNode, 'Matrix');

  editorInstance.registerNodeType('IoNode', IoNode, 'Io');

  editorInstance.registerNodeType('StartNode', StartNode, 'Input');
  editorInstance.registerNodeType('PauseNode', PauseNode, 'Input');
  editorInstance.registerNodeType('StopNode', StopNode, 'Input');
  editorInstance.registerNodeType('RestartNode', RestartNode, 'Input');

  editorInstance.registerNodeType('AlertNode', AlertNode, 'Alert');

  editorInstance.registerNodeType('ArithmeticNode', ArithmeticNode, 'Arithmetic');
}
