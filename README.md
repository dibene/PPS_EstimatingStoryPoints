# Deep-SE
Practica profesional supervisada UNLP
parte analisis de codigo Deep-SE

## Indicaciones
Tener instalado
python 2.7
Theano
keras 1.0.6
scikit-learn, cpickle, pandas, numby
export KERAS_BACKEND=theano

pruebas hechas solo con repositorio apache cuyos proyectos son mesos y usergrid

## quick instruction
There are three folders:
1. data: contains the dataset in csv and the code for spliting data into training set, validation set, and test set
2. NCE: contains pretraining modules, LSTM modules, and LSTM feature extraction.
3. classification: contains the Highway Net.

--- step-by-step to run DEEP SE ---(LSTM+Highway)
1. put the csv files in /data
2. run command "python run_script.py" in /data to divide data and prepare dictionary
3. run command "python exp_lstm2v_pre.py" in /NCE for pretraining (this step takes very very long time!!!. It can be skipped since the model has been trained.)
4. run commnad "python exp_script.py" in /classification for running DEEP SE

