export const menuList = [
  // just use icons only from material design https://materialdesignicons.com/
  {
    title: 'Sistema',
    component: 'system',
    icon: 'home',
    path: '/system',
    children: [
      {
        tile: 'Inicio',
        path: '/',
      }
  }

];

export function getCategoryList() {
  return [...new Set(menuList.map((description) => description.category))];
}

export function getDescription(nodeType) {
  const description = menuList.find((descr) => descr.type === nodeType);

  if (description) return description.text;
  return 'No description provided for node';
}

export function getTags(nodeType) {
  const description = menuList.find((descr) => descr.type === nodeType);

  if (description) return description.tags;
  return [];
}
