# Analisador de Carteira com IA

API em Python que recebe uma carteira de investimentos, calcula métricas de concentração e usa IA (Claude) para explicar o resultado em linguagem simples.

Projeto de estudo, feito durante o curso de Análise e Desenvolvimento de Sistemas, com foco em backend, Python e integração com IA.

## O que o projeto faz

1. Recebe uma lista de ativos com o valor investido em cada um.
2. Calcula, em Python puro:
   - o total investido;
   - o peso percentual de cada ativo;
   - a maior posição da carteira;
   - o índice de concentração **HHI** (soma dos pesos ao quadrado: quanto mais perto de 1, mais concentrada).
3. Envia as métricas já calculadas para a IA, que devolve uma explicação curta em português.

A divisão é intencional: a conta é feita pelo código, que é exato, e a IA só interpreta o resultado.

## Tecnologias

- Python 3.10+
- FastAPI
- Pydantic (validação dos dados de entrada)
- Uvicorn (servidor)
- Anthropic SDK (chamada à IA)

## Como rodar

```bash
# 1. Clone o repositório e entre na pasta
git clone <link-do-repositorio>
cd <nome-da-pasta>

# 2. (Opcional) crie um ambiente virtual
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install fastapi uvicorn anthropic pydantic

# 4. Configure sua chave da API da Anthropic
export ANTHROPIC_API_KEY="sua_chave"   # Windows (PowerShell): $env:ANTHROPIC_API_KEY="sua_chave"

# 5. Inicie o servidor
uvicorn main:app --reload
```

Depois abra `http://127.0.0.1:8000/docs`. O FastAPI gera uma tela para testar o endpoint.

## Endpoint

### `POST /analisar`

Exemplo de corpo da requisição:

```json
{
  "ativos": [
    { "ticker": "PETR4", "valor": 5000 },
    { "ticker": "VALE3", "valor": 3000 },
    { "ticker": "ITUB4", "valor": 2000 }
  ]
}
```

Exemplo de resposta (a parte `metricas` é o resultado real do cálculo; o texto de `explicacao_ia` varia a cada chamada):

```json
{
  "metricas": {
    "total": 10000,
    "pesos_percentuais": { "PETR4": 50.0, "VALE3": 30.0, "ITUB4": 20.0 },
    "maior_posicao": { "ticker": "PETR4", "peso": 50.0 },
    "indice_concentracao_hhi": 0.38
  },
  "explicacao_ia": "..."
}
```

### Erros

- `422`: dados inválidos (lista vazia, valor menor ou igual a zero, campo faltando).
- `502`: falha ao chamar a IA.

## Como ler o HHI

| Carteira | HHI |
|---|---|
| 4 ativos com 25% cada | 0,25 |
| 50% / 30% / 20% | 0,38 |
| 90% / 10% | 0,82 |

## Aviso

Projeto educacional. A explicação gerada pela IA não é recomendação de investimento.

## Próximos passos

- [ ] Salvar o histórico de análises em um banco SQL
- [ ] Buscar cotações reais por API
- [ ] Criar testes automatizados com pytest
- [ ] Conectar uma interface web ao endpoint

## Autor

Mateus, estudante de ADS, interessado na união entre tecnologia e mercado financeiro.
