import numpy as np
import matplotlib.pyplot as plt
# Biblioteca de estruturas básicas para tratamento e análise de dados \
# de SAXS.
import saxspy.saxspy as saxs

############## Importa os parâmetros e nomes de arquivos. ##############
########################################################################

def ImportParameter_Solvent(fileParameters):
  
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
  print("Correcting %d data files for the solvent scattering:" % numberFiles)
  
  # Inicia as listas para receberem os argumentos.
  fileSample = []
  fileSolvent = []
  soluteVolumetricFraction = []
  nameOutput = []

  # Separa os argumentos nas linhas e notifica caso o número de 
  # argumentos por linha não esteja adequado.
  for i in range(numberFiles):
    # Prepara a string removendo espaços e tabs.
    lines[i] = lines[i].replace(" ", "")
    lines[i] = lines[i].replace("\t", "")
    
    # Separa os argumentos pelas vírgulas.
    argument = lines[i].split(",")
    
    if (len(argument) != 4):
      print("\nError: number of arguments invalid in the line %d of parameters file!\n" % (i+1))
    else:
      # Obtêm os parâmetros e retorna.
      fileSample.append(str(argument[0].strip('\n')))
      fileSolvent.append(str(argument[1].strip('\n')))
      soluteVolumetricFraction.append(float(argument[2]))
      nameOutput.append(str(argument[3].strip('\n')))
      # Imprime os arquivos que serão corrigidos.
      print("%d) %s" % ((i+1), fileSample[i]))
  
  print(" ")
  
  return numberFiles, fileSample, fileSolvent, soluteVolumetricFraction, nameOutput

########################################################################


#################### Faz o gráfico do ajuste linear. ###################
########################################################################

def PlotCorrection_Solvent(
    data,
    label, 
    close=True, 
    save=False, 
    fileOutput="Solvent_output.pdf"):
	
  plt.errorbar(data.q, data.I, yerr=data.sI, linestyle='', color='k', \
      marker='', markersize=1, capsize=2)
  plt.semilogy(data.q, data.I, linestyle='', marker='x', markersize=2, \
      label=(label))
  plt.legend(loc='upper right')
  plt.grid(True)
  plt.xlabel(r'$q_\mathrm{\,calibrated} \quad (\,\AA^{-1})\,$')
  plt.ylabel(r'$I_\mathrm{\,solute} \quad (\,a.\ u.\,)$')
  
  #plt.xticks(np.arange(0, 0.40, 0.05))
  #plt.yticks(np.arange(0, 0.40, 0.05))
  plt.tick_params(axis='x', labelsize=8)
  plt.tick_params(axis='y', labelsize=8)
  plt.title(u'SAXS scattering intensity corrected\n for the solvent scattering')
  plt.draw()
  
  if(close):
    if(save):
      plt.savefig(fileOutput)
    
    plt.show()
  

######################### PROGRAMA PRINCIPAL ###########################
########################################################################

# Abertura do programa.
print("###############################################################")
print("# This program apply the correction for scattering solvent to")
print("# a SAXS measure of a sample.")
print("###############################################################")
print("\n")

# Define o arquivo de parâmetros.
fileParameters = input("Enter the parameters file: ")
print("\n")

# Importa os parâmetros e dados para serem corrigidos.
numberFiles, fileSample, fileSolvent, soluteVolumetricFraction, nameOutput = ImportParameter_Solvent(fileParameters)

for i in range(numberFiles):
  # Corrige os dados e salva em arquivo.
  correction = saxs.CorrectTo_Solvent(fileSample[i], fileSolvent[i], soluteVolumetricFraction[i], save=True, fileOutput=(nameOutput[i]+".dat"))

  # Faz o gráfico do ajuste de calibração.
  PlotCorrection_Solvent(correction, nameOutput[i], save=False, close=((i+1)//numberFiles))
