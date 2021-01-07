
import re 
import pandas as pd 

class Order_Lines(object):
    
    def __init__(self, url = []):
        self.url = url
    
#dosya yükleme 
     
    def add_url(self,address):
        self.url.append(address)        
    
    #stırları bulma 

    def file_upload(self):
        url = self.url[0]
        df = open(url, "r")
        lines = df.readlines()
        self.lines = lines
        df.close()
        return lines
        
    #AI AO DI DO içeren satırları bul
    def find_index(self):
        lines = self.lines
        index = []
        i = 0
        for line in lines:
            sonuc = re.search("[AD]+[IO]+[0-9]+x+",line)   
            if sonuc:
                index.append(i)
            i = i+1
        self.index = index
        return self.index

    def index_symbol(self):
        
        index = self.index
        lines = self.lines
        #AI AO DI DO ile başyalan satırlardan sonraki SYMBOLLERİ bul 
        index_symbol_list = []
        for m in range(len(index)):
            k = 0
            if m<len(index)-1:
                for line in lines[index[m]:index[m+1]]:       
                    symbol = re.search('SYMBOL',line)     
                    if symbol:
                        index_symbol_list.append(index[m]+k)
                    k = k+1
                    
            if m>len(index)-2:
                for line2 in lines[index[m]:]:
                    symbol = re.search('SYMBOL',line2) 
                    if symbol:
                        index_symbol_list.append(index[m]+k)
                    k = k+1
        self.index_symbol_list = index_symbol_list       
        return self.index_symbol_list

    def find_sjb(self):
        lines = self.lines          	
        #sjb İÇEREN SATIRLARI ARIYORUZ 
        
        index_sjb = list()
        i = 0
        for line in lines: 
            sonuc_sjb = re.search("-SJB-", line)
            if sonuc_sjb:
                index_sjb.append(i)
            i = i+1
        sjb_list = list()
        
        for i in range(len(index_sjb)):
            line_number = index_sjb[i]
            sjb_list.append(lines[line_number]) 
            
            #sjb için ayrı dataframe 
            df_sjb = pd.DataFrame(data = sjb_list, columns = [0])
            df_sjb = df_sjb[0].str.split(',', expand = True)
            df_sjb = df_sjb.rename(columns = {0 : 'DPSUBSYSTEM',
                                      1 : 'DPADDRESS',
                                      3 : 'SJB'})
            
            df_sjb = df_sjb.drop(columns = 2)
            df_sjb['DPSUBSYSTEM'] = df_sjb['DPSUBSYSTEM'].str.replace(r'\D', '')
            df_sjb['DPADDRESS'] = df_sjb['DPADDRESS'].str.replace(r'\D', '')
            df_sjb['SJB'] = df_sjb['SJB'].str.replace(r'"', '')
            df_sjb['SJB'] = df_sjb['SJB'].str[9:]
            df_sjb['SJB'] = df_sjb['SJB'].str.replace(r'\D', '')
            self.df_sjb = df_sjb
        return self.df_sjb

    def find_cpu(self):
        lines = self.lines
        #cpu hangi numaraya sahip 
        index_cpu = list()
        i = 0
        for line in lines: 
            sonuc = re.search("CPU_NO", line)
            if sonuc:
                index_cpu.append(i)
            i = i+1
        
        #cpu slot numarası belirleme
        cpu_text = lines[index_cpu[0]]
        cpu_text = cpu_text.replace(r'"', ' ')
        cpu_text = cpu_text.replace(r' ', '')
        cpu_text = cpu_text.replace(r'_', '')
        cpu_text = cpu_text[5]
        self.cpu_text = cpu_text
        return self.cpu_text


    #DATAFRAME için listeleri hazırıyoruz 
    def prepare_lists(self):
        index_symbol_list = self.index_symbol_list
        index = self.index 
        lines = self.lines
        
        birinci_list = []
        ikinci_list = []
    
        symbols = index_symbol_list.copy()
        for i in range(len(index)-1):
            
            for p in range(index[i+1]-index[i]):
                
                if len(symbols) > 0:
                   
                    if (symbols[1] - symbols[0]) == 1:               
                        value1 = symbols[0]
                        birinci_list.append(lines[index[i]])
                        ikinci_list.append(lines[value1])
                        symbols.remove(value1)
                    if len(symbols) > 1:
                        if (symbols[1] - symbols[0])>1:                       
                            value2= symbols[0]
                            birinci_list.append(lines[index[i]])           
                            ikinci_list.append(lines[value2])
                            symbols.remove(value2)
                            break
                    if len(symbols) == 1:
                            value2= symbols[0]
                            birinci_list.append(lines[index[i]])
                            ikinci_list.append(lines[value2])
                            symbols.remove(value2)
        self.birinci_list = birinci_list
        self.ikinci_list = ikinci_list                    
        return self.birinci_list, self.ikinci_list 
    
    def prepare_dfs(self,birinci_list,ikinci_list, df_sjb, cpu_text):
             
        #listeleri df haline getir         
        df = pd.DataFrame(columns = ['birinci','ikinci'])
        df['birinci'] = birinci_list
        df['ikinci'] = ikinci_list

        '''DF BİRİNCİ'''
        #birinci listeden gelen verileri virgül ile böl ve yeni kolonlor oluştur 
        df_birinci = df.iloc[:,0].str.split(',',expand = True)
    
        #kolon isimlerini değiştir
        df_birinci = df_birinci.rename(columns={0: 'DPSUBSYSTEM', 
                                            1: 'DPADDRESS',
                                            2: 'SLOT',
                                            3:'ORDER',
                                            4:'gizle1'})
    
        #kolonları temizle 
        #strinleri al götür 
        df_birinci['DPSUBSYSTEM'] = df_birinci['DPSUBSYSTEM'].str.replace(r'\D', '')
        df_birinci['DPADDRESS'] = df_birinci['DPADDRESS'].str.replace(r'\D', '')
        df_birinci['SLOT'] = df_birinci['SLOT'].str.replace(r'\D', '')
        
        #tırnak işaretlerini temizle
        df_birinci['ORDER'] = df_birinci['ORDER'].str.replace('"', '')
        
        '''DF İKİNCİ'''
        #ikinci listeden gelen verileri virgül ile böl ve yeni kolonlor oluştur 
        df_ikinci = df.iloc[:,1].str.split(',',expand = True)
        
        #kolon isimlerini değiştir
        df_ikinci = df_ikinci.rename(columns={0: 'gizle', 
                                                1: 'CHANNEL',
                                                2: 'SYMBOL',
                                                3:'DESCRIPTION'})
    
        #kolonları temizle  
        
        #tırnak işaretlerini temizle
        df_ikinci['SYMBOL'] =df_ikinci['SYMBOL'].str.replace('"', '')
        df_ikinci['DESCRIPTION'] = df_ikinci['DESCRIPTION'].str.replace('"', '')
    
        #iki dataframe i birleştir. 
        seperated = [df_birinci, df_ikinci]
        df_seperated = pd.concat(seperated, axis =1,sort = False)
    
        #excele kaydet 
        #df_seperated.to_excel('mehmet_sütün_kontrol_1.xls')
        df_seperated = df_seperated.drop(columns = ['gizle', 'gizle1'])
    
    
        #sjb değerlerini ana dataframe e ekle 
        sjb_final = list()
        for i in range(len(df_sjb)):
            for k in range(len(df_seperated)):
                if df_seperated['DPSUBSYSTEM'][k] == df_sjb['DPSUBSYSTEM'][i] and df_seperated['DPADDRESS'][k] == df_sjb['DPADDRESS'][i]:
                    sjb_final.append(df_sjb['SJB'][i])
                    
        df_seperated['SJB'] = sjb_final
        df_seperated = df_seperated.drop(columns = ['DPSUBSYSTEM'])
    
        #slot numarasını df_seperated a ekliyoruz
        cpu_to_list = list()
        
        for i in range(len(df_seperated)):
            cpu_to_list.append(cpu_text)
        
        df_seperated['CPU'] =  cpu_to_list
        
    
        area = list()
        lit_func = list()
        num = list()
        i_o = list()
        for i in range(len(df_seperated)):
            sliced_area = df_seperated['SYMBOL'][i][4:7]
            sliced_lit = df_seperated['SYMBOL'][i][7:10]
            sliced_num = df_seperated['SYMBOL'][i][10:]
            sliced_io = df_seperated['SYMBOL'][i][1:3]
            area.append(sliced_area)
            lit_func.append(sliced_lit)
            num.append(sliced_num)
            i_o.append(sliced_io)
        
        df_seperated['AREA'] = area
        df_seperated['LIT_FUNC'] = lit_func
        df_seperated['NUM'] = num
        df_seperated['I_O'] = i_o
        
        df_seperated['NUM'] = df_seperated['NUM'].str.replace(r'\D', '')
        self.df_seperated = df_seperated
        return self.df_seperated
    
    def preapre_index(self, df_seperated):
    #index oluşturuyoruz
    
    
        index_columns = ["PLCRackSlotCh","TagNum","I_O","Ord","Area","Func","Num","Suffix","ProcEqDesc",
        	"ProcEqNum","ProcRel","Description","FunctionalDescript","PIDNo","PLC","Rack","Slot","Channel",
            "POrder","ReqNo","Instrument Type","Power Supply","Process Operate Range","Instrument Range","Unit","FailMode",
            "Size","ProcessMaterial","Line Material","ProcessConnection","LineNum","Manufacturer","Model","Setpoint",
            "Calibration","Datasheet","Hookup","OtherDocs","Software Tag","Softw Tag 2","IO Tag","Notes","DI DB's",
            "Valve Check","Rev","Pair number","JB number","JB Terminal/wire number","Instrument Terminal Number","Connected",
        	"Connected date","Commissioned","Commission date","Site Notes","Range","Unit.1","LoLo","Lo","Hi",
            "HiHi","Control Lo","Control Hi"]
    
        df_final = pd.DataFrame(columns = index_columns)
        df_final = df_final.fillna(" ")
        #kolon yerleştirme 
        df_final['Model'] = df_seperated['ORDER']
        df_final['ProcEqDesc'] = df_seperated['DESCRIPTION']
        df_final['Channel'] = df_seperated['CHANNEL']
        df_final['Slot'] = df_seperated['SLOT']
        df_final['Rack'] = df_seperated['SJB']
        df_final['PLC'] = df_seperated['CPU']
        df_final['I_O'] = df_seperated['I_O']
        df_final['Num'] = df_seperated['NUM']
        df_final['Func'] = df_seperated['LIT_FUNC']
        df_final['Area'] = df_seperated['AREA']
        
        df_final['PLCRackSlotCh'] = df_final["PLC"] +"-"+ df_final["Rack"] + "-" + df_final["Slot"] + "-" + df_final["Channel"]
        df_final['TagNum'] = df_final["Area"] +"-"+ df_final["Func"] + "-" + df_final["Num"] + df_final["Suffix"]
        df_final['FunctionalDescript'] = df_final["ProcEqDesc"] +"-"+ df_final["ProcEqNum"] + "-" + df_final["ProcRel"] + df_final["Description"]
        
        df_final.to_excel("mehmet_index_2020.xls")















