import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
from collections import Counter
from konlpy.tag import Mecab
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Embedding, Dense, GRU
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from konlpy.tag import Okt
from konlpy.tag import Kkma
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.preprocessing.sequence import pad_sequences
global okt
global kkma
global new_sentence
global stopwords
global max_len
global loded_model
global vocab_size
global negative_words
global positive_words
global predictions
global realtests
global realdata
okt=Okt()
kkma=Kkma()
max_len=80
vocab_size=None

realdata=[]
new_sentence=[]
stopwords=['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게']
negative_words=[]
positive_words=[]
realtests=[]
predictions=[]

def deep_learning():
    urllib.request.urlretrieve("https://raw.githubusercontent.com/bab2min/corpus/master/sentiment/naver_shopping.txt", filename="ratings_total.txt")
    total_data=pd.read_table('ratings_total.txt',names=['ratings','reviews'])
#total_data변수에 ratings_total.txt에 있는 ratings라는 이름과 reviews라는 이름에 해당되는
#데이터 테이블들을 read_table함수를 통해 읽어서 저장

# 사용자로부터 파일 경로 입력 받기
    filename = r"C:/Users/bjhan/OneDrive/바탕 화면/대학교 자료/딥러닝 스터디/텍스트 전처리/data2.xlsx"

# Excel 파일 읽기
    dataframe = pd.read_excel(filename)

