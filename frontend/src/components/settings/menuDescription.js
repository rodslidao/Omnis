export const menuList = [
  // just use icons only from material design https://materialdesignicons.com/
  {
    title: 'Sistema',
    icon: 'application',
    path: '/system',
    children: [
      {
        tile: 'Inicio',
        href: '/',
      },
    ],
  },
  { title: 'Dispositivos', icon: 'devices', path: '/devices' },
  { title: 'Rede & Internet ', icon: 'wifi', path: '/network' },
  { title: 'Processo', icon: 'robot-industrial', path: '/process' },
  { title: 'Suporte', icon: 'handshake-outline', path: '/support' },
];

export function getCategoryList() {
  return [...new Set(menuList.map((description) => description.category))];
}
