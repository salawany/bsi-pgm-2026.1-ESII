# ADR-NNN: Decisão da arquitetura aplicada

**Status:** Accepted
**Data:** 2026-04-26

## Contexto
É necesário um código em que a adição de um novo tipo de equipamento não exija alterações em mais de um módulo do sistema. E que 
Os módulos de regra de negócio devem poder ser testados de forma isolada, sem dependência de entrada do usuário ou estado externo.

RNF03 — Manutenibilidade

RNF04 — Testabilidade

## Opções consideradas

Arquivo único
Simples de implementar, porém não atende bem aos requisitos de extensibilidade e testabilidade. (Descarte)


Em camadas
Melhora a organização e separação de responsabilidades, facilitando manutenção e testes. (Resolve)


MVC
Oferece boa separação e testabilidade, porém adiciona maior complexidade. (Descarte)

## Decisão

Foi decidido o uso em camadas, uma vez que há equilíbrio entre organização, testabilidade e baixo custo de complexidade para a equipe.


O sistema será dividido nas seguintes camadas:


- interface: responsável pela interação com o usuário (CLI)
- aplicacao: responsável pelo controle do fluxo da aplicação
- dominio: responsável pelas regras de negócio

## Consequências
A organização em camadas melhora a manutenção, facilita testes e reduz o acoplamento, mas adiciona uma complexidade inicial ao projeto/equipe.
