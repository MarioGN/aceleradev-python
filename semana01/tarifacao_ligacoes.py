from datetime import datetime

records = [
    {'source': '48-996355555', 'destination': '48-666666666', 'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097', 'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097', 'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788', 'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788', 'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099', 'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697', 'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099', 'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697', 'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097', 'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564627800, 'start': 1564626000}
]

TARIFACAO_NOTURNA = 0.36


def tarifacao_diurna(minutos):
    return minutos*0.09 + 0.36


def calcular_valor_ligacao(start, end):
    # converter timestamps -> datetime
    inicio = datetime.fromtimestamp(start)
    fim = datetime.fromtimestamp(end)

    # calcular valor da ligação
    valor_ligacao = 0
    duracao_segundos = (fim-inicio).total_seconds()
    duracao_minutos = int(duracao_segundos/60)

    if 6 <= inicio.hour <= 21:
        if fim.hour < 22:
            valor_ligacao = tarifacao_diurna(duracao_minutos)
        else:
            periodo_noturno = inicio.replace(hour=22, minute=0, second=0)
            duracao_noturna_segundos = (fim-periodo_noturno).total_seconds()
            duracao_noturna_minutos = int(duracao_noturna_segundos/60)

            valor_ligacao = tarifacao_diurna(
                                duracao_minutos-duracao_noturna_minutos)
            valor_ligacao += TARIFACAO_NOTURNA
    else:
        if 6 <= fim.hour <= 21:
            periodo_diurno = fim.replace(hour=6, minute=0, second=0)
            duracao_diurna_segundos = (fim-periodo_diurno).total_seconds()
            duracao_diurna_minutos = int(duracao_diurna_segundos/60)

            valor_ligacao = TARIFACAO_NOTURNA
            valor_ligacao += tarifacao_diurna(duracao_diurna_minutos)
        else:
            valor_ligacao = TARIFACAO_NOTURNA

    return valor_ligacao


def classify_by_phone_number(records):
    faturas = []
    for rec in records:
        source, start, end = rec['source'], rec['start'], rec['end']
        valor = calcular_valor_ligacao(start, end)

        for fatura in faturas:
            if source in fatura.values():
                fatura['total'] += valor
                valor = None

        if valor is not None:
            nova_fatura = {'source': source, 'total': valor}
            faturas.append(nova_fatura)

    for fatura in faturas:
        fatura['total'] = round(fatura['total'], 2)

    return sorted(faturas, key=lambda fat: fat['total'], reverse=True)
