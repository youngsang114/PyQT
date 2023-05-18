from PyQt5.QtWidgets import *
import sys,pickle

from PyQt5 import uic, QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QWidget
import data_visualize, table_display
import Linear_Regression,SVM,Random_Forest,Logistic_Regression,Multi_Layer_Perceptron

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("./mainwindow.ui",self)

        global data
        data=data_visualize.data_()
        self.show()
        self.target_value=''

        self.Browse = self.findChild(QPushButton,"Browse")     # 등록하는 방법 self.findChild(객체,'이름')
        self.column_list = self.findChild(QListWidget,'column_list')
        self.Submit_btn = self.findChild(QPushButton,"Submit")
        self.target_col = self.findChild(QLabel,"target_col")
        self.table = self.findChild(QTableView,"tableView")
        self.data_shape = self.findChild(QLabel,"shape")
        self.Nontarget_alarm = self.findChild(QLabel,"Nontarget_alarm")

        self.scaler = self.findChild(QComboBox,"scaler")
        self.scale_btn = self.findChild(QPushButton,"scale_btn")

        self.cat_column = self.findChild(QComboBox,"cat_column")
        self.convert_btn = self.findChild(QPushButton,"convert_btn")

        self.drop_column = self.findChild(QComboBox,"drop_column")
        self.drop_btn = self.findChild(QPushButton,"drop_btn")

        self.empty_column = self.findChild(QComboBox,"empty_column")
        self.fillmean_btn = self.findChild(QPushButton,"fillmean_btn")
        self.fillna_btn = self.findChild(QPushButton,"fillna_btn")

        # model training ui
        self.model_select = self.findChild(QComboBox,"model_select")
        self.train = self.findChild(QPushButton,"train")
        
        # line plot
        self.plot_X = self.findChild(QComboBox,"plot_X")
        self.plot_y = self.findChild(QComboBox,"plot_y")
        self.plot_c = self.findChild(QComboBox,"plot_c")
        self.plot_marker = self.findChild(QComboBox,"plot_marker")
        self.lineplot = self.findChild(QPushButton,"lineplot")
        
        # sccater plot
        self.scatter_X = self.findChild(QComboBox,"scatter_X")
        self.scatter_y = self.findChild(QComboBox,"scatter_y")
        self.scatter_c = self.findChild(QComboBox,"scatter_c")
        self.scatter_marker = self.findChild(QComboBox,"scatter_marker")
        self.scatterplot = self.findChild(QPushButton,"scatterplot")

        #  hist


        self.Browse.clicked.connect(self.getCSV)              # clicked.connect(함수): 눌렀을때 어떤 행동을 할지
        self.Submit_btn.clicked.connect(self.set_target)
        self.column_list.clicked.connect(self.target)
        self.convert_btn.clicked.connect(self.convert_cat)
        self.drop_btn.clicked.connect(self.dropc)
        self.fillmean_btn.clicked.connect(self.fillme)
        self.fillna_btn.clicked.connect(self.fillna)
        self.scale_btn.clicked.connect(self.scale_value)
        self.scatterplot.clicked.connect(self.scatter_plot)
        self.lineplot.clicked.connect(self.line_plot)

        self.train.clicked.connect(self.train_func)

    def train_func(self):
        my_dict = {'Linear_Regression':Linear_Regression,
                   'SVM':SVM,
                   'Logistic_Regression':Logistic_Regression,
                   'Random_Forest':Random_Forest,
                   'Multi_Layer_Perceptron':Multi_Layer_Perceptron}
        
        if self.target_value !='':
            name=self.model_select.currentText()
            self.win=my_dict[name].UI(self.df, self.target_value)

    def line_plot(self):                                    # plot 함수
        x=self.plot_X.currentText()
        y=self.plot_y.currentText()
        c=self.plot_c.currentText()
        marker=self.plot_marker.currentText()
        data.line_graph(df=self.df, x=x,y=y,c=c,marker=marker)
        

    def scatter_plot(self):                                  # scatter 함수
        x=self.scatter_X.currentText()
        y=self.scatter_y.currentText()
        c=self.scatter_c.currentText()
        marker=self.scatter_marker.currentText()
        data.scatter_graph(df=self.df, x=x,y=y,c=c,marker=marker)


    def scale_value(self):
        if self.scaler.currentText() == 'StandardScaler':
            self.df = data.StandardScaler(self.df,self.target_value)
        elif self.scaler.currentText() == 'MinMaxScaler':
            self.df = data.MinMaxScaler(self.df,self.target_value)
        elif self.scaler.currentText() == 'PowerScaler':
            self.df = data.PowerScaler(self.df,self.target_value)
        self.filldetails()

    def fillna(self):
        name = self.empty_column.currentText()
        self.df[name]= data.fillnan(self.df,name)
        self.filldetails()


    def fillme(self):                                        # fillmean버튼 함수
        name = self.empty_column.currentText()
        self.df[name]= data.fillmean(self.df,name)
        self.filldetails()


    def dropc(self):
        name=self.drop_column.currentText()

        if self.target_value=='':
            self.Nontarget_alarm.setText('please submit!!!')  
        else:

            if (name==self.target_value):
                pass

            else:
                self.df= data.drop_columns(self.df,name)
                self.filldetails()

    def convert_cat(self):                                       # object형식의 콜럼을 숫자형으로 바꿔주는 함수
        name=self.cat_column.currentText()
        self.df[name] = data.convert_category(self.df,name)
        self.filldetails() 
    
    def set_target(self):
        self.Nontarget_alarm.setText('')                                     # 클릭한 콜럼의 값 (Submit)눌렀을때
        self.target_value = str(self.item).split()[0]
        print(self.target_value)
        self.target_col.setText(self.target_value)


    def target(self):                                         # 클릭한 콜럼의 값 ------- 형태 (browse)를 눌렀을때
        self.item = self.column_list.currentItem().text()
        print(self.item)    

    def getCSV(self):                                       
        self.filepath,_ = QFileDialog.getOpenFileName(self,"Open File","C:/Users/dgh06/OneDrive/문서/GitHub/machine-learning/datasets","csv(*.csv)")
        # print(self.filepath)
        self.column_list.clear()
        # self.column_list.addItems(["브라우져",'브라우승','브라질'])
        self.filldetails(0)
        self.Nontarget_alarm.setText('NonTarget')  

    def fill_combo_box(self):                                  # combo box 실행(데이트프레임 넣기, object를 float으로 바꾸기)

        self.cat_column.clear()
        self.cat_column.addItems(self.cat_col_list)
        self.drop_column.clear()
        self.drop_column.addItems(self.column_arr)

        self.empty_column.clear()
        self.empty_column.addItems(self.empty_column_name)

        self.scatter_X.clear()
        self.scatter_X.addItems(self.column_arr)
        self.scatter_y.clear()
        self.scatter_y.addItems(self.column_arr)
        
        self.plot_X.clear()
        self.plot_X.addItems(self.column_arr)
        self.plot_y.clear()
        self.plot_y.addItems(self.column_arr)



        x=table_display.DataFrameModel(self.df)                                   
        self.table.setModel(x)


    def filldetails(self , flag=1):                           
        
        if (flag==0):
            self.df = data.read_file(self.filepath)

        self.cat_col_list = data.get_cat(self.df)    
        self.column_list.clear()
        self.empty_column_name= data.get_empty_list(self.df)
        
        if len(self.df) ==0:
            pass
            
        else:
            self.column_arr = data.get_column_list(self.df)
            for i,j in enumerate(self.column_arr):
                    stri = f'{j} ------- {str(self.df[j].dtype)}' 
                    self.column_list.insertItem(i,stri)

        df_shape = f'rows:{self.df.shape[0]},columns:{self.df.shape[1]}'
        self.data_shape.setText(df_shape)

        
        self.fill_combo_box()


        



if __name__ == '__main__':        ## 파이썬에서 실행할때, 가장먼저 시키고 싶을때
    app=QApplication(sys.argv)
    window = UI()
    app.exec_()