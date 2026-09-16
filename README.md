# Azure Data Quality Pipeline

Pipeline de **Data Quality** desenvolvido com **PySpark**, **PyTest** e preparado para execução futura em **Azure Databricks**.

O projeto tem como objetivo explorar um cenário de dados reais, estruturar seu processamento e implementar mecanismos de **profiling, validação, mensuração e monitoramento da qualidade dos dados**.

> **Status:** projeto em desenvolvimento.

---

## Objetivos

O projeto busca demonstrar, de ponta a ponta:

* ingestão de diferentes formatos de dados;
* profiling e entendimento das fontes;
* identificação de problemas de qualidade;
* definição de regras de Data Quality;
* validação automatizada utilizando PySpark;
* testes automatizados com PyTest;
* geração de métricas e resultados de qualidade;
* documentação das relações entre os datasets;
* organização de arquitetura para execução local;
* preparação para execução futura em Azure Databricks.

---

## Tecnologias

| Tecnologia       | Utilização                           |
| ---------------- | ------------------------------------ |
| Python 3.12      | Linguagem principal                  |
| PySpark 4.2.0    | Processamento e validação dos dados  |
| PyTest           | Testes automatizados                 |
| Setuptools       | Empacotamento do projeto             |
| Azure Databricks | Ambiente alvo para execução em Azure |

---

## Fontes de dados

Atualmente o projeto possui quatro fontes de dados em `data/raw/`:

| Dataset                   | Formato  | Descrição inicial                               |
| ------------------------- | -------- | ----------------------------------------------- |
| `bairros.csv`             | CSV      | Informações de bairros, municípios, UF e área   |
| `populacao.json`          | JSON     | Informações de população associadas a códigos   |
| `concorrentes.parquet`    | Parquet  | Informações sobre concorrentes e seus atributos |
| `eventos_de_fluxo.csv.gz` | CSV GZIP | Eventos de fluxo associados a concorrentes      |

### Volume inicial conhecido

* `concorrentes.parquet`: 4.202 registros
* `eventos_de_fluxo.csv.gz`: 248.589 registros

Os volumes e características dos demais datasets serão consolidados durante a etapa de profiling.

---

## Modelo de dados inicial

A partir da análise inicial das fontes, foram identificadas possíveis relações entre os datasets:

```text
                  ┌──────────────┐
                  │   bairros    │
                  │              │
                  │ codigo       │
                  │ nome         │
                  │ municipio    │
                  │ uf           │
                  │ area         │
                  └──────┬───────┘
                         │
              codigo_bairro
                         │
                         ▼
                  ┌──────────────┐
                  │ concorrentes │
                  │              │
                  │ codigo       │
                  │ nome         │
                  │ categoria    │
                  │ faixa_preco  │
                  │ codigo_bairro│
                  └──────┬───────┘
                         │
              codigo_concorrente
                         │
                         ▼
                  ┌──────────────┐
                  │    eventos   │
                  │              │
                  │ codigo       │
                  │ datetime     │
                  │ codigo_      │
                  │ concorrente  │
                  └──────────────┘

                  ┌──────────────┐
                  │  populacao   │
                  │              │
                  │ codigo       │
                  │ populacao    │
                  └──────┬───────┘
                         │
                       codigo
                         │
                         ▼
                      bairros
```

> As relações acima representam o **modelo inicial identificado durante a exploração dos dados**. Cardinalidade, integridade referencial e regras definitivas serão confirmadas durante o profiling.

---

## Data Quality

A estratégia de qualidade será organizada principalmente nas seguintes dimensões:

### Completeness

Verificação de campos obrigatórios e ocorrência de valores nulos.

Exemplos:

* `bairros.codigo`
* `bairros.nome`
* `bairros.municipio`
* `populacao.populacao`
* `eventos.datetime`

### Uniqueness

Identificação de registros ou chaves duplicadas.

Exemplos:

* unicidade de `bairros.codigo`;
* unicidade de identificadores de concorrentes;
* identificação de possíveis eventos duplicados.

