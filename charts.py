from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt

def get_main_image(score1_spicy_l,score2_acidity_l,score3_total_l,username_l,wine_selectedid2):
    """Rendering the scatter chart"""


    plt.figure()

    score3_total0 = [n*30 for n in score3_total_l[0]]
    score3_total1 = [n*30 for n in score3_total_l[1]]

    plt.scatter(score1_spicy_l[0], score2_acidity_l[0],s=score3_total0,label=wine_selectedid2[0].Brandname, color='lime',alpha=0.5)
    plt.scatter(score1_spicy_l[1], score2_acidity_l[1],s=score3_total1,label=wine_selectedid2[1].Brandname, color='magenta',alpha=0.5)
    #plt.scatter(score1_spicy_l[0], score2_acidity_l[0],s=score3_total_l[0],label='エノティカ フル ワイン', color='aqua',alpha=0.5)
    #plt.scatter(X2, Y2,s=Z2,label='aresred wine',color='olive', alpha=0.5)
    plt.title("ワイン試飲評価 グラフ",fontname="Meiryo",fontsize=18)
    plt.xlabel("辛さ",fontname="Meiryo",fontsize=14)
    plt.ylabel("酸味",fontname="Meiryo",fontsize=14)
    plt.xlim(0,6.5)
    plt.ylim(0,6.5)

    annotations0=username_l[0]
    annotations1=username_l[1]
   
    for i, label in enumerate(annotations0):
        #aaa= label+"\n"+ str(score3_total_l[0][i])+ "点"
        #print("---->",aaa)
        plt.annotate(label+"\n"+ str(score3_total_l[0][i])+ "点", (score1_spicy_l[0][i], score2_acidity_l[0][i]),fontname= "Meiryo")

    for i, label in enumerate(annotations1):
        aaa= label+"\n"+ str(score3_total_l[1][i])+ "点"
        print("---->",aaa)
        plt.annotate(label+"\n"+ str(score3_total_l[1][i])+ "点", (score1_spicy_l[1][i], score2_acidity_l[1][i]),fontname= "Meiryo")
    

    plt.grid(True)
    #plt.legend(bbox_to_anchor=(0, -0.1), loc='best', borderaxespad=0, fontsize=18,prop = {"family" : "Meiryo"})
    plt.legend(loc='best', borderaxespad=0, fontsize=18,prop = {"family" : "Meiryo"})

    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return img