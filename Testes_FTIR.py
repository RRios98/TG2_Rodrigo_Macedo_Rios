import unittest
from FTIR_TG2 import DynamicPlotApp
from tkinter import Tk
class TestFTIRApp(unittest.TestCase):

    def setUp(self):
        # Configura o ambiente para cada teste
        self.root = Tk()
        self.app = DynamicPlotApp(self.root)

    def tearDown(self):
        # Finalização do ambiente de testes
        self.root.destroy()

    # Helper para obter a mensagem de saída do label de erro
    def mensagem_erro(self):
        return self.app.error_label.cget("text")

    # Teste de coleta de data 
    def teste_coleta_data(self):
        self.app.data_entrada.insert(0, "10/11/2024")
        self.app.coletar_data()
        self.assertEqual((self.app.dia, self.app.mes, self.app.ano), (10, 11, 2024))
        self.assertEqual(self.mensagem_erro(), "A data coletada é 10/11/2024.")
    
    # Teste de coleta de data antes de 2024
    def teste_coleta_data_antes_2024(self):
        self.app.data_entrada.insert(0, "10/11/2023")
        self.app.coletar_data()
        self.assertEqual((self.app.dia, self.app.mes, self.app.ano), (0, 0, 0))
        self.assertEqual(self.mensagem_erro(), "A data inserida encontra-se em formato incorreto. Datas válidas a partir de 2024.")
    
    # Teste de coleta de data em formato incorreto
    def teste_coleta_data_formato_incorreto(self):
        self.app.data_entrada.insert(0, "-35/19/30596")
        self.app.coletar_data()
        self.assertEqual((self.app.dia, self.app.mes, self.app.ano), (0, 0, 0))
        self.assertEqual(self.mensagem_erro(), "Data em formato incorreto ou nenhuma data inserida ou erro no fluxo do programa.")

    # Teste de coleta de data sem inserção de dado
    def teste_coleta_data_sem_insercao(self):
        self.app.data_entrada.insert(0, "")
        self.app.coletar_data()
        self.assertEqual((self.app.dia, self.app.mes, self.app.ano), (0, 0, 0))
        self.assertEqual(self.mensagem_erro(), "Data em formato incorreto ou nenhuma data inserida ou erro no fluxo do programa.")
    
    # Teste de deleção de data sem coleta anterior 
    def teste_delecao_data_sem_coleta(self):
        self.app.deletar_data()
        self.assertEqual((self.app.dia, self.app.mes, self.app.ano), (0, 0, 0))
        self.assertEqual(self.mensagem_erro(), "Data ainda não inserida.")

     # Teste de deleção de data já inserida
    def teste_delecao_data_ja_coletada(self):
        self.app.data_entrada.insert(0, "10/11/2024")
        self.app.coletar_data()
        self.app.deletar_data()
        self.assertEqual((self.app.dia, self.app.mes, self.app.ano), (0, 0, 0))
        self.assertEqual(self.mensagem_erro(), "A data 10/11/2024 inserida foi excluída.")

    # Teste de coleta de R
    def teste_coleta_R(self):
        self.app.R_entrada.insert(0, "1")
        self.app.coletar_R()
        self.assertEqual(self.app.R, 1)
        self.assertEqual(self.mensagem_erro(), "O valor de R coletado é 1.0.")

    # Teste de coleta de R sem inserção de dado
    def teste_coleta_R_sem_insercao(self):
        self.app.R_entrada.insert(0, "")
        self.app.coletar_R()
        self.assertEqual(self.app.R, 0)
        self.assertEqual(self.mensagem_erro(), "R em formato incorreto ou nenhum R inserido ou erro no fluxo do programa.")

    # Teste de coleta de R negativo
    def teste_coleta_R_negativo(self):
        self.app.R_entrada.insert(0, "-30")
        self.app.coletar_R()
        self.assertEqual(self.app.R, 0)
        self.assertEqual(self.mensagem_erro(), "O valor de R inserido encontra-se em formato incorreto.")

    # Teste de coleta de R em formato incorreto
    def teste_coleta_R_formato_incorreto(self):
        self.app.R_entrada.insert(0, "1.25")
        self.app.coletar_R()
        self.assertEqual(self.app.R, 0)
        self.assertEqual(self.mensagem_erro(), "O valor de R inserido encontra-se em formato incorreto.")

    # Teste de deleção de R sem coleta anterior 
    def teste_delecao_R_sem_coleta(self):
        self.app.deletar_R()
        self.assertEqual(self.app.R, 0)
        self.assertEqual(self.mensagem_erro(), "R ainda não coletado.")

    # Teste de deleção de R já coletado
    def teste_delecao_R_ja_coletado(self):
        self.app.R = 1.0
        self.app.deletar_R()
        self.assertEqual(self.app.R, 0)
        self.assertEqual(self.mensagem_erro(), "O valor de R 1.0 inserido foi excluído.")
    
    # Testes de coleta de dados
    def teste_coleta_dados(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "Fr231289")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "Fr231319")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "Fr231348")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "0.052")
        self.app.valor_altura_segunda_medida_entrada.insert(0, "0.058")
        self.app.valor_altura_terceira_medida_entrada.insert(0, "0.059")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287', 'Fr231288', 'Fr231289'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317', 'Fr231318', 'Fr231319'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346', 'Fr231347', 'Fr231348'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113, 0.068, 0.052])
        self.assertEqual(self.app.valores_segunda_medida, [0.122, 0.065, 0.058])
        self.assertEqual(self.app.valores_terceira_medida, [0.109, 0.077, 0.059])
        self.assertEqual(self.app.maior_medida, [0.122, 0.077, 0.059])
        self.assertEqual(self.app.menor_medida, [0.109, 0.065, 0.052])
        self.assertEqual(self.app.valores_medianas, [0.113, 0.068, 0.058])         
        self.assertEqual(self.app.valores_porcentagens, [0.00, 39.82, 48.67])
        self.assertEqual(self.app.RD, [4, 6, 3])
        self.assertEqual(self.app.contador_coleta, 2)        
        self.assertEqual(self.mensagem_erro(), "Os Espectros Fr231289, Fr231319 e Fr231348 e medidas respectivas 0.052 cm, 0.058 cm e 0.059 cm foram armazenados.")
    
    # Testes de coleta de dados sem inserção de dado de nome do 1º espectro
    def teste_coleta_dados_sem_insercao_nome_1_espectro(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "Fr231319")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "Fr231348")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "0.052")
        self.app.valor_altura_segunda_medida_entrada.insert(0, "0.058")
        self.app.valor_altura_terceira_medida_entrada.insert(0, "0.059")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287', 'Fr231288'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317', 'Fr231318'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346', 'Fr231347'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113, 0.068])
        self.assertEqual(self.app.valores_segunda_medida, [0.122, 0.065])
        self.assertEqual(self.app.valores_terceira_medida, [0.109, 0.077])
        self.assertEqual(self.app.maior_medida, [0.122, 0.077])
        self.assertEqual(self.app.menor_medida, [0.109, 0.065])
        self.assertEqual(self.app.valores_medianas, [0.113, 0.068])         
        self.assertEqual(self.app.valores_porcentagens, [0.00, 39.82])
        self.assertEqual(self.app.RD, [4, 6])
        self.assertEqual(self.app.contador_coleta, 1)        
        self.assertEqual(self.mensagem_erro(), "Nomes de espectros incorretos/não inseridos ou medidas incorretas/não inseridas ou erro no fluxo do programa.")

    # Testes de coleta de dados sem inserção de dado de nome do 2º espectro
    def teste_coleta_dados_sem_insercao_nome_2_espectro(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "Fr231289")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "Fr231348")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "0.052")
        self.app.valor_altura_segunda_medida_entrada.insert(0, "0.058")
        self.app.valor_altura_terceira_medida_entrada.insert(0, "0.059")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287', 'Fr231288'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317', 'Fr231318'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346', 'Fr231347'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113, 0.068])
        self.assertEqual(self.app.valores_segunda_medida, [0.122, 0.065])
        self.assertEqual(self.app.valores_terceira_medida, [0.109, 0.077])
        self.assertEqual(self.app.maior_medida, [0.122, 0.077])
        self.assertEqual(self.app.menor_medida, [0.109, 0.065])
        self.assertEqual(self.app.valores_medianas, [0.113, 0.068])         
        self.assertEqual(self.app.valores_porcentagens, [0.00, 39.82])
        self.assertEqual(self.app.RD, [4, 6])
        self.assertEqual(self.app.contador_coleta, 1)        
        self.assertEqual(self.mensagem_erro(), "Nomes de espectros incorretos/não inseridos ou medidas incorretas/não inseridas ou erro no fluxo do programa.")

    # Testes de coleta de dados sem inserção de dado de nome do 3º espectro
    def teste_coleta_dados_sem_insercao_nome_3_espectro(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "Fr231289")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "Fr231319")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "0.052")
        self.app.valor_altura_segunda_medida_entrada.insert(0, "0.058")
        self.app.valor_altura_terceira_medida_entrada.insert(0, "0.059")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287', 'Fr231288'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317', 'Fr231318'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346', 'Fr231347'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113, 0.068])
        self.assertEqual(self.app.valores_segunda_medida, [0.122, 0.065])
        self.assertEqual(self.app.valores_terceira_medida, [0.109, 0.077])
        self.assertEqual(self.app.maior_medida, [0.122, 0.077])
        self.assertEqual(self.app.menor_medida, [0.109, 0.065])
        self.assertEqual(self.app.valores_medianas, [0.113, 0.068])         
        self.assertEqual(self.app.valores_porcentagens, [0.00, 39.82])
        self.assertEqual(self.app.RD, [4, 6])
        self.assertEqual(self.app.contador_coleta, 1)        
        self.assertEqual(self.mensagem_erro(), "Nomes de espectros incorretos/não inseridos ou medidas incorretas/não inseridas ou erro no fluxo do programa.")
    
    # Testes de coleta de dados com dado de nome do 1º espectro em formato incorreto
    def teste_coleta_dados_nome_1_espectro_formato_incorreto(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "Ab50")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "Fr231319")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "Fr231348")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "0.052")
        self.app.valor_altura_segunda_medida_entrada.insert(0, "0.058")
        self.app.valor_altura_terceira_medida_entrada.insert(0, "0.059")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287', 'Fr231288'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317', 'Fr231318'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346', 'Fr231347'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113, 0.068])
        self.assertEqual(self.app.valores_segunda_medida, [0.122, 0.065])
        self.assertEqual(self.app.valores_terceira_medida, [0.109, 0.077])
        self.assertEqual(self.app.maior_medida, [0.122, 0.077])
        self.assertEqual(self.app.menor_medida, [0.109, 0.065])
        self.assertEqual(self.app.valores_medianas, [0.113, 0.068])         
        self.assertEqual(self.app.valores_porcentagens, [0.00, 39.82])
        self.assertEqual(self.app.RD, [4, 6])
        self.assertEqual(self.app.contador_coleta, 1)        
        self.assertEqual(self.mensagem_erro(), "Algum nome de espectro não condizente. Nada foi armazenado.")

    # Testes de coleta de dados com dado de nome do 2º espectro em formato incorreto
    def teste_coleta_dados_nome_2_espectro_formato_incorreto(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "Fr231289")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "Ab50")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "Fr231348")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "0.052")
        self.app.valor_altura_segunda_medida_entrada.insert(0, "0.058")
        self.app.valor_altura_terceira_medida_entrada.insert(0, "0.059")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287', 'Fr231288'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317', 'Fr231318'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346', 'Fr231347'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113, 0.068])
        self.assertEqual(self.app.valores_segunda_medida, [0.122, 0.065])
        self.assertEqual(self.app.valores_terceira_medida, [0.109, 0.077])
        self.assertEqual(self.app.maior_medida, [0.122, 0.077])
        self.assertEqual(self.app.menor_medida, [0.109, 0.065])
        self.assertEqual(self.app.valores_medianas, [0.113, 0.068])         
        self.assertEqual(self.app.valores_porcentagens, [0.00, 39.82])
        self.assertEqual(self.app.RD, [4, 6])
        self.assertEqual(self.app.contador_coleta, 1)        
        self.assertEqual(self.mensagem_erro(), "Algum nome de espectro não condizente. Nada foi armazenado.")

    # Testes de coleta de dados com dado de nome do 3º espectro em formato incorreto
    def teste_coleta_dados_nome_3_espectro_formato_incorreto(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "Fr231289")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "Fr231319")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "Ab50")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "0.052")
        self.app.valor_altura_segunda_medida_entrada.insert(0, "0.058")
        self.app.valor_altura_terceira_medida_entrada.insert(0, "0.059")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287', 'Fr231288'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317', 'Fr231318'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346', 'Fr231347'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113, 0.068])
        self.assertEqual(self.app.valores_segunda_medida, [0.122, 0.065])
        self.assertEqual(self.app.valores_terceira_medida, [0.109, 0.077])
        self.assertEqual(self.app.maior_medida, [0.122, 0.077])
        self.assertEqual(self.app.menor_medida, [0.109, 0.065])
        self.assertEqual(self.app.valores_medianas, [0.113, 0.068])         
        self.assertEqual(self.app.valores_porcentagens, [0.00, 39.82])
        self.assertEqual(self.app.RD, [4, 6])
        self.assertEqual(self.app.contador_coleta, 1)        
        self.assertEqual(self.mensagem_erro(), "Algum nome de espectro não condizente. Nada foi armazenado.")
    
    # Testes de coleta de dados sem coleta prévia de R
    def teste_coleta_dados_sem_coleta_R(self):
        self.app.R = 0.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "Fr231289")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "Fr231319")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "Fr231348")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "0.052")
        self.app.valor_altura_segunda_medida_entrada.insert(0, "0.058")
        self.app.valor_altura_terceira_medida_entrada.insert(0, "0.059")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287', 'Fr231288'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317', 'Fr231318'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346', 'Fr231347'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113, 0.068])
        self.assertEqual(self.app.valores_segunda_medida, [0.122, 0.065])
        self.assertEqual(self.app.valores_terceira_medida, [0.109, 0.077])
        self.assertEqual(self.app.maior_medida, [0.122, 0.077])
        self.assertEqual(self.app.menor_medida, [0.109, 0.065])
        self.assertEqual(self.app.valores_medianas, [0.113, 0.068])         
        self.assertEqual(self.app.valores_porcentagens, [0.00, 39.82])
        self.assertEqual(self.app.RD, [4, 6])
        self.assertEqual(self.app.contador_coleta, 1)        
        self.assertEqual(self.mensagem_erro(), "Valor de R ainda não coletado.")
    
    # Testes de coleta de dados sem inserção de dado da 1ª medida
    def teste_coleta_dados_sem_insercao_medida_1(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "Fr231289")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "Fr231319")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "Fr231348")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "")
        self.app.valor_altura_segunda_medida_entrada.insert(0, "0.058")
        self.app.valor_altura_terceira_medida_entrada.insert(0, "0.059")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287', 'Fr231288'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317', 'Fr231318'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346', 'Fr231347'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113, 0.068])
        self.assertEqual(self.app.valores_segunda_medida, [0.122, 0.065])
        self.assertEqual(self.app.valores_terceira_medida, [0.109, 0.077])
        self.assertEqual(self.app.maior_medida, [0.122, 0.077])
        self.assertEqual(self.app.menor_medida, [0.109, 0.065])
        self.assertEqual(self.app.valores_medianas, [0.113, 0.068])         
        self.assertEqual(self.app.valores_porcentagens, [0.00, 39.82])
        self.assertEqual(self.app.RD, [4, 6])
        self.assertEqual(self.app.contador_coleta, 1)        
        self.assertEqual(self.mensagem_erro(), "Nomes de espectros incorretos/não inseridos ou medidas incorretas/não inseridas ou erro no fluxo do programa.")

    # Testes de coleta de dados sem inserção de dado da 2ª medida
    def teste_coleta_dados_sem_insercao_medida_2(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "Fr231289")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "Fr231319")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "Fr231348")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "0.052")
        self.app.valor_altura_segunda_medida_entrada.insert(0, "")
        self.app.valor_altura_terceira_medida_entrada.insert(0, "0.059")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287', 'Fr231288'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317', 'Fr231318'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346', 'Fr231347'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113, 0.068])
        self.assertEqual(self.app.valores_segunda_medida, [0.122, 0.065])
        self.assertEqual(self.app.valores_terceira_medida, [0.109, 0.077])
        self.assertEqual(self.app.maior_medida, [0.122, 0.077])
        self.assertEqual(self.app.menor_medida, [0.109, 0.065])
        self.assertEqual(self.app.valores_medianas, [0.113, 0.068])         
        self.assertEqual(self.app.valores_porcentagens, [0.00, 39.82])
        self.assertEqual(self.app.RD, [4, 6])
        self.assertEqual(self.app.contador_coleta, 1)        
        self.assertEqual(self.mensagem_erro(), "Nomes de espectros incorretos/não inseridos ou medidas incorretas/não inseridas ou erro no fluxo do programa.")

    # Testes de coleta de dados sem inserção de dado da 3ª medida
    def teste_coleta_dados_sem_insercao_medida_3(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "Fr231289")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "Fr231319")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "Fr231348")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "0.052")
        self.app.valor_altura_segunda_medida_entrada.insert(0, '0.058')
        self.app.valor_altura_terceira_medida_entrada.insert(0, "")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287', 'Fr231288'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317', 'Fr231318'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346', 'Fr231347'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113, 0.068])
        self.assertEqual(self.app.valores_segunda_medida, [0.122, 0.065])
        self.assertEqual(self.app.valores_terceira_medida, [0.109, 0.077])
        self.assertEqual(self.app.maior_medida, [0.122, 0.077])
        self.assertEqual(self.app.menor_medida, [0.109, 0.065])
        self.assertEqual(self.app.valores_medianas, [0.113, 0.068])         
        self.assertEqual(self.app.valores_porcentagens, [0.00, 39.82])
        self.assertEqual(self.app.RD, [4, 6])
        self.assertEqual(self.app.contador_coleta, 1)        
        self.assertEqual(self.mensagem_erro(), "Nomes de espectros incorretos/não inseridos ou medidas incorretas/não inseridas ou erro no fluxo do programa.")
    
    # Testes de coleta de dados com inserção de dado da 1ª medida em formato errado
    def teste_coleta_dados_insercao_medida_1_formato_errado(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "Fr231289")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "Fr231319")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "Fr231348")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "abc")
        self.app.valor_altura_segunda_medida_entrada.insert(0, "0.058")
        self.app.valor_altura_terceira_medida_entrada.insert(0, "0.059")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287', 'Fr231288'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317', 'Fr231318'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346', 'Fr231347'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113, 0.068])
        self.assertEqual(self.app.valores_segunda_medida, [0.122, 0.065])
        self.assertEqual(self.app.valores_terceira_medida, [0.109, 0.077])
        self.assertEqual(self.app.maior_medida, [0.122, 0.077])
        self.assertEqual(self.app.menor_medida, [0.109, 0.065])
        self.assertEqual(self.app.valores_medianas, [0.113, 0.068])         
        self.assertEqual(self.app.valores_porcentagens, [0.00, 39.82])
        self.assertEqual(self.app.RD, [4, 6])
        self.assertEqual(self.app.contador_coleta, 1)        
        self.assertEqual(self.mensagem_erro(), "Nomes de espectros incorretos/não inseridos ou medidas incorretas/não inseridas ou erro no fluxo do programa.")

    # Testes de coleta de dados com inserção de dado da 2ª medida em formato errado
    def teste_coleta_dados_insercao_medida_2_formato_errado(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "Fr231289")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "Fr231319")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "Fr231348")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "0.052")
        self.app.valor_altura_segunda_medida_entrada.insert(0, "abc")
        self.app.valor_altura_terceira_medida_entrada.insert(0, "0.059")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287', 'Fr231288'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317', 'Fr231318'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346', 'Fr231347'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113, 0.068])
        self.assertEqual(self.app.valores_segunda_medida, [0.122, 0.065])
        self.assertEqual(self.app.valores_terceira_medida, [0.109, 0.077])
        self.assertEqual(self.app.maior_medida, [0.122, 0.077])
        self.assertEqual(self.app.menor_medida, [0.109, 0.065])
        self.assertEqual(self.app.valores_medianas, [0.113, 0.068])         
        self.assertEqual(self.app.valores_porcentagens, [0.00, 39.82])
        self.assertEqual(self.app.RD, [4, 6])
        self.assertEqual(self.app.contador_coleta, 1)        
        self.assertEqual(self.mensagem_erro(), "Nomes de espectros incorretos/não inseridos ou medidas incorretas/não inseridas ou erro no fluxo do programa.")

    # Testes de coleta de dados com inserção de dado da 3ª medida em formato errado
    def teste_coleta_dados_insercao_medida_3_formato_errado(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "Fr231289")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "Fr231319")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "Fr231348")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "0.052")
        self.app.valor_altura_segunda_medida_entrada.insert(0, '0.058')
        self.app.valor_altura_terceira_medida_entrada.insert(0, "abc")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287', 'Fr231288'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317', 'Fr231318'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346', 'Fr231347'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113, 0.068])
        self.assertEqual(self.app.valores_segunda_medida, [0.122, 0.065])
        self.assertEqual(self.app.valores_terceira_medida, [0.109, 0.077])
        self.assertEqual(self.app.maior_medida, [0.122, 0.077])
        self.assertEqual(self.app.menor_medida, [0.109, 0.065])
        self.assertEqual(self.app.valores_medianas, [0.113, 0.068])         
        self.assertEqual(self.app.valores_porcentagens, [0.00, 39.82])
        self.assertEqual(self.app.RD, [4, 6])
        self.assertEqual(self.app.contador_coleta, 1)        
        self.assertEqual(self.mensagem_erro(), "Nomes de espectros incorretos/não inseridos ou medidas incorretas/não inseridas ou erro no fluxo do programa.")

    # Testes de coleta de dados com inserção de dado da 1ª pedida negativo
    def teste_coleta_dados_insercao_medida_1_negativo(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "Fr231289")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "Fr231319")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "Fr231348")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "-315")
        self.app.valor_altura_segunda_medida_entrada.insert(0, "0.058")
        self.app.valor_altura_terceira_medida_entrada.insert(0, "0.059")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287', 'Fr231288'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317', 'Fr231318'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346', 'Fr231347'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113, 0.068])
        self.assertEqual(self.app.valores_segunda_medida, [0.122, 0.065])
        self.assertEqual(self.app.valores_terceira_medida, [0.109, 0.077])
        self.assertEqual(self.app.maior_medida, [0.122, 0.077])
        self.assertEqual(self.app.menor_medida, [0.109, 0.065])
        self.assertEqual(self.app.valores_medianas, [0.113, 0.068])         
        self.assertEqual(self.app.valores_porcentagens, [0.00, 39.82])
        self.assertEqual(self.app.RD, [4, 6])
        self.assertEqual(self.app.contador_coleta, 1)        
        self.assertEqual(self.mensagem_erro(), "Valores de medidas não positivos. Nada foi armazenado.")

    # Testes de coleta de dados com inserção de dado da 2ª medida negativo
    def teste_coleta_dados_insercao_medida_2_negativo(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "Fr231289")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "Fr231319")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "Fr231348")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "0.052")
        self.app.valor_altura_segunda_medida_entrada.insert(0, "-315")
        self.app.valor_altura_terceira_medida_entrada.insert(0, "0.059")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287', 'Fr231288'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317', 'Fr231318'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346', 'Fr231347'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113, 0.068])
        self.assertEqual(self.app.valores_segunda_medida, [0.122, 0.065])
        self.assertEqual(self.app.valores_terceira_medida, [0.109, 0.077])
        self.assertEqual(self.app.maior_medida, [0.122, 0.077])
        self.assertEqual(self.app.menor_medida, [0.109, 0.065])
        self.assertEqual(self.app.valores_medianas, [0.113, 0.068])         
        self.assertEqual(self.app.valores_porcentagens, [0.00, 39.82])
        self.assertEqual(self.app.RD, [4, 6])
        self.assertEqual(self.app.contador_coleta, 1)        
        self.assertEqual(self.mensagem_erro(), "Valores de medidas não positivos. Nada foi armazenado.")

    # Testes de coleta de dados com inserção de dado da 3ª medida negativo
    def teste_coleta_dados_insercao_medida_3_negativo(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "Fr231289")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "Fr231319")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "Fr231348")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "0.052")
        self.app.valor_altura_segunda_medida_entrada.insert(0, '0.058')
        self.app.valor_altura_terceira_medida_entrada.insert(0, "-315")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287', 'Fr231288'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317', 'Fr231318'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346', 'Fr231347'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113, 0.068])
        self.assertEqual(self.app.valores_segunda_medida, [0.122, 0.065])
        self.assertEqual(self.app.valores_terceira_medida, [0.109, 0.077])
        self.assertEqual(self.app.maior_medida, [0.122, 0.077])
        self.assertEqual(self.app.menor_medida, [0.109, 0.065])
        self.assertEqual(self.app.valores_medianas, [0.113, 0.068])         
        self.assertEqual(self.app.valores_porcentagens, [0.00, 39.82])
        self.assertEqual(self.app.RD, [4, 6])
        self.assertEqual(self.app.contador_coleta, 1)        
        self.assertEqual(self.mensagem_erro(), "Valores de medidas não positivos. Nada foi armazenado.")
    
    # Testes de coleta de dados além das marcações temporais disponíveis
    def teste_coleta_dados_insercao_alem_marcacoes(self):
        self.app.R = 1.0
        self.app.contador_coleta = 13
        self.app.nome_espectro_primeira_medida_entrada.insert(0, "Fr231289")
        self.app.nome_espectro_segunda_medida_entrada.insert(0, "Fr231319")
        self.app.nome_espectro_terceira_medida_entrada.insert(0, "Fr231348")
        self.app.valor_altura_primeira_medida_entrada.insert(0, "0.052")
        self.app.valor_altura_segunda_medida_entrada.insert(0, '0.058')
        self.app.valor_altura_terceira_medida_entrada.insert(0, "0.059")
        self.app.coletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, [])
        self.assertEqual(self.app.ref_espectros_segunda_medida, [])
        self.assertEqual(self.app.ref_espectros_terceira_medida, [])
        self.assertEqual(self.app.valores_primeira_medida, [])
        self.assertEqual(self.app.valores_segunda_medida, [])
        self.assertEqual(self.app.valores_terceira_medida, [])
        self.assertEqual(self.app.maior_medida, [])
        self.assertEqual(self.app.menor_medida, [])
        self.assertEqual(self.app.valores_medianas, [])         
        self.assertEqual(self.app.valores_porcentagens, [])
        self.assertEqual(self.app.RD, [])
        self.assertEqual(self.app.contador_coleta, 13)        
        self.assertEqual(self.mensagem_erro(), "Todos os dados já foram coletados.")
    
    # Testes de deleção de dados sem inserção
    def teste_deleção_dados_sem_insercao(self):
        self.app.contador_coleta = -1
        self.app.deletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, [])
        self.assertEqual(self.app.ref_espectros_segunda_medida, [])
        self.assertEqual(self.app.ref_espectros_terceira_medida, [])
        self.assertEqual(self.app.valores_primeira_medida, [])
        self.assertEqual(self.app.valores_segunda_medida, [])
        self.assertEqual(self.app.valores_terceira_medida, [])
        self.assertEqual(self.app.maior_medida, [])
        self.assertEqual(self.app.menor_medida, [])
        self.assertEqual(self.app.valores_medianas, [])         
        self.assertEqual(self.app.valores_porcentagens, [])
        self.assertEqual(self.app.RD, [])
        self.assertEqual(self.app.contador_coleta, -1)        
        self.assertEqual(self.mensagem_erro(), "Não existem dados armazenados.")
    
    # Testes de deleção de dados
    def teste_delecao_dados(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        self.app.deletar_dados()
        self.assertEqual(self.app.ref_espectros_primeira_medida, ['Fr231287'])
        self.assertEqual(self.app.ref_espectros_segunda_medida, ['Fr231317'])
        self.assertEqual(self.app.ref_espectros_terceira_medida, ['Fr231346'])
        self.assertEqual(self.app.valores_primeira_medida, [0.113])
        self.assertEqual(self.app.valores_segunda_medida, [0.122])
        self.assertEqual(self.app.valores_terceira_medida, [0.109])
        self.assertEqual(self.app.maior_medida, [0.122])
        self.assertEqual(self.app.menor_medida, [0.109])
        self.assertEqual(self.app.valores_medianas, [0.113])         
        self.assertEqual(self.app.valores_porcentagens, [0.00])
        self.assertEqual(self.app.RD, [4])
        self.assertEqual(self.app.contador_coleta, 0)        
        self.assertEqual(self.mensagem_erro(), "Os dados dos espectros Fr231288, Fr231318 e Fr231347 e as medidas respectivas de altura da banda analisada 0.068 cm, 0.065 cm e 0.077 cm inseridos foram excluídos.")
    
    # Teste de geração e atualização de gráficos com coleta de R
    def teste_geracao_atualizacao_graficos_coleta_R(self):
        self.app.R = 1.0
        self.app.contador_coleta = 1
        self.app.ref_espectros_primeira_medida = ['Fr231287', 'Fr231288']
        self.app.ref_espectros_segunda_medida = ['Fr231317', 'Fr231318']
        self.app.ref_espectros_terceira_medida = ['Fr231346', 'Fr231347']
        self.app.valores_primeira_medida = [0.113, 0.068]
        self.app.valores_segunda_medida = [0.122, 0.065]
        self.app.valores_terceira_medida = [0.109, 0.077]
        self.app.maior_medida = [0.122, 0.077]
        self.app.menor_medida = [0.109, 0.065]
        self.app.valores_medianas = [0.113, 0.068]
        self.app.valores_porcentagens = [0.00, 39.82]
        self.app.RD = [4, 6]
        try:
            self.app.gerar_atualizar_grafico()
            success = True
        except Exception as e:
            success = False
        self.assertTrue(success)
        self.assertEqual(self.mensagem_erro(), "Gráficos gerados ou atualizados com sucesso.")
    
    # Teste de geração e atualização de gráficos sem coleta de R
    def teste_geracao_atualizacao_graficos_sem_coleta_R(self):
        self.app.R = 0.0
        try:
            self.app.gerar_atualizar_grafico()
            success = True
        except Exception as e:
            success = False
        self.assertTrue(success)
        self.assertEqual(self.mensagem_erro(), "Valor de R ainda não coletado.")

    # Testes de coleta de nome de arquivo PDF
    def teste_coleta_nome_pdf(self):
        self.app.nome_pdf_entrada.insert(0, "Relatorio_Teste")
        self.app.coletar_nome_arquivo()
        self.assertEqual(self.app.nome_arquivo, "Relatorio_Teste")
        self.assertEqual(self.app.contador_nome_arquivo, 1)
        self.assertEqual(self.mensagem_erro(), "O nome do arquivo PDF é Relatorio_Teste.")

    # Testes de coleta de nome de arquivo PDF em formato incorreto
    def teste_coleta_nome_formato_incorreto_pdf(self):
        self.app.nome_pdf_entrada.insert(0, "Relatorio/Teste")
        self.app.coletar_nome_arquivo()
        self.assertEqual(self.app.nome_arquivo, "rltftir")
        self.assertEqual(self.app.contador_nome_arquivo, -1)
        self.assertEqual(self.mensagem_erro(), "Nome do Arquivo em formato não aceito.")

    # Testes de coleta de nome de arquivo PDF sem inserção de dado
    def teste_coleta_nome_sem_dado_pdf(self):
        self.app.nome_pdf_entrada.insert(0, "")
        self.app.coletar_nome_arquivo()
        self.assertEqual(self.app.nome_arquivo, "")
        self.assertEqual(self.app.contador_nome_arquivo, 1)
        self.assertEqual(self.mensagem_erro(), "O nome do arquivo PDF é .")

    # Testes de deleção de nome de arquivo PDF já inserido
    def teste_delecao_nome_ja_inserido_pdf(self):
        self.app.nome_arquivo = "Relatorio_Teste"
        self.app.contador_nome_arquivo = 1
        self.app.deletar_nome_arquivo()
        self.assertEqual(self.app.contador_nome_arquivo, -1)
        self.assertEqual(self.app.nome_arquivo, "rltftir")
        self.assertEqual(self.mensagem_erro(), "O Nome do Arquivo (Relatorio_Teste) PDF inserido foi excluído.")

    # Testes de deleção de nome de arquivo PDF sem inserção prévia
    def teste_delecao_nome_sem_insercao_pdf(self):
        self.app.nome_arquivo = "rltftir"
        self.app.contador_nome_arquivo = -1
        self.app.deletar_nome_arquivo()
        self.assertEqual(self.app.contador_nome_arquivo, -1)
        self.assertEqual(self.app.nome_arquivo, "rltftir")
        self.assertEqual(self.mensagem_erro(), "Nome do Arquivo PDF ainda não inserido.")
    
    # Teste de geração do arquivo PDF
    def teste_geracao_pdf(self):
        self.app.nome_arquivo = "Relatorio_Teste"
        try:
            self.app.gerar_pdf()
            success = True
        except Exception as e:
            success = False
        self.assertTrue(success)
        self.assertEqual(self.mensagem_erro(), "Relatório em formato PDF gerado com o nome Relatorio_Teste.pdf.")
    
if __name__ == "__main__":
    unittest.main()