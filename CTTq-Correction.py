import numpy as np
import matplotlib.pyplot as plt
# Biblioteca para tratamento e análise de dados de medidas de SAXS.
import saxspy.saxspy as saxs


############## Importa os parâmetros e nomes de arquivos. ##############
########################################################################
def ImportParameter_CTTq(fileParameters):
  
  # Extrai os dados do arquivo ignorando as linhas comentadas e "em 
  # branco" (atenção que na verdade linhas que começam com tab e space 
  # são tratadas como linhas em branco).
  with open(fileParameters, 'r') as f:
    lines = []
    for line in f:
      if (line[0] != '#' and line[0] != '\n' and line[0] != ' ' and line[0] != '\t'):
        lines.append(line)
  
  # Indica o número de arquivos a serem corrigidos (número de linhas de
  # argumentos).
  numberFiles = len(lines)
  print("Correcting %d data files for the capillary scattering, transmission, thickness and q-scale calibration:" % numberFiles)
  
  # Inicia as listas para receberem os argumentos.
  qSlope = []
  qIntercept = []
  fileSample = []
  transmissionSample = []
  thicknessSample = []
  fileCapillary = []
  transmissionCapillary = []
  nameOutput = []

  # Separa os argumentos nas linhas e notifica caso o número de 
  # argumentos por linha não esteja adequado.
  for i in range(numberFiles):
    # Prepara a string removendo espaços e tabs.
    lines[i] = lines[i].replace(" ", "")
    lines[i] = lines[i].replace("\t", "")
    
    # Separa os argumentos pelas vírgulas.
    argument = lines[i].split(",")
    
    if (len(argument) != 8):
      print("\nError: number of arguments invalid in the line %d of parameters file!\n" % (i+1))
    else:
      # Obtêm os parâmetros e retorna.
      qSlope.append(float(argument[0]))
      qIntercept.append(float(argument[1]))
      fileSample.append(str(argument[2].strip('\n')))
      transmissionSample.append(float(argument[3]))
      thicknessSample.append(float(argument[4]))
      fileCapillary.append(str(argument[5].strip('\n')))
      transmissionCapillary.append(float(argument[6]))
      nameOutput.append(str(argument[7].strip('\n')))
      # Imprime os arquivos que serão corrigidos.
      print("%d) %s" % ((i+1), fileSample[i]))
  
  print(" ")
  
  return numberFiles, qSlope, qIntercept, fileSample, \
      transmissionSample, thicknessSample, fileCapillary, \
      transmissionCapillary, nameOutput

########################################################################


###################### Faz o gráfico da correção. ######################
########################################################################

def PlotCorrection_CTTq(
    data,
    label,
    close=True, 
    save=False, 
    fileOutput="CTTq_output.pdf"):
	
  plt.errorbar(data.q, data.I, yerr=data.sI, linestyle='', color='k', \
      marker='', markersize=1, capsize=2)
  plt.semilogy(data.q, data.I, linestyle='', marker='x', markersize=2, \
      label=(label))
  plt.legend(loc='upper right')
  plt.grid(True)
  plt.xlabel(r'$q_\mathrm{\,calibrated} \quad (\,\AA^{-1})\,$')
  plt.ylabel(r'$I_\mathrm{\,pre-corrected} \quad (\,a.\ u.\,)$')
  
  #plt.xticks(np.arange(0, 0.40, 0.05))
  #plt.yticks(np.arange(0, 0.40, 0.05))
  plt.tick_params(axis='x', labelsize=8)
  plt.tick_params(axis='y', labelsize=8)
  plt.title(u'SAXS scattering intensity corrected\n for capilar, transmission and thickness. q-scale calibrated.')
  plt.draw()
  
  if(close):
    if(save):
      plt.savefig(fileOutput)
  
    plt.show()

########################################################################



######################### PROGRAMA PRINCIPAL ###########################
########################################################################

# Abertura do programa.
print("###############################################################")
print("# This program apply the corrections to capillary, transmission")
print("# and thickness for the SAXS measure. It too calibrate the")
print("# measure's q-scale.")
print("###############################################################")
print("\n")

# Define o arquivo de parâmetros.
fileParameters = input("Enter the parameters file: ")
print("\n")

numberFiles, qSlope, qIntercept, fileSample, transmissionSample, thicknessSample, \
    fileCapillary, transmissionCapillary, \
    nameOutput = ImportParameter_CTTq(fileParameters)

for i in range(numberFiles):
  # Corrige os dados e salva em arquivo.
  correction = saxs.CorrectTo_CTTq(qSlope[i], qIntercept[i], \
      fileSample[i], transmissionSample[i], thicknessSample[i], \
      fileCapillary[i], transmissionCapillary[i], save=True, \
      fileOutput=(nameOutput[i]+".dat"))

  # Faz o gráfico do ajuste de calibração.
  PlotCorrection_CTTq(correction, nameOutput[i], close=((i+1)//numberFiles), save=False)
