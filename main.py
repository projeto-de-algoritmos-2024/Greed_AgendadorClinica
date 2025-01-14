def interval_partitioning(horarios):
    horarios.sort(key=lambda x: x[0])
    salas = []

    for horario in horarios:
        reservado = False
        for sala in salas:
            if sala[-1][1] <= horario[0]:
                sala.append(horario)
                reservado = True
                break
        if not reservado:
            salas.append([horario])

    return salas