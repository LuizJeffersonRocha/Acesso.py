import tkinter as tk
from tkinter import ttk
import sqlite3

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('servicos_publicos.db')
cursor = conn.cursor()

# Função para criar a tabela no banco de dados
def criar_tabela(nome_tabela):
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {nome_tabela} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT NOT NULL,
        local TEXT NOT NULL,
        horario_funcionamento TEXT NOT NULL,
        contatos TEXT NOT NULL
    )
    ''')
    conn.commit()

# Função para inserir dados nas tabelas
def inserir_dados(nome_tabela, nome, descricao, local, horario_funcionamento, contatos):
    cursor.execute(f'''
    INSERT INTO {nome_tabela} (nome, descricao, local, horario_funcionamento, contatos)
    VALUES (?, ?, ?, ?, ?)
    ''', (nome, descricao, local, horario_funcionamento, contatos))
    conn.commit()

# Função para mostrar os dados na interface gráfica
def mostrar_tabela(nome_tabela):
    cursor.execute(f'SELECT * FROM {nome_tabela}')
    rows = cursor.fetchall()

    # Limpando a Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Inserindo os dados na Treeview
    for row in rows:
        tree.insert('', tk.END, values=row)

# Criação das tabelas
criar_tabela('Saude')
criar_tabela('Educacao')
criar_tabela('Seguranca')
criar_tabela('AssistenciaSocial')
criar_tabela('ColetaLixo')

# Dados para cada tabela (adicionando mais entradas se necessário)
dados_saude = [
    ('UPA Novo Mundo', 'Atendimento de urgência e emergência', 'Av. Brasília, 2741', '24 horas', '41 3313-2800'),
    ('Unidade de Saúde Novo Mundo', 'Atendimento médico e odontológico', 'Rua Cel. João Guilherme Guimarães, 300', '7h - 19h', '41 3378-3818'),
    ('UPA Fazendinha', 'Atendimento de urgência e emergência', 'Rua Carlos Klemtz, 1700', '24 horas', '41 3213-2800'),
    ('Unidade de Saúde Fazendinha', 'Atendimento médico e odontológico', 'Rua Carlos Klemtz, 1000', '7h - 19h', '41 3214-5000'),
    ('Hospital do Trabalhador', 'Atendimento emergencial e consultas', 'Av. República Argentina, 4406', '24 horas', '41 3212-5700'),
    ('Hospital IPO', 'Especializado em otorrinolaringologia', 'Av. República Argentina, 210', '8h - 18h', '41 3314-1500'),
    ('Maternidade Bairro Novo', 'Atendimento especializado em obstetrícia', 'Rua Tijucas do Sul, 1700', '24 horas', '41 3287-0000'),
    ('Unidade de Saúde Vila Guaíra', 'Atendimento médico e odontológico', 'Rua São Mateus, 567', '7h - 19h', '41 3345-4479'),
    ('Unidade de Saúde Pinheirinho', 'Atendimento médico e odontológico', 'Rua Alfredo Parodi, 400', '7h - 19h', '41 3345-4479'),
    ('Unidade de Saúde Sítio Cercado', 'Atendimento médico e odontológico', 'Rua Izaac Ferreira da Cruz, 4000', '7h - 19h', '41 3345-0000')
]

# Inserção dos dados nas tabelas correspondentes
for dados in dados_saude:
    inserir_dados('Saude', *dados)

# Interface gráfica
root = tk.Tk()
root.title("Serviços Públicos")
root.geometry("1700x800")
root.configure(bg='#e0f7fa')

# Estilo para a Treeview
style = ttk.Style()
style.configure('Treeview', rowheight=40, font=('Helvetica', 12))
style.configure('Treeview.Heading', font=('Helvetica', 14, 'bold'))
style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
style.map('Treeview', background=[('selected', '#009688')])

# Frame para a exibição da tabela
frame_tabela = tk.Frame(root, bg='#e0f7fa')
frame_tabela.pack(padx=10, pady=10, fill='both', expand=True)

# Treeview para exibição dos dados
tree = ttk.Treeview(frame_tabela, columns=('ID', 'Nome', 'Descrição', 'Local', 'Horário de Funcionamento', 'Contatos'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Nome', text='Nome')
tree.heading('Descrição', text='Descrição')
tree.heading('Local', text='Local')
tree.heading('Horário de Funcionamento', text='Horário de Funcionamento')
tree.heading('Contatos', text='Contatos')

# Ajuste das larguras das colunas
tree.column('ID', width=50, anchor='center', stretch=tk.YES)
tree.column('Nome', width=200, anchor='center', stretch=tk.YES)
tree.column('Descrição', width=300, anchor='center', stretch=tk.YES)
tree.column('Local', width=290, anchor='center', stretch=tk.YES)
tree.column('Horário de Funcionamento', width=200, anchor='center', stretch=tk.YES)
tree.column('Contatos', width=150, anchor='center', stretch=tk.YES)

# Adicionando a Treeview ao frame
tree.pack(side='left', fill='both', expand=True)

# Scrollbar para a Treeview
scrollbar = ttk.Scrollbar(frame_tabela, orient='vertical', command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side='right', fill='y')

# Frame para os botões de seleção de tabela
frame_botoes = tk.Frame(root, bg='#e0f7fa')
frame_botoes.pack(padx=10, pady=10, fill='x')

# Estilo para os botões
style.configure('TButton', font=('Helvetica', 12, 'bold'), background='#00796b', foreground='#ffffff')

# Botões para selecionar qual tabela exibir
botoes = [
    ('Saúde', 'Saude'),
    ('Educação', 'Educacao'),
    ('Segurança', 'Seguranca'),
    ('Assistência Social', 'AssistenciaSocial'),
    ('Coleta de Lixo', 'ColetaLixo')
]

for texto, tabela in botoes:
    botao = tk.Button(frame_botoes, text=texto, command=lambda t=tabela: mostrar_tabela(t), bg='#00796b', fg='white', padx=10, pady=5)
    botao.pack(side='left', padx=5, expand=True, fill='x')

root.mainloop()

# Fechando a conexão com o banco de dados ao encerrar a aplicação
conn.close()
