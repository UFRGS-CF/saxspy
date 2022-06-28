import numpy as np

soluteMolarWeight = float(input("Entre com a massa molar do soluto:"))
#print("\n")
soluteDensity = float(input("Entre com a densidade do soluto:"))
#print("\n")
solventMolarWeight = float(input("Entre a massa molar do solvente:"))
#print("\n")
solventDensity = float(input("Entre com a densidade do solvente:"))
#print("\n")
soluteMolarFraction = float(input("Entre a fração molar (soluto):"))
print("\n")

soluteMolarVolume = soluteMolarWeight/soluteDensity
solventMolarVolume = solventMolarWeight/solventDensity 


soluteMassFraction = soluteMolarFraction*soluteMolarWeight/((1 - \
    soluteMolarFraction)*solventMolarWeight + \
    soluteMolarFraction*soluteMolarWeight)
    
soluteVolumetricFraction = soluteMolarFraction*soluteMolarVolume/((1 -\
    soluteMolarFraction)*solventMolarVolume + \
    soluteMolarFraction*soluteMolarVolume)

print("Solute Mass Fraction: %.5e" % soluteMassFraction)
print("Solute Volumetric Fraction: %.5e" % soluteVolumetricFraction)
