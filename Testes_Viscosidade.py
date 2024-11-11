import unittest
from Viscosidade_TG2 import DynamicPlotApp
from tkinter import Tk
class TestViscosidadeApp(unittest.TestCase):

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

    # Teste de coleta de passo
    def teste_coleta_passo(self):
        self.app.passo_entrada.insert(0, "15")
        self.app.coletar_passo()
        self.assertEqual(self.app.passo, 15)
        self.assertEqual(self.mensagem_erro(), "O passo coletado é 15.0 min.")

    # Teste de coleta de passo sem inserção de dado
    def teste_coleta_passo_sem_insercao(self):
        self.app.passo_entrada.insert(0, "")
        self.app.coletar_passo()
        self.assertEqual(self.app.passo, 0)
        self.assertEqual(self.mensagem_erro(), "Passo em formato incorreto ou nenhum passo inserido ou erro no fluxo do programa.")

    # Teste de coleta de passo negativo
    def teste_coleta_passo_negativo(self):
        self.app.passo_entrada.insert(0, "-30")
        self.app.coletar_passo()
        self.assertEqual(self.app.passo, 0)
        self.assertEqual(self.mensagem_erro(), "O passo inserido encontra-se em formato incorreto.")

    # Teste de coleta de passo em formato incorreto
    def teste_coleta_passo_formato_incorreto(self):
        self.app.passo_entrada.insert(0, "ab50")
        self.app.coletar_passo()
        self.assertEqual(self.app.passo, 0)
        self.assertEqual(self.mensagem_erro(), "Passo em formato incorreto ou nenhum passo inserido ou erro no fluxo do programa.")

    # Teste de deleção de passo sem coleta anterior 
    def teste_delecao_passo_sem_coleta(self):
        self.app.deletar_passo()
        self.assertEqual(self.app.passo, 0)
        self.assertEqual(self.mensagem_erro(), "Passo ainda não coletado.")

    # Teste de deleção de passo já coletado
    def teste_delecao_passo_ja_coletado(self):
        self.app.passo_entrada.insert(0, "15")
        self.app.coletar_passo()
        self.app.deletar_passo()
        self.assertEqual(self.app.passo, 0)
        self.assertEqual(self.mensagem_erro(), "O passo de 15.0 min inserido foi excluído.")

    # Teste de coleta de tempo total de experimento 
    def teste_coleta_tempo_total_experimento(self):
        self.app.temp_tot_entrada.insert(0, "120")
        self.app.coletar_temp_tot()
        self.assertEqual(self.app.temp_tot, 120)
        self.assertEqual(self.mensagem_erro(), "O tempo total de experimento coletado é 120.0 min.")

    # Teste de coleta de tempo total de experimento negativo
    def teste_coleta_tempo_total_experimento_negativo(self):
        self.app.temp_tot_entrada.insert(0, "-120")
        self.app.coletar_temp_tot()
        self.assertEqual(self.app.temp_tot, 0)
        self.assertEqual(self.mensagem_erro(), "O tempo total inserido encontra-se em formato incorreto.")

    # Teste de coleta de tempo total de experimento sem insercao de dado
    def teste_coleta_tempo_total_experimento_sem_insercao(self):
        self.app.temp_tot_entrada.insert(0, "")
        self.app.coletar_temp_tot()
        self.assertEqual(self.app.temp_tot, 0)
        self.assertEqual(self.mensagem_erro(), "Tempo Total em formato incorreto ou nenhum tempo total de experimento inserido ou erro no fluxo do programa.")

    # Teste de coleta de tempo total de experimento em formato incorreto
    def teste_coleta_tempo_total_experimento_formato_incorreto(self):
        self.app.temp_tot_entrada.insert(0, "abc50")
        self.app.coletar_temp_tot()
        self.assertEqual(self.app.temp_tot, 0)
        self.assertEqual(self.mensagem_erro(), "Tempo Total em formato incorreto ou nenhum tempo total de experimento inserido ou erro no fluxo do programa.")

    # Teste de deleção de tempo total de experimento sem coleta anterior
    def teste_delecao_tempo_total_experimento_sem_coleta(self):
        self.app.deletar_temp_tot()
        self.assertEqual(self.app.temp_tot, 0)
        self.assertEqual(self.mensagem_erro(), "Tempo Total de Experimento ainda não coletado.")

    # Teste de deleção de tempo total de experimento já coletado
    def teste_delecao_tempo_total_experimento_ja_coletado(self):
        self.app.temp_tot_entrada.insert(0, "120")
        self.app.coletar_temp_tot()
        self.app.deletar_temp_tot()
        self.assertEqual(self.app.temp_tot, 0)
        self.assertEqual(self.mensagem_erro(), "O tempo total de experimento de 120.0 min inserido foi excluído.")

    # Teste de geração de marcações temporais 
    def teste_geracao_marcacoes_temporais(self):
        self.app.passo = 10.0
        self.app.temp_tot = 50.0
        self.app.gerar_marc_temp()
        self.assertEqual(self.app.tempo_medidas, [0.0, 10.0, 20.0, 30.0, 40.0, 50.0])
        self.assertEqual(self.mensagem_erro(), "O intervalo de 50.0 min foi dividido em 6 marcações. A primeira marcação é de 0.0 min e a última é 50.0 min.")
    
    # Teste de geração de marcações temporais sem coleta de passo 
    def teste_geracao_marcacoes_temporais_sem_passo(self):
        self.app.temp_tot = 50
        self.app.gerar_marc_temp()
        self.assertEqual(self.app.tempo_medidas, [])
        self.assertEqual(self.mensagem_erro(), "Passo ainda não coletado.")
    
    # Teste de geração de marcações temporais sem coleta de tempo total
    def teste_geracao_marcacoes_temporais_sem_tempo_total(self):
        self.app.passo = 30
        self.app.gerar_marc_temp()
        self.assertEqual(self.app.tempo_medidas, [])
        self.assertEqual(self.mensagem_erro(), "Tempo Total de Experimento ainda não coletado.")
    
    # Testes de coleta de dados de viscosidade (laboratório)
    def teste_coleta_dados_viscosidade_laboratorio(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.valor_entrada_laboratorio.insert(0, "14000")
        self.app.coletar_dados_laboratorio()
        self.assertEqual(self.app.valores_laboratorio, [14000.0])
        self.assertEqual(self.app.valores_laboratorio_linear, [9.55])
        self.assertEqual(self.app.contador_lab, 0)
        self.assertEqual(self.mensagem_erro(), "O valor de viscosidade 14000.0 cP para a escala laboratorial relativo à marcação temporal 0.0 min foi coletada.")
    
    # Testes de coleta de dados de viscosidade (laboratório) sem inserção de dado
    def teste_coleta_dados_viscosidade_sem_insercao_laboratorio(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.valor_entrada_laboratorio.insert(0, "")
        self.app.coletar_dados_laboratorio()
        self.assertEqual(self.app.valores_laboratorio, [])
        self.assertEqual(self.app.valores_laboratorio_linear, [])
        self.assertEqual(self.app.insat_tempo_lab, [])
        self.assertEqual(self.app.insat_valor_lab, [])
        self.assertEqual(self.app.contador_lab, -1)
        self.assertEqual(self.mensagem_erro(), "Valor de viscosidade para escala laboratorial em formato incorreto ou nenhum valor de viscosidade laboratorial inserido ou erro no fluxo do programa.")

    # Testes de coleta de dados de viscosidade (laboratório) que nao satisfaz a condição de aceite superior
    def teste_coleta_dados_viscosidade_nao_satisfaz_sup_laboratorio(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.valores_laboratorio = [14000.0, 145000.0]
        self.app.valores_laboratorio_linear = [9.55, 9.58]
        self.app.contador_lab = 1
        self.app.valor_entrada_laboratorio.insert(0, "41000")
        self.app.coletar_dados_laboratorio()
        self.assertEqual(self.app.valores_laboratorio, [14000.0, 145000.0, 41000.0])
        self.assertEqual(self.app.valores_laboratorio_linear, [9.55, 9.58, 10.62])
        self.assertEqual(self.app.insat_tempo_lab, [20.0])
        self.assertEqual(self.app.insat_valor_lab, [41000.0])
        self.assertEqual(self.app.contador_lab, 2)
        self.assertEqual(self.mensagem_erro(), "O valor de viscosidade 41000.0 cP, que não satisfaz os critérios de aceite para a escala laboratorial, relativo à marcação temporal 20.0 min foi coletada.")

    # Testes de coleta de dados de viscosidade (laboratório) que nao satisfaz a condição de aceite inferior
    def teste_coleta_dados_viscosidade__nao_satisfaz_inf_laboratorio(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.valores_laboratorio = [14000.0, 145000.0]
        self.app.valores_laboratorio_linear = [9.55, 9.58]
        self.app.contador_lab = 1
        self.app.valor_entrada_laboratorio.insert(0, "4000")
        self.app.coletar_dados_laboratorio()
        self.assertEqual(self.app.valores_laboratorio, [14000.0, 145000.0, 4000.0])
        self.assertEqual(self.app.valores_laboratorio_linear, [9.55, 9.58, 8.29])
        self.assertEqual(self.app.insat_tempo_lab, [20.0])
        self.assertEqual(self.app.insat_valor_lab, [4000.0])
        self.assertEqual(self.app.contador_lab, 2)
        self.assertEqual(self.mensagem_erro(), "O valor de viscosidade 4000.0 cP, que não satisfaz os critérios de aceite para a escala laboratorial, relativo à marcação temporal 20.0 min foi coletada.")

    # Testes de coleta de dados de viscosidade (laboratório) negativo
    def teste_coleta_dados_viscosidade_negativo_laboratorio(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.valor_entrada_laboratorio.insert(0, "-8.5")
        self.app.coletar_dados_laboratorio()
        self.assertEqual(self.app.valores_laboratorio, [])
        self.assertEqual(self.app.valores_laboratorio_linear, [])
        self.assertEqual(self.app.insat_tempo_lab, [])
        self.assertEqual(self.app.insat_valor_lab, [])
        self.assertEqual(self.app.contador_lab, -1)
        self.assertEqual(self.mensagem_erro(), "O valor de viscosidade relativo à escala laboratorial inserido encontra-se em formato incorreto.")
    
    # Testes de coleta de dados de viscosidade (laboratório) sem as marcações temporais terem sido geradas
    def teste_coleta_dados_viscosidade_sem_marcacoes_temporais_laboratorio(self):
        self.app.tempo_medidas = []
        self.app.valor_entrada_laboratorio.insert(0, "8.5")
        self.app.coletar_dados_laboratorio()
        self.assertEqual(self.app.valores_laboratorio, [])
        self.assertEqual(self.app.valores_laboratorio_linear, [])
        self.assertEqual(self.app.insat_tempo_lab, [])
        self.assertEqual(self.app.insat_valor_lab, [])
        self.assertEqual(self.app.contador_lab, -1)
        self.assertEqual(self.mensagem_erro(), "Marcações temporais ainda não geradas e o dado inserido para laboratório não foi coletado.")

    # Testes de coleta de dados de viscosidade (laboratório) em formato errado
    def teste_coleta_dados_viscosidade_formato_errado_laboratorio(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.valor_entrada_laboratorio.insert(0, "abc50")
        self.app.coletar_dados_laboratorio()
        self.assertEqual(self.app.valores_laboratorio, [])
        self.assertEqual(self.app.valores_laboratorio_linear, [])
        self.assertEqual(self.app.insat_tempo_lab, [])
        self.assertEqual(self.app.insat_valor_lab, [])
        self.assertEqual(self.app.contador_lab, -1)
        self.assertEqual(self.mensagem_erro(), "Valor de viscosidade para escala laboratorial em formato incorreto ou nenhum valor de viscosidade laboratorial inserido ou erro no fluxo do programa.")

    # Testes de coleta de dados de viscosidade (laboratório) além das marcações temporais
    def teste_coleta_dados_viscosidade_alem_marcacoes_temporais_laboratorio(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.contador_lab = 2
        self.app.valores_laboratorio = [14000.0, 145000.0, 15000.0]
        self.app.valores_laboratorio_linear = [9.55, 9.58, 9.62]
        self.app.valor_entrada_laboratorio.insert(0, "9.8")
        self.app.coletar_dados_laboratorio()
        self.assertEqual(self.app.valores_laboratorio, [14000.0, 145000.0, 15000.0])
        self.assertEqual(self.app.valores_laboratorio_linear, [9.55, 9.58, 9.62])
        self.assertEqual(self.app.insat_tempo_lab, [])
        self.assertEqual(self.app.insat_valor_lab, [])
        self.assertEqual(self.app.contador_lab, 2)
        self.assertEqual(self.mensagem_erro(), "Todos os dados para a escala laboratorial já foram coletados.")

    # Testes de deleção de dados de viscosidade (laboratório)
    def teste_delecao_dados_viscosidade_laboratorio(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.valores_laboratorio = [14000.0, 14500.0]
        self.app.valores_laboratorio_linear = [9.55, 9.58]
        self.app.contador_lab = 1
        self.app.deletar_dados_laboratorio()
        self.assertEqual(self.app.valores_laboratorio, [14000.0])
        self.assertEqual(self.app.valores_laboratorio_linear, [9.55])
        self.assertEqual(self.app.contador_lab, 0)
        self.assertEqual(self.app.insat_valor_lab, [])
        self.assertEqual(self.app.insat_tempo_lab, [])
        self.assertEqual(self.mensagem_erro(), "O valor de viscosidade relativo à escala laboratorial 14500.0 cP correspondente à marcação temporal 10.0 min inserido foi excluído.")
    
    # Testes de deleção de dados de viscosidade (laboratório) sem coleta prévia
    def teste_delecao_dados_viscosidade_sem_coleta_laboratorio(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.contador_lab = -1
        self.app.deletar_dados_laboratorio()
        self.assertEqual(self.app.valores_laboratorio, [])
        self.assertEqual(self.app.valores_laboratorio_linear, [])
        self.assertEqual(self.app.contador_lab, -1)
        self.assertEqual(self.app.insat_valor_lab, [])
        self.assertEqual(self.app.insat_tempo_lab, [])
        self.assertEqual(self.mensagem_erro(), "Nenhum valor de viscosidade na escala laboratorial foi coletado.")
    
    # Testes de deleção de dados de viscosidade (laboratório) que não satisfaz o critério superior
    def teste_delecao_dados_viscosidade_nao_satisfaz_sup_laboratorio(self):
        self.app.tempo_medidas = [0.0, 10.0]
        self.app.valores_laboratorio = [14000.0, 41000.0]
        self.app.valores_laboratorio_linear = [9.55, 10.62]
        self.app.insat_valor_lab = [41000.0]
        self.app.insat_tempo_lab = [10.0]
        self.app.contador_lab = 1
        self.app.deletar_dados_laboratorio()
        self.assertEqual(self.app.valores_laboratorio, [14000.0])
        self.assertEqual(self.app.valores_laboratorio_linear, [9.55])
        self.assertEqual(self.app.contador_lab, 0)
        self.assertEqual(self.app.insat_valor_lab, [])
        self.assertEqual(self.app.insat_tempo_lab, [])
        self.assertEqual(self.mensagem_erro(), "O valor de viscosidade relativo à escala laboratorial 41000.0 cP correspondente à marcação temporal 10.0 min inserido foi excluído.")
    
    # Testes de deleção de dados de viscosidade (laboratório) que não satisfaz o critério inferior
    def teste_delecao_dados_viscosidade_nao_satisfaz_inf_laboratorio(self):
        self.app.tempo_medidas = [0.0, 10.0]
        self.app.valores_laboratorio = [14000.0, 4000.0]
        self.app.valores_laboratorio_linear = [9.55, 8.29]
        self.app.insat_valor_lab = [4000.0]
        self.app.insat_tempo_lab = [10.0]
        self.app.contador_lab = 1
        self.app.deletar_dados_laboratorio()
        self.assertEqual(self.app.valores_laboratorio, [14000.0])
        self.assertEqual(self.app.valores_laboratorio_linear, [9.55])
        self.assertEqual(self.app.contador_lab, 0)
        self.assertEqual(self.app.insat_valor_lab, [])
        self.assertEqual(self.app.insat_tempo_lab, [])
        self.assertEqual(self.mensagem_erro(), "O valor de viscosidade relativo à escala laboratorial 4000.0 cP correspondente à marcação temporal 10.0 min inserido foi excluído.")

    # Testes de coleta de dados de viscosidade (processo)
    def teste_coleta_dados_viscosidade_processo(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.valor_entrada_processo.insert(0, "14000")
        self.app.coletar_dados_processo()
        self.assertEqual(self.app.valores_processo, [14000.0])
        self.assertEqual(self.app.valores_processo_linear, [9.55])
        self.assertEqual(self.app.contador_proc, 0)
        self.assertEqual(self.mensagem_erro(), "O valor de viscosidade 14000.0 cP para a escala processual relativo à marcação temporal 0.0 min foi coletada.")
    
    # Testes de coleta de dados de viscosidade (processo) sem inserção de dado
    def teste_coleta_dados_viscosidade_sem_insercao_processo(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.valor_entrada_processo.insert(0, "")
        self.app.coletar_dados_processo()
        self.assertEqual(self.app.valores_processo, [])
        self.assertEqual(self.app.valores_processo_linear, [])
        self.assertEqual(self.app.insat_tempo_proc, [])
        self.assertEqual(self.app.insat_valor_proc, [])
        self.assertEqual(self.app.contador_proc, -1)
        self.assertEqual(self.mensagem_erro(), "Valor de viscosidade para escala processual em formato incorreto ou nenhum valor de viscosidade processual inserido ou erro no fluxo do programa.")

    # Testes de coleta de dados de viscosidade (processo) que nao satisfaz a condição de aceite superior
    def teste_coleta_dados_viscosidade_nao_satisfaz_sup_processo(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.valores_processo = [14000.0, 145000.0]
        self.app.valores_processo_linear = [9.55, 9.58]
        self.app.contador_proc = 1
        self.app.valor_entrada_processo.insert(0, "41000")
        self.app.coletar_dados_processo()
        self.assertEqual(self.app.valores_processo, [14000.0, 145000.0, 41000.0])
        self.assertEqual(self.app.valores_processo_linear, [9.55, 9.58, 10.62])
        self.assertEqual(self.app.insat_tempo_proc, [20.0])
        self.assertEqual(self.app.insat_valor_proc, [41000.0])
        self.assertEqual(self.app.contador_proc, 2)
        self.assertEqual(self.mensagem_erro(), "O valor de viscosidade 41000.0 cP, que não satisfaz os critérios de aceite para a escala processual, relativo à marcação temporal 20.0 min foi coletada.")

    # Testes de coleta de dados de viscosidade (processo) que nao satisfaz a condição de aceite inferior
    def teste_coleta_dados_viscosidade__nao_satisfaz_inf_processo(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.valores_processo = [14000.0, 145000.0]
        self.app.valores_processo_linear = [9.55, 9.58]
        self.app.contador_proc = 1
        self.app.valor_entrada_processo.insert(0, "4000")
        self.app.coletar_dados_processo()
        self.assertEqual(self.app.valores_processo, [14000.0, 145000.0, 4000.0])
        self.assertEqual(self.app.valores_processo_linear, [9.55, 9.58, 8.29])
        self.assertEqual(self.app.insat_tempo_proc, [20.0])
        self.assertEqual(self.app.insat_valor_proc, [4000.0])
        self.assertEqual(self.app.contador_proc, 2)
        self.assertEqual(self.mensagem_erro(), "O valor de viscosidade 4000.0 cP, que não satisfaz os critérios de aceite para a escala processual, relativo à marcação temporal 20.0 min foi coletada.")

    # Testes de coleta de dados de viscosidade (processo) negativo
    def teste_coleta_dados_viscosidade_negativo_processo(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.valor_entrada_processo.insert(0, "-8.5")
        self.app.coletar_dados_processo()
        self.assertEqual(self.app.valores_processo, [])
        self.assertEqual(self.app.valores_processo_linear, [])
        self.assertEqual(self.app.insat_tempo_proc, [])
        self.assertEqual(self.app.insat_valor_proc, [])
        self.assertEqual(self.app.contador_proc, -1)
        self.assertEqual(self.mensagem_erro(), "O valor de viscosidade relativo à escala processual inserido encontra-se em formato incorreto.")
    
    # Testes de coleta de dados de viscosidade (processo) sem as marcações temporais terem sido geradas
    def teste_coleta_dados_viscosidade_sem_marcacoes_temporais_processo(self):
        self.app.tempo_medidas = []
        self.app.valor_entrada_processo.insert(0, "8.5")
        self.app.coletar_dados_processo()
        self.assertEqual(self.app.valores_processo, [])
        self.assertEqual(self.app.valores_processo_linear, [])
        self.assertEqual(self.app.insat_tempo_proc, [])
        self.assertEqual(self.app.insat_valor_proc, [])
        self.assertEqual(self.app.contador_proc, -1)
        self.assertEqual(self.mensagem_erro(), "Marcações temporais ainda não geradas e o dado inserido para processo não foi coletado.")

    # Testes de coleta de dados de viscosidade (processo) em formato errado
    def teste_coleta_dados_viscosidade_formato_errado_processo(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.valor_entrada_processo.insert(0, "abc50")
        self.app.coletar_dados_processo()
        self.assertEqual(self.app.valores_processo, [])
        self.assertEqual(self.app.valores_processo_linear, [])
        self.assertEqual(self.app.insat_tempo_proc, [])
        self.assertEqual(self.app.insat_valor_proc, [])
        self.assertEqual(self.app.contador_proc, -1)
        self.assertEqual(self.mensagem_erro(), "Valor de viscosidade para escala processual em formato incorreto ou nenhum valor de viscosidade processual inserido ou erro no fluxo do programa.")

    # Testes de coleta de dados de viscosidade (processo) além das marcações temporais
    def teste_coleta_dados_viscosidade_alem_marcacoes_temporais_processo(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.contador_proc = 2
        self.app.valores_processo = [14000.0, 145000.0, 15000.0]
        self.app.valores_processo_linear = [9.55, 9.58, 9.62]
        self.app.valor_entrada_processo.insert(0, "9.8")
        self.app.coletar_dados_processo()
        self.assertEqual(self.app.valores_processo, [14000.0, 145000.0, 15000.0])
        self.assertEqual(self.app.valores_processo_linear, [9.55, 9.58, 9.62])
        self.assertEqual(self.app.insat_tempo_proc, [])
        self.assertEqual(self.app.insat_valor_proc, [])
        self.assertEqual(self.app.contador_proc, 2)
        self.assertEqual(self.mensagem_erro(), "Todos os dados para a escala processual já foram coletados.")

    # Testes de deleção de dados de viscosidade (processo)
    def teste_delecao_dados_viscosidade_processo(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.valores_processo = [14000.0, 14500.0]
        self.app.valores_processo_linear = [9.55, 9.58]
        self.app.contador_proc = 1
        self.app.deletar_dados_processo()
        self.assertEqual(self.app.valores_processo, [14000.0])
        self.assertEqual(self.app.valores_processo_linear, [9.55])
        self.assertEqual(self.app.contador_proc, 0)
        self.assertEqual(self.app.insat_valor_proc, [])
        self.assertEqual(self.app.insat_tempo_proc, [])
        self.assertEqual(self.mensagem_erro(), "O valor de viscosidade relativo à escala processual 14500.0 cP correspondente à marcação temporal 10.0 min inserido foi excluído.")
    
    # Testes de deleção de dados de viscosidade (processo) sem coleta prévia
    def teste_delecao_dados_viscosidade_sem_coleta_processo(self):
        self.app.tempo_medidas = [0.0, 10.0, 20.0]
        self.app.contador_proc = -1
        self.app.deletar_dados_processo()
        self.assertEqual(self.app.valores_processo, [])
        self.assertEqual(self.app.valores_processo_linear, [])
        self.assertEqual(self.app.contador_proc, -1)
        self.assertEqual(self.app.insat_valor_proc, [])
        self.assertEqual(self.app.insat_tempo_proc, [])
        self.assertEqual(self.mensagem_erro(), "Nenhum valor de viscosidade na escala processual foi coletado.")
    
    # Testes de deleção de dados de viscosidade (processo) que não satisfaz o critério superior
    def teste_delecao_dados_viscosidade_nao_satisfaz_sup_processo(self):
        self.app.tempo_medidas = [0.0, 10.0]
        self.app.valores_processo = [14000.0, 41000.0]
        self.app.valores_processo_linear = [9.55, 10.62]
        self.app.insat_valor_proc = [41000.0]
        self.app.insat_tempo_proc = [10.0]
        self.app.contador_proc = 1
        self.app.deletar_dados_processo()
        self.assertEqual(self.app.valores_processo, [14000.0])
        self.assertEqual(self.app.valores_processo_linear, [9.55])
        self.assertEqual(self.app.contador_proc, 0)
        self.assertEqual(self.app.insat_valor_proc, [])
        self.assertEqual(self.app.insat_tempo_proc, [])
        self.assertEqual(self.mensagem_erro(), "O valor de viscosidade relativo à escala processual 41000.0 cP correspondente à marcação temporal 10.0 min inserido foi excluído.")
    
    # Testes de deleção de dados de viscosidade (processo) que não satisfaz o critério inferior
    def teste_delecao_dados_viscosidade_nao_satisfaz_inf_processo(self):
        self.app.tempo_medidas = [0.0, 10.0]
        self.app.valores_processo = [14000.0, 4000.0]
        self.app.valores_processo_linear = [9.55, 8.29]
        self.app.insat_valor_proc = [4000.0]
        self.app.insat_tempo_proc = [10.0]
        self.app.contador_proc = 1
        self.app.deletar_dados_processo()
        self.assertEqual(self.app.valores_processo, [14000.0])
        self.assertEqual(self.app.valores_processo_linear, [9.55])
        self.assertEqual(self.app.contador_proc, 0)
        self.assertEqual(self.app.insat_valor_proc, [])
        self.assertEqual(self.app.insat_tempo_proc, [])
        self.assertEqual(self.mensagem_erro(), "O valor de viscosidade relativo à escala processual 4000.0 cP correspondente à marcação temporal 10.0 min inserido foi excluído.")

    # Teste de geração e atualização de gráficos
    def teste_geracao_atualizacao_graficos(self):
        self.app.tempo_medidas = [0, 10, 20, 30, 40, 50]
        self.app.valores_processo = [9.5, 9.6, 9.7]
        self.app.valores_processo_linear = [2.25, 2.26, 2.27]
        self.app.valores_laboratorio_linear = [2.21, 2.22]
        self.app.valores_laboratorio = [9.1, 9.2]
        self.app.contador_lab = 1
        self.app.contador_proc = 2
        try:
            self.app.gerar_atualizar_grafico()
            success = True
        except Exception as e:
            success = False
        self.assertTrue(success)
        self.assertEqual(self.mensagem_erro(), "Gráficos gerados ou atualizados com sucesso.")

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
        self.assertEqual(self.app.nome_arquivo, "rltpd")
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
        self.assertEqual(self.app.nome_arquivo, "rltpd")
        self.assertEqual(self.mensagem_erro(), "O Nome do Arquivo (Relatorio_Teste) PDF inserido foi excluído.")

    # Testes de deleção de nome de arquivo PDF sem inserção prévia
    def teste_delecao_nome_sem_insercao_pdf(self):
        self.app.nome_arquivo = "rltpd"
        self.app.contador_nome_arquivo = -1
        self.app.deletar_nome_arquivo()
        self.assertEqual(self.app.contador_nome_arquivo, -1)
        self.assertEqual(self.app.nome_arquivo, "rltpd")
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
        self.assertEqual(self.mensagem_erro(), "Relatório em formato PDF gerado com o nome Relatorio_Teste.pdf")
    
if __name__ == "__main__":
    unittest.main()