### Validity

Verificação de valores pertencentes aos domínios esperados.

Exemplos:

* UF válida;
* categoria válida;
* faixa de preço dentro do domínio esperado;
* população não negativa;
* área maior que zero.

### Referential Integrity

Verificação das relações entre datasets.

Exemplos:

```text
populacao.codigo
        ↓
bairros.codigo
```

```text
concorrentes.codigo_bairro
        ↓
bairros.codigo
```

```text
eventos.codigo_concorrente
        ↓
concorrentes.codigo
```

Essas regras serão confirmadas após a análise completa das fontes.

### Data Type

Validação dos tipos utilizados durante a ingestão e transformação.

### Temporal Validity

Validação dos campos relacionados a data e hora, principalmente:

```text
eventos.datetime
```

---

## Arquitetura

### Execução local

A arquitetura inicial será baseada no seguinte fluxo:

```text
┌──────────────┐
│  Data / Raw  │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ PySpark Ingestion│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Data Profiling   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Data Quality     │
│ Rules            │
└────────┬─────────┘
         │
     ┌───┴───────────┐
     ▼               ▼
┌────────────┐ ┌──────────────┐
│ Processed  │ │ Quality      │
│ Data       │ │ Results      │
└────────────┘ └──────────────┘
```

### Arquitetura alvo em Azure

A execução em Azure Databricks será tratada como uma evolução do projeto:

```text
┌──────────────────────┐
│ Azure Data Lake      │
│ Storage               │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Azure Databricks     │
│                      │
│ ┌──────────────────┐ │
│ │ Ingestion        │ │
│ ├──────────────────┤ │
│ │ Profiling        │ │
│ ├──────────────────┤ │
│ │ Data Quality     │ │
│ └──────────────────┘ │
└──────────┬───────────┘
           │
      ┌────┴─────────┐
      ▼              ▼
┌─────────────┐ ┌──────────────┐
│ Quality     │ │ Data         │
│ Metrics     │ │ Products     │
└─────────────┘ └──────────────┘
```

> A arquitetura Azure representa o **estado alvo do projeto**, não a infraestrutura atualmente implantada.

---

## Estrutura do projeto

A estrutura planejada é:

```text
azure-data-quality-pipeline/
│
├── README.md
├── pyproject.toml
├── .gitignore
│
├── docs/
│   ├── architecture/
│   │   ├── architecture.md
│   │   ├── architecture-local.md
│   │   └── architecture-azure.md
│   │
│   ├── data/
│   │   ├── datasets.md
│   │   ├── data-dictionary.md
│   │   └── relationships.md
│   │
│   ├── data-quality/
│   │   ├── quality-dimensions.md
│   │   ├── quality-rules.md
│   │   └── quality-report.md
│   │
│   └── decisions/
│       └── adr-001-project-architecture.md
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── quality/
│
├── src/
│   └── azure_data_quality/
│       ├── __init__.py
│       ├── config/
│       ├── ingestion/
│       ├── profiling/
│       ├── validation/
│       ├── reporting/
│       └── utils/
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── scripts/
│   ├── profile_data.py
│   ├── validate_data.py
│   └── run_pipeline.py
│
└── diagrams/
    ├── architecture.drawio
    ├── data-lineage.drawio
    └── data-quality-flow.drawio
```

Parte dessa estrutura ainda será criada conforme o desenvolvimento avançar.

---

## Configuração do ambiente

O projeto utiliza Python 3.12.

Para criar o ambiente virtual:

```bash
python3.12 -m venv .venv
```

Ativar o ambiente:

### Linux / macOS

```bash
source .venv/bin/activate
```

Instalar o projeto e as dependências de desenvolvimento:

```bash
python -m pip install -e ".[dev]"
```

---

## Validação do ambiente PySpark

Para verificar se o PySpark está funcionando:

