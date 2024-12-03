O variante multifuncional é um projeto que tentaram implementar na Scania durante vários anos, porém sem sucesso devido a sua complexidade, contudo, eu mostrei que era possível fazer esse projeto de maneira fácil e rápida usando python como a base de programação e também utilizado o Teams como ferramenta de comunicação.

O projeto visa a segurança do colaborador, assim como a qualidade do produto e a qualidade do processo.

Na fábrica temos uma pessoa por cada área responsável por uma montagem complexa, ela é chamada de variante, ele tem como foco ajudar o processo quando se passa veículos complexos na linha de montagem (caminhões a gás, com motor V8, 8x2/8x4, etc).
Porém foi notado que havia um desbalanço muito grande entre áreas, onde uma área estava livre de caminhões complexos, e outra com diversos gargalos, então surgiu o termo variante multifuncional, irá ser a pessoa responsável por ajudar outras áreas quando as mesmas estiverem passando por problemas, como o "bottleneck".

Foi desenvolvido um script que tem como objetivo de avisar os variantes multifuncionais onde está precisando de ajuda, então foi desenvolvido o código visando esse objetivo, nele é possivel:

- Monitorar a linha de produção em tempo real.
- Escolher qual variante cada área irá querer ser ajudada.
- Quando precisar de ajuda, o script irá identificar as áreas com bottleneck e será mandado uma mensagem na equipe do Teams avisando os variants multifuncionais quem irá ajudar e onde irão ajudar.
- Na própria mensagem do Teams, irá ter dois botões onde só a pessoa mencionada irá conseguir "clicar" onde irá ter as opções "consigo ajudar" e "não consigo ajudar", lembrando que quando a resposta for negativa, irá abrir uma caixa de mensagem onde a pessoa precisa explicar por qual motivo não conseguiu ajudar, gerando um report geral todo final do mês onde será apresentado para todos no briefing 
