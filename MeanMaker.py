import numpy as np
import matplotlib.pyplot as plt
# Biblioteca de estruturas básicas para tratamento e análise de dados \
# de SAXS.
import saxspy.saxspy as saxs


# Importa a lista de arquivos e insere o endereço para ela.
def ImportListFiles(fileListFiles, directoryFiles):
  directoryFiles = directoryFiles.strip('/') + "/"
  # Importa a lista de arquivos dos quais o programa vai fazer a média.    
  with open(fileListFiles,'r') as f:    
    listFiles = []
    for line in f:
      if (line[0] != '#' and line[0] != '\n' and line[0] != ' ' and line[0] != '\t'):
        listFiles.append(directoryFiles + line.strip('\n'))
    
  return listFiles

  
# Importa os dados dos arquivos, faz a média 
def SAXSMean(listFiles, fileOutput, printFileNames=False):
  # Importa os dados dos arquivos de dados, a partir da linha 31.
  numberFiles = len(listFiles)
  mean = saxs.Saxs()
  qmean = 0
  Imean = 0
  sImean = 0
  timeTotal = 0
  for fileData in listFiles:
    with open(fileData, 'r') as f:
      for _ in range(6):
        timeLine = (f.readline()).split()
        
      time = float(timeLine[2])/1000 # Divide por 1000 para ficar em segundos
      timeTotal += time
      
      if(printFileNames):
        print("%s \t %.0f" % (fileData, time))
    
    # Extrai os dados do arquivo, ignorando 30 linhas (opcional, porque as linhas são comentadas).
    q, I, sI = np.loadtxt(fileData, skiprows=30, usecols=(0,1,2), unpack=True)

    # Faz a média pesando pelo tempo de medida.
    qmean += time*q # É desnecessária essa média.
    Imean += time*I
    sImean += (time*sI)**2

  mean.q = qmean/timeTotal
  mean.I = Imean/timeTotal
  mean.sI = np.sqrt(sImean)/timeTotal


  # Salva os dados de media em um arquivo.
  #if(fileOutput==0):
  #  fileOutput = fileListFiles.split(".")[0] + "_mean.dat"
  
  with open(fileOutput, 'w') as f:
    f.write("# Médias dos dados para calibração: %s.\n" % fileOutput)
    f.write("# q\t I(q)\t sI\n")
    for i in range(mean.Size()):
      f.write("%.6e\t %.6e\t %.6e\n" % (mean.q[i], mean.I[i], mean.sI[i]))

  return mean


# Plota a intensidade vs vetor de espalhamento.
def PlotMean(
    data,
    label,
    close=True, 
    save=False, 
    fileOutput="MeanMaker_output.pdf"):
	
  plt.errorbar(data.q, data.I, yerr=data.sI, linestyle='', color='k', \
      marker='', markersize=1, capsize=2)
  plt.plot(data.q, data.I, linestyle='', marker='x', markersize=2, \
      label=(label))
  
  plt.yscale("log")
  plt.legend(loc='upper right')
  plt.grid(True)
  plt.xlabel(r'$q \quad (\,\AA^{-1})\,$')
  plt.ylabel(r'$I \quad (\,a.\ u.)$')
  
  #plt.xticks(np.arange(0, 0.40, 0.05))
  #plt.yticks(np.arange(0, 0.40, 0.05))
  plt.tick_params(axis='x', labelsize=8)
  plt.tick_params(axis='y', labelsize=8)
  plt.title(u'Mean SAXS scattering intensity')
  plt.draw()
  
  if(close):
    if(save):
      plt.savefig(fileOutput)
  
    plt.show()

########################################################################

########################### Programa Principal #########################

########################################################################

print("\nEsse programa faz as médias de um conjunto de arquivos de medidas de SAXS e salva em arquivo.\n\n")

fileListFiles = input("Entre com a lista de arquivos: ") #'lista_para_media.txt'

directoryFiles = input("Entre com o diretório dos arquivos: ")

fileOutput = input("Entre com o nome do arquivo de saída: ")
fileOutput = fileOutput.split(".")[0] + ".dat"

listFiles = ImportListFiles(fileListFiles, directoryFiles)

data = SAXSMean(listFiles, fileOutput, printFileNames=False)

PlotMean(data, label=fileOutput)

  
