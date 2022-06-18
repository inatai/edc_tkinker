import tkinter
import tkinter.ttk

import random
import math
import copy

from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps 

class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('tkinter canvas trial')
        self.pack()
        self.create_widgets()

    def create_canvas(self):
        self.canvas_width = 500
        self.canvas_height = 500
        self.back_color = 'lightblue'
        self.test_canvas = tkinter.Canvas(self, bg=self.back_color, width=self.canvas_width, height=self.canvas_height, highlightthickness=0)
        self.test_canvas.grid(row=0, column=0, rowspan=13)

    def create_widgets(self):
        self.create_canvas()
        self.button_create_map = tkinter.ttk.Button(self, text="都市手動作成", command=self.create_map)
        self.button_create_map.grid(row=0, column=1)
        self.count = 0 #都市の丸のタグに使う

        self.button_auto_map = tkinter.ttk.Button(self, text="都市自動作成", command=self.auto_map)
        self.button_auto_map.grid(row=1, column=1)
        self.citylist_x = []

    def destroy_home_widget(self):
        self.button_create_map.destroy()
        self.button_auto_map.destroy()

    def create_map(self): #手動都市作成
        self.destroy_home_widget()
        
        self.city_kosuu = tkinter.StringVar()
        self.label_city_kosuu = tkinter.ttk.Label(self, textvariable=self.city_kosuu)
        self.label_city_kosuu.grid(row=0, column=1)

        self.button_reset_city = tkinter.ttk.Button(self, text="リセット", command=self.reset_map)
        self.button_reset_city.grid(row=8, column=2)
        self.button_delete_city = tkinter.ttk.Button(self, text="都市削除", command=self.delete_map)
        self.button_delete_city.grid(row=6, column=2)
        self.button_add_city = tkinter.ttk.Button(self, text="都市追加", command=self.add_map)
        self.button_add_city.grid(row=6, column=1)
        self.button_title_create_map = tkinter.ttk.Button(self, text="タイトルへ", command=self.create_map_destroy)
        self.button_title_create_map.grid(row=12, column=1)
 
        self.create_menu()
        self.mk_label()

        self.citylist_x = []
        self.citylist_y = []
        self.citylist_tags = []
        self.count = 0

    def create_map_destroy(self): #手動からタイトルに戻る
        self.mk_label_destroy()
        self.label_city_kosuu.destroy()
        self.button_reset_city.destroy()
        self.button_delete_city.destroy()
        self.button_add_city.destroy()
        self.button_title_create_map.destroy()
        self.label_record.destroy()
        self.create_widgets()



    def add_map(self): #マウスクリックで都市追加
        self.test_canvas.bind('<ButtonPress-1>', self.add_city)

    def add_city(self, event):
        tag = f'oval-{self.count}'
        self.test_canvas.create_oval(event.x-6, event.y-6, event.x+6, event.y+6, fill="black", tag=tag)
        self.citylist_x.append(event.x-6)
        self.citylist_y.append(event.y-6)
        self.citylist_tags.append(tag)
        self.count += 1
        self.city_kosuu.set('都市数 : ' + str(len(self.citylist_x)))


    def delete_map(self): #都市クリックで都市削除
        self.test_canvas.bind('<ButtonPress-1>', self.delete_city)

    def delete_city(self, event):
        self.test_canvas.delete("line")
        x,y = self.test_canvas.canvasx(event.x),self.test_canvas.canvasy(event.y)
        s = ' current'
        for obj in self.test_canvas.find_overlapping(x,y,x,y):
            tag = str(self.test_canvas.itemcget(obj, 'tags'))
            # print(tag)
            if s in tag:
                t = tag.replace(s, '')
                n = self.citylist_tags.index(t)
                # print(f'{t} : {n}')
                self.test_canvas.delete(t)
                del self.citylist_tags[n]
                del self.citylist_x[n]
                del self.citylist_y[n]
                self.city_kosuu.set('都市数 : ' + str(len(self.citylist_x)))
                break


    def reset_map(self): #リセットボタン
        self.test_canvas.delete("all")
        self.citylist_x = []
        self.citylist_y = []
        self.citylist_tags = []
        self.count = 0
        self.city_kosuu.set('都市数 :  0')
        self.record.set('')



    #自動都市作成
    def auto_map(self):
        self.destroy_home_widget()

        self.label_numCity = tkinter.ttk.Label(self, text='都市数')
        self.label_numCity.grid(row=0, column=1)
        self.txt_numCity = tkinter.ttk.Entry(self, width=10)
        self.txt_numCity.grid(row=0, column=2)

        #都市自動作成ボタン
        self.auto_auto_add_city = tkinter.ttk.Button(self, text="都市作成", command=self.auto_add_city)
        self.auto_auto_add_city.grid(row=0, column=3)

        self.button_title_auto_map = tkinter.ttk.Button(self, text="タイトルへ", command=self.auto_map_destroy)
        self.button_title_auto_map.grid(row=12, column=1)

        self.mk_label()



    def auto_add_city(self): #指定した数だけ都市を自動作成
        self.test_canvas.delete("all")
        self.NUM_CITY = int(self.txt_numCity.get())
        self.City = [[0 for j in range(2)] for i in range(self.NUM_CITY)]
        self.Kyori_city = [[0 for j in range(self.NUM_CITY)] for i in range(self.NUM_CITY)]

        self.mk_city()
        self.put_map()

    def put_map(self):#都市を描画
        for i in range(0, self.NUM_CITY):
            x = int(self.City[i][0]*(self.canvas_width-12))+6
            y = int(self.City[i][1]*(self.canvas_height-12))+6
            self.test_canvas.create_oval(x-6, y-6, x+6, y+6, fill="black", tag="oval")
    
    
    def auto_map_destroy(self):# 自動からタイトルへ
        self.mk_label_destroy()
        self.label_numCity.destroy()
        self.txt_numCity.destroy()
        self.auto_auto_add_city.destroy()
        self.button_title_auto_map.destroy()
        self.label_record.destroy()
        self.create_widgets()


    def mk_label(self):#入力欄作成
        self.label_numGene = tkinter.ttk.Label(self, text='遺伝子数')
        self.label_numGene.grid(row=1, column=1)
        self.label_G_fin = tkinter.ttk.Label(self, text='世代数')
        self.label_G_fin.grid(row=2, column=1)
        self.label_p_select = tkinter.ttk.Label(self, text='選択割合')
        self.label_p_select.grid(row=3, column=1)
        self.label_p_kousa = tkinter.ttk.Label(self, text='交叉割合')
        self.label_p_kousa.grid(row=4, column=1)
        self.label_p_mut = tkinter.ttk.Label(self, text='突然変異率')
        self.label_p_mut.grid(row=5, column=1)

        self.txt_numGene = tkinter.ttk.Entry(self, width=10)
        self.txt_numGene.grid(row=1, column=2)
        self.txt_G_fin = tkinter.ttk.Entry(self, width=10)
        self.txt_G_fin.grid(row=2, column=2)
        self.txt_p_select = tkinter.ttk.Entry(self, width=10)
        self.txt_p_select.grid(row=3, column=2)
        self.txt_p_kousa = tkinter.ttk.Entry(self, width=10)
        self.txt_p_kousa.grid(row=4, column=2)
        self.txt_p_mut = tkinter.ttk.Entry(self, width=10)
        self.txt_p_mut.grid(row=5, column=2)

        self.txt_numGene.insert(0, "100")
        self.txt_G_fin.insert(0, "100")
        self.txt_p_select.insert(0, "0.5")
        self.txt_p_kousa.insert(0, "0.25")
        self.txt_p_mut.insert(0, "0.05")

        self.txt_get_button = tkinter.ttk.Button(self, text="計算開始", command=self.edc)
        self.txt_get_button.grid(row=7, column=2)


    def mk_label_destroy(self):
        self.label_numGene.destroy()
        self.label_G_fin.destroy()
        self.label_p_select.destroy()
        self.label_p_kousa.destroy()
        self.label_p_mut.destroy()
        self.txt_numGene.destroy()
        self.txt_G_fin.destroy()
        self.txt_p_select.destroy()
        self.txt_p_kousa.destroy()
        self.txt_p_mut.destroy()
        self.txt_get_button.destroy()

    
    def edc(self): #送信が押されたら起動する関数
        self.citylist_len = len(self.citylist_x)
        if(self.citylist_len > 0):
            self.NUM_CITY = int(self.citylist_len)
            self.City = [[0 for j in range(2)] for i in range(self.NUM_CITY)]
            self.Kyori_city = [[0 for j in range(self.NUM_CITY)] for i in range(self.NUM_CITY)]
            for i in range(0, self.NUM_CITY):
                self.City[i][0] = self.citylist_x[i]/(self.canvas_width-12)
                self.City[i][1] = self.citylist_y[i]/(self.canvas_height-12)
            self.get_kyori_city()


        self.NUM_GENE = int(self.txt_numGene.get())
        self.G_fin = int(self.txt_G_fin.get())
        self.p_select = float(self.txt_p_select.get())
        self.p_kousa = float(self.txt_p_kousa.get())
        self.p_mut = float(self.txt_p_mut.get())

        self.Gene = [[0 for j in range(self.NUM_CITY)] for i in range(self.NUM_GENE)]
        self.G_disp_GA = 10 #出力制御
        self.record_length = math.ceil(self.G_fin/self.G_disp_GA)
        self.genelist = [[0 for j in range(self.NUM_CITY)] for i in range(self.record_length)]
        self.recordlist = [0 for j in range(self.record_length)]
        self.last_record = 0.0
        self.last_gene = []

        self.main_GA()

        self.record = tkinter.StringVar()
        self.label_record = tkinter.ttk.Label(self, textvariable=self.record)
        self.label_record.grid(row=14, column=0)

        self.loop(0)
    
    def loop(self, i):
        self.test_canvas.delete("line")
        self.draw_line(self.genelist[i])
        self.record.set(f'{(i+1)*10}世代目  総距離:{self.recordlist[i]}')
        if(i < self.record_length - 1):
            self.after(300, self.loop, i+1)
        else:
            return

    def draw_line(self, city_list):
        for i in range(0, self.NUM_CITY):
            sx = int(self.City[city_list[i]][0]*(self.canvas_width-12)+6)
            sy = int(self.City[city_list[i]][1]*(self.canvas_width-12)+6)
            if(i==self.NUM_CITY-1):
                ex = int(self.City[city_list[0]][0]*(self.canvas_width-12)+6)
                ey = int(self.City[city_list[0]][1]*(self.canvas_width-12)+6)
            else:
                ex = int(self.City[city_list[i+1]][0]*(self.canvas_width-12)+6)
                ey = int(self.City[city_list[i+1]][1]*(self.canvas_width-12)+6)

            self.test_canvas.create_line(sx, sy, ex, ey, tag="line")



