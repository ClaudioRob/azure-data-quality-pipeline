# Datasets

Este documento descreve as fontes de dados utilizadas pelo projeto `azure-data-quality-pipeline`.

Os datasets atualmente disponíveis estão armazenados em `data/raw/` e são utilizados como entrada para as etapas de profiling, validação e processamento.

## Visão geral

| Dataset                   | Formato  | Localização | Descrição                                  |
| ------------------------- | -------- | ----------- | ------------------------------------------ |
| `bairros.csv`             | CSV      | `data/raw/` | Cadastro de bairros                        |
| `populacao.json`          | JSON     | `data/raw/` | Dados populacionais associados a códigos   |
| `concorrentes.parquet`    | Parquet  | `data/raw/` | Cadastro de concorrentes                   |
| `eventos_de_fluxo.csv.gz` | CSV GZIP | `data/raw/` | Eventos de fluxo associados a concorrentes |

---

## 1. bairros.csv

### Descrição

Dataset contendo informações cadastrais e geográficas de bairros.

### Formato

CSV separado por vírgulas.

### Schema identificado

| Campo       | Tipo observado | Nullable | Descrição inicial        |
| ----------- | -------------- | -------: | ------------------------ |
| `codigo`    | inteiro        |      Sim | Identificador do bairro  |
| `nome`      | string         |      Sim | Nome do bairro           |
| `municipio` | string         |      Sim | Município                |
| `uf`        | string         |      Sim | Unidade federativa       |
| `area`      | decimal/número |      Sim | Área associada ao bairro |

### Exemplo

```text
codigo,nome,municipio,uf,area
355620110,Observatório,Valinhos,SP,68.0009
3519071024,Rp 6-24,Hortolândia,SP,0.981768
3536505002,Jardim De Itapoan,Paulínia,SP,0.808537
```

### Pontos de atenção

Durante a análise inicial, os seguintes aspectos foram identificados como candidatos a validação:

* unicidade de `codigo`;
* preenchimento de `codigo`;
* preenchimento de `nome`;
* preenchimento de `municipio`;
* domínio de `uf`;
* valores positivos para `area`;
* possíveis duplicidades cadastrais.

---

## 2. populacao.json

### Descrição

Dataset contendo informações de população associadas a códigos.

### Formato

JSON contendo uma coleção de objetos.

### Schema identificado

| Campo       | Tipo observado | Nullable | Descrição inicial             |
| ----------- | -------------- | -------: | ----------------------------- |
| `codigo`    | inteiro        |      Sim | Código de referência          |
| `populacao` | inteiro        |      Sim | População associada ao código |

### Exemplo

```json
{
  "codigo": 3519071,
  "populacao": null
}
```

### Pontos de atenção

Foi identificado durante a exploração inicial pelo menos um registro com:

```text
populacao = null
```

A relação entre `populacao.codigo` e `bairros.codigo` deverá ser confirmada por profiling.

Também deverão ser avaliados:

* unicidade de `codigo`;
* valores nulos;
* valores negativos;
* tipo e escala de `populacao`;
* integridade referencial;
* existência de códigos sem correspondência em `bairros`.

---

## 3. concorrentes.parquet

### Descrição

Dataset contendo informações cadastrais de concorrentes.

### Formato

Apache Parquet.

### Volume inicial observado

**4.202 registros.**

### Schema identificado

| Campo           | Tipo observado | Nullable | Descrição inicial            |
| --------------- | -------------- | -------: | ---------------------------- |
| `codigo`        | long           |      Sim | Identificador do concorrente |
| `nome`          | string         |      Sim | Nome do concorrente          |
| `categoria`     | string         |      Sim | Categoria do estabelecimento |
| `faixa_preco`   | long           |      Sim | Faixa de preço               |
| `endereco`      | string         |      Sim | Endereço                     |
| `municipio`     | string         |      Sim | Município                    |
| `uf`            | string         |      Sim | Unidade federativa           |
| `codigo_bairro` | double         |      Sim | Código do bairro associado   |

### Exemplo

```text
codigo              nome                    categoria
431962533652067     Boizão Lanches          Bar
1663855903830869    Bar do Serjão           Bar
567824576564110     Recanto Do Kuca         Restaurant
```

### Pontos de atenção

O campo `codigo_bairro` apresentou valores nulos durante a amostragem inicial.

Esse comportamento ainda não deve ser classificado como erro de qualidade, pois é necessário determinar se o relacionamento com bairro é obrigatório ou opcional.

Também deverão ser avaliados:

* unicidade de `codigo`;
* preenchimento de campos cadastrais;
* domínio de `categoria`;
* domínio de `faixa_preco`;
* relacionamento entre `codigo_bairro` e `bairros.codigo`;
* consistência entre `municipio` e bairro;
* consistência de `uf`.

---

## 4. eventos_de_fluxo.csv.gz

### Descrição

Dataset contendo eventos de fluxo associados a concorrentes.

### Formato

CSV compactado com GZIP.

### Volume inicial observado

**248.589 registros.**

### Schema identificado

| Campo                | Tipo observado | Nullable | Descrição inicial                 |
| -------------------- | -------------- | -------: | --------------------------------- |
| `codigo`             | string         |      Sim | Identificador do evento           |
| `datetime`           | timestamp      |      Sim | Data e hora do evento             |
| `codigo_concorrente` | long           |      Sim | Código do concorrente relacionado |

### Exemplo

```text
codigo                                                     datetime                  codigo_concorrente
oMn07h1bJYV0Wdx+RTzsDcT8JQlT7QXc7q8A/4y+cO5gBQKOUoYGB...  2017-07-27 09:51:02       650509405109544
iZuQeTd9am+qfaiqnn5kkixogIbwN0nY2gtMwZqH9bFqph8qYvYch...  2017-06-24 14:00:26.405   650509405109544
```

### Pontos de atenção

Deverão ser avaliados:

* unicidade de `codigo`;
* preenchimento de `datetime`;
* validade temporal de `datetime`;
* preenchimento de `codigo_concorrente`;
* integridade referencial com `concorrentes.codigo`;
* possíveis eventos duplicados;
* distribuição temporal dos eventos.

---

## Origem e versionamento

Os datasets são considerados **dados de entrada** do projeto e estão armazenados localmente em:

```text
data/raw/
```

A estratégia de versionamento desses arquivos ainda será definida.

O código-fonte e as regras de qualidade devem permanecer independentes dos arquivos físicos de entrada sempre que possível.

---

## Próximas análises

A etapa de profiling deverá complementar este documento com métricas objetivas, incluindo:

* quantidade total de registros;
* quantidade de registros distintos;
* quantidade e percentual de nulos;
* cardinalidade;
* distribuição dos valores;
* valores mínimos e máximos;
* duplicidades;
* integridade referencial;
* domínios encontrados;
* anomalias identificadas.
