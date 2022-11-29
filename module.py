def label(data):
    new=[]
    for val in data:
        if val in ("1+0","2+1"):
            new.append("Bullet")
        elif val in ("3+0","3+2","5+0","5+3"):
            new.append("Blitz")
        elif val in ("10+0","10+5","15+10"):
            new.append("Rapid")
        elif val in ("30+0", "30+20"):
            new.append("Classical")
        else:
            new.append("Custom")
    return(new)

def create_fen(data):
    import chess
    new=[]
    for val in data:
        board = chess.Board()
        for move in val.split():
            board.push_san(move)
            new.append(board.fen())
    return(new)

#input needs to be in the form of df.new.iloc[0:x ,7]
def stockfish_metric(data, num_topmoves):
    import chess   
    import chess.engine
    import math
    from stockfish import Stockfish
    
    W_rate=[]
    B_rate=[]
    num_topmoves = 3  

    for tes in data:
        W = 0
        B = 0
        Wnum = 0 
        Bnum = 0
        board = chess.Board()
        fishboard = chess.Board()           

        for i in range(len(tes)):
            stockfish = Stockfish(r"C:\Users\Stephanie Tanasia\Downloads\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe")
            stockfish.set_fen_position(board.fen()) #updates the current board position for stockfish
            engine_moves = stockfish.get_top_moves(num_topmoves) #returns a list of dictionaries containing the top moves
            fishfen=[]
        
            if i % 2 == 0: #for white pieces
                board.push_san(tes[i])
                fen1 = board.fen()
                Wnum = Wnum + 1
                board.pop()

                for dic in engine_moves:
                    board.push_san(dic['Move'])
                    k = board.fen()
                    fishfen.append(k)
                    board.pop()
                    
                board.push_san(tes[i]) #makes the piece move again
                
                if fen1 in fishfen: #counter
                    W=W+1
                
                
            elif i % 2 == 1: #for black pieces
                board.push_san(tes[i])
                fen1 = board.fen()
                Bnum = Bnum + 1
                board.pop()

                for dic in engine_moves:
                    board.push_san(dic['Move'])
                    k = board.fen()
                    fishfen.append(k)
                    board.pop()
                    
                board.push_san(tes[i]) 
                
                if fen1 in fishfen:
                    B=B+1
        
        W_rate.append(W/Wnum)
        B_rate.append(B/Bnum)

    return(W_rate, B_rate)

# The confusion matrix function is borrowed from https://github.com/DTrimarchi10/confusion_matrix/blob/master/cf_matrix.py
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def make_confusion_matrix(cf,
                          group_names=None,
                          categories='auto',
                          count=True,
                          percent=True,
                          cbar=True,
                          xyticks=True,
                          xyplotlabels=True,
                          sum_stats=True,
                          figsize=None,
                          cmap='Blues',
                          title=None):
    '''
    This function will make a pretty plot of an sklearn Confusion Matrix cm using a Seaborn heatmap visualization.
    Arguments
    ---------
    cf:            confusion matrix to be passed in
    group_names:   List of strings that represent the labels row by row to be shown in each square.
    categories:    List of strings containing the categories to be displayed on the x,y axis. Default is 'auto'
    count:         If True, show the raw number in the confusion matrix. Default is True.
    normalize:     If True, show the proportions for each category. Default is True.
    cbar:          If True, show the color bar. The cbar values are based off the values in the confusion matrix.
                   Default is True.
    xyticks:       If True, show x and y ticks. Default is True.
    xyplotlabels:  If True, show 'True Label' and 'Predicted Label' on the figure. Default is True.
    sum_stats:     If True, display summary statistics below the figure. Default is True.
    figsize:       Tuple representing the figure size. Default will be the matplotlib rcParams value.
    cmap:          Colormap of the values displayed from matplotlib.pyplot.cm. Default is 'Blues'
                   See http://matplotlib.org/examples/color/colormaps_reference.html
                   
    title:         Title for the heatmap. Default is None.
    '''


    # CODE TO GENERATE TEXT INSIDE EACH SQUARE
    blanks = ['' for i in range(cf.size)]

    if group_names and len(group_names)==cf.size:
        group_labels = ["{}\n".format(value) for value in group_names]
    else:
        group_labels = blanks

    if count:
        group_counts = ["{0:0.0f}\n".format(value) for value in cf.flatten()]
    else:
        group_counts = blanks

    if percent:
        group_percentages = ["{0:.2%}".format(value) for value in cf.flatten()/np.sum(cf)]
    else:
        group_percentages = blanks

    box_labels = [f"{v1}{v2}{v3}".strip() for v1, v2, v3 in zip(group_labels,group_counts,group_percentages)]
    box_labels = np.asarray(box_labels).reshape(cf.shape[0],cf.shape[1])


    # CODE TO GENERATE SUMMARY STATISTICS & TEXT FOR SUMMARY STATS
    if sum_stats:
        #Accuracy is sum of diagonal divided by total observations
        accuracy  = np.trace(cf) / float(np.sum(cf))

        #if it is a binary confusion matrix, show some more stats
        if len(cf)==2:
            #Metrics for Binary Confusion Matrices
            precision = cf[1,1] / sum(cf[:,1])
            recall    = cf[1,1] / sum(cf[1,:])
            f1_score  = 2*precision*recall / (precision + recall)
            stats_text = "\n\nAccuracy={:0.3f}\nPrecision={:0.3f}\nRecall={:0.3f}\nF1 Score={:0.3f}".format(
                accuracy,precision,recall,f1_score)
        else:
            stats_text = "\n\nAccuracy={:0.4f}".format(accuracy)
    else:
        stats_text = ""


    # SET FIGURE PARAMETERS ACCORDING TO OTHER ARGUMENTS
    if figsize==None:
        #Get default figure size if not set
        figsize = plt.rcParams.get('figure.figsize')

    if xyticks==False:
        #Do not show categories if xyticks is False
        categories=False


    # MAKE THE HEATMAP VISUALIZATION
    plt.figure(figsize=figsize)
    sns.heatmap(cf,annot=box_labels,fmt="",cmap=cmap,cbar=cbar,xticklabels=categories,yticklabels=categories)

    if xyplotlabels:
        plt.ylabel('True label')
        plt.xlabel('Predicted label' + stats_text)
    else:
        plt.xlabel(stats_text)
    
    if title:
        plt.title(title)
