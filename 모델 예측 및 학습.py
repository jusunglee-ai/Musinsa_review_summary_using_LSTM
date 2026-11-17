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
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from konlpy.tag import Okt
from konlpy.tag import Kkma
okt=Okt()
kkma=Kkma()
def setting_modeling(vocab_size,X_train,y_train,X_test,y_test):
   

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
    return history,loaded_model
#리뷰 예측

def sentiment_predict(new_sentence,max_len,stopwords,tokenizer):
    
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
        
        # 테스트 데이터로 예측 수행

def predict_sentences(real_tests,test_data,model,real_test0,real_test1,real_test2,real_test3,real_test4,real_test5):   
    predictions0 =model.predict(real_test0)
    predictions1 =model.predict(real_test1)
    predictions2 =model.predict(real_test2)
    predictions3 =model.predict(real_test3)
    predictions4 =model.predict(real_test4)
    predictions5 =model.predict(real_test5)

    predictions=[predictions0,predictions1,predictions2,predictions3,predictions4,predictions5]
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
        print() 
# 테스트 데이터로 예측 수행
    predictions = model.predict(test_data)
# 긍정 리뷰와 부정 리뷰 개수 초기화
    positive_count = 0
    negative_count = 0
# 예측 결과를 기반으로 긍정 리뷰와 부정 리뷰 개수 계산
    for prediction in predictions:
        if prediction > 0.5:  # 예측 확률이 0.5보다 크면 긍정 리뷰로 판단
            positive_count += 1
        else:  # 예측 확률이 0.5보다 작거나 같으면 부정 리뷰로 판단
            negative_count += 1
# 긍정 리뷰와 부정 리뷰 비율 계산
    total_count = len(predictions)
    positive_rate = positive_count / total_count 
    negative_rate = negative_count / total_count
# 결과 출력
    print("긍정 리뷰 비율:", positive_rate)
    print("부정 리뷰 비율:", negative_rate)    
    s=input(' ')
    sentiment_predict(s)
    return s