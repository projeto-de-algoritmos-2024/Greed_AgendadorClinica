import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
from datetime import datetime

def converter_para_minutos(horario_str):
    try:
        horario_obj = datetime.strptime(horario_str, "%H:%M")
        return horario_obj.hour * 60 + horario_obj.minute
    except ValueError:
        messagebox.showerror("Erro", f"Horário inválido: {horario_str}. Use o formato HH:MM.")
        return None

def particionar_intervalos(consultas):
    consultas_ordenadas = sorted(consultas, key=lambda x: x[1])
    salas = []

    for consulta in consultas_ordenadas:
        alocada = False
        for sala in salas:
            if sala[-1][1] <= consulta[0]:
                sala.append(consulta)
                alocada = True
                break
        if not alocada:
            salas.append([consulta])

    return salas

def adicionar_consulta():
    try:
        nome_paciente = entrada_nome.get()
        nome_medico = entrada_medico.get()
        horario_inicio_str = entrada_inicio.get()
        horario_fim_str = entrada_fim.get()

        horario_inicio = converter_para_minutos(horario_inicio_str)
        horario_fim = converter_para_minutos(horario_fim_str)

        if horario_inicio is None or horario_fim is None:
            return
        if horario_inicio >= horario_fim:
            messagebox.showerror("Erro", "O horário de início deve ser menor que o de término!")
            return

        nova_consulta = (horario_inicio, horario_fim, nome_paciente, nome_medico)
        consultas.append(nova_consulta)
        tabela.insert("", "end", values=(nome_paciente, nome_medico, "-", horario_inicio_str, horario_fim_str))
        entrada_nome.delete(0, tk.END)
        entrada_medico.delete(0, tk.END)
        entrada_inicio.delete(0, tk.END)
        entrada_fim.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Erro", "Insira valores válidos para os campos de horários!")

def calcular_alocacao():
    if not consultas:
        messagebox.showerror("Erro", "Nenhuma consulta foi adicionada!")
        return

    alocacao = particionar_intervalos(consultas)

    tabela.delete(*tabela.get_children())
    for i, sala in enumerate(alocacao, start=1):
        for inicio, fim, paciente, medico in sala:
            horario_inicio_str = f"{inicio // 60:02d}:{inicio % 60:02d}"
            horario_fim_str = f"{fim // 60:02d}:{fim % 60:02d}"
            tabela.insert("", "end", values=(paciente, medico, f"Sala {i}", horario_inicio_str, horario_fim_str))

raiz = tk.Tk()
raiz.title("Sistema de Agendamento Médico")
raiz.geometry("1000x600")

consultas = []

titulo_label = tk.Label(raiz, text="Sistema de Agendamento de Consultas", font=("Arial", 16))
titulo_label.pack(pady=10)

quadro_entradas = tk.Frame(raiz)
quadro_entradas.pack(pady=10)

tk.Label(quadro_entradas, text="Paciente:").grid(row=0, column=0, padx=5)
entrada_nome = tk.Entry(quadro_entradas, width=20)
entrada_nome.grid(row=0, column=1, padx=5)

tk.Label(quadro_entradas, text="Médico:").grid(row=0, column=2, padx=5)
entrada_medico = tk.Entry(quadro_entradas, width=20)
entrada_medico.grid(row=0, column=3, padx=5)

tk.Label(quadro_entradas, text="Início (HH:MM):").grid(row=1, column=0, padx=5)
entrada_inicio = tk.Entry(quadro_entradas, width=10)
entrada_inicio.grid(row=1, column=1, padx=5)

tk.Label(quadro_entradas, text="Término (HH:MM):").grid(row=1, column=2, padx=5)
entrada_fim = tk.Entry(quadro_entradas, width=10)
entrada_fim.grid(row=1, column=3, padx=5)

botao_adicionar = tk.Button(quadro_entradas, text="Adicionar Consulta", command=adicionar_consulta)
botao_adicionar.grid(row=2, column=0, columnspan=4, pady=10)

tabela = ttk.Treeview(raiz, columns=("nome", "medico", "sala", "inicio", "fim"), show="headings", height=15)
tabela.pack(pady=10, fill="x", expand=True)

tabela.heading("nome", text="Paciente")
tabela.heading("medico", text="Médico")
tabela.heading("sala", text="Sala")
tabela.heading("inicio", text="Início")
tabela.heading("fim", text="Término")

botao_calcular = tk.Button(raiz, text="Exibir Agenda por Salas", command=calcular_alocacao)
botao_calcular.pack(pady=20)

raiz.mainloop()
