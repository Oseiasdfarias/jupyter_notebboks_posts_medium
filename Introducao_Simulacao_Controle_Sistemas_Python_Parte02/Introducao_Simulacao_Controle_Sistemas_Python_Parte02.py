
import control as ctl 
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("seaborn")

# Use no Jupyter notebook, colab
# %matplotlib inline


# Variáveis da Simulação
R = 20.0e3
C = 10.0e-6
tau = R*C
Temp_simu = 2.0

# Função que calcula a resposta ao degrau
def Simulacao_RC(K_p = 3.0):
  # Cria a Função de Transferência em Malha Aberta
  numerador = [1/tau]
  denominador = [1.0, 1/tau]
  H_s = ctl.tf(numerador, denominador)
  #print(f"\n\n> Função de Transferência em Malha Aberta:\n {H_s}")

  # Cria a Função de Transferência do Controlador
  C_s=ctl.tf([K_p],[1.])
  #print(f"\n> Função de Transferência do Controlador:\n {C_s}")

  # Cria a Função de Transferência do Sensor
  P_s=ctl.tf([1.],[1.])

  # Função de Transferência em Malha Fechada
  G_s=ctl.series(C_s, H_s);
  G1_s=ctl.feedback(G_s, P_s, sign=-1);
  #print(f"\n> Função de Transferência em Malha fechada:\n {G1_s}")

  # Calcula a resposta ao Degrau Unitário
  T_mf, yout_mf = ctl.step_response(G1_s, Temp_simu)

  # Plotando o degrau unitário
  Temp_deg = np.linspace(-0.2, Temp_simu, 1000)
  degrau = np.ones_like(Temp_deg)
  degrau[Temp_deg < 0] = 0

  return T_mf, yout_mf, Temp_deg, degrau, K_p

# Função que plota 3 gráficos com K_p diferentes para a resposta ao degrau
def prot_grafico(T_mf, yout_mf, Temp_deg, degrau, K_p, x):
  plt.subplot(1, 3, x)
  plt.plot(T_mf, yout_mf, linewidth = 1.2)
  plt.plot(Temp_deg, degrau, color = "r", linestyle = "--", linewidth = 1.2)
  
  # Customizando a figura com Titulo,  Títulos nos eixos, Legenda e Grid
  plt.title(f"Circuito RC - Resposta ao \nDegrau em Malha Fechada, K_p = {K_p}", fontweight="bold", fontsize =  10)
  plt.ylabel("Tensão no Capacitor (V)", fontweight="bold", fontsize = 8)
  plt.xlabel("Tempo (s)", fontweight="bold", fontsize = 8)
  plt.legend(["Resposta ao Degrau", "Degrau Unitário"], fontsize = 8)


if __name__ == "__main__":
    
    # Plotando a resposta ao Degrau usando o metodo plt.plot() da biblioteca matplotlib
    plt.figure(figsize=(15, 7))

    T_mf, yout_mf, Temp_deg, degrau, K_p = Simulacao_RC(K_p = 1)
    prot_grafico(T_mf, yout_mf, Temp_deg, degrau, K_p, x = 1)

    T_mf, yout_mf, Temp_deg, degrau, K_p = Simulacao_RC(K_p = 4)
    prot_grafico(T_mf, yout_mf, Temp_deg, degrau, K_p, x = 2)

    T_mf, yout_mf, Temp_deg, degrau, K_p = Simulacao_RC(K_p = 8)
    prot_grafico(T_mf, yout_mf, Temp_deg, degrau, K_p, x = 3)

    plt.show()
