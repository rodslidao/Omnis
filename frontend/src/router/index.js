import Vue from 'vue';
import Router from 'vue-router';

import Home from '@/views/Home.vue';
import Settings from '@/views/Settings.vue';
import IntroLogo from '@/views/IntroLogo.vue';
import Success from '@/views/Success.vue';
import Scan from '@/views/Scan.vue';
import Progress from '@/views/Progress.vue';
import Dashboard from '@/views/Dashboard.vue';
import NodeWorkspace from '@/views/NodeWorkspace.vue';
import NodeEditor from '@/components/node/NodeEditor.vue';
import NodeConfig from '@/views/NodeConfig.vue';

Vue.use(Router);

const routes = [
  {
    name: 'home',
    path: '/home',
    component: Home,
  },
  {
    name: 'settings',
    path: '/config',
    component: Settings,
  },
  {
    name: 'settings',
    path: '/settings',
    component: Settings,
  },
  {
    name: 'intro-logo',
    path: '/',
    component: IntroLogo,
  },
  {
    name: 'scan',
    path: '/scan',
    component: Scan,
  },
  {
    name: 'progress',
    path: '/progress',
    component: Progress,
  },
  {
    name: 'success',
    path: '/success',
    component: Success,
  },
  {
    name: 'dashboard',
    path: '/dashboard',
    component: Dashboard,
  },
  {
    name: 'node',
    path: '/node',
    component: NodeWorkspace,
  },
  {
    name: 'nodeEditor',
    path: '/node-editor',
    component: NodeEditor,
  },
  {
    name: 'nodeConfig',
    path: '/node-config',
    component: NodeConfig,
  },
];

const router = new Router({ routes });

export default router;
