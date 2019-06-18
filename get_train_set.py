import sys
import os
import random


def get_train_set(filename_source, filename_target, evaluatePercent):
    try:
        with open(filename_source, 'r', errors='ignore') as fs:
            text_source = fs.readlines()
    except IOError:
        print(filename_source, "doesn't exit")
        return
        
    try:
        with open(filename_target, 'r', errors='ignore') as ft:
            text_target = ft.readlines()
    except IOError:
        print(filename_target, "doesn't exit")
        return

    nrLines = len(text_source)
    
    if nrLines != len(text_target):
    	print("The number of lines in each file must match")
    	return
    
    nrEvaluation = (int(evaluatePercent)*nrLines)//100
    nrTraining = nrLines - nrEvaluation

    if nrLines==0:
        print("The files supplied are empty")
        return
            
    if nrEvaluation==0:
        print("You must provide a higher evaluation percentage value")
        return
            
    if nrTraining==0:
        print("You must provide a smaller evaluation percentage value")
        return
		
    evaluationLines = random.sample(range(0, nrLines), nrEvaluation)
    
    filepath_train = "./training_sets/train/"
    dirname_train = os.path.dirname(filepath_train)
    if not os.path.exists(dirname_train):
        os.makedirs(dirname_train)
        
    filepath_evaluate = "./training_sets/eval/"
    dirname_evaluate = os.path.dirname(filepath_evaluate)
    if not os.path.exists(dirname_evaluate):
        os.makedirs(dirname_evaluate)

    with open(filepath_train + "src-train" + ".txt", 'w') as fts, \
        open(filepath_train + "tgt-train" + ".txt", 'w') as ftt, \
        open(filepath_evaluate + "src-val" + ".txt", 'w') as fes, \
        open(filepath_evaluate + "tgt-val" + ".txt", 'w') as fet:

        for i in range(nrLines):
            if i in evaluationLines:
                fes.write(text_source[i])
                fet.write(text_target[i])
            else:
                fts.write(text_source[i])
                ftt.write(text_target[i])
			
				
if len(sys.argv)==1:
    print("Specify source file.")

elif len(sys.argv)==2:
    print("Specify target file.")

elif len(sys.argv)==3:
    print("Specify the size of the evaluation set (1-99).")

else:
    get_train_set(sys.argv[1], sys.argv[2], sys.argv[3])
