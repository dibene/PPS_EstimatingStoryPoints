import os
import sys
# run preprocess_storypoint.py

datasetDict = {
      'mesos': 'apache'
   , 'usergrid': 'apache'
}

dataPres = ['apache']

# para preparar los datos se ejecutan estos 3 comandos
# mejorar las llamadas a los metodos..
for project, repo in datasetDict.items():
    print project + ' ' + repo
    cmd = 'python divide_data_sortdate.py ' + project
    print cmd
    os.system(cmd)

for dataPre in dataPres:
  #esta linea no tiene sentido, a menos que este mal identado
    #print project + ' ' + repo
    cmd = 'python preprocess.py ' + dataPre
    print cmd
    os.system(cmd)

for project, repo in datasetDict.items():
    print project + ' ' + repo
    cmd = 'python preprocess_storypoint.py ' + project + ' ' + repo
    print cmd
    os.system(cmd)

