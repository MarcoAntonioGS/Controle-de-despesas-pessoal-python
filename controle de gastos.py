import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Função para criar conexão com o banco de dados
def criar_conexao():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # Substitua pelo seu nome de usuário do MySQL
            password='221203Ma',  # Substitua pela sua senha do MySQL
            database='controle_gastos'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para adicionar uma nova despesa
def adicionar_despesa():
    data = entry_data.get()
    valor = entry_valor.get()
    categoria = entry_categoria.get()
    descricao = entry_descricao.get()

    if not data or not valor or not categoria:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
        return

    try:
        valor = float(valor)
        data_formatada = datetime.strptime(data, '%d/%m/%Y').strftime('%Y-%m-%d')
        conn = criar_conexao()
        if conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO despesas (data, valor, categoria, descricao) VALUES (%s, %s, %s, %s)',
                           (data_formatada, valor, categoria, descricao))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Despesa adicionada com sucesso!")
            atualizar_lista()
        else:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
    except ValueError:
        messagebox.showerror("Erro", "O valor deve ser um número válido.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado: {e}")

# Função para atualizar uma despesa
def atualizar_despesa():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione uma despesa para atualizar.")
        return

    item = tree.item(selected_item)
    id_despesa = item['values'][0]
    data = entry_data.get()
    valor = entry_valor.get()
    categoria = entry_categoria.get()
    descricao = entry_descricao.get()

    if not data or not valor or not categoria:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
        return

    try:
        valor = float(valor)
        data_formatada = datetime.strptime(data, '%d/%m/%Y').strftime('%Y-%m-%d')
        conn = criar_conexao()
        if conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE despesas
                SET data = %s, valor = %s, categoria = %s, descricao = %s
                WHERE id = %s
            ''', (data_formatada, valor, categoria, descricao, id_despesa))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Despesa atualizada com sucesso!")
            atualizar_lista()
        else:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
    except ValueError:
        messagebox.showerror("Erro", "O valor deve ser um número válido.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado: {e}")

# Função para excluir uma despesa
def excluir_despesa():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione uma despesa para excluir.")
        return

    item = tree.item(selected_item)
    id_despesa = item['values'][0]
    confirm = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir esta despesa?")
    if confirm:
        try:
            conn = criar_conexao()
            if conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM despesas WHERE id = %s', (id_despesa,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Despesa excluída com sucesso!")
                atualizar_lista()
            else:
                messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}")

# Função para atualizar a lista de despesas
def atualizar_lista():
    for item in tree.get_children():
        tree.delete(item)
    try:
        conn = criar_conexao()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM despesas')
            despesas = cursor.fetchall()
            for despesa in despesas:
                data_formatada = datetime.strftime(despesa[1], '%d/%m/%Y')
                tree.insert("", tk.END, values=(despesa[0], data_formatada, despesa[2], despesa[3], despesa[4]))
            conn.close()
        else:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado: {e}")

# Função para gerar um relatório de despesas por categoria
def gerar_relatorio():
    try:
        conn = criar_conexao()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT categoria, SUM(valor) FROM despesas GROUP BY categoria')
            relatorio = cursor.fetchall()
            conn.close()
            
            # Limpar a tabela de relatório
            for item in tree_relatorio.get_children():
                tree_relatorio.delete(item)
            
            for categoria, total in relatorio:
                tree_relatorio.insert("", tk.END, values=(categoria, f"R${total:.2f}"))
        else:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado: {e}")

# Criação da janela principal
root = tk.Tk()
root.title("Controle de Despesas Pessoal")

# Criar widgets para adicionar/atualizar despesas
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Data (DD/MM/AAAA):").grid(row=0, column=0, sticky=tk.W)
entry_data = tk.Entry(frame)
entry_data.grid(row=0, column=1)

tk.Label(frame, text="Valor:").grid(row=1, column=0, sticky=tk.W)
entry_valor = tk.Entry(frame)
entry_valor.grid(row=1, column=1)

tk.Label(frame, text="Categoria:").grid(row=2, column=0, sticky=tk.W)
entry_categoria = tk.Entry(frame)
entry_categoria.grid(row=2, column=1)

tk.Label(frame, text="Descrição:").grid(row=3, column=0, sticky=tk.W)
entry_descricao = tk.Entry(frame)
entry_descricao.grid(row=3, column=1)

btn_adicionar = tk.Button(frame, text="Adicionar Despesa", command=adicionar_despesa)
btn_adicionar.grid(row=4, column=0, pady=10)

btn_atualizar = tk.Button(frame, text="Atualizar Despesa", command=atualizar_despesa)
btn_atualizar.grid(row=4, column=1, pady=10)

btn_excluir = tk.Button(frame, text="Excluir Despesa", command=excluir_despesa)
btn_excluir.grid(row=4, column=2, pady=10)

# Criar a tabela de despesas com rolagem
frame_lista = tk.Frame(root)
frame_lista.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

canvas = tk.Canvas(frame_lista)
scroll_y = tk.Scrollbar(frame_lista, orient="vertical", command=canvas.yview)
scroll_y.pack(side="right", fill="y")

# Criar um frame dentro do canvas
frame_canvas = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame_canvas, anchor="nw")

frame_canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.pack(side="left", fill="both", expand=True)

# Definir as colunas da tabela
cols = ('ID', 'Data', 'Valor', 'Categoria', 'Descrição')
tree = ttk.Treeview(frame_canvas, columns=cols, show='headings', yscrollcommand=scroll_y.set)

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor='center')  

# Ajuste específico para a coluna de descrição para garantir que o texto não fique cortado
tree.column('Descrição', width=300, anchor='center')

tree.pack(fill=tk.BOTH, expand=True)

scroll_y.config(command=canvas.yview)

# Criar widgets para o relatório
frame_relatorio = tk.Frame(root)
frame_relatorio.pack(padx=10, pady=10)

btn_relatorio = tk.Button(frame_relatorio, text="Gerar Relatório", command=gerar_relatorio)
btn_relatorio.pack(pady=10)

# Criar a tabela de relatório
cols_relatorio = ('Categoria', 'Valor Total')
tree_relatorio = ttk.Treeview(frame_relatorio, columns=cols_relatorio, show='headings')

for col in cols_relatorio:
    tree_relatorio.heading(col, text=col)
    tree_relatorio.column(col, width=150, anchor='center')  

tree_relatorio.pack(padx=10, pady=10)

# Atualizar a lista de despesas ao iniciar
atualizar_lista()

# Iniciar o loop principal
root.mainloop()