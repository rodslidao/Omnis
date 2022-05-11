export const descriptions = [
  // just use icons only from material design https://materialdesignicons.com/
  // {
  //   name: 'Operações Matemáticas',
  //   type: 'math',
  //   text: `
  //           Com esse node você será capaz de fazer operações matemáticas
  //       `,
  //   icon: 'calculator-variant',
  //   examples: `Quando precisamos subtrair dar uma margem da lateral da maquina
  //   `,
  //   category: 'Utilidades',
  //   tags: ['json', 'mapping', 'object'],
  //   resettable: true,
  //   stoppable: false,
  //   configurable: true,
  //   hasHistory: false,
  // },
  {
    name: 'Matriz',
    type: 'MatrixNode',
    text: `Cria uma matriz a partir de um dados fornecidos na tela de cadastro de matrizes.
    `,
    icon: 'grid',
    examples: `
    Digamos que voce queira pegar um ovo em uma bandeja de 12 ovos e colocar em uma bandeja de 30 ovos.
    `,
    category: 'Utilidades',
    tags: ['matrix', 'mapping', 'object', 'array', 'img'],
    resettable: true,
    stoppable: false,
    configurable: true,
    hasHistory: false,
  },
  {
    name: 'Identificação',
    type: 'IdentifyNode',
    text: `
    Esse node irá identificar o objeto que está na imagem extraindo o máximo de informações possíveis, como; area, perímetro, diâmetro, raio, centro de massa, altura, largura e diagonal.
    `,
    icon: 'eye',
    examples: `
    Digamos que você queira saber o tamanho das manchas nos ovos
    `,
    category: 'Utilidades',
    tags: ['identification', 'mapping', 'object', 'array', 'img'],
    resettable: true,
    stoppable: false,
    configurable: true,
    hasHistory: false,
  },
  {
    name: 'Condicinal IF',
    type: 'IfNode',
    text: `
            Com esse node você será capaz de fazer operações condicionais
        `,
    icon: 'call-merge',
    examples: `Se por exemplo a Entrada 'A' for maior que a 'B', você pode definir a saída de acordo com a condição
    `,
    category: 'Lógica',
    tags: ['if', 'condition', 'if-else', 'else'],
    resettable: true,
    stoppable: false,
    configurable: true,
    hasHistory: false,
  },
  // {
  //   name: 'Blur (Borrar)',
  //   type: 'filter-blur',
  //   text: `
  //           Esse node é capaz de borrar uma imagem
  //       `,
  //   icon: 'blur',
  //   examples: `Esse filtro é util quando precisamos suavizar uma borda que é imperfeita
  //   `,
  //   category: 'Filtros',
  //   tags: ['filter', 'blur', 'borrar', 'borrado', 'imagem', 'filtros'],
  //   resettable: true,
  //   stoppable: false,
  //   configurable: true,
  //   hasHistory: false,
  // },
  // {
  //   name: 'Detecção de Borda',

  //   type: 'filter-canny',
  //   text: `
  //           Esse node é capaz de detectar bordas de uma imagem
  //       `,
  //   icon: 'border-all-variant',
  //   examples: `
  //           Esse filtro é util quando precisamos detectar bordas de uma imagem
  //       `,
  //   category: 'Filtros',
  //   tags: ['filter', 'canny', 'bordas', 'imagem', 'filtros'],
  //   resettable: true,
  //   stoppable: false,
  //   configurable: true,
  //   hasHistory: false,
  // },
  {
    name: 'Cor (HSV)',
    type: 'HsvFilterNode',
    text: `
    Esse filtro é usado para pegar regiões com uma determinada cor em uma imagem.
    `,
    icon: 'palette',
    examples: `
     Digamos que você queira ver se os ovos estão na cor vermelhos ou brancos, sabendo quais são os ovos vermelhos, saberemos os bancos`,
    category: 'Filtros',
    tags: ['filter', 'hsv', 'cor', 'imagem', 'filtros'],
    resettable: true,
    stoppable: false,
    configurable: true,
    hasHistory: false,
  },
  // {
  //   name: 'Comunicação Serial',
  //   type: 'serial',
  //   text: `
  //           Esse node é capaz de enviar dados para um arduino
  //       `,
  //   icon: 'serial-port',
  //   examples: `
  //           Esse node é capaz de enviar dados para um arduino
  //       `,
  //   category: 'Hardware',
  //   tags: ['serial', 'arduino', 'comunicação', 'comunicacao'],
  //   resettable: true,
  //   stoppable: false,
  //   configurable: true,
  //   hasHistory: false,
  // },
  {
    name: 'Camera',
    type: 'CameraNode',
    text: `
            Esse node é capaz de capturar uma imagem da camera
        `,
    icon: 'camera',
    examples: `
            Digamos que você queira capturar uma imagem da camera para fazer a identificação de algum ovo em uma bandeja de ovos.
        `,
    category: 'Hardware',
    tags: ['camera', 'hardware', 'comunicação', 'comunicacao'],
    resettable: true,
    stoppable: false,
    configurable: true,
    hasHistory: false,
  },
  // {
  //   name: 'Alerta',
  //   type: 'alert',
  //   text: `
  //          Esse node envia um alerta para o usuário
  //   `,
  //   icon: 'alert',
  //   examples: `
  //           Se precisar enviar um alerta para quando precisar de uma ajuda ou algo do tipo
  //       `,
  //   category: 'Feedback',
  //   tags: ['alert', 'utilidades', 'utilidade', 'feedback', 'depuração'],
  //   resettable: true,
  //   stoppable: false,
  //   configurable: true,
  //   hasHistory: false,
  // },
  // {
  //   name: 'log',
  //   type: 'log',
  //   text: ` Esse armazena a informação toda vez que passa pelo node.
  //   `,
  //   icon: 'console-line',
  //   examples: `
  //           Caso você queira ver o resultado de uma operação matemática toda vez que passe a informação por aquele node
  //       `,
  //   category: 'Feedback',
  //   tags: ['log', 'utilidades', 'utilidade', 'feedback', 'depuração'],
  //   resettable: true,
  //   stoppable: false,
  //   configurable: true,
  //   hasHistory: false,
  // },
  // {
  //   name: 'Botão',
  //   type: 'button',
  //   text: 'Esse node é capaz de criar um botão',
  //   icon: 'gesture-tap-button',
  //   examples: 'A ação vai iniciar assim que o botão  for clicado',
  //   category: 'Entradas',
  //   tags: ['button', 'utilidades', 'utilidade', 'feedback', 'depuração'],
  //   resettable: true,
  //   stoppable: false,
  //   configurable: true,
  //   hasHistory: false,
  // },
  // {
  //   name: 'Texto',
  //   type: 'text-template',
  //   text: 'Esse node é capaz de criar um texto',
  //   icon: 'text',
  //   examples: 'A ação vai iniciar assim que o botão  for clicado',
  //   category: 'Entradas',
  //   tags: ['text', 'utilidades', 'utilidade', 'feedback', 'depuração'],
  //   resettable: true,
  //   stoppable: false,
  //   configurable: true,
  //   hasHistory: false,
  // },
  {
    name: 'Mover Eixo',
    type: 'MoveAxisNode',
    text: 'Esse node é capaz de mover um eixo',
    icon: 'axis-arrow',
    examples: 'A ação vai iniciar assim que o botão  for clicado',
    category: 'Hardware',
    tags: ['move', 'axis', 'hardware'],
    resettable: true,
    stoppable: false,
    configurable: true,
    hasHistory: false,
  },
];

export function getCategoryList() {
  return [...new Set(descriptions.map((description) => description.category))];
}

export function getDescription(nodeType) {
  const description = descriptions.find((descr) => descr.type === nodeType);

  if (description) return description.text;
  return 'No description provided for node';
}

export function getTags(nodeType) {
  const description = descriptions.find((descr) => descr.type === nodeType);

  if (description) return description.tags;
  return [];
}
