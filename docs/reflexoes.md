# Reflexões

## Aula 04 — SRP

A fronteira mais difícil de tomar foi a separação entre
**`ServicoEmprestimo` e `Notificador`**. Em uma primeira leitura do
`emprestimos.py`, parecia natural manter o envio de e-mail dentro do
método `devolver`: afinal, "notificar o usuário sobre a multa" parece
parte do mesmo fluxo de negócio. O critério que me fez decidir pela
separação veio de Valente Cap. 5, na seção sobre coesão: um módulo
coeso tem um único motivo para mudar. Olhando assim, ficou claro
que **o cálculo da multa muda por uma razão (regras de cobrança,
definidas pelo setor de patrimônio) e a notificação muda por outra
razão (canal de comunicação — hoje e-mail, amanhã SMS ou push)**.
Stakeholders distintos = motivos de mudança distintos = classes
distintas.

A dificuldade foi resistir à tentação de "facilitar agora": juntar
tudo no Service deixaria o código menor no curto prazo, mas qualquer
mudança futura em qualquer um dos lados (regra ou canal) forçaria
editar um método que faz duas coisas. Decidi pela separação aplicando
o "teste do *e*" — se preciso descrever a classe usando a palavra "e",
ela está fazendo demais. A versão final tem `ServicoEmprestimo`
coordenando regra de empréstimo e `Notificador` isolando o canal de
comunicação, conectados apenas pela chamada
`self.notificador.notificar_*` — interface mínima, evolução independente.

## Aula 05 — OCP

A hierarquia criada — `Notebook`, `Projetor` e `Cabo` herdando de
`Equipamento` — resolve o problema da variação por tipo: cada subclasse
fornece sua fórmula de multa sem que o `ServicoEmprestimo` precise
conhecer o tipo concreto. Para os equipamentos atuais, isso funciona e
atende o RNF01 (adição de novo tipo sem alterar o serviço).

O problema aparece quando o eixo de variação muda. Um equipamento com
multa calculada por hora, ou cuja política dependa do dia da semana,
não é uma nova subclasse do mesmo problema — é uma nova dimensão de
variação. Nesse caso, a hierarquia plana que criei precisaria ser
reestruturada: ou a lógica condicional voltaria ao `calcular_multa`, ou
haveria uma proliferação de subclasses como `NotebookFimDeSemana`.
Valente (Cap. 5) aponta esse risco ao lembrar que "o OCP é mais útil
quando existe um número limitado e conhecido de variações" — encapsular
variações hipotéticas viola YAGNI e gera complexidade sem retorno
imediato.

Para o cenário das multas por hora ou por dia da semana, uma solução
mais robusta seria separar a política de cobrança do tipo de
equipamento, talvez com um objeto `PoliticaMulta` injetado em
`Equipamento`. Com os tipos atuais — fixos e estáveis — a hierarquia
presente é suficiente e não exige reestruturação.

## Aula 06 — Verificação de LSP

O contrato de `Equipamento.calcular_multa(dias_atraso: int) -> float`
estabelece retorno do tipo `float >= 0.0`, sem lançamento de exceção.

**`Notebook`:** `calcular_multa(0)` → `max(0.0, 0 * 10.0)` = `0.0` ✓;
`calcular_multa(-5)` → `max(0.0, -50.0)` = `0.0` ✓. Nenhuma exceção
possível. LSP satisfeito.

**`Projetor`:** `calcular_multa(0)` → `0.0` ✓; `calcular_multa(-5)` →
`0.0` ✓. LSP satisfeito.

**`Cabo`:** `calcular_multa(0)` → `0.0` ✓; `calcular_multa(-5)` →
`0.0` ✓. LSP satisfeito.

As três subclasses honram o contrato. O `ServicoEmprestimo` pode
receber qualquer `Equipamento` e chamar `calcular_multa` com qualquer
inteiro sem risco de exceção ou valor negativo.

## Aula 06 — DIP

Antes da alteração, o `ServicoEmprestimo` criava internamente seu
repositório e seu notificador. Isso significa que ele não apenas
*usava* essas dependências — ele *decidia qual* usar. A dependência
era unidirecional e apontava para baixo: a camada de serviço
controlava quem a implementava.

Com a injeção, essa relação se inverte. O `ServicoEmprestimo` agora
descreve o que precisa (um objeto com `buscar_equipamento`,
`salvar_emprestimo` etc.; outro com `notificar_*`) sem determinar quem
vai fornecê-lo. Quem instancia e injeta passa a ser o `main.py`.
Valente (Cap. 5) descreve exatamente esse movimento: módulos de alto
nível não devem depender de módulos de baixo nível; ambos devem
depender de abstrações.

