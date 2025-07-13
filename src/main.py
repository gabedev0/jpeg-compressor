import numpy as np
from PIL import Image
import math

# ---------- Arquivos -------------
INPUT_FILE = 'imagem.jpg'
OUTPUT_FILE = 'reconstrução.png'

# ---------- Geração das matrizes DCT e IDCT ------------
def create_dct_matrix(N=8):
    """Cria a matriz de transformação DCT (ortonormal)."""
    M = np.zeros((N, N), dtype=np.float32)
    for k in range(N):
        for n in range(N):
            c = math.sqrt(1/N) if k == 0 else math.sqrt(2/N)
            M[k, n] = c * math.cos((2*n + 1) * k * math.pi / (2 * N))
    return M

# DCT direta (forward)/ e sua inversa (transpose) ortonormal
DCT_M = create_dct_matrix()
IDCT_M = DCT_M.T

# ---------- Tabelas de Quantização Padrão -------------
Q50_LUMA = np.array([
    16,11,10,16,24,40,51,61,
    12,12,14,19,26,58,60,55,
    14,13,16,24,40,57,69,56,
    14,17,22,29,51,87,80,62,
    18,22,37,56,68,109,103,77,
    24,35,55,64,81,104,113,92,
    49,64,78,87,103,121,120,101,
    72,92,95,98,112,100,103,99
], dtype=np.float32).reshape((8,8))

Q50_CHROMA = np.array([
    17,18,24,47,99,99,99,99,
    18,21,26,66,99,99,99,99,
    24,26,56,99,99,99,99,99,
    47,66,99,99,99,99,99,99,
    99,99,99,99,99,99,99,99,
    99,99,99,99,99,99,99,99,
    99,99,99,99,99,99,99,99,
    99,99,99,99,99,99,99,99
], dtype=np.float32).reshape((8,8))

# ---------- Funções Auxiliares --------------

def clamp(arr):
    """Limita valores ao intervalo de bytes [0,255]."""
    return np.clip(arr, 0, 255).astype(np.uint8)


def ycbcr_to_rgb(y, cb, cr):
    """Converte canais Y, Cb, Cr de volta para RGB."""
    r = y + 1.402 * (cr - 128)
    g = y - 0.344136 * (cb - 128) - 0.714136 * (cr - 128)
    b = y + 1.772 * (cb - 128)
    return clamp(np.stack([r, g, b], axis=-1))


def dividir_blocos(canal):
    """Divide o canal 2D em blocos 8x8, com padding se necessário."""
    altura, largura = canal.shape
    pad_h = (8 - altura % 8) % 8
    pad_w = (8 - largura % 8) % 8
    padded = np.pad(canal, ((0, pad_h), (0, pad_w)), mode='edge')
    blocos = (
        padded
        .reshape(padded.shape[0]//8, 8, -1, 8)
        .swapaxes(1,2)
        .reshape(-1, 8, 8)
    )
    return blocos, padded.shape


def juntar_blocos(blocos, shape):
    """Reagrupa blocos 8x8 em canal 2D e remove padding."""
    h_pad, w_pad = shape
    blocos = blocos.reshape(h_pad//8, w_pad//8, 8, 8).swapaxes(1,2)
    merged = blocos.reshape(h_pad, w_pad)
    orig_h = h_pad - ((8 - h_pad % 8) % 8)
    orig_w = w_pad - ((8 - w_pad % 8) % 8)
    return merged[:orig_h, :orig_w]


def processar_canal(canal, qtable):
    """Aplica DCT, quantização, desquantização e IDCT em um canal."""
    canal = canal - 128.0
    blocos, shape = dividir_blocos(canal)

    for i in range(blocos.shape[0]):
        bloco = blocos[i]
        # DCT forward
        dct_bloco = DCT_M @ bloco @ DCT_M.T
        # quantização
        q_bloco = np.round(dct_bloco / qtable).astype(np.int32)
        # desquantização
        deq_bloco = (q_bloco * qtable).astype(np.float32)
        # DCT inverse
        idct_bloco = IDCT_M @ deq_bloco @ IDCT_M.T
        blocos[i] = idct_bloco

    processed = juntar_blocos(blocos, shape) + 128.0
    return processed

# ---------- Função Principal do Pipeline ------------
def pipeline_jpeg():
    """Carrega imagem, processa canais e salva resultado reconstruído."""
    img = Image.open(INPUT_FILE).convert('YCbCr')
    y, cb, cr = img.split()
    y_arr = np.array(y, dtype=np.float32)
    cb_arr = np.array(cb, dtype=np.float32)
    cr_arr = np.array(cr, dtype=np.float32)

    # processa cada canal
    y2 = processar_canal(y_arr, Q50_LUMA)
    cb2 = processar_canal(cb_arr, Q50_CHROMA)
    cr2 = processar_canal(cr_arr, Q50_CHROMA)

    # recombina e converte para RGB
    resultado_rgb = ycbcr_to_rgb(y2, cb2, cr2)
    out_img = Image.fromarray(resultado_rgb)
    out_img.save(OUTPUT_FILE)
    print(f"Imagem reconstruída: {OUTPUT_FILE}")

if __name__ == '__main__':
    pipeline_jpeg()