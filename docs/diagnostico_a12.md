# Diagnóstico Aula 12

## 1. services/servico_emprestimo.py

**Smell:** Primitive Obsession

**Refactoring proposto:** Replace Primitive with Object

**Justificativa:** Os eventos eram representados por dicionários, sem um tipo próprio definido. Isso dificultava a validação dos dados e aumentava o risco de erros de chave.


## 2. services/servico_emprestimo.py

**Smell:** Mysterious Name

**Refactoring proposto:** Rename

**Justificativa:** A variável `atraso` foi renomeada para `dias_atraso`, deixando mais claro o significado do valor armazenado.


## 3. services/servico_emprestimo.py

**Smell:** Long Method

**Refactoring proposto:** Extract Function

**Justificativa:** O método `listar_atrasados()` realizava cálculo, impressão e notificação. Parte dessa responsabilidade foi extraída para o método `_imprimir_atraso()`.


## 4. services/notificador_email.py

**Smell:** Primitive Obsession

**Refactoring proposto:** Replace Primitive with Object

**Justificativa:** O observer acessava informações por meio de chaves de dicionário. A utilização da classe `Evento` tornou a estrutura mais clara e tipada.


## 5. models/equipamento.py

**Smell:** Smell aparente — Data Class (não refatorado)

**Refactoring proposto:** Nenhum

**Justificativa:** As classes `Notebook`, `Projetor` e `Cabo` ficaram vazias após a aplicação do padrão Strategy. Apesar de parecerem Data Classes, elas continuam representando tipos distintos do domínio e removê-las desfaria a solução adotada na Aula 11.
