# Data Relationships

Este documento registra os relacionamentos identificados entre os datasets do projeto.

Neste estágio, os relacionamentos são considerados **hipóteses técnicas** baseadas nos nomes e estruturas dos campos. A cardinalidade e a integridade referencial serão confirmadas através do profiling.

---

## Visão geral

```text
                    ┌──────────────┐
                    │   bairros    │
                    │              │
                    │ PK codigo    │
                    └──────┬───────┘
                           │
             codigo_bairro │
                           │
                           ▼
                    ┌──────────────┐
                    │ concorrentes │
                    │              │
                    │ PK codigo    │
                    └──────┬───────┘
                           │
         codigo_concorrente│
                           │
                           ▼
                    ┌──────────────┐
                    │   eventos    │
                    │              │
                    │ PK codigo    │
                    └──────────────┘


                    ┌──────────────┐
                    │  populacao   │
                    │              │
                    │ codigo       │
                    └──────┬───────┘
                           │
                           │ codigo
                           ▼
                    ┌──────────────┐
                    │   bairros    │
                    └──────────────┘
```

---

## Relacionamento 1 — população → bairros

### Campos

```text
populacao.codigo
        ↓
bairros.codigo
```

### Hipótese

O campo `populacao.codigo` aparentemente representa um código associado ao cadastro de bairros.

### Validações necessárias

Devemos verificar:

* quantidade de códigos distintos em `populacao`;
* quantidade de códigos distintos em `bairros`;
* códigos de população inexistentes em bairros;
* bairros sem registro correspondente em população;
* duplicidade de `populacao.codigo`;
* percentual de valores nulos.

### Cardinalidade

Ainda não definida.

---

## Relacionamento 2 — concorrentes → bairros

### Campos

```text
concorrentes.codigo_bairro
        ↓
bairros.codigo
```

### Hipótese

Um concorrente pode estar associado a um bairro.

A relação esperada inicialmente é:

```text
bairros 1 ───────── N concorrentes
```

### Validações necessárias

Devemos verificar:

* percentual de `codigo_bairro` nulo;
* códigos existentes em `concorrentes` que não existem em `bairros`;
* quantidade de concorrentes por bairro;
* possibilidade de múltiplos concorrentes no mesmo bairro;
* consistência entre município do concorrente e município do bairro.

### Observação

O campo `concorrentes.codigo_bairro` foi identificado como `double`, enquanto `bairros.codigo` é inteiro.

Esse ponto deve ser analisado antes da implementação da regra de integridade referencial.

---

## Relacionamento 3 — eventos → concorrentes

### Campos

```text
eventos_de_fluxo.codigo_concorrente
        ↓
concorrentes.codigo
```

### Hipótese

Cada evento de fluxo está associado a um concorrente.

A relação esperada inicialmente é:

```text
concorrentes 1 ───────── N eventos
```

### Validações necessárias

Devemos verificar:

* percentual de `codigo_concorrente` nulo;
* códigos de concorrentes presentes nos eventos mas ausentes no cadastro;
* quantidade de eventos por concorrente;
* concorrentes sem eventos;
* distribuição temporal dos eventos.

---

## Chaves candidatas

| Dataset            | Campo    | Status                       |
| ------------------ | -------- | ---------------------------- |
| `bairros`          | `codigo` | Candidata a chave            |
| `populacao`        | `codigo` | Candidata a chave/referência |
| `concorrentes`     | `codigo` | Candidata a chave            |
| `eventos_de_fluxo` | `codigo` | Candidata a chave            |

Nenhuma chave deve ser considerada definitivamente validada antes da execução do profiling.

---

## Integridade referencial

As seguintes regras são candidatas a serem implementadas posteriormente:

```text
populacao.codigo
    ∈
bairros.codigo
```

```text
concorrentes.codigo_bairro
    ∈
bairros.codigo
```

```text
eventos_de_fluxo.codigo_concorrente
    ∈
concorrentes.codigo
```

A regra deverá considerar valores nulos separadamente. Um campo nulo pode representar ausência de relacionamento opcional e não necessariamente uma violação de integridade referencial.

---

## Cardinalidade

A cardinalidade inicial esperada é:

```text
bairros 1 ─── N concorrentes

concorrentes 1 ─── N eventos_de_fluxo
```

A relação entre `populacao` e `bairros` permanece pendente de confirmação.

---

## Próxima etapa

A próxima etapa deverá executar profiling específico para os relacionamentos.

O objetivo será substituir as hipóteses deste documento por evidências quantitativas, como:

* número de chaves;
* percentual de correspondência;
* percentual de órfãos;
* percentual de nulos;
* duplicidades;
* cardinalidade observada.

Somente depois dessa análise as regras de integridade referencial deverão ser formalizadas em `docs/data-quality/quality-rules.md`.
