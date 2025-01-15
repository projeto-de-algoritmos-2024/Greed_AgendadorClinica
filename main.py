import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring


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


def add_interval():
    try:
        start = int(entry_start.get())
        end = int(entry_end.get())
        name = askstring("Nome do Evento", "Digite o nome do evento:")

        if start >= end:
            messagebox.showerror("Erro", "O início deve ser menor que o fim!")
            return

        intervalos.append((start, end, name))
        tree.insert("", "end", values=(name, start, end))
        entry_start.delete(0, tk.END)
        entry_end.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Erro", "Insira valores válidos para início e fim!")


def calculate_allocation():
    if not intervalos:
        messagebox.showerror("Erro", "Nenhum intervalo foi adicionado!")
        return

    horario_intervalos = [(start, end) for start, end, _ in intervalos]
    alocacao = interval_partitioning(horario_intervalos)

    result_window = tk.Toplevel(root)
    result_window.title("Resultado da Alocação")

    tk.Label(result_window, text="Alocação de Salas", font=("Arial", 14)).pack(pady=10)

    for i, sala in enumerate(alocacao):
        tk.Label(result_window, text=f"Sala {i + 1}:", font=("Arial", 12)).pack(anchor="w")
        for start, end in sala:
            event_name = next(name for s, e, name in intervalos if s == start and e == end)
            tk.Label(result_window, text=f"  - {event_name} ({start}, {end})").pack(anchor="w")


root = tk.Tk()
root.title("Sistema de Agendamento de Consultas")
root.geometry("600x400")

intervalos = []

title_label = tk.Label(root, text="Gerenciador de Consultas", font=("Arial", 16))
title_label.pack(pady=10)

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Início:").grid(row=0, column=0, padx=5)
entry_start = tk.Entry(frame_inputs, width=10)
entry_start.grid(row=0, column=1, padx=5)

tk.Label(frame_inputs, text="Fim:").grid(row=0, column=2, padx=5)
entry_end = tk.Entry(frame_inputs, width=10)
entry_end.grid(row=0, column=3, padx=5)

add_button = tk.Button(frame_inputs, text="Adicionar Consulta", command=add_interval)
add_button.grid(row=0, column=4, padx=10)

tree = ttk.Treeview(root, columns=("name", "start", "end"), show="headings", height=10)
tree.pack(pady=10, fill="x", expand=True)

tree.heading("name", text="Nome")
tree.heading("start", text="Início")
tree.heading("end", text="Fim")

calculate_button = tk.Button(root, text="Calcular Alocação", command=calculate_allocation)
calculate_button.pack(pady=20)

root.mainloop()
