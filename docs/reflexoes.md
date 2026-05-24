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

Ao revisar as subclasses Notebook, Projetor e Cabo, foi possível perceber que todas seguem o comportamento esperado pela classe base Equipamento. Nos testes feitos, calcular_multa(0) retornou 0.0 e calcular_multa(-5) também não gerou valores negativos nem erros inesperados.

Cada subclasse implementa o cálculo de multa de forma diferente, mas todas mantêm o contrato definido na superclasse: retornar um valor do tipo float maior ou igual a zero. Nenhuma delas lança exceções durante o uso normal do sistema.

Isso é importante porque o ServicoEmprestimo utiliza os equipamentos sem precisar saber qual tipo específico está sendo usado. O serviço apenas chama calcular_multa(), confiando que qualquer subclasse vai responder corretamente.

Dessa forma, o princípio LSP é respeitado, já que Notebook, Projetor e Cabo podem substituir Equipamento sem alterar o funcionamento do sistema ou causar comportamentos inesperados.

## Aula 06 — DIP

Antes da aplicação do DIP, o ServicoEmprestimo criava diretamente o RepositorioEmprestimo e o Notificador dentro do construtor. Isso fazia com que o serviço ficasse preso a essas implementações específicas, aumentando o acoplamento entre os módulos.

Depois da alteração, o serviço passou a receber essas dependências pelo construtor. Na prática, isso mudou a forma como os módulos se relacionam, porque agora o ServicoEmprestimo não controla mais a criação dos objetos que utiliza. Essa responsabilidade passou para o main.py, que instancia e entrega as dependências prontas.

A mudança não foi apenas técnica, relacionada aos parâmetros do construtor, mas também conceitual. Antes, o módulo principal dependia diretamente de implementações concretas. Agora, ele atua mais como consumidor das dependências, tornando o código mais flexível e fácil de modificar.

Segundo Valente, no Capítulo 5 de Engenharia de Software Moderna, a inversão de dependência busca reduzir o acoplamento entre módulos de alto e baixo nível. Isso também facilita testes isolados, já que agora seria possível utilizar versões falsas do repositório e do notificador sem alterar o funcionamento do serviço.
