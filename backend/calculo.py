# calculo.py

# calcula o custo em reais
def calcular_custo(kwh, tarifa):
    return round(kwh * tarifa, 2)

# retorna o status com base na meta
def calcular_status(kwh, limite):
    if limite is None:
        return "SEM META"
    if kwh >= limite:
        return "CRITICO"
    elif kwh >= limite * 0.8:
        return "ATENCAO"
    else:
        return "OK"

# calcula a variacao percentual entre dois meses
def calcular_variacao(atual, anterior):
    if anterior is None or anterior == 0:
        return None
    return round(((atual - anterior) / anterior) * 100, 2)

# formata a variacao para exibir na tela
def formatar_variacao(v):
    if v is None:
        return "Sem mes anterior"
    sinal = "+" if v > 0 else ""
    return f"{sinal}{v}%"
