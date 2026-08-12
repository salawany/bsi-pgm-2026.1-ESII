# Production Readiness Checklist

## 1. Pipeline e qualidade

| Item                                        | Status     | Esforço   | Prioridade | Observação                                                                                               |
| ------------------------------------------- | ---------- | --------- | ---------- | -------------------------------------------------------------------------------------------------------- |
| Testes automatizados executados a cada push | ✅ OK       | feito     | alta       | O GitHub Actions executa os testes automaticamente a cada push.                                          |
| Lint com Ruff integrado ao pipeline         | ✅ OK       | feito     | alta       | O Ruff está configurado no `pyproject.toml` e é executado pela CI.                                       |
| Gate de cobertura mínima de 80%             | ⚠️ PARCIAL | 2–4 horas | alta       | A cobertura atingiu o mínimo de 80%, mas ainda existem partes do sistema com baixa ou nenhuma cobertura. |
| Testes de integração do fluxo principal     | ✅ OK       | feito     | média      | Existe teste de integração para o fluxo completo de empréstimo.                                          |

## 2. Containerização

| Item                                                     | Status     | Esforço       | Prioridade | Observação                                                                                                     |
| -------------------------------------------------------- | ---------- | ------------- | ---------- | -------------------------------------------------------------------------------------------------------------- |
| Receita de build com Dockerfile                          | ❌ FALTA    | 2–4 horas     | média      | O projeto não possui atualmente um `Dockerfile`.                                                               |
| Build reprodutível da aplicação                          | ⚠️ PARCIAL | 2–4 horas     | média      | Existem dependências de desenvolvimento, mas ainda não existe uma imagem que padronize o ambiente de execução. |
| Execução do container sem root                           | ❌ FALTA    | 1–2 horas     | baixa      | Não há configuração de usuário não privilegiado porque ainda não existe containerização.                       |
| Exclusão de arquivos desnecessários do contexto de build | ❌ FALTA    | 30 min–1 hora | baixa      | Não existe `.dockerignore`, pois ainda não há uma receita de build com Docker.                                 |

## 3. Persistência

| Item                                               | Status  | Esforço  | Prioridade | Observação                                                                                                 |
| -------------------------------------------------- | ------- | -------- | ---------- | ---------------------------------------------------------------------------------------------------------- |
| Empréstimos sobrevivem ao encerramento do programa | ❌ FALTA | 1–2 dias | alta       | Os empréstimos são mantidos em memória. Ao finalizar o processo, os dados são perdidos.                    |
| Disponibilidade dos equipamentos é persistida      | ❌ FALTA | 1–2 dias | alta       | A disponibilidade é alterada durante a execução, mas não existe persistência em banco de dados ou arquivo. |
| Backup e recuperação dos dados                     | ❌ FALTA | 1–2 dias | média      | Não existe mecanismo de backup ou recuperação dos dados.                                                   |
| Cadastro dos equipamentos é persistido             | ❌ FALTA | 1–2 dias | média      | Os equipamentos também não possuem persistência externa.                                                   |

## 4. Segurança

| Item                                           | Status     | Esforço   | Prioridade | Observação                                                                                                                                       |
| ---------------------------------------------- | ---------- | --------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Credenciais fora do código-fonte               | ⚠️ PARCIAL | 2–4 horas | alta       | Não foram identificadas credenciais reais no código, mas ainda não existe uma estratégia formal de gerenciamento de segredos.                    |
| Validação das entradas                         | ⚠️ PARCIAL | 4–8 horas | alta       | Existem verificações para equipamentos inválidos ou indisponíveis, mas nome, e-mail e quantidade de dias poderiam ter validações mais completas. |
| Dependências fixadas                           | ⚠️ PARCIAL | 2–4 horas | média      | O Ruff está fixado em uma versão específica, mas outras dependências ainda utilizam versões mínimas.                                             |
| Auditoria de vulnerabilidades das dependências | ❌ FALTA    | 2–4 horas | média      | Não existe atualmente uma etapa específica no pipeline para auditoria de vulnerabilidades.                                                       |

