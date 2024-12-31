import time
import threading


class TempoLimiteExcedido(Exception):
    pass


def manipulador_tempo_limite(tempo_limite, resultado, excecao):
    def manipulador():
        time.sleep(tempo_limite)
        excecao.append(TempoLimiteExcedido)
        resultado.append(None)
    return manipulador


def ordenacao_selecao(arr):
    n = len(arr)
    for i in range(n):
        indice_minimo = i
        for j in range(i + 1, n):
            if arr[j] < arr[indice_minimo]:
                indice_minimo = j
        arr[i], arr[indice_minimo] = arr[indice_minimo], arr[i]


def ordenacao_insercao(arr):
    n = len(arr)
    for i in range(1, n):
        chave = arr[i]
        j = i - 1
        while j >= 0 and chave < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = chave


def ler_arquivo(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            return list(map(int, arquivo.readlines()))
    except FileNotFoundError:
        print(f"Arquivo {caminho_arquivo} não encontrado.")
        return []
    except PermissionError:
        print(f"Permissão negada para ler {caminho_arquivo}.")
        return []
    except Exception as e:
        print(f"Erro ao ler o arquivo {caminho_arquivo}: {e}")
        return []


def executar_com_tempo_limite(func, args, tempo_limite=10):
    resultado = []
    excecao = []
    temporizador = threading.Timer(tempo_limite, manipulador_tempo_limite(tempo_limite, resultado, excecao))
    try:
        temporizador.start()
        func(*args)
    except TempoLimiteExcedido:
        print(f"{func.__name__} excedeu o tempo limite!")
        return float('inf')
    finally:
        temporizador.cancel()


def principal():
    arquivos = [
        "C:/Users/Kezia/Documents/Projetos em Python/num.1000.1.in",
        "C:/Users/Kezia/Documents/Projetos em Python/num.1000.2.in",
        "C:/Users/Kezia/Documents/Projetos em Python/num.1000.3.in",
        "C:/Users/Kezia/Documents/Projetos em Python/num.1000.4.in",
        "C:/Users/Kezia/Documents/Projetos em Python/num.10000.1.in",
        "C:/Users/Kezia/Documents/Projetos em Python/num.10000.2.in",
        "C:/Users/Kezia/Documents/Projetos em Python/num.10000.3.in",
        "C:/Users/Kezia/Documents/Projetos em Python/num.10000.4.in",
        "C:/Users/Kezia/Documents/Projetos em Python/num.100000.1.in",
        "C:/Users/Kezia/Documents/Projetos em Python/num.100000.2.in",
        "C:/Users/Kezia/Documents/Projetos em Python/num.100000.3.in",
        "C:/Users/Kezia/Documents/Projetos em Python/num.100000.4.in"
    ]

    resultados = []

    for arquivo in arquivos:
        print(f"Processando arquivo: {arquivo}")
        dados = ler_arquivo(arquivo)

        if not dados:
            print(f"Pulando {arquivo} devido a erros ou problemas no arquivo.")
            continue

        print(f"Número de elementos em {arquivo}: {len(dados)}")
        if len(dados) > 1000000:
            print(f"Pulando {arquivo} devido ao tamanho grande.")
            continue

        # Medir tempo de execução da OrdenacaoSelecao
        try:
            copia_dados = dados.copy()
            inicio_tempo = time.time()
            executar_com_tempo_limite(ordenacao_selecao, (copia_dados,), tempo_limite=10)
            tempo_selecao = time.time() - inicio_tempo
            print(f"OrdenacaoSelecao levou {tempo_selecao:.4f} segundos")
        except TempoLimiteExcedido:
            tempo_selecao = float('inf')

        # Medir tempo de execução da OrdenacaoInsercao
        try:
            copia_dados = dados.copy()
            inicio_tempo = time.time()
            executar_com_tempo_limite(ordenacao_insercao, (copia_dados,), tempo_limite=10)
            tempo_insercao = time.time() - inicio_tempo
            print(f"OrdenacaoInsercao levou {tempo_insercao:.4f} segundos")
        except TempoLimiteExcedido:
            tempo_insercao = float('inf')

        # Adicionar resultados para comparação
        resultados.append((arquivo, tempo_selecao, tempo_insercao))
        print("-" * 50)

    # Comparação final dos tempos de execução
    print("Comparação Final dos Tempos de Execução:")
    print(f"{'Arquivo':<40} {'OrdenacaoSelecao':<20} {'OrdenacaoInsercao':<20}")
    for arquivo, tempo_sel, tempo_ins in resultados:
        print(f"{arquivo:<40} {tempo_sel:<20.4f} {tempo_ins:<20.4f}")


if __name__ == "__main__":
    principal()
