# Compressor de Imagem JPEG

Um implementação em Python do algoritmo de compressão JPEG que demonstra os conceitos fundamentais da compressão de imagens através da Transformada Discreta do Cosseno (DCT) e quantização.

## 📋 Descrição

Este projeto implementa um pipeline simplificado de compressão JPEG que:
- Converte imagens RGB para o espaço de cores YCbCr
- Aplica a Transformada Discreta do Cosseno (DCT) em blocos 8x8
- Realiza quantização usando tabelas padrão JPEG
- Reconstrói a imagem através do processo inverso (IDCT)
- Salva o resultado demonstrando a perda de qualidade típica da compressão JPEG

## 🔧 Requisitos

```bash
pip install numpy pillow
```

## 📁 Estrutura do Projeto

```
├── main.py          # Código principal
├── imagem.jpg            # Imagem de entrada (você deve fornecer)
└── reconstrução.png      # Imagem de saída (gerada pelo programa)
```

## 🚀 Como Usar

1. Coloque sua imagem de entrada no mesmo diretório do script com o nome `imagem.jpg`
2. Execute o programa:
   ```bash
   python main.py
   ```
3. A imagem reconstruída será salva como `reconstrução.png`

## ⚙️ Funcionamento

### Pipeline de Compressão

1. **Conversão de Espaço de Cores**: RGB → YCbCr
2. **Divisão em Blocos**: Cada canal é dividido em blocos 8x8 pixels
3. **DCT Forward**: Transformada do domínio espacial para frequencial
4. **Quantização**: Redução de precisão usando tabelas padrão JPEG Q50
5. **Desquantização**: Processo inverso da quantização
6. **IDCT**: Transformada inversa do domínio frequencial para espacial
7. **Reconstrução**: Junção dos blocos e conversão YCbCr → RGB

### Componentes Principais

- **`create_dct_matrix()`**: Gera a matriz DCT ortonormal 8x8
- **`processar_canal()`**: Aplica o pipeline completo em um canal de cor
- **`dividir_blocos()` / `juntar_blocos()`**: Gerencia a divisão e reagrupamento em blocos
- **Tabelas de Quantização**: Q50_LUMA e Q50_CHROMA (padrão JPEG com qualidade 50%)

## 📊 Parâmetros de Configuração

Você pode modificar as seguintes variáveis no início do código:

```python
INPUT_FILE = 'imagem.jpg'    # Arquivo de entrada
OUTPUT_FILE = 'reconstrução.png'  # Arquivo de saída
```

As tabelas de quantização também podem ser ajustadas para diferentes níveis de qualidade.

## 🎯 Objetivos Educacionais

Este projeto é ideal para entender:
- Como funciona a compressão JPEG
- Conceitos de transformadas de frequência (DCT)
- Efeitos da quantização na qualidade da imagem
- Processamento de imagens em blocos
- Conversão entre espaços de cores

## 📸 Resultados Esperados

A imagem reconstruída apresentará:
- Ligeira perda de qualidade devido à quantização
- Possíveis artefatos de compressão em áreas de alta frequência
- Tamanho de arquivo reduzido (se salva como JPEG)
- Demonstração visual dos efeitos da compressão lossy

## 🔍 Notas Técnicas

- Utiliza quantização fixa (Q50) - não implementa codificação entropy
- Não inclui subamostragem de crominância
- Implementação focada em demonstração educacional
- Padding automático para imagens não múltiplas de 8 pixels

## 📝 Limitações

- Não é um compressor JPEG completo (falta codificação Huffman)
- Qualidade fixa em 50%
- Não otimizado para performance
- Voltado para fins educacionais
