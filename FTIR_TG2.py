import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fpdf import FPDF
from datetime import datetime
import statistics
import math

class DynamicPlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coletor Dinâmico de Dados de FT-IR")

      # Variável para o cronômetro
        self.tempo_decorrido = 0

        self.tempo_medidas = [0, 0.25, 0.5, 0.75, 1, 2, 3, 4, 5, 6, 7, 8, 24, 48]
        self.valores_primeira_medida = []
        self.valores_segunda_medida = []
        self.valores_terceira_medida = []
        self.ref_espectros_primeira_medida = []
        self.ref_espectros_segunda_medida = []
        self.ref_espectros_terceira_medida = []
        self.maior_medida =[]
        self.menor_medida =[]
        self.valores_medianas = []
        self.valores_porcentagens = []
        self.RD = []
        
        self.dia = 0
        self.mes = 0
        self.ano = 0
        self.temp_tot = 48
        self.R = 0
        self.contador_coleta = -1
        self.nome_arquivo = "rltftir"
        self.contador_nome_arquivo = -1
        
        main_frame = tk.Frame(root)
        main_frame.pack(pady=10)

        # Adição do frame do cronômetro
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

        # Adicionar um frame para o campo R e o botão de coleta e deleção
        R_frame = tk.Frame(dados_experimentais_frame)
        R_frame.grid(row=1, column=0, sticky="w", pady=5)

        # Adicionar um frame para o campo "Laboratorio" e o botão de coleta e deleção de dados de viscosidade
        dados_coletados_frame = tk.Frame(coleta_dados_frame)
        dados_coletados_frame.grid(row=0, column=0, padx=10, pady=10)

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

        # Campo para entrada do "R"
        tk.Label(R_frame, text="").grid(row=0, columnspan=2)
        tk.Label(R_frame, text="Valor de R (TDI/HTPB)(massa):", font=("Arial", 10, "bold")).grid(row=1, column=0)
        self.R_entrada = tk.Entry(R_frame)
        self.R_entrada.grid(row=1, column=1)

        # Botão para coletar o "R"
        self.coletar_R_botao = tk.Button(R_frame, text="Coletar R", font=("Arial", 10, "bold"), command=self.coletar_R)
        self.coletar_R_botao.grid(row=2, column=0, pady=5)
        tk.Label(R_frame, text="", font=("Arial", 10, "bold")).grid(row=3, column=0)
        tk.Label(R_frame, text="Valores de R possíveis: 1.0, 1.05, 1.10 e 1.15.", font=("Arial", 10, "bold")).grid(row=4, column=0)

        # Botão para deletar "R"
        self.deletar_R_botao = tk.Button(R_frame, text="Deletar R", font=("Arial", 10, "bold"), command=self.deletar_R)
        self.deletar_R_botao.grid(row=2, column=1, pady=5)

        # Campo para entrada do "Laboratório"
        tk.Label(dados_coletados_frame, text="").grid(row=0, columnspan=2)
        tk.Label(dados_coletados_frame, text="Nome do Espectro da 1ª Medida (FrX):", font=("Arial", 10, "bold")).grid(row=1, column=0)
        self.nome_espectro_primeira_medida_entrada = tk.Entry(dados_coletados_frame)
        self.nome_espectro_primeira_medida_entrada.grid(row=1, column=1)
        tk.Label(dados_coletados_frame, text="Valor da 1ª Medida (A2270)(cm):", font=("Arial", 10, "bold")).grid(row=2, column=0)
        self.valor_altura_primeira_medida_entrada = tk.Entry(dados_coletados_frame)
        self.valor_altura_primeira_medida_entrada.grid(row=2, column=1)
        tk.Label(dados_coletados_frame, text="").grid(row=3, columnspan=2)
        tk.Label(dados_coletados_frame, text="Nome do Espectro da 2ª Medida (FrX):", font=("Arial", 10, "bold")).grid(row=4, column=0)
        self.nome_espectro_segunda_medida_entrada = tk.Entry(dados_coletados_frame)
        self.nome_espectro_segunda_medida_entrada.grid(row=4, column=1)
        tk.Label(dados_coletados_frame, text="Valor da 2ª Medida (A2270)(cm):", font=("Arial", 10, "bold")).grid(row=5, column=0)
        self.valor_altura_segunda_medida_entrada = tk.Entry(dados_coletados_frame)
        self.valor_altura_segunda_medida_entrada.grid(row=5, column=1)
        tk.Label(dados_coletados_frame, text="").grid(row=6, columnspan=2)
        tk.Label(dados_coletados_frame, text="Nome do Espectro da 3ª Medida (FrX):", font=("Arial", 10, "bold")).grid(row=7, column=0)
        self.nome_espectro_terceira_medida_entrada = tk.Entry(dados_coletados_frame)
        self.nome_espectro_terceira_medida_entrada.grid(row=7, column=1)
        tk.Label(dados_coletados_frame, text="Valor da 3ª Medida (A2270)(cm):", font=("Arial", 10, "bold")).grid(row=8, column=0)
        self.valor_altura_terceira_medida_entrada = tk.Entry(dados_coletados_frame)
        self.valor_altura_terceira_medida_entrada.grid(row=8, column=1)
        tk.Label(dados_coletados_frame, text="").grid(row=9, columnspan=2)

        # Botão para coletar o dados
        self.coletar_dados_botao = tk.Button(dados_coletados_frame, text="Coletar Dados", font=("Arial", 10, "bold"), command=self.coletar_dados)
        self.coletar_dados_botao.grid(row=10, column=0, pady=5)

        # Botão para deletar ultimos dados coletados
        self.deletar_dados_botao = tk.Button(dados_coletados_frame, text="Deletar Últimos Dados Coletados", font=("Arial", 10, "bold"), command=self.deletar_dados)
        self.deletar_dados_botao.grid(row=10, column=1, pady=5)

        # Campo para Manipulação de Gráficos e PDF
        tk.Label(graf_frame, text="").grid(row=0, columnspan=2)

        # Botão para atualizar ou gerar gráficos
        self.plotar_botao = tk.Button(graf_frame, text="Gerar ou Atualizar Gráficos", font=("Arial", 10, "bold"), command=self.gerar_atualizar_grafico)
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
        self.ax.set_title(f"Mediana de A2270 para R = {self.R}")
        self.ax.set_xlabel("Tempo(h)")
        self.ax.set_ylabel("A2270(cm)")

        # Posiciona a figura na tela
        self.canvas = FigureCanvasTkAgg(self.figure, master=graficos_frame)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

       # Define uma figura para que se tenha o plot da curva de cura
        self.figure2, self.ax2 = plt.subplots(figsize=(4, 4))
        self.ax2.set_title(f"Porcentagem de grupos NCO reagidos para R = {self.R}")
        self.ax2.set_xlabel("Tempo(h)")
        self.ax2.set_ylabel("Porcentagem(%)")

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

            if data.day > 0 and data.day < 31 and data.month > 0 and data.month < 12 and data.year >= 2024:
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

            if self.dia == 0 or self.mes == 0 or self.ano == 0:
                self.error_label.config(text="Data ainda não inserida.")

            else:
                self.error_label.config(text=f"A data {self.dia}/{self.mes}/{self.ano} inserida foi excluída.")
                self.dia = 0
                self.mes = 0
                self.ano = 0              

        except ValueError:
            self.error_label.config(text="Erro ao executar a função.")
    
    def coletar_R(self):
        try:
            
            self.error_label.config(text="")

            R = float(self.R_entrada.get())
            
            if R == 1.0 or R == 1.05 or R == 1.10 or R == 1.15:
                self.valores_primeira_medida = []
                self.valores_segunda_medida = []
                self.valores_terceira_medida = []
                self.ref_espectros_primeira_medida = []
                self.ref_espectros_segunda_medida = []
                self.ref_espectros_terceira_medida = []
                self.maior_medida =[]
                self.menor_medida =[]
                self.valores_medianas = []
                self.valores_porcentagens = []
                self.RD = []
                self.contador_coleta = -1
                self.R = R
                self.error_label.config(text=f"O valor de R coletado é {self.R}.") 

            else:
                self.error_label.config(text="O valor de R inserido encontra-se em formato incorreto.")              
   
            self.R_entrada.delete(0, tk.END)

        except ValueError:
            self.error_label.config(text="R em formato incorreto ou nenhum R inserido ou erro no fluxo do programa.")

    def deletar_R(self):
        try:
            
            self.error_label.config(text="")

            if self.R == 0:
                self.error_label.config(text="R ainda não coletado.")

            else:
                self.error_label.config(text=f"O valor de R {self.R} inserido foi excluído.")
                self.R = 0             

        except ValueError:
            self.error_label.config(text="Erro ao executar a função.")
    
    def arredondar(self, numero):

        if numero < 0.0005:
            return 0.001
        elif numero == 0:
            return 0
        else:
            return round(numero, 3)

    def coletar_dados(self):
        try:

            if self.R != 0:
                if self.contador_coleta < len(self.tempo_medidas) - 1:
                    self.error_label.config(text="")

                    primeiro_espectro = self.nome_espectro_primeira_medida_entrada.get()
                    R_1 = float(primeiro_espectro[2:])
                    primeira_medida = float(self.valor_altura_primeira_medida_entrada.get())
                    segundo_espectro = self.nome_espectro_segunda_medida_entrada.get()
                    R_2 = float(segundo_espectro[2:])
                    segunda_medida = float(self.valor_altura_segunda_medida_entrada.get())
                    terceiro_espectro = self.nome_espectro_terceira_medida_entrada.get()
                    R_3 = float(terceiro_espectro[2:])
                    terceira_medida = float(self.valor_altura_terceira_medida_entrada.get())

                    if primeiro_espectro[0:2] == "Fr" and segundo_espectro[0:2] == "Fr" and terceiro_espectro[0:2] == "Fr" and R_1 >=0 and R_2 >= 0 and R_3 >= 0:
                        if primeira_medida >= 0 and segunda_medida >= 0 and terceira_medida >= 0:
                            self.ref_espectros_primeira_medida.append(primeiro_espectro)
                            self.ref_espectros_segunda_medida.append(segundo_espectro)
                            self.ref_espectros_terceira_medida.append(terceiro_espectro)
                            self.valores_primeira_medida.append(primeira_medida)
                            self.valores_segunda_medida.append(segunda_medida)
                            self.valores_terceira_medida.append(terceira_medida)
                            self.maior_medida.append(max([primeira_medida, segunda_medida, terceira_medida]))
                            self.menor_medida.append(min([primeira_medida, segunda_medida, terceira_medida]))
                            self.valores_medianas.append(statistics.median([primeira_medida, segunda_medida, terceira_medida]))
                            if self.valores_medianas[-1] != 0 and self.valores_medianas[0] != 0:
                                self.valores_porcentagens.append(round((((self.valores_medianas[0] - self.valores_medianas[-1])/self.valores_medianas[0])*100), 2))
                                self.RD.append(round((self.arredondar(self.arredondar((0.591*(self.maior_medida[-1] -self.menor_medida[-1])))/math.sqrt(3)) * 100) / self.valores_medianas[-1]))
                            else:
                                self.valores_porcentagens.append(0)
                                self.RD.append(0)
                            self.contador_coleta = self.contador_coleta + 1
                            self.error_label.config(text=f"Os Espectros {primeiro_espectro}, {segundo_espectro} e {terceiro_espectro} e medidas respectivas {primeira_medida} cm, {segunda_medida} cm e {terceira_medida} cm foram armazenados.")

                        else:
                            self.error_label.config(text="Valores de medidas não positivos. Nada foi armazenado.")
                    else:
                        self.error_label.config(text="Algum nome de espectro não condizente. Nada foi armazenado.")
                else:
                    self.error_label.config(text="Todos os dados já foram coletados.")           
            else:
                self.error_label.config(text="Valor de R ainda não coletado.")

            self.nome_espectro_primeira_medida_entrada.delete(0, tk.END)
            self.nome_espectro_segunda_medida_entrada.delete(0, tk.END)
            self.nome_espectro_terceira_medida_entrada.delete(0, tk.END)
            self.valor_altura_primeira_medida_entrada.delete(0, tk.END)
            self.valor_altura_segunda_medida_entrada.delete(0, tk.END)
            self.valor_altura_terceira_medida_entrada.delete(0, tk.END)

        except ValueError:
            self.error_label.config(text="Nomes de espectros incorretos/não inseridos ou medidas incorretas/não inseridas ou erro no fluxo do programa.")   

    def deletar_dados(self):
        try:
            
            self.error_label.config(text="")

            if self.contador_coleta == -1:
                self.error_label.config(text="Não existem dados armazenados.")

            else:
                self.error_label.config(text=f"Os dados dos espectros {self.ref_espectros_primeira_medida[self.contador_coleta]}, {self.ref_espectros_segunda_medida[self.contador_coleta]} e {self.ref_espectros_terceira_medida[self.contador_coleta]} e as medidas respectivas de altura da banda analisada {self.valores_primeira_medida[self.contador_coleta]} cm, {self.valores_segunda_medida[self.contador_coleta]} cm e {self.valores_terceira_medida[self.contador_coleta]} cm inseridos foram excluídos.")
                self.contador_coleta = self.contador_coleta - 1 
                self.ref_espectros_primeira_medida.pop()
                self.ref_espectros_segunda_medida.pop() 
                self.ref_espectros_terceira_medida.pop() 
                self.valores_primeira_medida.pop() 
                self.valores_segunda_medida.pop() 
                self.valores_terceira_medida.pop() 
                self.maior_medida.pop()
                self.menor_medida.pop()
                self.valores_medianas.pop() 
                self.RD.pop()
                self.valores_porcentagens.pop()       

        except ValueError:
            self.error_label.config(text="Erro ao executar a função.")

    def gerar_atualizar_grafico(self):
        
        if self.R > 0:
            self.ax.cla()
        
            self.ax.set_title(f"Mediana de A2270 para R = {self.R}")
            self.ax.set_xlabel("Tempo(h)")
            self.ax.set_ylabel("A2270(cm)")

            self.ax.plot(self.tempo_medidas[0:self.contador_coleta + 1], self.valores_medianas, marker='o', label="Medianas", color="blue")

            self.ax.legend()

            self.canvas.draw()

            self.ax2.cla()

            self.ax2.set_title(f"Porcentagem de grupos NCO reagidos para R = {self.R}")
            self.ax2.set_xlabel("Tempo(h)")
            self.ax2.set_ylabel("Porcentagem(%)")

            self.ax2.plot(self.tempo_medidas[0:self.contador_coleta + 1], self.valores_porcentagens, marker='o', label="Porcentagem", color="blue")
            self.ax2.legend()

            self.canvas2.draw()

            self.error_label.config(text="Gráficos gerados ou atualizados com sucesso.")

        else:
            self.error_label.config(text="Valor de R ainda não coletado.")

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
                self.nome_arquivo = "rltftir"
                self.contador_nome_arquivo = -1             
   
            self.nome_pdf_entrada.delete(0, tk.END)

        except ValueError:
            self.error_label.config(text="Erro ao executar a função.")

    def arredondar_EM(self, numero):

        if numero - int(numero) >= 0.5:
            return math.ceil(numero)
        else:
            return math.floor(numero)

    def gerar_pdf(self):
        #Gera um arquivo PDF contendo os gráficos e os dados.
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, "Relatorio de Dados de FT-IT", ln=True, align='C')

        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 10, f"Data: {self.dia}/{self.mes}/{self.ano}.", ln=True)
        pdf.cell(200, 10, f"Valor de R: {self.R}", ln=True)
        pdf.cell(200, 10, f"Tempo Total de Experimento: {self.temp_tot} h", ln=True)
        pdf.cell(200, 10, "", ln=True)

        pdf.cell(200, 10, "Espectros, Medidas e Tempo para a 1ª Medição", ln=True)
        pdf.set_font("Arial", '', 10)
        for i in range(len(self.valores_primeira_medida)):
            pdf.cell(200, 10, f"Espectro: {self.ref_espectros_primeira_medida[i]}       Medida: {self.valores_primeira_medida[i]} cm      Tempo: {self.tempo_medidas[i]} horas", ln=True)
        pdf.cell(200, 10, "", ln=True)

        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 10, "Espectros, Medidas e Tempo para a 2ª Medição", ln=True)
        pdf.set_font("Arial", '', 10)
        for i in range(len(self.valores_segunda_medida)):
            pdf.cell(200, 10, f"Espectro: {self.ref_espectros_segunda_medida[i]}       Medida: {self.valores_segunda_medida[i]} cm      Tempo: {self.tempo_medidas[i]} horas", ln=True)
        pdf.cell(200, 10, "", ln=True)

        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 10, "Espectros, Medidas e Tempo para a 3ª Medição", ln=True)
        pdf.set_font("Arial", '', 10)
        for i in range(len(self.valores_terceira_medida)):
            pdf.cell(200, 10, f"Espectro: {self.ref_espectros_terceira_medida[i]}       Medida: {self.valores_terceira_medida[i]} cm      Tempo: {self.tempo_medidas[i]} horas", ln=True)
        pdf.cell(200, 10, "", ln=True)

        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 10, "Medidas e Tempo para as Medianas das Alturas", ln=True)
        pdf.set_font("Arial", '', 10)
        for i in range(len(self.valores_medianas)):
            pdf.cell(200, 10, f"Medida da Mediana: {self.valores_medianas[i]} cm      Tempo: {self.tempo_medidas[i]} horas", ln=True)
        pdf.cell(200, 10, "", ln=True)

        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 10, "Medidas e Tempo para as Porcentagens Consumidas do grupo NCO", ln=True)
        pdf.set_font("Arial", '', 10)
        for i in range(len(self.valores_porcentagens)):
            pdf.cell(200, 10, f"Medida da Porcentagem: {self.valores_porcentagens[i]:.3f} %      Tempo: {self.tempo_medidas[i]} horas", ln=True)
        pdf.cell(200, 10, "", ln=True)

        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 10, "Estatísticas dos dados", ln=True)
        pdf.set_font("Arial", '', 10)
        if len(self.valores_medianas) != 0:
            for i in range(len(self.valores_medianas)):
                pdf.cell(200, 10, f"Tempo: {self.tempo_medidas[i]} horas    Desvio Padrão Médio: {self.arredondar(self.arredondar((0.591*(self.maior_medida[i] -self.menor_medida[i])))/math.sqrt(3))}    RD(%): {self.RD[i]}", ln=True)
            if self.R == 1.0:
                if len(self.RD) >= 10:
                    pdf.cell(200, 10, f"Erro da Metodologia: {self.arredondar_EM(statistics.median(self.RD[0:10]))}", ln=True)
                else:
                    pdf.cell(200, 10, f"Erro da Metodologia: {self.arredondar_EM(statistics.median(self.RD))}", ln=True)
            if self.R == 1.05:
                if len(self.RD) >= 9:
                    pdf.cell(200, 10, f"Erro da Metodologia: {self.arredondar_EM(statistics.median(self.RD[0:9]))}", ln=True)
                else:
                    pdf.cell(200, 10, f"Erro da Metodologia: {self.arredondar_EM(statistics.median(self.RD))}", ln=True)
            if self.R == 1.10:
                if len(self.RD) >= 8:
                    pdf.cell(200, 10, f"Erro da Metodologia: {self.arredondar_EM(statistics.median(self.RD[0:8]))}", ln=True)
                else:
                    pdf.cell(200, 10, f"Erro da Metodologia: {self.arredondar_EM(statistics.median(self.RD))}", ln=True)
            if self.R == 1.15:
                if len(self.RD) >= 9:
                    pdf.cell(200, 10, f"Erro da Metodologia: {self.arredondar_EM(statistics.median(self.RD[0:9]))}", ln=True)
                else:
                    pdf.cell(200, 10, f"Erro da Metodologia: {self.arredondar_EM(statistics.median(self.RD))}", ln=True)
        pdf.cell(200, 10, "", ln=True)

        pdf.add_page()
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 10, "Gráficos dos dados analisados:", ln=True)
        self.figure.savefig("graficoftir1.png")
        self.figure2.savefig("graficoftir2.png")

        pdf.image("graficoftir1.png", x=10, y=None, w=180)
        pdf.image("graficoftir2.png", x=10, y=None, w=180)

        pdf.output(f"{self.nome_arquivo}.pdf")

        self.error_label.config(text=f"Relatório em formato PDF gerado com o nome {self.nome_arquivo}.pdf.")
      
root = tk.Tk()
app = DynamicPlotApp(root)
root.mainloop()