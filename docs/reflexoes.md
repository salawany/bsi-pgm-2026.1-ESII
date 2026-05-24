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

As subclasses Notebook, Projetor e Cabo respeitam o contrato definido pela classe base Equipamento.

Em todos os casos:
- calcular_multa(0) retorna 0.0;
- calcular_multa(-5) também retorna 0.0;
- nenhuma das subclasses lança exceções inesperadas.

O contrato da classe base define que o método deve retornar um valor float maior ou igual a zero, sem gerar erros durante a execução. As subclasses mantêm esse comportamento corretamente.

Dessa forma, o princípio LSP (Liskov Substitution Principle) é satisfeito, pois qualquer subclasse pode substituir a classe Equipamento sem quebrar o funcionamento do ServicoEmprestimo.

## Aula 06 — DIP

Antes da aplicação do DIP, o ServicoEmprestimo criava diretamente suas dependências internas, como o repositório e o notificador. Isso fazia com que o módulo ficasse fortemente acoplado às implementações concretas, dificultando testes e alterações futuras.

Com a inversão de dependência, o serviço passou a apenas receber essas dependências pelo construtor. Dessa forma, ele deixou de controlar a criação dos objetos e passou a consumir recursos fornecidos externamente. Essa mudança não é apenas técnica, mas também conceitual, pois o módulo principal deixa de depender diretamente de detalhes de implementação.

Segundo Valente, no Capítulo 5 de Engenharia de Software Moderna, o DIP estabelece que módulos de alto nível não devem depender de módulos de baixo nível, mas sim de abstrações. Na prática, isso reduz acoplamento e aumenta flexibilidade no sistema.

Além disso, a aplicação do DIP permitiu criar versões falsas do repositório e do notificador para testes isolados, sem necessidade de acessar componentes reais. Isso melhora a testabilidade e facilita a manutenção do código.o.
