from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt

def get_main_image(score1_spicy_s,score2_acidity_s,score3_total_s,username_s):
    """Rendering the scatter chart"""


    X2=np.random.randint(10, size=(5))
    Y2=np.random.randint(10, size=(5))
    Z2=[90,300,50,660,300]

    
    

    plt.scatter(score1_spicy_s, score2_acidity_s,s=score3_total_s,label='エノティカ フル ワイン', color='aqua',alpha=0.5)
    plt.scatter(X2, Y2,s=Z2,label='aresred wine',color='olive', alpha=0.5)
    plt.title("ワイン評価結果",fontname="MS Gothic",fontsize=20)
    plt.xlabel("辛さ",fontname="MS Gothic",fontsize=18)
    plt.ylabel("酸味",fontname="MS Gothic",fontsize=18)

    annotations=username_s
   

    for i, label in enumerate(annotations):
        aaa= label+"\n"+ str(score3_total_s[i])+ "点"
        print("---->",aaa)
        plt.annotate(label+"\n"+ str(score3_total_s[i])+ "点", (score1_spicy_s[i], score2_acidity_s[i]),fontname="MS Gothic")
        plt.annotate(label, (X2[i], Y2[i]),fontname="MS Gothic")

    plt.grid(True)
    plt.legend(bbox_to_anchor=(0, -0.1), loc='lower left', borderaxespad=0, fontsize=18,prop = {"family" : "Meiryo"})

    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return img