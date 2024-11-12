import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
from fpdf import FPDF
from datetime import datetime
import numpy as np
from scipy.stats import linregress

class DynamicPlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coletor Dinâmico de Dados de Viscosidade")

      # Variável para o cronômetro
        self.tempo_decorrido = 0

        self.tempo_medidas = []
        self.valores_processo = []
        self.valores_laboratorio = []
        self.valores_processo_linear = []
        self.valores_laboratorio_linear = []
        self.ref_sup = [10.38, 10.68, 10.98, 11.28, 11.58, 11.88, 12.19, 12.49]
        self.ref_med = [9.43, 9.71, 9.98, 10.26, 10.53, 10.8, 11.08, 11.35]
        self.ref_inf = [8.49, 8.74, 8.98, 9.23, 9.48, 9.72, 9.97, 10.22]
        self.tempo_ref = [0, 30, 60, 90, 120, 150, 180, 210]
        self.insat_tempo_proc = []
        self.insat_tempo_lab = []
        self.insat_valor_proc = []
        self.insat_valor_lab = []
        
        self.passo = 0
        self.dia = 0
        self.mes = 0
        self.ano = 0
        self.temp_tot = 0
        self.contador_proc = -1
        self.contador_lab = -1
        self.nome_arquivo = "rltpd"
        self.contador_nome_arquivo = -1

        main_frame = tk.Frame(root)
        main_frame.pack(pady=10)

        #Adição do frame do cronômetro
        cronometro_frame = tk.Frame(root)
        cronometro_frame.pack(anchor="n", pady=10)  # Centraliza e fixa no topo

        # Adição do cronômetro
        self.cronometro_label = tk.Label(cronometro_frame, text="Cronômetro: 00:00:00", font=("Arial",10, "bold"))
        self.cronometro_label.pack()

        # Iniciar cronômetro
        self.atualizar_cronometro()

        # Adicionar um frame para a seção de Dados Experimentais
        dados_experimentais_frame = tk.LabelFrame(main_frame, text="Dados Experimentais", padx=10, pady=10, font=("Arial", 10, "bold"))
        dados_experimentais_frame.grid(row=0, column=0, padx=10, pady=10)

        # Adicionar um frame para a seção de |Coleta de Dados
        coleta_dados_frame = tk.LabelFrame(main_frame, text="Coleta de Dados", padx=10, pady=10, font=("Arial", 10, "bold"))
        coleta_dados_frame.grid(row=0, column=1, padx=10, pady=10)

        # Adicionar um frame para a seção de Maipulação de Gráficos e de PDF
        manipulacao_dados_frame = tk.LabelFrame(main_frame, text="Manipulação de Gráficos e de PDF", padx=10, pady=10, font=("Arial", 10, "bold"))
        manipulacao_dados_frame.grid(row=0, column=2, padx=10, pady=10)

        # Adicionar um frame de mensagens
        mensagens_frame = tk.LabelFrame(root, text="Mensagens", padx=10, pady=10, font=("Arial", 10, "bold"))
        mensagens_frame.pack(padx=10, pady=10, fill="x")

        # Adicionar um frame para conter os gráficos 
        graficos_frame = tk.LabelFrame(root, text="Gráficos", padx=10, pady=10, font=("Arial", 10, "bold"))
        graficos_frame.pack(padx=10, pady=10, fill="both", expand=False)

        # Adicionar um frame para o campo "Data" e o botão de coleta e deleção
        data_frame = tk.Frame(dados_experimentais_frame)
        data_frame.grid(row=0, column=0, sticky="w", pady=5)

        # Adicionar um frame para o campo "Passo" e o botão de coleta e deleção
        passo_frame = tk.Frame(dados_experimentais_frame)
        passo_frame.grid(row=1, column=0, sticky="w", pady=5)

        # Adicionar um frame para o campo "Tempo Total de Experimento" e o botão de coleta e deleção
        temp_tot_frame = tk.Frame(dados_experimentais_frame)
        temp_tot_frame.grid(row=2, column=0, sticky="w", pady=5)

        # Adicionar um frame para o campo "Gerar Macação Tempotal"
        marc_temp_frame = tk.Frame(dados_experimentais_frame)
        marc_temp_frame.grid(row=3, column=0, sticky="w", pady=5)

        # Adicionar um frame para o campo "Laboratorio" e o botão de coleta e deleção de dados de viscosidade
        laboratorio_frame = tk.Frame(coleta_dados_frame)
        laboratorio_frame.grid(row=0, column=0, padx=10, pady=10)

        # Adicionar um frame para o campo "Processo" e o botão de coleta e deleção de dados de viscosidade
        processo_frame = tk.Frame(coleta_dados_frame)
        processo_frame.grid(row=1, column=0, padx=10, pady=10)

        # Adicionar um frame para Gerar/Atualizar gráficos
        graf_frame = tk.Frame(manipulacao_dados_frame)
        graf_frame.grid(row=0, column=0, padx=10, pady=10)

        # Adicionar um frame para Gerar Relatório em PDF
        pdf_frame = tk.Frame(manipulacao_dados_frame)
        pdf_frame.grid(row=1, column=0, padx=10, pady=10)

        # Campo para entrada de "Data"
        tk.Label(data_frame, text="").grid(row=0, columnspan=2)
        tk.Label(data_frame, text="Data (XX/XX/XXXX):", font=("Arial", 10, "bold")).grid(row=1, column=0)
        self.data_entrada = tk.Entry(data_frame)
        self.data_entrada.grid(row=1, column=1)

        # Botão para coletar "Data"
        self.coletar_data_botao = tk.Button(data_frame, text="Coletar Data", font=("Arial", 10, "bold"), command=self.coletar_data)
        self.coletar_data_botao.grid(row=2, column=0, pady=5)

        # Botão para deletar "Data"
        self.deletar_data_botao = tk.Button(data_frame, text="Deletar Data", font=("Arial", 10, "bold"), command=self.deletar_data)
        self.deletar_data_botao.grid(row=2, column=1, pady=5)

        # Campo para entrada do "Passo"
        tk.Label(passo_frame, text="").grid(row=0, columnspan=2)
        tk.Label(passo_frame, text="Passo (min):", font=("Arial", 10, "bold")).grid(row=1, column=0)
        self.passo_entrada = tk.Entry(passo_frame)
        self.passo_entrada.grid(row=1, column=1)

        # Botão para coletar o "Passo"
        self.coletar_passo_botao = tk.Button(passo_frame, text="Coletar Passo", font=("Arial", 10, "bold"), command=self.coletar_passo)
        self.coletar_passo_botao.grid(row=2, column=0, pady=5)

        # Botão para deletar "Passo"
        self.deletar_passo_botao = tk.Button(passo_frame, text="Deletar Passo", font=("Arial", 10, "bold"), command=self.deletar_passo)
        self.deletar_passo_botao.grid(row=2, column=1, pady=5)

        # Campo para entrada do "Tempo Total de Experimento"
        tk.Label(temp_tot_frame, text="").grid(row=0, columnspan=2)
        tk.Label(temp_tot_frame, text="Tempo Total de Experimento (min):", font=("Arial", 10, "bold")).grid(row=1, column=0)
        self.temp_tot_entrada = tk.Entry(temp_tot_frame)
        self.temp_tot_entrada.grid(row=1, column=1)

        # Botão para coletar o "Tempo Total de Experimento"
        self.coletar_temp_tot_botao = tk.Button(temp_tot_frame, text="Coletar Tempo Total de Experimento", font=("Arial", 10, "bold"), command=self.coletar_temp_tot)
        self.coletar_temp_tot_botao.grid(row=2, column=0, pady=5)

        # Botão para deletar "Tempo Total de Experimento"
        self.deletar_temp_tot_botao = tk.Button(temp_tot_frame, text="Deletar Tempo Total de Experimento", font=("Arial", 10, "bold"), command=self.deletar_temp_tot)
        self.deletar_temp_tot_botao.grid(row=2, column=1, pady=5)

        # Botão para "Gerar Marcações Temporais"
        tk.Label(marc_temp_frame, text="").grid(row=0, columnspan=2)
        self.gerar_marc_temp_botao = tk.Button(marc_temp_frame, text="Gerar Marcações Temporais", font=("Arial", 10, "bold"), command=self.gerar_marc_temp)
        self.gerar_marc_temp_botao.grid(row=1, column=0, pady=5)

        # Campo para entrada do "Laboratório"
        tk.Label(laboratorio_frame, text="").grid(row=0, columnspan=2)
        tk.Label(laboratorio_frame, text="Laboratório", font=("Arial", 10, "bold")).grid(row=1, columnspan=2)
        tk.Label(laboratorio_frame, text="Valor de viscosidade (cP):", font=("Arial", 10, "bold")).grid(row=2, column=0)
        self.valor_entrada_laboratorio = tk.Entry(laboratorio_frame)
        self.valor_entrada_laboratorio.grid(row=2, column=1)

        # Botão para coletar o dados de Viscosidade do Laboratório
        self.coletar_laboratorio_botao = tk.Button(laboratorio_frame, text="Coletar Dados de Viscosidade (Laboratório)", font=("Arial", 10, "bold"), command=self.coletar_dados_laboratorio)
        self.coletar_laboratorio_botao.grid(row=3, column=1, pady=5)

        # Botão para deletar dados de viscosidade do Laboratório
        self.deletar_laboratorio_botao = tk.Button(laboratorio_frame, text="Deletar Último Dado de Viscosidade (Laboratório)", font=("Arial", 10, "bold"), command=self.deletar_dados_laboratorio)
        self.deletar_laboratorio_botao.grid(row=4, column=1, pady=5)
        
        # Campo para entrada do "Processo"
        tk.Label(laboratorio_frame, text="").grid(row=0, columnspan=2)
        tk.Label(processo_frame, text="Processo", font=("Arial", 10, "bold")).grid(row=1, columnspan=2)
        tk.Label(processo_frame, text="Valor de viscosidade (cP):", font=("Arial", 10, "bold")).grid(row=2, column=0)
        self.valor_entrada_processo = tk.Entry(processo_frame)
        self.valor_entrada_processo.grid(row=2, column=1)

        # Botão para coletar o dados de Viscosidade do Processo
        self.coletar_processo_botao = tk.Button(processo_frame, text="Coletar Dados de Viscosidade (Processo)", font=("Arial", 10, "bold"), command=self.coletar_dados_processo)
        self.coletar_processo_botao.grid(row=3, column=1, pady=5)

        # Botão para deletar dados de viscosidade do Processo
        self.deletar_processo_botao = tk.Button(processo_frame, text="Deletar Útimo Dado de Viscosidade (Processo)", font=("Arial", 10, "bold"), command=self.deletar_dados_processo)
        self.deletar_processo_botao.grid(row=4, column=1, pady=5)

        # Campo para Manipulação de Gráficos e PDF
        tk.Label(graf_frame, text="").grid(row=0, columnspan=2)

        # Botão para atualizar ou gerar gráficos
        self.plotar_botao = tk.Button(graf_frame, text="Gerar/Atualizar Gráficos", font=("Arial", 10, "bold"), command=self.gerar_atualizar_grafico)
        self.plotar_botao.grid(row=1, column=0)

        # Campo para Gerar Relatório em PDF
        tk.Label(pdf_frame, text="").grid(row=2, column=0)
        tk.Label(pdf_frame, text="Nome do Arquivo PDF:", font=("Arial", 10, "bold")).grid(row=3, column=0)
        self.nome_pdf_entrada = tk.Entry(pdf_frame)
        self.nome_pdf_entrada.grid(row=3, column=1)

        # Botão para coletar nome do arquivo pdf
        self.coletar_nome_pdf_botao = tk.Button(pdf_frame, text="Coletar Nome do Arquivo PDF", font=("Arial", 10, "bold"), command=self.coletar_nome_arquivo)
        self.coletar_nome_pdf_botao.grid(row=4, column=1, pady=5)

        # Botão para deletar nome do arquivo pdf
        self.deletar_nome_pdf_botao = tk.Button(pdf_frame, text="Deletar Nome do Arquivo PDF", font=("Arial", 10, "bold"), command=self.deletar_nome_arquivo)
        self.deletar_nome_pdf_botao.grid(row=5, column=1, pady=5)

        # Botão para gerar arquivo pdf
        tk.Label(pdf_frame, text="").grid(row=4, column=0)
        self.gerar_pdf_botao = tk.Button(pdf_frame, text="Gerar Arquivo PDF", font=("Arial", 10, "bold"), command=self.gerar_pdf)
        self.gerar_pdf_botao.grid(row=6, column=1, pady=5)
        
        self.error_label = tk.Label(mensagens_frame, text="", font=("Arial", 10, "bold"), fg="red")
        self.error_label.pack()

        # Define uma figura para que se tenha o plot da curva linearizada de cura
        self.figure, self.ax = plt.subplots(figsize=(4, 4))
        self.ax.set_title("Curva linearizada de cura")
        self.ax.set_xlabel("Tempo(min)")
        self.ax.set_ylabel("Ln da viscosidade")

        # Posiciona a figura na tela
        self.canvas = FigureCanvasTkAgg(self.figure, master=graficos_frame)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

       # Define uma figura para que se tenha o plot da curva de cura
        self.figure2, self.ax2 = plt.subplots(figsize=(4, 4))
        self.ax2.set_title("Curva de Cura")
        self.ax2.set_xlabel("Tempo(min)")
        self.ax2.set_ylabel("Viscosidade(cP)")

        # Posiciona a figura na tela
        self.canvas2 = FigureCanvasTkAgg(self.figure2, master=graficos_frame)
        self.canvas2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def atualizar_cronometro(self):
            horas = self.tempo_decorrido // 3600
            minutos = (self.tempo_decorrido % 3600) // 60
            segundos = self.tempo_decorrido % 60
            self.cronometro_label.config(text=f"Cronômetro: {horas:02}:{minutos:02}:{segundos:02}")
            self.tempo_decorrido += 1
            self.root.after(1000, self.atualizar_cronometro)  # Atualiza o cronômetro a cada segundo

    def coletar_data(self):
        try:
            
            self.error_label.config(text="")

            data = datetime.strptime(self.data_entrada.get(), "%d/%m/%Y")

            if data.day > 0 and data.day <= 31 and data.month > 0 and data.month <= 12 and data.year >= 2024:
                self.dia = data.day
                self.mes = data.month
                self.ano = data.year
                self.error_label.config(text=f"A data coletada é {self.dia}/{self.mes}/{self.ano}.")

            else:
                self.error_label.config(text="A data inserida encontra-se em formato incorreto. Datas válidas a partir de 2024.")               
   
            self.data_entrada.delete(0, tk.END)

        except ValueError:
            self.error_label.config(text="Data em formato incorreto ou nenhuma data inserida ou erro no fluxo do programa.")

    def deletar_data(self):
        try:
            
            self.error_label.config(text="")

            if self.dia == 0 and self.mes == 0 and self.ano == 0:
                self.error_label.config(text="Data ainda não inserida.")

            else:
                self.error_label.config(text=f"A data {self.dia}/{self.mes}/{self.ano} inserida foi excluída.")
                self.dia = 0
                self.mes = 0
                self.ano = 0              

        except ValueError:
            self.error_label.config(text="Erro ao executar a função.")
    
    def coletar_passo(self):
        try:
            
            self.error_label.config(text="")

            passo = float(self.passo_entrada.get())

            if passo <= 0:
                self.error_label.config(text="O passo inserido encontra-se em formato incorreto.")

            else:
                self.passo = passo
                self.tempo_medidas = []
                self.valores_processo = []
                self.valores_laboratorio = []
                self.valores_processo_linear = []
                self.valores_laboratorio_linear = []
                self.insat_tempo_proc = []
                self.insat_tempo_lab = []
                self.insat_valor_proc = []
                self.insat_valor_lab = []
                self.contador_proc = -1
                self.contador_lab = -1
                self.error_label.config(text=f"O passo coletado é {self.passo} min.")               
   
            self.passo_entrada.delete(0, tk.END)

        except ValueError:
            self.error_label.config(text="Passo em formato incorreto ou nenhum passo inserido ou erro no fluxo do programa.")

    def deletar_passo(self):
        try:
            
            self.error_label.config(text="")

            if self.passo == 0:
                self.error_label.config(text="Passo ainda não coletado.")

            else:
                self.error_label.config(text=f"O passo de {self.passo} min inserido foi excluído.")
                self.passo = 0             

        except ValueError:
            self.error_label.config(text="Erro ao executar a função.")

    def coletar_temp_tot(self):
        try:
            
            self.error_label.config(text="")

            ttot = float(self.temp_tot_entrada.get())

            if ttot <= 0:
                self.error_label.config(text="O tempo total inserido encontra-se em formato incorreto.")

            else:
                self.temp_tot = ttot
                self.tempo_medidas = []
                self.valores_processo = []
                self.valores_laboratorio = []
                self.valores_processo_linear = []
                self.valores_laboratorio_linear = []
                self.insat_tempo_proc = []
                self.insat_tempo_lab = []
                self.insat_valor_proc = []
                self.insat_valor_lab = []
                self.contador_proc = -1
                self.contador_lab = -1
                self.error_label.config(text=f"O tempo total de experimento coletado é {self.temp_tot} min.")               
   
            self.temp_tot_entrada.delete(0, tk.END)

        except ValueError:
            self.error_label.config(text="Tempo Total em formato incorreto ou nenhum tempo total de experimento inserido ou erro no fluxo do programa.")

    def deletar_temp_tot(self):
        try:
            
            self.error_label.config(text="")

            if self.temp_tot == 0:
                self.error_label.config(text="Tempo Total de Experimento ainda não coletado.")

            else:
                self.error_label.config(text=f"O tempo total de experimento de {self.temp_tot} min inserido foi excluído.")
                self.temp_tot = 0             

        except ValueError:
            self.error_label.config(text="Erro ao executar a função.")

    def gerar_marc_temp(self):

        self.error_label.config(text="")

        if self.passo == 0:
            self.error_label.config(text="Passo ainda não coletado.")

        elif self.temp_tot == 0:
            self.error_label.config(text="Tempo Total de Experimento ainda não coletado.")

        else:
            self.tempo_medidas = []
            self.valores_processo = []
            self.valores_laboratorio = []
            self.valores_processo_linear = []
            self.valores_laboratorio_linear = []
            self.insat_tempo_proc = []
            self.insat_tempo_lab = []
            self.insat_valor_proc = []
            self.insat_valor_lab = []
            self.contador_proc = -1
            self.contador_lab = -1
            for i in range(0, math.floor(self.temp_tot / self.passo) + 1):
                self.tempo_medidas.append(i * self.passo)
            self.error_label.config(text=f"O intervalo de {self.temp_tot} min foi dividido em {math.floor(self.temp_tot / self.passo) + 1} marcações. A primeira marcação é de {self.tempo_medidas[0]} min e a última é de {math.floor((self.temp_tot / self.passo))*self.passo} min.")

    def coletar_dados_laboratorio(self):
        try:
            
            self.error_label.config(text="")
            
            valor_laboratorio = float(self.valor_entrada_laboratorio.get())
            
            if len(self.tempo_medidas) == 0:
                self.error_label.config(text="Marcações temporais ainda não geradas e o dado inserido para laboratório não foi coletado.")
            elif self.contador_lab < len(self.tempo_medidas) - 1:
                if valor_laboratorio < 0:
                    self.error_label.config(text="O valor de viscosidade relativo à escala laboratorial inserido encontra-se em formato incorreto.")
                else:
                    self.contador_lab = self.contador_lab + 1
                    self.valores_laboratorio.append(valor_laboratorio)
                    self.valores_laboratorio_linear.append(round(math.log(valor_laboratorio), 2))
                    if (0.01*self.tempo_medidas[self.contador_lab] + 10.378) < math.log(valor_laboratorio) or (0.0082*self.tempo_medidas[self.contador_lab] + 8.49) > math.log(valor_laboratorio):
                        self.error_label.config(text=f"O valor de viscosidade {valor_laboratorio} cP, que não satisfaz os critérios de aceite para a escala laboratorial, relativo à marcação temporal {self.tempo_medidas[self.contador_lab]} min foi coletado.")
                        self.insat_tempo_lab.append(self.tempo_medidas[self.contador_lab])
                        self.insat_valor_lab.append(valor_laboratorio)
                    else:
                        self.error_label.config(text=f"O valor de viscosidade {valor_laboratorio} cP para a escala laboratorial relativo à marcação temporal {self.tempo_medidas[self.contador_lab]} min foi coletado.")
            else:
                self.error_label.config(text="Todos os dados para a escala laboratorial já foram coletados.")

            self.valor_entrada_laboratorio.delete(0, tk.END)

        except ValueError:
            self.error_label.config(text="Valor de viscosidade para escala laboratorial em formato incorreto ou nenhum valor de viscosidade laboratorial inserido ou erro no fluxo do programa.")   

    def deletar_dados_laboratorio(self):
        try:
            
            self.error_label.config(text="")

            if self.contador_lab == -1:
                self.error_label.config(text="Nenhum valor de viscosidade na escala laboratorial foi coletado.")

            else:
                self.error_label.config(text=f"O valor de viscosidade relativo à escala laboratorial {self.valores_laboratorio[self.contador_lab]} cP, correspondente à marcação temporal {self.tempo_medidas[self.contador_lab]} min, inserido foi excluído.")
                if len(self.insat_valor_lab) != 0:    
                    if self.insat_valor_lab[-1] == self.valores_laboratorio[self.contador_lab]:
                        self.insat_valor_lab.pop()
                        self.insat_tempo_lab.pop()
                self.contador_lab = self.contador_lab - 1 
                self.valores_laboratorio.pop()  
                self.valores_laboratorio_linear.pop()          

        except ValueError:
            self.error_label.config(text="Erro ao executar a função.")

    def coletar_dados_processo(self):
        try:
            
            self.error_label.config(text="")
            
            valor_processo = float(self.valor_entrada_processo.get())
            
            if len(self.tempo_medidas) == 0:
                self.error_label.config(text="Marcações temporais ainda não geradas e o dado inserido para processo não foi coletado.")
            elif self.contador_proc < len(self.tempo_medidas) - 1:
                if valor_processo < 0:
                    self.error_label.config(text="O valor de viscosidade relativo à escala processual inserido encontra-se em formato incorreto.")
                else:
                    self.contador_proc = self.contador_proc + 1
                    self.valores_processo.append(valor_processo)
                    self.valores_processo_linear.append(round(math.log(valor_processo), 2))
                    if (0.01*self.tempo_medidas[self.contador_proc] + 10.378) < math.log(valor_processo) or (0.0082*self.tempo_medidas[self.contador_proc] + 8.49) > math.log(valor_processo):
                        self.error_label.config(text=f"O valor de viscosidade {valor_processo} cP, que não satisfaz os critérios de aceite para a escala processual, relativo à marcação temporal {self.tempo_medidas[self.contador_proc]} min foi coletado.")
                        self.insat_tempo_proc.append(self.tempo_medidas[self.contador_proc])
                        self.insat_valor_proc.append(valor_processo)
                    else:
                        self.error_label.config(text=f"O valor de viscosidade {valor_processo} cP para a escala processual relativo à marcação temporal {self.tempo_medidas[self.contador_proc]} min foi coletado.")
            else: 
                self.error_label.config(text="Todos os dados para a escala processual já foram coletados.")

            self.valor_entrada_processo.delete(0, tk.END)

        except ValueError:
            self.error_label.config(text="Valor de viscosidade para escala processual em formato incorreto ou nenhum valor de viscosidade processual inserido ou erro no fluxo do programa.") 

    def deletar_dados_processo(self):
        try:
            
            self.error_label.config(text="")

            if self.contador_proc == -1:
                self.error_label.config(text="Nenhum valor de viscosidade na escala processual foi coletado.")

            else:
                self.error_label.config(text=f"O valor de viscosidade relativo à escala processual {self.valores_processo[self.contador_proc]} cP, correspondente à marcação temporal {self.tempo_medidas[self.contador_proc]} min, inserido foi excluído.")
                if len(self.insat_valor_proc) != 0:    
                    if self.insat_valor_proc[-1] == self.valores_processo[self.contador_proc]:
                        self.insat_valor_proc.pop()
                        self.insat_tempo_proc.pop()
                self.contador_proc = self.contador_proc - 1  
                self.valores_processo.pop() 
                self.valores_processo_linear.pop()          

        except ValueError:
            self.error_label.config(text="Erro ao executar a função.")

    def gerar_atualizar_grafico(self):
        
        self.ax.cla()
      
        self.ax.set_title("Curva de Cura linearizada")
        self.ax.set_xlabel("Tempo(min)")
        self.ax.set_ylabel("Ln da viscosidade")

        self.ax.plot(self.tempo_medidas[0:self.contador_proc + 1], self.valores_processo_linear, marker='o', label="Processo", color="blue")
        self.ax.plot(self.tempo_medidas[0:self.contador_lab + 1], self.valores_laboratorio_linear, marker='o', label="Laboratório", color="green")
        self.ax.plot(self.tempo_ref, self.ref_inf, marker='o', label="Limite inferior", color="red")
        self.ax.plot(self.tempo_ref, self.ref_med, marker='o', label="Linha media", color="black")
        self.ax.plot(self.tempo_ref, self.ref_sup, marker='o', label="Limite inferior", color="pink")

        self.ax.legend()

        self.canvas.draw()

        self.ax2.cla()

        self.ax2.set_title("Curva de cura")
        self.ax2.set_xlabel("Tempo(min)")
        self.ax2.set_ylabel("Viscosidade(cP)")

        self.ax2.plot(self.tempo_medidas[0:self.contador_proc + 1], self.valores_processo, marker='o', label="Processo", color="blue")
        self.ax2.plot(self.tempo_medidas[0:self.contador_lab + 1], self.valores_laboratorio, marker='o', label="Laboratório", color="green")
        self.ax2.legend()

        self.canvas2.draw()

        self.error_label.config(text="Gráficos gerados ou atualizados com sucesso.")

    def coletar_nome_arquivo(self):
        try:
            
            self.error_label.config(text="")

            nome = self.nome_pdf_entrada.get()

            caracteres_proibidos = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '.']

            if any(caractere in nome for caractere in caracteres_proibidos) == True:
                self.error_label.config(text="Nome do Arquivo em formato não aceito.")

            else:
                self.nome_arquivo = nome
                self.contador_nome_arquivo = 1
                self.error_label.config(text=f"O nome do arquivo PDF é {self.nome_arquivo}.")               
   
            self.nome_pdf_entrada.delete(0, tk.END)

        except ValueError:
            self.error_label.config(text="Nome do Arquivo PDF em formato errado ou não inserido ou erro ao executar a função.")

    def deletar_nome_arquivo(self):
        try:
            
            self.error_label.config(text="")

            if self.contador_nome_arquivo == -1:
                self.error_label.config(text="Nome do Arquivo PDF ainda não inserido.")

            else:
                self.error_label.config(text=f"O Nome do Arquivo ({self.nome_arquivo}) PDF inserido foi excluído.")
                self.nome_arquivo = "rltpd"
                self.contador_nome_arquivo = -1             

        except ValueError:
            self.error_label.config(text="Erro ao executar a função.")
   
    def gerar_pdf(self):
        #Gera um arquivo PDF contendo os gráficos e os dados.
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, "Relatorio de Dados de Viscosidade", ln=True, align='C')

        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 10, f"Data: {self.dia}/{self.mes}/{self.ano}.", ln=True)
        pdf.cell(200, 10, f"Valor do Passo: {self.passo} min.", ln=True)
        pdf.cell(200, 10, f"Tempo Total de Experimento: {self.temp_tot} min.", ln=True)
        pdf.cell(200, 10, "", ln=True)

        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 10, "Medidas Laboratoriais - Tempos e Valores de Viscosidade", ln=True)
        pdf.set_font("Arial", '', 10)
        for i in range(len(self.valores_laboratorio)):
            pdf.cell(200, 10, f"Tempo: {self.tempo_medidas[i]} min      Viscosidade: {self.valores_laboratorio[i]} cP", ln=True)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 10, "Medidas Laboratoriais - Tempos e Valores de Viscosidade Linearizados", ln=True)
        pdf.set_font("Arial", '', 10)
        for i in range(len(self.valores_laboratorio_linear)):
            pdf.cell(200, 10, f"Tempo: {self.tempo_medidas[i]} min      Viscosidade: {self.valores_laboratorio_linear[i]}", ln=True)
        if len(self.insat_tempo_lab) != 0:
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(200, 10, "Os seguintes pontos não satisfizeram as condição de cura satisfatória para o experimento laboratorial:", ln=True)
            pdf.set_font("Arial", '', 10)
            for i in range(len(self.insat_tempo_lab)):
                pdf.cell(200, 10, f"Tempo: {self.insat_tempo_lab[i]} min        Viscosidade: {self.insat_valor_lab[i]} cP      Viscosidade Linearizada: {math.log(self.insat_valor_lab):.2f}", ln=True)
        pdf.cell(200, 10, "", ln=True)

        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 10, "Medidas Processuais - Tempos e Valores de Viscosidade", ln=True)
        pdf.set_font("Arial", '', 10)
        for i in range(len(self.valores_processo)):
            pdf.cell(200, 10, f"Tempo: {self.tempo_medidas[i]} min      Viscosidade: {self.valores_processo[i]} cP", ln=True)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 10, "Medidas Processuais - Tempos e Valores de Viscosidade Linearizados", ln=True)
        pdf.set_font("Arial", '', 10)
        for i in range(len(self.valores_processo_linear)):
            pdf.cell(200, 10, f"Tempo: {self.tempo_medidas[i]} min      Viscosidade Linearizada: {self.valores_processo_linear[i]}", ln=True)
        if len(self.insat_tempo_proc) != 0:
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(200, 10, "Os seguintes pontos não satisfizeram as condição de cura satisfatória para o experimento processual:", ln=True)
            pdf.set_font("Arial", '', 10)
            for i in range(len(self.insat_tempo_proc)):
                pdf.cell(200, 10, f"Tempo: {self.insat_tempo_proc[i]} min       Viscosidade: {self.insat_valor_proc[i]} cP     Viscosidade Linearizada: {math.log(self.insat_valor_proc):.2f}", ln=True)
        pdf.cell(200, 10, "", ln=True)

        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 10, "Equações das Curvas Linearizadas de Referência:", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.cell(200, 10, "Equação da Curva de Limite Superior: y = 0.0100t + 10.3780.", ln=True)
        pdf.cell(200, 10, "Equação da Curva Média: y = 0.0091t + 9.4333.", ln=True)
        pdf.cell(200, 10, "Equação da Curva de Limite Inferior: y = 0.0082t + 8.4900.", ln=True)
        pdf.cell(200, 10, "", ln=True)

        if len(self.valores_laboratorio_linear) >= 2 and len(self.valores_processo_linear) >= 2:
            valores_proc = np.array(self.valores_processo_linear[0:self.contador_proc + 1])
            valores_lab = np.array(self.valores_laboratorio_linear[0:self.contador_lab + 1])
            tempo_proc = np.array(self.tempo_medidas[0:self.contador_proc + 1])
            tempo_lab = np.array(self.tempo_medidas[0:self.contador_lab + 1])
            coef_ang_proc, coef_lin_proc, r_proc, _, _ = linregress(tempo_proc, valores_proc)
            coef_ang_lab, coef_lin_lab, r_lab, _, _ = linregress(tempo_lab, valores_lab)
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(200, 10, "Equações das Curvas Linearizadas e seus respectivos valores de R²:", ln=True)
            pdf.set_font("Arial", '', 10)
            pdf.cell(200, 10, f" Equação da Curva Linearizada para Escala Laboratorial: y = {coef_ang_lab:.4f}t + {coef_lin_lab:.4f}    R² = {r_lab**2:.4f}", ln=True)
            pdf.cell(200, 10, f" Equação da Curva Linearizada para Escala Processual: y = {coef_ang_proc:.4f}t + {coef_lin_proc:.4f}  R² = {r_proc**2:.4f}", ln=True)
            pdf.cell(200, 10, "", ln=True)
        else:
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(200, 10, "Nenhum dado de curva linearizada coletado ou pontos insuficientes.", ln=True)
            pdf.cell(200, 10, "", ln=True)
        
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 10, "Conclusão do Experimento:", ln=True)
        if len(self.insat_valor_lab) != 0:
            pdf.cell(200, 10, "O experimento em escala laboratorial não satisfaz os critérios de cura satisfatória.", ln=True)
            if len(self.insat_valor_proc) != 0:
                pdf.cell(200, 10, "O experimento em escala processual não satisfaz os critérios de cura satisfatória.", ln=True)
            else:
                pdf.cell(200, 10, "O experimento em escala processual satisfaz os critérios de cura satisfatória.", ln=True)
        else:
            pdf.cell(200, 10, "O experimento em escala laboratorial satisfaz os critérios de cura satisfatória.", ln=True)
            if len(self.insat_valor_proc) != 0:
                pdf.cell(200, 10, "O experimento em escala processual não satisfaz os critérios de cura satisfatória.", ln=True)
            else:
                pdf.cell(200, 10, "O experimento em escala processual satisfaz os critérios de cura satisfatória.", ln=True)
        pdf.cell(200, 10, "", ln=True)
        
        pdf.add_page()
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 10, "Gráficos dos dados analisados:", ln=True)

        self.figure.savefig("grafico1visc.png")
        self.figure2.savefig("grafico2visc.png")

        pdf.image("grafico1visc.png", x=10, y=None, w=180)
        pdf.image("grafico2visc.png", x=10, y=None, w=180)

        pdf.output(f"{self.nome_arquivo}.pdf")

        self.error_label.config(text=f"Relatório em formato PDF gerado com o nome {self.nome_arquivo}.pdf")
    
root = tk.Tk()
app = DynamicPlotApp(root)
root.mainloop()