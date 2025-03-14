import tkinter as tk
from tkinter import messagebox

def calcular_inss(salario):
    tabela_inss = [
        (1518.00, 7.5),
        (2793.88, 9),
        (4190.83, 12),
        (8157.41, 14)
    ]
    total_inss = 0.0
    salario_restante = salario
    limite_anterior = 0.0

    for limite, aliquota in tabela_inss:
        if salario_restante <= 0:
            break
        diferenca = limite - limite_anterior
        if salario > limite:
            contribuicao = diferenca * (aliquota / 100)
            total_inss += contribuicao
            salario_restante -= diferenca
        else:
            contribuicao = (salario - limite_anterior) * (aliquota / 100)
            total_inss += contribuicao
            salario_restante = 0
        limite_anterior = limite

    return round(total_inss, 4)  # Precisão aumentada para 4 casas decimais

def calcular_irrf(base_calculo, num_dependentes):
    deducao_por_dependente = 189.59
    deducao_total = num_dependentes * deducao_por_dependente
    base_calculo -= deducao_total

    tabela_irrf = [
        (4664.68, 0.275, 896.00),
        (3751.06, 0.225, 662.77),
        (2826.66, 0.15, 381.44),
        (1903.99, 0.075, 169.44),
        (0, 0.0, 0.0)
    ]

    irrf = 0.0
    for limite, aliquota, deducao in tabela_irrf:
        if base_calculo > limite:
            irrf = (base_calculo * aliquota) - deducao
            break
    return max(round(irrf, 4), 0)  # Precisão aumentada para 4 casas decimais

def calcular_gross_from_net(net_alvo, dependentes):
    baixo = max(net_alvo, 0.0)
    alto = net_alvo * 2  # Estimativa inicial melhorada
    precisao = 0.0001    # Precisão aumentada
    max_iteracoes = 200  # Número máximo de iterações aumentado
    
    for _ in range(max_iteracoes):
        meio = (baixo + alto) / 2
        inss = calcular_inss(meio)
        base_irrf = meio - inss
        irrf = calcular_irrf(base_irrf, dependentes)
        liquido = meio - inss - irrf
        
        if abs(liquido - net_alvo) < precisao:
            return round(meio, 2)  # Arredondamento final para 2 casas
        elif liquido < net_alvo:
            baixo = meio
        else:
            alto = meio
            
    return round((baixo + alto) / 2, 2)  # Retorno mais preciso

def atualizar_interface(*args):
    ent_salario.delete(0, tk.END)
    ent_dependentes.delete(0, tk.END)
    lbl_inss.config(text="INSS: R$ 0.00")
    lbl_irrf.config(text="IRRF: R$ 0.00")
    if modo.get() == "Salário Bruto":
        lbl_salario.config(text="Salário Bruto (R$):")
        lbl_liquido.config(text="Salário Líquido: R$ 0.00")
    else:
        lbl_salario.config(text="Salário Líquido (R$):")
        lbl_liquido.config(text="Salário Bruto: R$ 0.00")

def calcular_salario():
    try:
        if modo.get() == "Salário Bruto":
            salario_bruto = float(ent_salario.get())
            dependentes = int(ent_dependentes.get())
            
            if salario_bruto < 0 or dependentes < 0:
                raise ValueError
            
            inss = calcular_inss(salario_bruto)
            base_irrf = salario_bruto - inss
            irrf = calcular_irrf(base_irrf, dependentes)
            
            salario_liquido = salario_bruto - inss - irrf
            
            lbl_inss.config(text=f"INSS: R$ {inss:.2f}")
            lbl_irrf.config(text=f"IRRF: R$ {irrf:.2f}")
            lbl_liquido.config(text=f"Salário Líquido: R$ {salario_liquido:.2f}")
            
        else:
            salario_liquido = float(ent_salario.get())
            dependentes = int(ent_dependentes.get())
            
            if salario_liquido < 0 or dependentes < 0:
                raise ValueError
            
            salario_bruto = calcular_gross_from_net(salario_liquido, dependentes)
            inss = calcular_inss(salario_bruto)
            base_irrf = salario_bruto - inss
            irrf = calcular_irrf(base_irrf, dependentes)
            
            lbl_inss.config(text=f"INSS: R$ {inss:.2f}")
            lbl_irrf.config(text=f"IRRF: R$ {irrf:.2f}")
            lbl_liquido.config(text=f"Salário Bruto: R$ {salario_bruto:.2f}")
            
    except ValueError:
        messagebox.showerror("Erro", "Valores inválidos! Insira números positivos.")

# Configuração da janela
janela = tk.Tk()
janela.title("Calculadora Salarial 2025")

# Variável de controle para o modo de cálculo
modo = tk.StringVar(value="Salário Bruto")

# Widgets
tk.Label(janela, text="Tipo de Cálculo:").grid(row=0, column=0, padx=10, pady=5)
menu_modo = tk.OptionMenu(janela, modo, "Salário Bruto", "Salário Líquido", command=atualizar_interface)
menu_modo.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

lbl_salario = tk.Label(janela, text="Salário Bruto (R$):")
lbl_salario.grid(row=1, column=0, padx=10, pady=5)
ent_salario = tk.Entry(janela)
ent_salario.grid(row=1, column=1, padx=10, pady=5)

tk.Label(janela, text="Número de Dependentes:").grid(row=2, column=0, padx=10, pady=5)
ent_dependentes = tk.Entry(janela)
ent_dependentes.grid(row=2, column=1, padx=10, pady=5)

btn_calcular = tk.Button(janela, text="Calcular", command=calcular_salario)
btn_calcular.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

lbl_inss = tk.Label(janela, text="INSS: R$ 0.00")
lbl_inss.grid(row=4, column=0, columnspan=2)

lbl_irrf = tk.Label(janela, text="IRRF: R$ 0.00")
lbl_irrf.grid(row=5, column=0, columnspan=2)

lbl_liquido = tk.Label(janela, text="Salário Líquido: R$ 0.00", font=('Arial', 10, 'bold'))
lbl_liquido.grid(row=6, column=0, columnspan=2, pady=10)

# Iniciar aplicação
janela.mainloop()