#####画像配置#####
    def create_menu(self):
        # メニューバーの作成
        menubar = tkinter.Menu(self)

        # ファイル
        menu_file = tkinter.Menu(menubar, tearoff = False)
        menu_file.add_command(label = "画像ファイルを開く", command = self.menu_file_open_click, accelerator="Ctrl+O")
        menu_file.add_separator() # 仕切り線
        menu_file.add_command(label = "終了", command = self.master.destroy)
        # ショートカットキーの関連付け
        menu_file.bind_all("<Control-o>", self.menu_file_open_click)

        # メニューバーに各メニューを追加
        menubar.add_cascade(label="ファイル", menu = menu_file)

        # 親ウィンドウのメニューに、作成したメニューバーを設定
        self.master.config(menu = menubar)

    def menu_file_open_click(self, event=None):
        filename = filedialog.askopenfilename(
            title = "ファイルを開く",
            filetypes = [("Image file", ".bmp .png .jpg .tif"), ("Bitmap", ".bmp"), ("PNG", ".png"), ("JPEG", ".jpg"), ("Tiff", ".tif") ], # ファイルフィルタ
            initialdir = "./" # 自分自身のディレクトリ
            )
        # 画像の表示
        self.disp_image(filename)

    def disp_image(self, filename):
        '''画像をCanvasに表示する'''
        if not filename:
            return
        # PIL.Imageで開く
        pil_image = Image.open(filename)

        # キャンバスのサイズを取得
        canvas_width = self.test_canvas.winfo_width()
        canvas_height = self.test_canvas.winfo_height()

        # 画像のアスペクト比（縦横比）を崩さずに指定したサイズ（キャンバスのサイズ）全体に画像をリサイズする
        pil_image = ImageOps.pad(pil_image, (canvas_width, canvas_height), color = self.back_color)

        #PIL.ImageからPhotoImageへ変換する
        self.photo_image = ImageTk.PhotoImage(image=pil_image)

        # 画像の描画
        
        self.test_canvas.tag_lower(
            self.test_canvas.create_image(
                canvas_width / 2,       # 画像表示位置(Canvasの中心)
                canvas_height / 2,                   
                image=self.photo_image  # 表示画像データ
            )
        )



    #######edc#############

    def mk_city(self):
        for i in range(0, self.NUM_CITY):
            self.City[i][0] = random.random()
            self.City[i][1] = random.random()
        self.get_kyori_city()

    def get_kyori_city(self):
        for i in range(0, self.NUM_CITY):    
            for j in range(0, self.NUM_CITY):
                if(i != j):
                    wk1 = self.City[i][0] - self.City[j][0]
                    wk2 = self.City[i][1] - self.City[j][1]
                    self.Kyori_city[i][j] = math.sqrt(wk1 * wk1 + wk2 * wk2)

    def main_GA(self):
        self.init_gene()

        n = 0
        for g in range(0, self.G_fin):
            self.sort_gene()

            if(g%self.G_disp_GA == 0):
                self.recordlist[n] = round(self.kyori_gene(0), 3)
                self.genelist[n] = copy.copy(self.Gene[0])
                n+=1

            self.select_gene_zyoui()
            self.kousa_gene_zyoui()
            self.mutate_gene()
        self.sort_gene()
        record = self.kyori_gene(0)
        # print("ittyanhayai")
        # print(record)

    def init_gene(self): #Geneの並び順の初期化
        for i in range(0, self.NUM_GENE):
            self.Gene[i] = self.rand_ints_nodup(0, self.NUM_CITY-1, self.NUM_CITY)

    def rand_ints_nodup(self, a, b, k): #a~b,要素数kの重複無し乱数リスト
        ns = []
        while len(ns) < k:
            n = random.randint(a, b)
            if not n in ns:
                ns.append(n)
        return ns

    def sort_gene(self):
        kyori = []
        temp = []
        for i in range(0, self.NUM_GENE):
            kyori.append(self.kyori_gene(i)) 
        for i in range(0, self.NUM_GENE - 1):
            for j in range(i+1, self.NUM_GENE):
                if(kyori[i] > kyori[j]):
                    temp = copy.copy(self.Gene[i])
                    self.Gene[i] = copy.copy(self.Gene[j])
                    self.Gene[j] = copy.copy(temp)

                    kyori[i], kyori[j] = kyori[j], kyori[i]
        
    def kyori_gene(self, i):
        sum = 0
        n1 = 0
        n2 = 0
        for j in range(0, self.NUM_CITY):
            n1 = self.Gene[i][j]
            if (j != self.NUM_CITY - 1):
                n2 = self.Gene[i][j+1]
            else:
                n2 = self.Gene[i][0]
            sum += self.Kyori_city[n1][n2]
        return sum

    def select_gene_zyoui(self): # 上位(self.p_select * 100)%を選択
        Num_select = int(self.NUM_GENE * self.p_select)
        wk1 = math.ceil(self.NUM_GENE / self.p_select)
        for i in range(1, wk1):
            for j in range(0, Num_select):
                wk2 = Num_select*i + j
                if(wk2 == self.NUM_GENE - 1):
                    return
                self.Gene[wk2] = copy.copy(self.Gene[j])


    def kousa_gene_zyoui(self): # 上位(n*100)%を交叉
        Num_kousa = int(self.NUM_GENE * self.p_kousa)
        for i in range(0, Num_kousa):
            self.cross_cycle(i, i+1)
            i += 1

    def cross_cycle(self, i, j):
        mask = 0
        start = self.Gene[i][mask]
        wk1 = mask  
        while(start != self.Gene[j][wk1]):
            for l in range(0, self.NUM_CITY):
                if(self.Gene[j][wk1] == self.Gene[i][l]):
                    self.Gene[i][wk1],self.Gene[j][wk1] = self.Gene[j][wk1],self.Gene[i][wk1]
                    wk1 = l
                    break
        self.Gene[i][wk1],self.Gene[j][wk1] = self.Gene[j][wk1],self.Gene[i][wk1]

    def mutate_gene(self): # pの確率で変異
        for i in range(0, self.NUM_GENE):
            if(self.P_select(self.p_mut)):
                randam_no = random.randint(0, self.NUM_CITY-1)
                randam_ge = random.randint(0, self.NUM_CITY-1)
                for j in range(0, self.NUM_CITY):
                    if(self.Gene[i][j] == randam_ge):
                        self.Gene[i][randam_no], self.Gene[i][j] = self.Gene[i][j], self.Gene[i][randam_no]
                        break

    def P_select(self, epsilon):
        if(epsilon > random.random()):
            return True
        else:
            return False

root = tkinter.Tk()
app = Application(master=root)
app.mainloop()