```bash
python -c "from pyspark.sql import SparkSession; spark = SparkSession.builder.master('local[*]').getOrCreate(); print(spark.version); spark.stop()"
```

A versão esperada atualmente é:

```text
4.2.0
```

---

## Testes

Os testes automatizados serão implementados utilizando PyTest.

A estrutura planejada separa:

```text
tests/
├── unit/
└── integration/
```

Os testes unitários deverão validar componentes individuais, enquanto os testes de integração deverão validar o comportamento do pipeline utilizando os datasets.

---

## Profiling

O profiling será utilizado para transformar a exploração inicial dos dados em informações estruturadas sobre:

* quantidade de registros;
* quantidade de colunas;
* tipos de dados;
* valores nulos;
* valores distintos;
* duplicidades;
* distribuição dos dados;
* valores mínimos e máximos;
* domínios;
* integridade referencial;
* possíveis anomalias.

Os resultados deverão posteriormente alimentar a definição das regras de Data Quality.

---

## Roadmap

### Fase 1 — Fundação

* [x] Criar projeto Python
* [x] Configurar ambiente virtual
* [x] Configurar PySpark
* [x] Configurar PyTest
* [x] Adicionar datasets raw
* [x] Realizar exploração inicial dos datasets
* [ ] Estruturar documentação

### Fase 2 — Data Understanding

* [ ] Criar dicionário de dados
* [ ] Documentar datasets
* [ ] Validar relacionamentos
* [ ] Consolidar profiling
* [ ] Identificar problemas de qualidade

### Fase 3 — Data Quality

* [ ] Definir dimensões de qualidade
* [ ] Definir regras de qualidade
* [ ] Implementar validações PySpark
* [ ] Criar métricas de qualidade
* [ ] Criar relatório de qualidade

### Fase 4 — Testes

* [ ] Testes unitários
* [ ] Testes de integração
* [ ] Testes das regras de Data Quality
* [ ] Testes de regressão

### Fase 5 — Pipeline

* [ ] Implementar pipeline completo
* [ ] Organizar execução por etapas
* [ ] Processar dados válidos
* [ ] Isolar dados inválidos
* [ ] Persistir resultados de qualidade

### Fase 6 — Azure

* [ ] Definir arquitetura Azure detalhada
* [ ] Preparar execução no Azure Databricks
* [ ] Integrar com Azure Data Lake Storage
* [ ] Avaliar orquestração
* [ ] Documentar deployment

---

## Princípios do projeto

O desenvolvimento seguirá alguns princípios:

1. **Qualidade antes de transformação**
   Entender os dados antes de aplicar regras ou transformações.

2. **Regras explícitas**
   As validações devem ser documentadas e rastreáveis.

3. **Código testável**
   Componentes devem ser separados para permitir testes unitários e de integração.

4. **Observabilidade**
   O resultado das validações deve gerar métricas que permitam acompanhar a qualidade.

5. **Separação entre dados e regras**
   Regras de qualidade não devem ficar acopladas diretamente aos datasets.

6. **Local first, Azure ready**
   O projeto deve funcionar localmente e possuir uma arquitetura preparada para evolução para Azure Databricks.

7. **Documentação como parte do desenvolvimento**
   Arquitetura, modelo de dados, regras e decisões técnicas devem evoluir junto com o código.

---

## Status atual

O projeto encontra-se na etapa de **fundação e entendimento dos dados**.

Neste momento já estão definidos:

* ambiente Python;
* versão do PySpark;
* estrutura inicial do projeto;
* datasets de entrada;
* primeiras observações sobre os schemas;
* possíveis relacionamentos entre as fontes;
* dimensões iniciais de Data Quality.

As regras definitivas de qualidade ainda serão estabelecidas após a conclusão do profiling e da documentação dos datasets.

Esse README já pode ser usado como a **visão geral do projeto**. O próximo passo natural é criar `docs/data/datasets.md`, `data-dictionary.md` e `relationships.md`, porque aí transformamos o profiling que já fizemos em documentação técnica rastreável.
