import numpy as np

############### Define uma classe com o formato dos dados do SAXS. #########################
############################################################################################

class Saxs():
  
  def __init__(self, size=0):
    
    self.size = size
    self.q = np.zeros(size)
    self.I = np.zeros(size)
    self.sI = np.zeros(size)
  
  def ImportData(self, fileData):
    
    self.q, self.I, self.sI = np.loadtxt(fileData, usecols=(0,1,2), unpack=True)
    self.size = len(self.q)
  
  def Size(self):
    
    self.size = len(self.q)
    
    if((self.size!=len(self.I)) or (self.size!=len(self.sI))):
      print("\nSAXSPY Error: incompatibility in the size of the data arrays.\n")
    
    return self.size

########################################################################
# Define as funções de correção.
########################################################################

# Função de correção para o espalhamento do capilar (Capillary), 
# transmissão (Transmission), espessura (Thickness) e calibração da 
# escala q (q).
def CorrectTo_CTTq(
    qSlope,  
    qIntercept, 
    fileSample, 
    transmissionSample, 
    thicknessSample,
    fileCapillary, 
    transmissionCapillary,
    save=True,
    fileOutput=0):
  
  # Importa os dados SAXS.
  sample = Saxs()
  capillary = Saxs()
  sample.ImportData(fileSample)
  capillary.ImportData(fileCapillary)
  
  # Faz as correções.
  correction = Saxs()

  # Correção da escala q.
  correction.q = qSlope*sample.q + qIntercept

  # Correção da intensidade pelo capilar, transmissão e espessura.
  correction.I = (sample.I/transmissionSample - \
      capillary.I/transmissionCapillary)/thicknessSample

  # Cálculo da nova incerteza.
  correction.sI = np.sqrt((sample.sI/transmissionSample)**2 +\
      (capillary.sI/transmissionCapillary)**2)/thicknessSample

  # Salva os dados corrigidos em arquivo.
  if(save):
    # Nome do arquivo de dados para a saída corrigida.
    if(fileOutput==0):
      fileOutput = fileSample.split(".")[0] + "_cttqcorrected.dat"

    with open(fileOutput, 'w') as arq:
      arq.write("# Corrected data file from: %s \n" % fileSample)
      arq.write("# q\t\t I\t\t sI\n")
      for i in range(correction.Size()):
        arq.write("%.6e\t %.6e\t %.6e\n" % (correction.q[i], \
            correction.I[i], correction.sI[i]))

  return correction

# Função de correção para o espalhamento do solvente.
def CorrectTo_Solvent(
    fileSample,  
    fileSolvent, 
    soluteVolumetricFraction, 
    save=True, 
    fileOutput=0):
  
  # Nome do arquivo de dados para a saída corrigida.
  if(fileOutput==0):
    fileOutput = fileSample.split(".")[0] + "_solventcorrected.dat"
  
  # Importa os dados SAXS.
  sample = Saxs()
  solvent = Saxs()
  sample.ImportData(fileSample)
  solvent.ImportData(fileSolvent)
    
  # Aplica a correção.
  correction = Saxs()

  # Correção da escala q.
  correction.q = sample.q

  # Correção da intensidade pelo capilar, transmissão e espessura.
  correction.I = sample.I - (1 - soluteVolumetricFraction)*solvent.I

  # Cálculo da nova incerteza.
  correction.sI = np.sqrt((sample.sI)**2 + ((1 - soluteVolumetricFraction)*solvent.sI)**2)

  # Salva os dados corrigidos em arquivo.
  if(save):
    with open(fileOutput, 'w') as arq:
      arq.write("# Corrected data (for solvent scattering) from file: %s \n" % fileSample)
      arq.write("# q\t\t I\t\t sI\n")
      for i in range(correction.Size()):
        arq.write("%.6e\t %.6e\t %.6e\n" % (correction.q[i], \
            correction.I[i], correction.sI[i]))

  return correction

# Função de correção para a escala absoluta.
def CorrectTo_AbsoluteScale(
    absoluteScaleFactor,
    fileSample,
    save=True,
    fileOutput=0):
  
  # Define arquivo de saída caso não seja passado o argumento.
  if(fileOutput==0):
    fileOutput = fileSample.split(".")[0] + "_absolute.dat"
  
  # Importa os dados SAXS.
  sample = Saxs()
  sample.ImportData(fileSample)
  
  # Aplica a correção.
  correction = Saxs()

  # Correção da escala q.
  correction.q = sample.q

  # Correção da intensidade pelo capilar, transmissão e espessura.
  correction.I = sample.I/absoluteScaleFactor

  # Cálculo da nova incerteza.
  correction.sI = np.sqrt((sample.sI/absoluteScaleFactor)**2)
  # Tipicamente a incerteza no fator de escala é pelo menos uma ordem \
  # de grandeza menor que a incerteza nos dados, portanto não é \
  # considerada no cálculo da nova incerteza dos dados.

  # Salva os dados corrigidos em arquivo.
  if(save):
    with open(fileOutput, 'w') as arq:
      arq.write("# Corrected data (absolute scale) from file: %s\n" % (fileSample))
      arq.write("# q (A-1)\t\t I (cm-1)\t\t sI (cm-1)\n")
      for i in range(correction.Size()):
        arq.write("%.6e\t %.6e\t %.6e\n" % (correction.q[i], \
            correction.I[i], correction.sI[i]))

  return correction
