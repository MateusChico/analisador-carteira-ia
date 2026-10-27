"""
API de análise de carteira com Python + FastAPI + IA (Claude).

Rodar:
    pip install fastapi uvicorn anthropic pydantic
    export ANTHROPIC_API_KEY="sua_chave"
    uvicorn main:app --reload

Testar: abra http://127.0.0.1:8000/docs
"""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
import anthropic

app = FastAPI(title="Analisador de Carteira com IA")
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


class Ativo(BaseModel):
    ticker: str = Field(..., examples=["PETR4"])
    valor: float = Field(..., gt=0, description="Valor investido em R$")


class Carteira(BaseModel):
    ativos: list[Ativo]

    @field_validator("ativos")
    @classmethod
    def precisa_ter_ativos(cls, v):
        if not v:
            raise ValueError("A carteira precisa ter ao menos um ativo.")
        return v


def calcular_metricas(carteira: Carteira) -> dict:
    """Parte 'determinística': cálculo feito em Python puro, sem IA."""
    total = sum(a.valor for a in carteira.ativos)
    pesos = {a.ticker.upper(): round(a.valor / total * 100, 2) for a in carteira.ativos}
    maior_ticker = max(pesos, key=pesos.get)
    # HHI: soma dos pesos ao quadrado. Perto de 1 = muito concentrado.
    hhi = round(sum((p / 100) ** 2 for p in pesos.values()), 3)
    return {
        "total": round(total, 2),
        "pesos_percentuais": pesos,
        "maior_posicao": {"ticker": maior_ticker, "peso": pesos[maior_ticker]},
        "indice_concentracao_hhi": hhi,
    }


def explicar_com_ia(metricas: dict) -> str:
    """Parte 'IA': transforma números em explicação em linguagem simples."""
    prompt = (
        "Você é um analista educativo. Com base nas métricas abaixo, explique em "
        "português, em até 5 linhas, os pontos de atenção sobre concentração da "
        "carteira. Não recomende compra ou venda de ativos.\n\n"
        f"{metricas}"
    )
    resposta = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return resposta.content[0].text


@app.post("/analisar")
def analisar(carteira: Carteira):
    metricas = calcular_metricas(carteira)
    try:
        explicacao = explicar_com_ia(metricas)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Falha ao chamar a IA: {e}")
    return {"metricas": metricas, "explicacao_ia": explicacao}
