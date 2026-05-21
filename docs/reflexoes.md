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

A hierarquia criada aplicou o princípio OCP usando polimorfismo. Cada equipamento passou a calcular sua própria multa, eliminando os blocos if/elif do sistema. Isso deixou o código mais organizado, fácil de manter e aberto para novos tipos de equipamentos sem precisar alterar o serviço principal.

Porém, se surgirem regras muito diferentes, como multa por hora ou dependendo do dia da semana, apenas criar subclasses talvez não seja suficiente. Nesse caso, seria necessário reorganizar melhor a lógica do sistema.

Segundo Valente, no Capítulo 5, o OCP deve ser aplicado com cuidado, pois muitas abstrações podem aumentar a complexidade do código em vez de simplificar.

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
