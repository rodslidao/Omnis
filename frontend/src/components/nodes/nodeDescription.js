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
  {
    name: 'Condicional OU',
    type: 'OrNode',
    text: `
            Com esse node você será capaz de fazer operações condicionais do tipo OU, ou seja, se uma das entradas for verdadeira, a saída será verdadeira.
        `,
    icon: 'set-merge',
    examples: 'quando você precisar de duas entradas em um nó',
    category: 'Lógica',
    tags: ['or', 'condition'],
    resettable: false,
    stoppable: false,
    configurable: false,
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
  {
    name: 'Alerta',
    type: 'AlertNode',
    text: `
           Esse node envia um alerta para o usuário
    `,
    icon: 'alert',
    examples: `
            Quando precisamos de um alerta para o usuário, como por exemplo, falha em determinado processo que a maquina num consegue prosseguir.
        `,
    category: 'Feedback',
    tags: ['alert', 'utilidades', 'utilidade', 'feedback', 'depuração'],
    resettable: true,
    stoppable: false,
    configurable: true,
    hasHistory: false,
  },
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
  {
    name: 'Portas I/O',
    type: 'IoNode',
    text: 'Com esse nó você consegue acionar uma porta I/O',
    icon: 'electric-switch',
    examples: 'Digamos que você queira acionar uma porta para acionar a solenoide de uma garra',
    category: 'Hardware',
    tags: ['io', 'hardware'],
    resettable: true,
    stoppable: false,
    configurable: true,
    hasHistory: false,
  },
  {
    name: 'Iniciar',
    type: 'StartNode',
    text: 'Esse node é capaz de iniciar o processo',
    icon: 'play',
    examples: 'Digamos que quando a pessoa apertar o botão de iniciar na tela inicial, é por esse nó que o processo vai começar a rodar',
    category: 'Entradas',
    tags: ['start', 'entradas'],
    resettable: false,
    stoppable: false,
    configurable: false,
    hasHistory: false,
  },
  {
    name: 'Parar',
    type: 'StopNode',
    text: 'Esse node é capaz de parar o processo, mas não é capaz de reiniciar da onde parou',
    icon: 'stop',
    examples: 'Digamos que houve uma falha em um determinado nó que não é possível continuar a montagem, ele para o processo',
    category: 'Entradas',
    tags: ['stop', 'entradas'],
    resettable: false,
    stoppable: false,
    configurable: false,
    hasHistory: false,
  },
  {
    name: 'Pausar',
    type: 'PauseNode',
    text: 'Esse node é capaz de pausar o processo, com a opção de continuar da onde parou',
    icon: 'pause',
    examples: 'Digamos que tenha dado erro em um determinado nó, e você queira pausar o processo até que você resolva o problema',
    category: 'Entradas',
    tags: ['pause', 'entradas'],
    resettable: false,
    stoppable: false,
    configurable: false,
    hasHistory: false,
  },
  {
    name: 'Reiniciar',
    type: 'RestartNode',
    text: 'Esse node é capaz de resetar o processo',
    icon: 'restart',
    examples: 'Digamos que você queira recomeçar o processo, mas não quer reiniciar da onde parou',
    category: 'Entradas',
    tags: ['reset', 'entradas'],
    resettable: false,
    stoppable: false,
    configurable: false,
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
