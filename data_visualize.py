import pandas as pd
from sklearn.preprocessing import LabelEncoder,StandardScaler,MinMaxScaler,PowerTransformer
import matplotlib.pyplot as plt


class data_:

    def read_file(self,filepath):                                      # 파일 읽는 함수
        if str(filepath) ==  '':
            return ""
        else:
            return pd.read_csv(str(filepath) , index_col=False)
    
    def get_column_list(self, df):                                    # 파일에서 컬럼값들만 받는 함수
        #columnname_list=[]
        # for i in df.columns:
        #     columnname_list.append(i)
        return list(df.columns)
    
    def get_cat(self,df):                                              # object컬럼들을 받기
        cat_col=[x for x in df.columns if df[x].dtype=='object']
        # cat_col = []
        # for i in df.columns:
        #     if (df[i].dtype == 'object'):
        #         cat_col.append(i)
        return cat_col
    
    def convert_category(self, df, column_name):                       # 라벨 인코딩으로 숫자형으로 바꿔주는 함수
        le= LabelEncoder()
        df[column_name]=le.fit_transform(df[column_name])
        return df[column_name]

    def drop_columns(self,df,column_name):                             # 컬럼을 삭제하는 함수
        return df.drop(column_name,axis=1)
    
    def get_empty_list(self,df):
        empty_list = [x for x in df.columns if df[x].isnull().values.any()]
        return empty_list
    
    def fillmean(self, df, column_name):
        df[column_name].fillna(df[column_name].mean(),inplace = True)
        return df[column_name]
    
    def fillnan(self, df, column_name):
        df[column_name].fillna("Unknown",inplace = True)
        return df[column_name]
    
    def StandardScaler(self,df,target_name):
        mc=StandardScaler()
        x= df.drop(target_name,axis=1)
        scaled_features = mc.fit_transform(x)
        scaled_features_df = pd.DataFrame(scaled_features, index=x.index,columns=x.columns)
        scaled_features_df[target_name]=df[target_name]

        return scaled_features_df
    
    def MinMaxScaler(self,df,target_name):
        sc=MinMaxScaler()
        x= df.drop(target_name,axis=1)
        scaled_features = sc.fit_transform(x)
        scaled_features_df = pd.DataFrame(scaled_features, index=x.index,columns=x.columns)
        scaled_features_df[target_name]=df[target_name]

        return scaled_features_df
    
    def PowerScaler(self,df,target_name):
        pc=PowerTransformer()
        x= df.drop(target_name,axis=1)
        scaled_features = pc.fit_transform(x)
        scaled_features_df = pd.DataFrame(scaled_features, index=x.index,columns=x.columns)
        scaled_features_df[target_name]=df[target_name]

        return scaled_features_df


    def scatter_graph(self,df,x,y,c,marker):
        plt.figure()
        plt.scatter(df[x],df[y],c=c,marker=marker)
        plt.xlabel(x)
        plt.xlabel(y)
        plt.title(f'{y} vs {x}')
        plt.show()

    def line_graph(self,df,x,y,c,marker):
        plt.figure()
        df=df.sort_values(by=[x])
        plt.plot(df[x],df[y],c=c,marker=marker)
        plt.xlabel(x)
        plt.xlabel(y)
        plt.title(f'{y} vs {x}')
        plt.show()
