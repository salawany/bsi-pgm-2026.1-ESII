# ADR-001: Escolha da Arquitetura do Sistema

**Status:** Accepted

**Data:** 2026-04-22

## Contexto

O sistema de empréstimo de equipamentos (v1.0) concentra toda a lógica em um único arquivo (`emprestimos.py`). Os requisitos não funcionais do `requisitos.md` exigem:

- **RNF03:** a adição de um novo tipo de equipamento não deve exigir alterações em mais de um módulo do sistema.
- **RNF04:** os módulos de regra de negócio devem poder ser testados de forma isolada, sem dependência de entrada do usuário ou estado externo.

A v1.0 não atende nenhum dos dois.

## Opções consideradas

| Critério | Arquivo único | Em camadas | MVC |
|---|---|---|---|
| Atende RNF03 (novo tipo sem modificar múltiplos módulos)? | Não | Sim | Parcial |
| Atende RNF04 (testar regras sem estado externo)? | Não | Sim | Parcial |
| Adequado para CLI sem interface gráfica? | Sim | Sim | Overengineering |
| Familiar para equipe iniciante? | Sim | Sim | Parcial |

- **Arquivo único:** descartado — impossibilita RNF03 e RNF04.
- **MVC:** descartado — concebido para interfaces gráficas; gera abstração desnecessária (View/Controller) para uma CLI simples e introduz vocabulário com o qual a equipe ainda não tem fluência.
- **Em camadas:** atende os dois RNFs, é adequado para CLI e tem complexidade compatível com uma equipe iniciante.

## Decisão

Adotar arquitetura em camadas com quatro camadas:

- `main.py` — interface: menu CLI, sem regra de negócio
- `services/` — negócio: todas as regras aqui, sem conhecimento de interface ou persistência
- `repositories/` — dados: toda persistência em memória aqui, o serviço não acessa dados diretamente
- `models/` — entidades: representações do domínio, sem lógica de negócio

## Consequências

- Adicionar uma nova forma de entrada (ex.: leitura de arquivo em lote) = reescrever apenas `main.py`
- Trocar persistência (memória → banco) = reescrever apenas `repositories/`
- Regras de negócio em `services/` ficam isoladas e testáveis (RNF04 atendido)
- Adicionar novo tipo de equipamento = nova classe em `models/`, sem tocar em `services/` (RNF03 atendido)
