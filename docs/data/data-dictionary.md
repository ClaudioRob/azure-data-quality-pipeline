# Data Dictionary

Este documento apresenta o dicionário de dados inicial das fontes utilizadas pelo projeto.

Os tipos apresentados representam os tipos observados durante a ingestão inicial com PySpark. As descrições e regras definitivas serão refinadas durante o profiling.

---

## bairros

| Campo       | Tipo   | Descrição               | Regra candidata  |
| ----------- | ------ | ----------------------- | ---------------- |
| `codigo`    | long   | Identificador do bairro | Não nulo e único |
| `nome`      | string | Nome do bairro          | Não nulo         |
| `municipio` | string | Município do bairro     | Não nulo         |
| `uf`        | string | Unidade federativa      | Domínio válido   |
| `area`      | double | Área do bairro          | Valor positivo   |

### Chave candidata

```text
bairros.codigo
```

---

## populacao

| Campo       | Tipo | Descrição                | Regra candidata |
| ----------- | ---- | ------------------------ | --------------- |
| `codigo`    | long | Código de referência     | Não nulo        |
| `populacao` | long | Quantidade de habitantes | Não nulo e >= 0 |

### Chave / relacionamento candidato

```text
populacao.codigo
        ↓
bairros.codigo
```

A obrigatoriedade e cardinalidade desse relacionamento deverão ser confirmadas pelo profiling.

---

## concorrentes

| Campo           | Tipo   | Descrição                    | Regra candidata                         |
| --------------- | ------ | ---------------------------- | --------------------------------------- |
| `codigo`        | long   | Identificador do concorrente | Não nulo e único                        |
| `nome`          | string | Nome do concorrente          | Não nulo                                |
| `categoria`     | string | Categoria do estabelecimento | Domínio válido                          |
| `faixa_preco`   | long   | Faixa de preço               | Domínio válido                          |
| `endereco`      | string | Endereço do estabelecimento  | Avaliar completude                      |
| `municipio`     | string | Município do estabelecimento | Não nulo                                |
| `uf`            | string | Unidade federativa           | Domínio válido                          |
| `codigo_bairro` | double | Código do bairro             | Integridade referencial, se obrigatório |

### Chave candidata

```text
concorrentes.codigo
```

### Relacionamento candidato

```text
concorrentes.codigo_bairro
        ↓
bairros.codigo
```

> O tipo `double` de `codigo_bairro` deverá ser avaliado. Caso represente uma chave inteira, pode ser necessário normalizá-lo durante a ingestão.

---

## eventos_de_fluxo

| Campo                | Tipo      | Descrição                         | Regra candidata                 |
| -------------------- | --------- | --------------------------------- | ------------------------------- |
| `codigo`             | string    | Identificador do evento           | Não nulo e potencialmente único |
| `datetime`           | timestamp | Data e hora do evento             | Não nulo e temporalmente válido |
| `codigo_concorrente` | long      | Concorrente relacionado ao evento | Integridade referencial         |

### Chave candidata

```text
eventos_de_fluxo.codigo
```

### Relacionamento candidato

```text
eventos_de_fluxo.codigo_concorrente
        ↓
concorrentes.codigo
```

---

## Convenções

### Identificadores

Campos denominados `codigo` são tratados inicialmente como possíveis identificadores ou chaves de relacionamento.

A unicidade de cada identificador deverá ser confirmada por profiling.

### Campos numéricos

Campos numéricos devem ser avaliados quanto a:

* valores nulos;
* valores negativos;
* limites plausíveis;
* precisão;
* escala;
* consistência com o domínio de negócio.

### Campos categóricos

Campos como `uf`, `categoria` e `faixa_preco` deverão ter seus domínios determinados a partir dos dados e, posteriormente, formalizados como regras de qualidade.

### Datas

Campos temporais deverão ser avaliados quanto a:

* valores nulos;
* formato;
* intervalo temporal;
* valores futuros;
* distribuição temporal;
* duplicidades ou eventos inconsistentes.

---

## Status do dicionário

Este documento representa a **versão inicial do entendimento dos dados**.

As regras marcadas como "candidatas" não devem ser consideradas regras definitivas de Data Quality até que sejam confirmadas pelo profiling e pelo entendimento do domínio.
