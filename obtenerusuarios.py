usuarios = []
archivo = open('usuarios.txt', 'r')
for lineas in archivo:
  lineas = lineas.strip('\n')
  elementos = lineas.split(',')
  usuarios.append(dict(user=elementos[0], nombre = elementos[1], imagen = elementos[2]))