## 5. Observabilidade

| Item                                  | Status     | Esforço   | Prioridade | Observação                                                                                                       |
| ------------------------------------- | ---------- | --------- | ---------- | ---------------------------------------------------------------------------------------------------------------- |
| Logs estruturados com nível e destino | ❌ FALTA    | 4–8 horas | alta       | O sistema utiliza `print()` para mensagens, sem níveis de log ou destino persistente.                            |
| Métricas da aplicação                 | ❌ FALTA    | 1 dia     | média      | Não existem métricas para acompanhar empréstimos, devoluções, atrasos ou falhas.                                 |
| Investigação de falhas anteriores     | ❌ FALTA    | 1 dia     | alta       | Sem logs persistentes, não é possível investigar adequadamente uma falha ocorrida anteriormente.                 |
| Notificações de eventos monitoradas   | ⚠️ PARCIAL | 4–8 horas | média      | O sistema possui Observer e `NotificadorEmail`, mas ainda seria necessário monitorar a entrega das notificações. |

## 6. Deployment

| Item                                              | Status     | Esforço   | Prioridade | Observação                                                                                              |
| ------------------------------------------------- | ---------- | --------- | ---------- | ------------------------------------------------------------------------------------------------------- |
| Processo automatizado de publicação               | ❌ FALTA    | 1–2 dias  | média      | O GitHub Actions valida o código, mas ainda não realiza deployment automático.                          |
| Processo definido para disponibilizar nova versão | ⚠️ PARCIAL | 4–8 horas | média      | Existe CI para validar alterações, mas ainda não existe um fluxo completo de homologação e publicação.  |
| Plano de rollback                                 | ❌ FALTA    | 4–8 horas | alta       | Não existe um procedimento documentado e automatizado para retornar à versão anterior em caso de falha. |
| Separação entre ambiente de teste e produção      | ⚠️ PARCIAL | 4–8 horas | média      | A CI realiza validações, mas não existem ambientes separados de homologação e produção.                 |

## Síntese executiva

Para tornar o sistema production-ready, eu atacaria primeiro a **persistência**, em segundo lugar a **observabilidade** e em terceiro a **segurança**. A persistência é a primeira prioridade porque atualmente os empréstimos e a disponibilidade dos equipamentos ficam em memória. Se o processo for encerrado, essas informações são perdidas, o que representa um risco direto para o funcionamento do sistema. O segundo item seria observabilidade, principalmente a substituição dos `print()` por logs estruturados. Isso permitiria identificar erros e entender o comportamento da aplicação depois que ela estiver em execução. Em terceiro lugar, eu reforçaria a segurança com validação das entradas, gerenciamento de credenciais e maior controle das dependências.

Existe uma dependência importante entre essas ações. A **persistência deve vir antes de uma evolução mais completa da observabilidade e do deployment**, porque não faz sentido colocar o sistema em produção sem garantir primeiro que os dados dos empréstimos serão preservados. Depois, os logs e métricas ajudam a acompanhar a aplicação persistente e fornecem informações para operar e corrigir problemas em produção. Fazer o deployment antes dessas etapas aumentaria o risco de colocar um sistema que pode perder dados e cuja falha seria difícil de investigar.

A containerização pode esperar inicialmente. Ela é importante para padronizar o ambiente e facilitar o deployment, mas, considerando o risco atual, a perda de dados e a falta de observabilidade são problemas mais críticos. Depois que essas bases estiverem resolvidas, Docker e um processo de deployment com rollback podem ser implementados com menor risco.

Essa ordem segue a ideia de priorizar os riscos mais relevantes e suas dependências, em vez de tentar implementar todas as melhorias ao mesmo tempo, conforme a abordagem de qualidade e evolução de software discutida por Valente no Capítulo 10.

Essa decisão também considera a relação entre risco, esforço e dependências, priorizando primeiro os problemas que podem comprometer diretamente os dados e a operação do sistema.
