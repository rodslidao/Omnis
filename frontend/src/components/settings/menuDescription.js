export const menuList = [
  // just use icons only from material design https://materialdesignicons.com/
  {
    title: 'settings.system.name',
    icon: 'application',
    path: '/system',
    children: [
      {
        tile: 'Inicio',
        href: '/',
      },
    ],
  },
  // { title: 'settings.devices.name', icon: 'devices', path: '/devices' },
  { title: 'settings.process.name', icon: 'robot-industrial', path: '/process' },
  { title: 'settings.users.name', icon: 'account', path: '/users' },
  // { title: 'settings.networkAndInternet.name', icon: 'wifi', path: '/network' },
  // { title: 'settings.personalize.name', icon: 'brush', path: '/personalize' },
  // { title: 'settings.support.name', icon: 'handshake-outline', path: '/support' },
];

export function getCategoryList() {
  return [...new Set(menuList.map((description) => description.category))];
}
