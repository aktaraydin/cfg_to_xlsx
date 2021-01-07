# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 13:36:56 2020

@author: aktar
"""

#imports 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (QWidget, QProgressBar,
                             QPushButton, QApplication,
                             QLineEdit,QLabel,QHBoxLayout,
                             QFormLayout,QFileDialog,
                             QMessageBox)
#imports transform codes 
from cfg_to_xls_preapring import Order_Lines
import sys

class OxpsToXls(QWidget):
    def __init__(self):
        super().__init__()
        self.setUI()
    
    def setUI(self):
        
        #Call file works 
        self.url_link = Order_Lines()
                  
        '''-----------------------------------------------'''
        
        '''Widgets inside Window'''
        
        #oxps to pdf side design 
        self.setWindowTitle('Mehmet Bayboğan İndex Exceli Oluşturma')  
        self.setGeometry(600, 250, 1000, 500)           
        define_label_1 = QLabel('<b>Dosya Yükleme</b>')
        define_label_1.setAlignment(Qt.AlignCenter)
    
        address_label = QLabel ('.cfg Uzantılı Dosya Konumu')
    
        self.browse_buttonAddress = QPushButton('Adresleri Yükle')
        self.browse_buttonAddress.clicked.connect(self.choose_address)
    
        self.line_editAddress = QLineEdit()
        self.line_editAddress.setReadOnly(True)
        
        self.address_status = QLabel(' ')
        self.address_status.setAlignment(Qt.AlignLeft)
    
        #convert  
        self.start_button = QPushButton('.cfg Dosyasınndan Index Oluştur')
        self.start_button.clicked.connect(self.start_transform)
        
        #butondan sonraki boşluk   
        ayrac = QLabel(' ')

        #compleated works notes part  
        finalStatus_label = QLabel('<b>Yapılan İşlemler</b>')
        finalStatus_label.setAlignment(Qt.AlignCenter)
                 
        self.start_label = QLabel()
        self.file_upload = QLabel()
        self.index_finded = QLabel()
        self.symbols_finded = QLabel()
        self.sjb_finded = QLabel()
        self.data_organized = QLabel()
        self.done = QLabel()
        
        #who developed 
        gelistiren = QLabel('<b>Aydın AKTAR Tarafından geliştirildi</b>')
        gelistiren.setAlignment(Qt.AlignBottom)
        gelistiren.setAlignment(Qt.AlignRight)
        e_posta = QLabel('<b>aktaraydin@gmail.com</b>')
        e_posta.setAlignment(Qt.AlignBottom)
        e_posta.setAlignment(Qt.AlignRight)

        '''design with hbox and form''' 
        
        #oxps to pdf part 
        h_boxAddress = QHBoxLayout()
        h_boxAddress.addWidget(self.line_editAddress)
        h_boxAddress.addWidget(self.browse_buttonAddress)
    
    
        form = QFormLayout()
        form.addRow(define_label_1)
     
        form.addRow(address_label)
        form.addRow(h_boxAddress)
        
        form.addRow(self.address_status)
    
        form.addRow(self.start_button)
        
        
        h_boxAddressPDF = QHBoxLayout() 
        
        form.addRow(ayrac)

        form.addRow(h_boxAddressPDF)
        
    
        form.setAlignment(Qt.AlignLeft)
        
        form.addRow(finalStatus_label)
        form.addRow(self.start_label)
        form.addRow(self.file_upload)
        form.addRow(self.index_finded)
        form.addRow(self.symbols_finded)
        form.addRow(self.sjb_finded)
        form.addRow(self.data_organized)
        form.addRow(self.done)
        
        form.addRow(gelistiren)
        form.addRow(e_posta)
    
    
        #assess form to window  
        self.setLayout(form)
    
        '''-----------------------------------------------'''
         
        self.show()
    
    def choose_address(self):
        fname_adres = QFileDialog.getOpenFileName(self,'Dosya Adı','c:','Adres Dosyası (*.cfg)')
        self.address_status.setText('Adresler Dosyası Yüklendi')
        self.line_editAddress.setText(fname_adres[0])
        self.url_link.add_url(fname_adres[0])
       
    def start_transform(self):
        start = Order_Lines()
        self.start_label.setText("Başladı")
        lines = start.file_upload()
        self.file_upload.setText("Dosya Yüklendi. Satırlara Ayrıldı")
        index = start.find_index()
        self.index_finded.setText("İndex numaraları bulundu")
        index_symbol = start.index_symbol()
        self.symbols_finded.setText("Sembol index numaraları bulundu")
        df_sjb = start.find_sjb()
        self.sjb_finded.setText("SJB adresleri bulundu")
        cpu_text = start.find_cpu()
        birinci_list, ikinci_list = start.prepare_lists()
        df_seperated = start.prepare_dfs(birinci_list, ikinci_list, df_sjb, cpu_text)
        self.data_organized.setText("Veriler tekrar bir araya getirildi")
        final_index = start.preapre_index(df_seperated)
        self.done.setText("Bitti")
        self.doneMessage()
        
    # def pdfTOxls_start(self):
    #     self.start_ok.setText('Çalışıyor')
    #     startPDF = File_works()       
    #     address_df = startPDF.addressTOdf()
    #     self.addressTOdf_ok.setText('Adress PDF Dosyası Veriye Dönüştürüldü')
    #     symbols_df = startPDF.symbolTOdf()
    #     self.symbolTOdf_ok.setText('Symbols PDF Dosyası Veriye Dönüştürüldü')
    #     occurIndex = OccurIndex()
    #     index = occurIndex.index(address_df['address_x'],
    #                              address_df['address_sjb'],
    #                              symbols_df)
    #     self.index_ok.setText('İndex Oluşturuldu')
    #     self.xls_doneMessage()
    
    def doneMessage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("<b>Tamamlanan İş</b>")
        msg.setInformativeText("İndex Dosyası Hazırlandı")
        msg.setWindowTitle("İş Bildirimi")
        msg.setDetailedText("İndex Dosyası Program ile aynı yere kaydedilir.")
        msg.setStandardButtons(QMessageBox.Ok)       
        retval = msg.exec_()       
                     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OxpsToXls()
    #çarpıya basınca programdan çık 
    sys.exit(app.exec())