A mudança não é só técnica. Conceitualmente, o `ServicoEmprestimo`
deixou de ser criador de infraestrutura e se tornou consumidor de
contratos. Quem decide agora é a camada mais externa — `main.py` —
que escolhe qual repositório e qual notificador fornecer. Na prática,
isso abre espaço para instanciar o serviço com um `RepositorioFalso`
que armazena dados em listas e um `NotificadorFalso` que registra
chamadas em vez de enviar e-mails. As regras de negócio ficam isoladas
da infraestrutura, que era exatamente o que o RNF02 exigia e que a
Aula 5 ainda não resolvia por completo.

## Aula 08 — Testes e Integração

Nesta atividade percebi como a aplicação do DIP facilitou a criação de testes. Como o ServicoEmprestimo depende de abstrações, foi possível testar o comportamento do sistema sem alterar a lógica principal. A criação das interfaces tornou o código mais desacoplado e preparado para evolução.

Também foi interessante utilizar o pytest para automatizar a validação das regras de negócio. Os testes permitiram verificar rapidamente se alterações no código afetavam funcionalidades já implementadas. O teste de integração ajudou a validar o fluxo completo de empréstimo e devolução, simulando um cenário próximo ao uso real da aplicação.

## Aula 09 — TDD

Comparando o teste TDD com o cenário BDD, acho que o BDD comunica melhor com um cliente não técnico, porque usa uma linguagem mais próxima do dia a dia. No cenário “Dado-Quando-Então”, dá para entender a regra sem precisar saber Python, assert ou estrutura de teste. Por exemplo, dizer que o usuário devolveu antes do prazo e recebeu desconto é mais claro para alguém que só quer validar a regra de negócio.

Já o TDD é melhor para quem está programando, porque mostra exatamente o que o código precisa retornar e ajuda a encontrar erro rápido quando algo quebra. Eu usaria BDD para conversar com cliente, professor ou colega que quer entender o comportamento esperado. Usaria TDD durante a implementação, porque ele guia o código em pequenos passos e deixa mais seguro mudar depois.

## Aula 10 — Factory e Facade

Na Factory, ainda existe uma decisão que relaciona o tipo do equipamento com a classe que será criada. Isso parece parecido com o problema dos vários if/elif discutidos anteriormente, mas a diferença é que agora essa decisão está concentrada em um único lugar. Antes, a criação dos objetos poderia ficar espalhada pelo sistema. Com a fábrica, caso seja necessário adicionar um novo tipo de equipamento, a alteração fica centralizada. Dessa forma, o restante do código continua desacoplado das classes concretas. Na prática, a fábrica "paga" esse acoplamento para evitar que ele se espalhe por todo o sistema. Conforme discutido por Valente (Cap. 6), esse padrão ajuda a organizar a criação de objetos e reduzir dependências entre módulos.

A Facade também não desfaz o DIP aplicado anteriormente. O Serviço de Empréstimo continua recebendo suas dependências por injeção, o que permite que os testes utilizem dublês normalmente. A diferença é que agora a montagem dos objetos concretos fica concentrada na chamada raiz de composição, representada pela classe SistemaDeEmprestimos. Assim, o main.py ficou mais simples e passou a conversar apenas com a fachada. Segundo Valente (Cap. 6), a Facade simplifica o acesso ao subsistema sem alterar suas responsabilidades internas. Por isso, os testes continuaram funcionando sem necessidade de modificações. 

## Aula 11 — Strategy e Observer

Na Aula 5, o cálculo da multa ficava dentro das classes Notebook, Projetor e Cabo. Funcionava bem para os valores atuais, mas qualquer nova regra de multa exigiria alterar ou criar novas classes. Com o padrão Strategy, o cálculo passou a ser responsabilidade das estratégias de multa, enquanto o Equipamento apenas delega essa tarefa. Na prática, percebi que ficou mais fácil trocar a regra sem mexer na estrutura principal do sistema. O OCP continua sendo respeitado, mas agora através da composição em vez da herança.

Já com o Observer, o ServicoEmprestimo deixou de enviar notificações diretamente. Agora ele apenas gera eventos, e os observers registrados decidem o que fazer com eles. Durante a atividade, isso ficou visível quando substituí o notificador antigo pelo NotificadorEmail e passei a registrar observers na fachada. Dessa forma, seria simples adicionar novos destinos, como SMS ou logs, sem alterar o serviço.

O uso de um dicionário para representar os eventos facilita a implementação, mas também pode causar erros por depender de chaves escritas manualmente. Mesmo assim, para esta atividade, a escolha ajudou a focar no entendimento do padrão Observer. Conforme discutido por Valente (Cap. 6), esses padrões contribuem para reduzir o acoplamento e tornar o sistema mais flexível para futuras mudanças.
