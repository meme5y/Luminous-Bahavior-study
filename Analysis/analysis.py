"""
Luminous Behavior Study - Data Analysis Pipeline
Authors: [Your Name] & [Friend's Name]
Country: Mozambique
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
// ====== PROTOCOLO CIENTÍFICO - EFEITO DAS CORES ======
// Experimento controlado com randomização

// Definição dos pinos (mesmo do projeto 1)
const int pinoTrig = 2;
const int pinoEcho = 3;
const int pinoBuzzer = 4;
const int pinoVermelho = 5;
const int pinoVerde = 6;
const int pinoAzul = 7;
const int pinoIR = A0;

// ====== VARIÁVEIS DO EXPERIMENTO ======
// Cores a serem testadas
const int CORES[3][3] = {
  {255, 0, 0},   // Vermelho
  {0, 255, 0},   // Verde
  {0, 0, 255}    // Azul
};

const char* NOMES_CORES[3] = {"VERMELHO", "VERDE", "AZUL"};

// Parâmetros do experimento
const int DURACAO_TESTE = 10000;    // 10 segundos por cor
const int PAUSA_ENTRE_TESTES = 2000; // 2 segundos entre cores
const int NUM_REPETICOES = 3;        // 3 repetições de cada cor

// Variáveis de estado
int sequencia[9];      // Ordem randomizada das cores
int testeAtual = 0;
unsigned long inicioTeste = 0;
bool experimentoAtivo = false;
int leiturasPorTeste = 0;
float somaDistancias = 0;
int valorIR = 0;

// ====== SETUP ======
void setup() {
  Serial.begin(115200);
  
  // Configura pinos
  pinMode(pinoTrig, OUTPUT);
  pinMode(pinoEcho, INPUT);
  pinMode(pinoBuzzer, OUTPUT);
  pinMode(pinoVermelho, OUTPUT);
  pinMode(pinoVerde, OUTPUT);
  pinMode(pinoAzul, OUTPUT);
  
  // Gera sequência randomizada do experimento
  randomSeed(analogRead(A5)); // Semente aleatória
  gerarSequenciaRandomica();
  
  // Mensagem inicial
  Serial.println("=== INÍCIO DO EXPERIMENTO ===");
  Serial.println("Protocolo: 3 cores x 3 repetições = 9 testes");
  Serial.println("Cada teste: 10 segundos");
  Serial.println("Formato: TesteID,Cor,TimestampMs,DistanciaCm,LuminosidadeIR");
  Serial.println("==============================");
  
  delay(2000);
  iniciarExperimento();
}

// ====== LOOP PRINCIPAL ======
void loop() {
  if (!experimentoAtivo) return;
  
  unsigned long tempoAtual = millis();
  unsigned long tempoDecorrido = tempoAtual - inicioTeste;
  
  // Verifica se terminou o teste atual
  if (tempoDecorrido >= DURACAO_TESTE) {
    finalizarTeste();
    return;
  }
  
  // Durante o teste: coleta dados
  if (tempoAtual % 200 == 0) { // A cada 200ms
    int distancia = lerSensorUltrassonico();
    valorIR = analogRead(pinoIR);
    
    if (distancia > 0 && distancia < 100) {
      somaDistancias += distancia;
      leiturasPorTeste++;
      
      // Envia dados em tempo real
      Serial.print(testeAtual + 1);
      Serial.print(",");
      Serial.print(NOMES_CORES[sequencia[testeAtual]]);
      Serial.print(",");
      Serial.print(tempoAtual);
      Serial.print(",");
      Serial.print(distancia);
      Serial.print(",");
      Serial.println(valorIR);
    }
  }
}

// ====== FUNÇÕES DO PROTOCOLO ======

void gerarSequenciaRandomica() {
  // Gera array: [0,1,2,0,1,2,0,1,2] depois embaralha
  for (int i = 0; i < 9; i++) {
    sequencia[i] = i % 3;
  }
  
  // Embaralha usando Fisher-Yates
  for (int i = 8; i > 0; i--) {
    int j = random(i + 1);
    int temp = sequencia[i];
    sequencia[i] = sequencia[j];
    sequencia[j] = temp;
  }
  
  // Log da sequência (apenas para pesquisador)
  Serial.print("SEQUENCIA_RANDOMICA: ");
  for (int i = 0; i < 9; i++) {
    Serial.print(NOMES_CORES[sequencia[i]]);
    if (i < 8) Serial.print("-");
  }
  Serial.println();
}

void iniciarExperimento() {
  experimentoAtivo = true;
  testeAtual = 0;
  iniciarTeste();
}

void iniciarTeste() {
  inicioTeste = millis();
  leiturasPorTeste = 0;
  somaDistancias = 0;
  
  // Ativa a cor do teste atual
  int corIndex = sequencia[testeAtual];
  setColor(CORES[corIndex][0], CORES[corIndex][1], CORES[corIndex][2]);
  
  // Sinal sonoro (participante não sabe qual cor)
  tone(pinoBuzzer, 1000, 300);
  
  // Log do início do teste
  Serial.print("INICIO_TESTE:");
  Serial.print(testeAtual + 1);
  Serial.print(",COR:");
  Serial.println(NOMES_CORES[corIndex]);
}

void finalizarTeste() {
  // Calcula estatísticas do teste
  float media = (leiturasPorTeste > 0) ? somaDistancias / leiturasPorTeste : 0;
  
  Serial.print("FIM_TESTE:");
  Serial.print(testeAtual + 1);
  Serial.print(",COR:");
  Serial.print(NOMES_CORES[sequencia[testeAtual]]);
  Serial.print(",MEDIA:");
  Serial.print(media, 2);
  Serial.print(",AMOSTRAS:");
  Serial.println(leiturasPorTeste);
  
  // Desliga LED e vai para próximo teste
  setColor(0, 0, 0);
  
  testeAtual++;
  
  if (testeAtual >= 9) {
    finalizarExperimento();
  } else {
    delay(PAUSA_ENTRE_TESTES);
    iniciarTeste();
  }
}

void finalizarExperimento() {
  experimentoAtivo = false;
  setColor(0, 0, 0);
  
  // Sinal de término
  for (int i = 0; i < 3; i++) {
    tone(pinoBuzzer, 800 + i * 200, 200);
    delay(300);
  }
  
  Serial.println("=== EXPERIMENTO CONCLUÍDO ===");
  Serial.println("Analise os dados para verificar a hipótese");
}

// ====== FUNÇÕES AUXILIARES ======
int lerSensorUltrassonico() {
  digitalWrite(pinoTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pinoTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinoTrig, LOW);
  
  long duracao = pulseIn(pinoEcho, HIGH);
  int distancia = duracao * 0.034 / 2;
  
  return (distancia > 0 && distancia < 300) ? distancia : 0;
}

void setColor(int vermelho, int verde, int azul) {
  analogWrite(pinoVermelho, 255 - vermelho);
  analogWrite(pinoVerde, 255 - verde);
  analogWrite(pinoAzul, 255 - azul);
}

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import pingouin as pg  # Instale: pip install pingouin

# Configuração estética
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# 1. CARREGAR OS DADOS
print("=== CARREGANDO DADOS DO EXPERIMENTO ===\n")

# Leitura dos dados
df = pd.read_csv('dados_experimento.csv', 
                  names=['TesteID', 'Cor', 'Timestamp', 'Distancia', 'Luminosidade'])

print("Primeiras linhas dos dados:")
print(df.head())
print(f"\nTotal de medições: {len(df)}")
print(f"Participantes únicos (se houver): {df['TesteID'].nunique()}")

# 2. PRÉ-PROCESSAMENTO
# Remover outliers (distâncias fisicamente impossíveis)
df = df[(df['Distancia'] > 10) & (df['Distancia'] < 100)]

# Calcular estatísticas por teste
estatisticas = df.groupby(['TesteID', 'Cor']).agg({
    'Distancia': ['mean', 'std', 'count', 'min', 'max'],
    'Luminosidade': 'mean'
}).round(2)

estatisticas.columns = ['Media_Distancia', 'Desvio_Distancia', 'N_Amostras', 
                        'Min_Distancia', 'Max_Distancia', 'Media_Luminosidade']
estatisticas = estatisticas.reset_index()

print("\n=== ESTATÍSTICAS DESCRITIVAS POR GRUPO ===")
print(estatisticas.groupby('Cor')['Media_Distancia'].describe())

# 3. VISUALIZAÇÃO DOS DADOS
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Gráfico 1: Distribuição por cor
axes[0, 0].boxplot([df[df['Cor'] == 'VERMELHO']['Distancia'],
                    df[df['Cor'] == 'VERDE']['Distancia'],
                    df[df['Cor'] == 'AZUL']['Distancia']])
axes[0, 0].set_xticklabels(['Vermelho', 'Verde', 'Azul'])
axes[0, 0].set_ylabel('Distância (cm)')
axes[0, 0].set_title('Distribuição das Distâncias por Cor')
axes[0, 0].grid(True, alpha=0.3)

# Gráfico 2: Média com intervalo de confiança
media_por_cor = estatisticas.groupby('Cor')['Media_Distancia'].mean()
erro_por_cor = estatisticas.groupby('Cor')['Media_Distancia'].std() / np.sqrt(estatisticas.groupby('Cor')['Media_Distancia'].count())

cores_plot = ['red', 'green', 'blue']
for idx, cor in enumerate(['VERMELHO', 'VERDE', 'AZUL']):
    axes[0, 1].bar(idx, media_por_cor[cor], color=cores_plot[idx], alpha=0.7,
                   yerr=erro_por_cor[cor] * 1.96, capsize=10)
axes[0, 1].set_xticks(range(3))
axes[0, 1].set_xticklabels(['Vermelho', 'Verde', 'Azul'])
axes[0, 1].set_ylabel('Distância Média (cm)')
axes[0, 1].set_title('Média com Intervalo de Confiança (95%)')
axes[0, 1].grid(True, alpha=0.3)

# Gráfico 3: Evolução temporal por teste
for cor in ['VERMELHO', 'VERDE', 'AZUL']:
    dados_cor = estatisticas[estatisticas['Cor'] == cor]
    axes[0, 2].plot(dados_cor['TesteID'], dados_cor['Media_Distancia'], 
                   'o-', label=cor, alpha=0.7)
axes[0, 2].set_xlabel('Número do Teste')
axes[0, 2].set_ylabel('Distância Média (cm)')
axes[0, 2].set_title('Evolução ao Longo dos Testes')
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

# Gráfico 4: Histograma cumulativo
for cor, color in zip(['VERMELHO', 'VERDE', 'AZUL'], ['red', 'green', 'blue']):
    dados = df[df['Cor'] == cor]['Distancia']
    axes[1, 0].hist(dados, bins=20, alpha=0.5, density=True, 
                   cumulative=True, histtype='step', linewidth=2,
                   color=color, label=cor)
axes[1, 0].set_xlabel('Distância (cm)')
axes[1, 0].set_ylabel('Probabilidade Cumulativa')
axes[1, 0].set_title('Função de Distribuição Acumulada')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Gráfico 5: Correlação Distância x Luminosidade
scatter = axes[1, 1].scatter(df['Distancia'], df['Luminosidade'], 
                            c=pd.Categorical(df['Cor']).codes, 
                            cmap='viridis', alpha=0.6)
axes[1, 1].set_xlabel('Distância (cm)')
axes[1, 1].set_ylabel('Luminosidade (IR)')
axes[1, 1].set_title('Correlação: Distância vs Luminosidade')
plt.colorbar(scatter, ax=axes[1, 1], label='Cor')

# Gráfico 6: Resíduos
modelo = pg.anova(data=estatisticas, dv='Media_Distancia', between='Cor')
# Placeholder para gráfico de resíduos
axes[1, 2].text(0.5, 0.5, 'Análise de Variância\n(Ver resultados no console)', 
                ha='center', va='center', fontsize=12)
axes[1, 2].axis('off')

plt.tight_layout()
plt.savefig('analise_completa.png', dpi=150, bbox_inches='tight')
plt.show()

# 4. TESTES ESTATÍSTICOS FORMALAIS
print("\n=== TESTES ESTATÍSTICOS ===")

# ANOVA de uma via (teste paramétrico)
print("\n1. ANOVA (Análise de Variância):")
anova_result = pg.anova(data=estatisticas, dv='Media_Distancia', between='Cor')
print(anova_result)

if anova_result['p-unc'][0] < 0.05:
    print("✓ Diferença estatisticamente significativa (p < 0.05)")
    
    # Testes post-hoc (Tukey HSD)
    print("\n2. Teste Post-Hoc (Tukey HSD):")
    posthoc = pg.pairwise_tukey(data=estatisticas, dv='Media_Distancia', between='Cor')
    print(posthoc)
    
    # Efeito prático (Cohen's d)
    print("\n3. Tamanho do Efeito (Cohen's d):")
    vermelho_verde = pg.compute_effsize(
        estatisticas[estatisticas['Cor'] == 'VERMELHO']['Media_Distancia'],
        estatisticas[estatisticas['Cor'] == 'VERDE']['Media_Distancia'],
        eftype='cohen'
    )
    vermelho_azul = pg.compute_effsize(
        estatisticas[estatisticas['Cor'] == 'VERMELHO']['Media_Distancia'],
        estatisticas[estatisticas['Cor'] == 'AZUL']['Media_Distancia'],
        eftype='cohen'
    )
    
    print(f"Vermelho vs Verde: d = {vermelho_verde:.3f}")
    print(f"Vermelho vs Azul: d = {vermelho_azul:.3f}")
    
    # Interpretação
    print("\n4. INTERPRETAÇÃO:")
    print("|d| < 0.2: Efeito trivial")
    print("0.2 ≤ |d| < 0.5: Efeito pequeno")
    print("0.5 ≤ |d| < 0.8: Efeito médio")
    print("|d| ≥ 0.8: Efeito grande")
else:
    print("✗ Nenhuma diferença estatisticamente significativa (p ≥ 0.05)")

# 5. TESTE NÃO PARAMÉTRICO (Kruskal-Wallis)
print("\n5. Teste de Kruskal-Wallis (não paramétrico):")
kw_result = stats.kruskal(
    estatisticas[estatisticas['Cor'] == 'VERMELHO']['Media_Distancia'],
    estatisticas[estatisticas['Cor'] == 'VERDE']['Media_Distancia'],
    estatisticas[estatisticas['Cor'] == 'AZUL']['Media_Distancia']
)
print(f"H = {kw_result.statistic:.3f}, p = {kw_result.pvalue:.4f}")

# 6. PODER ESTATÍSTICO
print("\n6. Poder Estatístico (Power Analysis):")
# Para planejar futuros experimentos
effect_size = 0.8  # Tamanho do efeito esperado
alpha = 0.05
power = 0.8

# Cálculo do tamanho amostral necessário
from statsmodels.stats.power import FTestAnovaPower
ftest = FTestAnovaPower()
sample_size = ftest.solve_power(effect_size=effect_size, alpha=alpha, power=power, k_groups=3)
print(f"Para detectar efeito médio (d=0.8) com 80% de poder:")
print(f"Tamanho amostral necessário por grupo: {np.ceil(sample_size):.0f} testes")

# 7. EXPORTAR RELATÓRIO
with open('relatorio_experimento.txt', 'w') as f:
    f.write("=== RELATÓRIO DO EXPERIMENTO ===\n\n")
    f.write(f"Total de medições: {len(df)}\n")
    f.write(f"Total de testes: {len(estatisticas)}\n\n")
    
    f.write("RESULTADOS PRINCIPAIS:\n")
    for cor in ['VERMELHO', 'VERDE', 'AZUL']:
        media = estatisticas[estatisticas['Cor'] == cor]['Media_Distancia'].mean()
        std = estatisticas[estatisticas['Cor'] == cor]['Media_Distancia'].std()
        f.write(f"{cor}: {media:.1f} ± {std:.1f} cm\n")
    
    f.write(f"\nANOVA: F = {anova_result['F'][0]:.3f}, p = {anova_result['p-unc'][0]:.4f}\n")
    
    if anova_result['p-unc'][0] < 0.05:
        f.write("\nCONCLUSÃO: Rejeita-se H0. Há evidência de que a cor influencia a distância.\n")
    else:
        f.write("\nCONCLUSÃO: Não se rejeita H0. Sem evidência de diferença entre cores.\n")

print("\n=== RELATÓRIO GERADO: 'relatorio_experimento.txt' ===")

print("Luminous Behavior Study - Analysis Complete")
print("Project by: Mozambican Students")