# A열부터 F열까지의 데이터 가져오기
    realdata = dataframe.iloc[:, 0:6]  # 0부터 5까지의 열 인덱스 범위로 선택

    total_data['label']=np.select([total_data.ratings >3],[1],default=0)
    #np.select(condlist,choice,default=0)
    #condlist(부울 배열 시퀀스):이 매개변수는 요소별로 평가되는 조건 목록을 의미
    #즉 데이터 테이블에서 내가 선택할 해당목록 작성
    #defalut=는 보통 0으로 설정 condlist조건이 충족되지 않을때 사용되는 기본값 혹으 배열 지정
    total_data['ratings'].nunique(),total_data['reviews'].nunique(),total_data['label'].nunique()
    #total_data['데이터 프레임에서 찾고싶은 목록 값'].nunique()는
    #데이터 프레임에서 찾고싶은 리스트의 목록의 해당하는 개수를 제공한다
    #현재 ratings(별점)은 1,2,4,5만있음으로 4개
    #reviews는 중복제외 199908개,labes은 2개 20만개 리뷰중에서 중복이있다
    realdata[1].nunique(),realdata[0].nunique(),realdata[2].nunique(),realdata[3].nunique(),realdata[4].nunique(),realdata[5].nunique()
    total_data.drop_duplicates(subset=['reviews'],inplace=True)
    #'reviews'열을 기반으로 'total_data'의 데이터 프레임에서 중복행을 제거함
    #total_data=는 작업이 수행되는 데이터 프레임
    #drop_duplicates(subset=['중복행을 삭제할 열'],inplace=True ):중복행을 삭제해주는 함수 
    #inplcae=true는 매개변수 변경이'total_data'데이터 프레임에서 직접이루어져야하며
    #새 데이터 프레임을 반환하는 대신 제자리에서 수정함
    realdata.columns = realdata.columns.astype(str)
    realdata.loc[:, '0'].drop_duplicates(inplace=True)
    realdata.loc[:, '1'].drop_duplicates(inplace=True)
    realdata.loc[:, '2'].drop_duplicates(inplace=True)
    realdata.loc[:, '3'].drop_duplicates(inplace=True)
    realdata.loc[:, '4'].drop_duplicates(inplace=True)
    realdata.loc[:, '5'].drop_duplicates(inplace=True)
    print(total_data.isnull().values.any())
    #total_data 데이터 프레임에서 누락된 값이나 null있는지 확인하여 출력
    #isnull():동일한 모양의 boolean 데이터 프레임을 반환하는 데이터 프레임의 매서드이며
    #원본 데이터 프레임에서 null값이거나 누락된경우엔 true 그외엔 false
    #valus:numpy배열을 반환하는 boolean 데이터 프레임의 속성
    #any():배열의 요소가 true이면 true반환 그 외엔 false를 반환하는 numpy배열의 메서드
    train_data,test_data=train_test_split(total_data,test_size=0.25,random_state=42)
    #train_data와 test데이터를  분류함 test_size=0.25를 통해 test_data는 전체 비율의 25퍼센트로 설정
    #train_data는 전체 비율의 75퍼센트로 설정
    #random_state=42는 재현성을 위해 분할을 보장하기 위해 42로설정
    #즉 호출할 때마다 동일한 학습/테스트용 데이터 세트를 생성하기 위해 설정함
    train_data['label'].value_counts().plot(kind='bar')
    #train_data['label']:train_data 데이터 프레임에 접근해서 'label'열을 액세스함
    #value_counts():'label'열의 고유한 값을 세어 그 개수를 series로 반환하는 메서드
    #plot(kind='bar'):막대 그래프를 생성하는 series 객체의 매서드
    #kink매개변수는 플롯 유형을 지정하며 막대차트를 생성하기 위해'bar'로 설정
    print(train_data.groupby('label').size().reset_index(name='count'))
    #groupby('label'):label열을 기준으로 그룹화를 시켜주는 함수
    #size():그룹화시킨 데이터포인트의 개수
    #reset_index(name='count'):size를 통해 얻은 개수를 'count'라는 이름의 열로 결과를
    #데이터 프레임으로 출력
    total_data['label']=np.select([total_data.ratings >3],[1],default=0)
    #np.select(condlist,choice,default=0)
    #condlist(부울 배열 시퀀스):이 매개변수는 요소별로 평가되는 조건 목록을 의미
    #즉 데이터 테이블에서 내가 선택할 해당목록 작성
    #defalut=는 보통 0으로 설정 condlist조건이 충족되지 않을때 사용되는 기본값 혹으 배열 지정
    total_data[:5]
    total_data['ratings'].nunique(),total_data['reviews'].nunique(),total_data['label'].nunique()
    #total_data['데이터 프레임에서 찾고싶은 목록 값'].nunique()는
    #데이터 프레임에서 찾고싶은 리스트의 목록의 해당하는 개수를 제공한다
    #현재 ratings(별점)은 1,2,4,5만있음으로 4개
    #reviews는 중복제외 199908개,labes은 2개 20만개 리뷰중에서 중복이있다


    total_data.drop_duplicates(subset=['reviews'],inplace=True)
    train_data['reviews'] = train_data['reviews'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")

    train_data['reviews'].replace('',np.nan,inplace=True)
    realdata.loc[:, '0'] = realdata.loc[:, '0'].str.replace("[^ㄱ-ㅎ아-ㅣ가-힣 ]", "")
    realdata['0'].replace('', np.nan, inplace=True)
    realdata.loc[:, '1'] = realdata.loc[:, '0'].str.replace("[^ㄱ-ㅎ아-ㅣ가-힣 ]", "")
    realdata['1'].replace('', np.nan, inplace=True)
    realdata.loc[:, '2'] = realdata.loc[:, '0'].str.replace("[^ㄱ-ㅎ아-ㅣ가-힣 ]", "")
    realdata['2'].replace('', np.nan, inplace=True)
    realdata.loc[:, '3'] = realdata.loc[:, '0'].str.replace("[^ㄱ-ㅎ아-ㅣ가-힣 ]", "")
    realdata['3'].replace('', np.nan, inplace=True)
    realdata.loc[:, '4'] = realdata.loc[:, '0'].str.replace("[^ㄱ-ㅎ아-ㅣ가-힣 ]", "")
    realdata['4'].replace('', np.nan, inplace=True)
    realdata.loc[:, '5'] = realdata.loc[:, '0'].str.replace("[^ㄱ-ㅎ-ㅣ가-ㅎ ]", "")
    realdata['5'].replace('', np.nan, inplace=True)

    #train_data['reviews']리뷰열을 선택
    #replace('',np.nan,inplace=True):리뷰 열에 대한 매서드 호출
    #빈 문자열(즉 ' ')자리에 np.nan을 통해 빈 자리 대신 nan값으로 바꿔줌 
    #inplcae=True를 통해 수정은 내부에서 수행 즉 '리뷰'열이 직접 내부에서 업데이트됨
    print(train_data.isnull().sum())
    #sum():이는 데이터 프레임의 각 열에 대해 값들의 합계를 계산하는 데이터 프레임 매서드
    #즉 train_data 데이터 프레임의 각 요소가 null값인지 아니면 null값이 아닌지 나타내어 데이터 프레임을 
    #반환하는 isnull()함수를통해 반환 후 sum()함수를 통해서 null값을 계산하여 나타냄
    print(realdata.isnull().sum())
    test_data.drop_duplicates(subset=['reviews'],inplace=True)
    #test_data 데이터프레임의 'reviews'열의 중복 내용을 데이터프레임 내에서 직접 내부에서 제거 작업
    test_data['reviews']=test_data['reviews'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
    #정규표현식 수행
    #test_data 데이터 프레임의 'review'열을 선택 한 뒤
    #tr.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")한글이 아닌 문자, 공백 또는 특수문자를 모두 빈무자열로 변경

    test_data['reviews'].replace(' ',np.nan,inplace=True)
    #test_data 데이터프레임의 'reviews'열의 공백값은 NUll값으로 데이터 프레임 내부에서 작업
    #토큰화 하는 과정
    
    okt=Okt()
    kkma=Kkma()
    print(okt.morphs('와 이런 것도 상품이라고 차라리 내가 만드는 게 나을뻔'))
    
    train_data['tokenized']=train_data['reviews'].apply(okt.morphs)
    realdata['tokenized0']=realdata['0'].apply(okt.morphs)
    realdata['tokenized1']=realdata['1'].apply(okt.morphs)
    realdata['tokenized2']=realdata['2'].apply(okt.morphs)
    realdata['tokenized3']=realdata['3'].apply(okt.morphs)
    realdata['tokenized4']=realdata['4'].apply(okt.morphs)
    realdata['tokenized5']=realdata['5'].apply(okt.morphs)
    #train_data['tokenized']:이는 'tokenized'라는 새로운 열을 train_data 데이터 프레임에 생성
    #train_data['reviews'].apply(okt.morphs) train_data 데이터 프레임의 'reviews'열에 있는 문장들을
    #형태소 단위로 쪼개서 토큰화 하고 tokenized열에 저장 
    train_data['tokenized']=train_data['tokenized'].apply(lambda x:[item for item in x if item not in stopwords])
    realdata['tokenized0']=realdata['tokenized0'].apply(lambda x:[item for item in x if item not in stopwords])
    realdata['tokenized1']=realdata['tokenized1'].apply(lambda x:[item for item in x if item not in stopwords])
    realdata['tokenized2']=realdata['tokenized2'].apply(lambda x:[item for item in x if item not in stopwords])
    realdata['tokenized3']=realdata['tokenized3'].apply(lambda x:[item for item in x if item not in stopwords])
    realdata['tokenized4']=realdata['tokenized4'].apply(lambda x:[item for item in x if item not in stopwords])
    realdata['tokenized5']=realdata['tokenized5'].apply(lambda x:[item for item in x if item not in stopwords])
    #train_data 데이터 프레임의 'tokenized'열을 선택한후 
    #item for item in x:리스트 내부의 각 item에 대해 반복문을 실행
    #if item no in stopwords:item에 stopwords(불용어 없을 경우)가 없는 경우에만 해당 item을 유지
    #이렇게 리스트 내부의 모든 item마다 반복문을 실시하여 stopwords가 없는 토큰만 필터링하고 
    #필터링된 단어를 tokenized 열에 저장
    #결과적으로 tokenized 열의 각 토큰 리스트에서 stopwords에 해당하는 단어를 제거 후
    #필터링 된 토큰리스트를 tokenzied열에 저장
    test_data['tokenized']=test_data['reviews'].apply(okt.morphs)
    test_data['tokenized']=test_data['tokenized'].apply(lambda x:[item for item in x if item not in stopwords])
    negative_words = np.hstack(train_data[train_data.label == 0]['tokenized'].values)
    #train_data[train_data.label==0]:train_data 데이터 프레임에서 label열이 0인 행들을 선택
    #tokenized열에서 tokenized열의 값을 .values를 통해 numpy배열로 변환
    #np.hstack():numpy배열을 수평으로 결합하는 함수
    #train_data 데이터 프레임에서 label열이 0인 행들의 tokenized 열 값을 numpy배열로 가져온 뒤
    #수평으로 결합하여 하나의 numpy배열인 negetive_words에 저장하는 작업
    positive_words = np.hstack(train_data[train_data.label == 1]['tokenized'].values)
    #위와 똑같지만 label열에서 값이 1인 행들을 선택하여 tokenized열의 값을 가져와서 
    #똑같이 numpy배열로 가져온 뒤 수평으로 결합하고 numpy배열인 positive_words에 저장
    negative_words_count=Counter(negative_words)
    #negative_words에 있는 값들을 카운팅하여 negative_words_count에 저장
    positive_words_count=Counter(positive_words)
    #훈련용 및 테스트용 데이터 분류
    X_train=train_data['tokenized'].values
    y_train=train_data['label'].values
    X_test=test_data['tokenized'].values
    y_test=test_data['label'].values
        
    real_test0=realdata['tokenized0'].values
    real_test1=realdata['tokenized1'].values
    real_test2=realdata['tokenized2'].values
    real_test3=realdata['tokenized3'].values
    real_test4=realdata['tokenized4'].values
    real_test5=realdata['tokenized5'].values
    real_tests=[real_test0,real_test1,real_test2,real_test3,real_test4,real_test5]

    #사전에 분류해둔 test_data train_data 데이터 프레임을 이용하여 훈련용, 테스트용 데이터를 만듬
    #x_train=은 tokenized열의 값(column)값들 y_train=은 label열의 값(column값)들을 numpy배열로 가져와서 저장
    #정수인코딩
    tokenizer=Tokenizer()#토큰화 시키는 함수를 실행하는 변수
    tokenizer.fit_on_texts(X_train)
    #x_train데이터의 text들을 토큰화 함
    for i in range(6):
        tokenizer.fit_on_texts(real_tests[i])

    threshold=2
    total_cnt=len(tokenizer.word_index)#token화 된 단어의 개수를 저장
    rare_cnt=0#등장 빈도수가 threshold보다 작은 단어의 개수를 카운트하기 위한 값
    total_freq=0#훈련 데이터의 전체 단어 빈도수 총 합
    rare_freq=0#등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합 
    for key,value in tokenizer.word_counts.items():
        #word_counts는 딕셔너리 형태로 저장되어 있으며, 각 단어와 해당 단어의 빈도수가 저장되어있음
        #tokenizer.word_counts의 항목들을 하나씩 반복하여 key(단어)와 value(등장 빈도수)로 분류
        #즉 tokenzier.word_counts의 각 항목을 반복(iterate)하면서 각 단어와 해당 단어의 등장 빈도수를 key와 value로 
        #가져와서 아래 작업을 수행 
        total_freq=total_freq+value
        #총 등장 빈도수=총 등장 빈도수+해당 단어의 등장 빈도수하여 등장 단어를 누적하여 저장
        if(value<threshold):
            #만약 threshold보다 빈도수가 적을시 즉 2보다 적은 등장 빈도수가 1회인 단어
            rare_cnt=rare_cnt+1#희귀 단어 등장 횟수+1
            rare_freq=rare_freq+value#희귀 등장 빈도수+1

    #등장횟수가 1인 단어들의 비율은 55프로나 차지하지만
    #등장빈도에서는 2.65프로밖에 차지하지 않음으로 쓰레기 데이터 값으로취급
    #전체 단어 개수 중 빈도수 2이하인 단어 개수는 모두 제거.
    #0번 패딩 토큰과 1번 OOV 토큰을 고려하여 +2
    vocab_size=total_cnt-rare_cnt+2
    #전체등장 빈도-희귀 단어 빈도수 +2

    tokenizer=Tokenizer(vocab_size,oov_token='OOV')
    #Tokenizer 객체 생성
    #oov_token:Out-of-Vocabulary(단어 집합에 없는 단어)를 나타내는 토큰을 지정
    tokenizer.fit_on_texts(X_train)
    for i in range(6):
        tokenizer.fit_on_texts(real_tests[i])
   
    #Tokenizer객체에 텍스트 데이터인 X_train을 입력하여 단어 집합을 생성한 뒤 고유 정수 인덱스를 할당
    X_train=tokenizer.texts_to_sequences(X_train)
    for i in range(6):
        real_tests[i]=tokenizer.texts_to_sequences(real_tests[i])

    #X_train의 정수 인덱스가 할당된 텍스트 데이터를 정수 인덱스로 변환하는 작업
    #즉 단어들이 이제 각각의 정수 (1,2,3,4.5)로 단어 대신 정수(숫자)로 대체됨
    X_test=tokenizer.texts_to_sequences(X_test)
    #테스트데이터도 똑같이 작업진행
    max_len=80
   
    
    X_train=pad_sequences(X_train,maxlen=max_len)
    for i in range(6):
        real_tests[i]=pad_sequences(real_tests[i],maxlen=max_len)

    #X_train의 시퀀스 데이터를 패딩
    #시퀀스 데이터의 길이(문장의 길이)를 모두 동일하게 맞추기 위해 사용
    #maxlen=은 패딩 후 문장 길이
    #max_len 즉 문장 길이가 80보다 짧은 문장을 패딩함
    X_train=pad_sequences(X_train,maxlen=max_len)
    X_test=pad_sequences(X_test,maxlen=max_len)
    
    embedding_dim = 100
    hidden_units = 128

    model = Sequential()
    model.add(Embedding(vocab_size, embedding_dim))
    model.add(GRU(hidden_units))
    model.add(Dense(1, activation='sigmoid'))

    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
    mc = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)

    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
    history = model.fit(X_train, y_train, epochs=15, callbacks=[es, mc], batch_size=64, validation_split=0.2)
    loaded_model=load_model('best_model.h5')
    print("\n 테스트 정확도: %.4f"%(load_model.evaluate(X_test,y_test)[1]))
        # 테스트 데이터로 예측 수행
    for i in range(6):
        predictions[i]=model.predict(real_tests[i])


    # 초기화: 긍정 및 부정 리뷰 개수
    positive_count = []
    negative_count = []

    # 예측 결과를 기반으로 긍정 및 부정 리뷰 개수 계산
    for prediction in predictions:
        positive = sum(prediction > 0.5)  # 예측 확률이 0.5보다 크면 긍정으로 간주
        negative = sum(prediction <= 0.5)  # 예측 확률이 0.5보다 작거나 같으면 부정으로 간주
        positive_count.append(positive)
        negative_count.append(negative)

    # 전체 리뷰 개수
    total_count = len(predictions[0])

    # 긍정 및 부정 리뷰 비율 계산
    positive_rate = [count / total_count for count in positive_count]
    negative_rate = [count / total_count for count in negative_count]

    # 결과 출력
    for i in range(len(predictions)):
        print("Real Test Data", i)
        print("Positive review rate:", positive_rate[i])
        print("Negative review rate:", negative_rate[i])
    return positive_rate,negative_rate,loaded_model,vocab_size
    
positive_rate,negative_rate,loaded_model,vocab_size=deep_learning()


#리뷰 예측

def sentiment_predict(new_sentence,stopwords,max_len,okt,vocab_size):
    tokenizer=Tokenizer(vocab_size,oov_token='OOV')
    new_sentence=re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','',new_sentence)
    new_sentence=okt.morphs(new_sentence)
    new_sentence=[word for word in new_sentence if not word in stopwords]
    encoded=tokenizer.texts_to_sequences([new_sentence])
    pad_new = pad_sequences(encoded, maxlen=max_len)
    
    score=float(load_model.predict(pad_new))
    if(score>0.5):
        print("{:.2f}% 확률로 긍정 리뷰입니다.".format(score*100))
    else:
        print("{:.2f}% 확률로 부정 리뷰입니다.".format((1-score)*100))
    return score
 
score=sentiment_predict(new_sentence,stopwords,max_len,vocab_size)