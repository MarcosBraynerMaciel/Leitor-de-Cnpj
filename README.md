# 📊 Leitor de CNPJs - Projeto Completo

## 📁 Estrutura do Projeto

```
📦 Big Data/
├── 📄 202508_CNPJ.csv          # Arquivo de dados com CNPJs
├── 📊 README.md                # Este arquivo (documentação completa)
├── 🌐 leitor_web.py            # Interface web (PRINCIPAL)
├── 📁 .streamlit/              # Configurações do Streamlit
│   └── config.toml             # Configurações em português
└── 📁 .venv/                   # Ambiente virtual Python
    ├── bin/python              # Interpretador Python
    └── lib/                    # Bibliotecas instaladas
```

---

## 🎯 Sobre o Projeto

### 📋 **Descrição:**
Sistema para análise de dados de CNPJs brasileiros com interface web moderna e intuitiva.

### 🎨 **Versão Principal:**
**`leitor_web.py`** - Interface web moderna com múltiplas opções de pesquisa

### 💡 **Objetivo:**
Facilitar a consulta e análise de CNPJs por estado, região ou capital, com geração de relatórios e downloads.

---

## 🔍 **Funcionalidades**

### 📊 **Análise de CNPJs**
- Upload de arquivos CSV com dados de CNPJs brasileiros
- Carregamento automático do arquivo `202508_CNPJ.csv`
- Processamento e análise de dados em tempo real
- Interface web responsiva e amigável

### 🗺️ **Opções de Pesquisa**

#### 🏛️ **Por Estado**
- Digite manualmente os estados desejados
- Formato: siglas separadas por vírgula (Ex: SP, RJ, MG)
- Pesquisa customizada por múltiplos estados

#### 🌎 **Por Região**
- **Norte:** AC, AP, AM, PA, RO, RR, TO
- **Nordeste:** AL, BA, CE, MA, PB, PE, PI, RN, SE  
- **Centro-Oeste:** DF, GO, MT, MS
- **Sudeste:** ES, MG, RJ, SP
- **Sul:** PR, RS, SC

#### 🏙️ **Só Capitais**
- Análise exclusiva das 27 capitais brasileiras
- Inclui todas as capitais estaduais + Brasília
- Filtro automático para áreas metropolitanas principais

### 📈 **Resultados e Relatórios**
- Contagem de CNPJs por estado
- Cálculo de porcentagens relativas
- Totalizadores automáticos
- Tabelas organizadas e formatadas

### 💾 **Downloads**
- **Excel (.xlsx):** Planilha completa com dados processados
- **CSV (.csv):** Arquivo de texto com dados tabulados
- Exportação instantânea dos resultados

---

## 🚀 Como Usar

### 🌐 **Interface Web (Recomendada)**

#### 1️⃣ **Iniciar a aplicação:**
```bash
cd "/Users/macbookpro/Documents/Big Data"
"/Users/macbookpro/Documents/Big Data/.venv/bin/python" -m streamlit run leitor_web.py
```

#### 2️⃣ **Acessar no navegador:**
```
http://localhost:8501
```

#### 3️⃣ **Como usar:**
1. **📂 Carregue os dados:** O arquivo `202508_CNPJ.csv` é carregado automaticamente
2. **🗺️ Escolha o tipo de pesquisa:**
   - **🏛️ Por Estado:** Digite estados separados por vírgula (Ex: "SP, RJ, MG")
   - **🌎 Por Região:** Selecione uma das 5 regiões brasileiras
   - **🏙️ Só Capitais:** Pesquise apenas nas 27 capitais
3. **🔍 Pesquise:** Clique no botão correspondente ao tipo de pesquisa
4. **📊 Veja os resultados:** Tabela formatada com quantidades e porcentagens
5. **💾 Baixe relatórios:** Excel (.xlsx) ou CSV (.csv)

---

## 🔧 Especificações Técnicas

### 📦 **Dependências a serem Instaladas**
```
streamlit     # Framework web para interface
pandas        # Manipulação e análise de dados
openpyxl      # Geração de arquivos Excel
```
### 📄 **Formato dos Dados**
- **Separador:** `;` (ponto e vírgula)
- **Codificação:** ISO-8859-1
- **Coluna principal:** `UF` (siglas dos estados)
- **Exemplo de linha:** `12345678000199;Empresa Exemplo;SP;...`

### 🐍 **Ambiente Python**
- **Versão:** Python 3.13.7
- **Tipo:** Virtual Environment (.venv)
- **Localização:** `/Documents/Big Data/.venv/`

### 🌐 **Servidor Web**
- **Framework:** Streamlit
- **Porta padrão:** 8501
- **Acesso local:** http://localhost:8501