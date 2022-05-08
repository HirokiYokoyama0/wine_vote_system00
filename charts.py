from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt

def get_main_image(score1_spicy_l,score2_acidity_l,score3_total_l,username_l,wine_selectedid2):
    """Rendering the scatter chart"""


    #plt.figure()
    fig = plt.figure()
    #plt.rcParams["figure.figsize"] = (20, 20)
    fig.set_figheight(8)
    fig.set_figwidth(10)

    score3_total0 = [n*30 for n in score3_total_l[0]]
    score3_total1 = [n*30 for n in score3_total_l[1]]

    #世の中平均用ダミー
    aveave = [[4,3.5,2.7],[3,2.3,2.9]]

    plt.scatter(score1_spicy_l[0], score2_acidity_l[0],s=score3_total0,label=wine_selectedid2[0].Brandname, color='lime',alpha=0.5)
    plt.scatter(aveave[0][0], aveave[0][1],s=aveave[0][2]*30,label=wine_selectedid2[0].Brandname + "(世の中平均)", marker=",",color='lime',alpha=0.5)
    plt.scatter(score1_spicy_l[1], score2_acidity_l[1],s=score3_total1,label=wine_selectedid2[1].Brandname, color='magenta',alpha=0.5)
    plt.scatter(aveave[1][0],aveave[1][1],s=aveave[1][2]*30,label=wine_selectedid2[1].Brandname + "(世の中平均)", marker=",",color='magenta',alpha=0.5)

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

    #世の中平均
    plt.annotate( "平均" +"\n"+ str(aveave[0][2])+ "点", (aveave[0][0], aveave[0][1]),fontname= "Meiryo")  
    plt.annotate( "平均" +"\n"+ str(aveave[1][2])+ "点", (aveave[1][0], aveave[1][1]),fontname= "Meiryo")    


    plt.grid(True)
    #plt.legend(bbox_to_anchor=(0, -0.1), loc='best', borderaxespad=0, fontsize=18,prop = {"family" : "Meiryo"})
    plt.legend(loc='best', borderaxespad=0, fontsize=18,prop = {"family" : "Meiryo"})

    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return img