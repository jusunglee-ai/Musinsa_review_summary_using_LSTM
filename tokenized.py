from nltk.tokenize import word_tokenize
from nltk.tokenize import WordPunctTokenizer
import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras.preprocessing.text import text_to_word_sequence
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import sent_tokenize
print('단어 토큰화1:',word_tokenize("Don't be foolded by the dark sounding name, Mr. Jone's Orphanage is as cheery as cheery goes for a pastry shop."))
print('단어 토큰화2:',WordPunctTokenizer().tokenize("Don't be foolded by the dark sounding name, Mr.Jone's Orphanage is as cheery as cheery goes for a pastry shop."))
print('단어 토큰화3:',text_to_word_sequence("Don't be foolded by the dark sounding name, Mr.Jone's Orphanage is as cheery as cheery goes for a pastry shop."))

tokenizer=TreebankWordTokenizer()
text="Starting a home-based restaurant may be an ideal. It doesn't have a food chain or restaurand of their own."
print('트리뱅크 워드토크나이저:',tokenizer.tokenize(text))

text = "His barber kept his word. But keeping such a huge secret to himself was driving him crazy. Finally, the barber went up a mountain and almost to the edge of a cliff. He dug a hole in the midst of some reeds. He looked about, to make sure no one was near."
print('문장 토큰화1:',sent_tokenize(text))

text="I am actively looking for Ph.D. students. and you are a Ph.D student"
print('문장 토큰화2:',sent_tokenize(text))

import kss
text='딥 러닝 자연어 처리가 재미있기는 합니다. 그런데 문제는 영어보다 한국어로 할 때 너무 어렵습니다. 이제 해보면 알걸요?'
print('한국어 문장 토큰화:',kss.split_sentences(text))

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
text="I am actively looking for Ph.D. students. and you are a Ph.D student."
tokenized_setence=word_tokenize(text)
print('단어 토큰화:',tokenized_setence)
print('품사 태깅:',pos_tag(tokenized_setence))

from konlpy.tag import Okt
from konlpy.tag import Kkma

okt=Okt()
kkma=Kkma()
print('OKT 형태소 분석:',okt.morphs("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))
print('OKT 품사 태깅:',okt.pos("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))
print('OKT 명사 추출:',okt.nouns("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))

print('KKMA 형태소 분석:',kkma.morphs("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))
print('KKMA 품사 태깅:',kkma.pos("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))
print('KKMA 명사 추출:',kkma.nouns("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))

import re
text = "I was wondering if anyone out there could enlighten me on this car."

# 길이가 1~2인 단어들을 정규 표현식을 이용하여 삭제
shortword = re.compile(r'\W*\b\w{1,2}\b')
print(shortword.sub('', text))

from nltk.stem import WordNetLemmatizer

lemmatizer=WordNetLemmatizer()
words=['policy','doing','organization','have', 'going', 'love', 'lives', 'fly', 'dies', 'watched', 'has', 'starting']
print('표제어 추출 전:',words)
print('표제어 추출 후:',[lemmatizer.lemmatize(word) for word in words])

lemmatizer.lemmatize('dies','v')
lemmatizer.lemmatize('watched','v')
lemmatizer.lemmatize('has','v')

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

stemmer=PorterStemmer()

sentence="This was not the map we found in Billy Bones's chest, but an accurate copy, complete in all things--names and heights and soundings--with the single exception of the red crosses and the written notes."
tokenized_setence=word_tokenize(sentence)
print('어간 추출 전:', tokenized_setence)
print('어간 추출 후:',[stemmer.stem(word) for word in tokenized_setence])

words=['formalize','allowance','electricial']
print('어간 추출 전:',words)
print('어간 추출 후:',[stemmer.stem(word)for word in words])

from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer

porter_stemmer=PorterStemmer()
lancaster_stemmer=LancasterStemmer()
words= ['policy', 'doing', 'organization', 'have', 'going', 'love', 'lives', 'fly', 'dies', 'watched', 'has', 'starting']

print('어간 추출 전:',words)
print('포터 스테머의 어간 추출 후:',[porter_stemmer.stem(w) for w in words])
print('랭커스터 스테머의 어간 추출 후:',[lancaster_stemmer.stem(w) for w in words])

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from konlpy.tag import Okt
stop_words_list = stopwords.words('english')
#영어로 된 불용어 단어리스트 단 nltk에서 정의한 불용어만
print('불용어 개수 :', len(stop_words_list))
print('불용어 10개 출력 :',stop_words_list[:10])

example = "Family is not an important thing. It's everything."
stop_words = set(stopwords.words('english')) 

word_tokens = word_tokenize(example)

result = []
for word in word_tokens: 
    if word not in stop_words: 
        result.append(word) 

print('불용어 제거 전 :',word_tokens) 
print('불용어 제거 후 :',result)

okt=Okt()
example = "고기를 아무렇게나 구우려고 하면 안 돼. 고기라고 다 같은 게 아니거든. 예컨대 삼겹살을 구울 때는 중요한 게 있지."
stop_words = "를 아무렇게나 구 우려 고 안 돼 같은 게 구울 때 는"

stop_words = set(stop_words.split(' '))
word_tokens = okt.morphs(example)

result = [word for word in word_tokens if not word in stop_words]

print('불용어 제거 전 :',word_tokens) 
print('불용어 제거 후 :',result)

import re

r=re.compile("a.c")
r.search("kkk")
r.search("abc")

r=re.compile("ab?c")
r.search("abbc")
r.search("ac")

r=re.compile("ab*c")
r.search("a")
r.search("abc")
r.search("abbbbc")

r=re.compile("ab+c")
r.search("ac")
r.search("abc")
r.search("abbbbc")

r=re.compile("^ab")
r.search("bbc")
r.search('zab')
r.search("abz")

r=re.compile("a{2,}bc")#==aabc와같으며 aaabc와도 같다 즉 앞에 a가 최소 2개이상 반복되는 글자와같다
r.search("bc")
r.search("aa")
r.search("aabc")
r.search("aaaaaaaaaaabc")


r=re.compile("[abc]")
r.search("zzz")
r.search("a")
 
r.search("baac")
r=re.compile("[a-z]")
r.search("AAA")
r.search("111")
r.search("aBC")

r=re.compile("[^abc]")
r.search("a")
r.search("ab")
r.search("b")
r.search("d")
r.search("1")

r=re.compile("ab.")
r.match("kkkabc")
r.search("kkkabc")
r.match("abckkk")

text="사과 딸기 수박 메론 바나나"
re.split(" ",text)

text="""사과
딸기
수박
메론
바나나"""
re.split("\n",text)

re.findall()
text="""이름: 김철수
전화번호 : 010 - 1234 -1234
나이 : 30
성별 : 남"""
re.findall("\d+",text)
re.findall("\d+","문자열입니다.")

text = "Regular expression : A regular expression, regex or regexp[1] (sometimes called a rational expression)[2][3] is, in theoretical computer science and formal language theory, a sequence of characters that define a search pattern."

preprocessed_text = re.sub('[^a-zA-Z]', ' ', text)
print(preprocessed_text)

text = """100 John    PROF
101 James   STUD
102 Mac   STUD"""
#re.split('문자열들을 구분할 기준',문자열이 저장되어있는 value)
#re.split()함수는 함수 내에 넣어둔 문자열들을 구분할 기준으로 value에 있는 텍스트들을 구분한다.

re.split('\s+', text)  
['100', 'John', 'PROF', '101', 'James', 'STUD', '102', 'Mac', 'STUD']

#re.findall('찾아내고 싶은 문자 형태',value)
#re.findall()함수는 함수에 넣어둔 찾고자 하는 문자형태를 value내에있는 text전체에서 찾아서 구분하여 리턴해준다.
re.findall('\d+',text)
#'\d+'는 숫자에 해당되는 정규표현식

re.findall('[A-Z]',text)
#[A-Z]는 대문자에 해당되는 정규표현식

re.findall('[A-Z]{4}',text)  
#{숫자}숫자 이상만큼 반복한다는 의미로 [A-Z]{4}는 대문자가 연속 4번이상 해당되는 정규표현식이다

from nltk.tokenize import RegexpTokenizer

text = "Don't be fooled by the dark sounding name, Mr. Jone's Orphanage is as cheery as cheery goes for a pastry shop"
tokenizer1=RegexpTokenizer("[\w]+")
#\w+ 문자 또는 숫자가 1개 이상인 경우를 의미함
tokenizer2=RegexpTokenizer("\s",gaps=True)
#\s는 공백을 나타내는 정규표현식
#gaps=True를 쓰지않으면 공백만 리턴을 해주기 때문에 공백을 기준으로 토큰화 시키고싶으면 무조건써야함
print(tokenizer1.tokenize(text))
print(tokenizer2.tokenize(text))

from nltk.tokenize import sent_tokenize
#영어 문장들을 토큰화 시켜주는 library
#토큰의 단위는 문장으로 한다.
from nltk.tokenize import word_tokenize
#단어를 기준으로 단어 단위로 나누는 library
from nltk.corpus import stopwords
#불용어 라이브럴리 
raw_text = "A barber is a person. a barber is good person. a barber is huge person. he Knew A Secret! The Secret He Kept is huge secret. Huge secret. His barber kept his word. a barber kept his word. His barber kept his secret. But keeping and keeping such a huge secret to himself was driving the barber crazy. the barber went up a huge mountain."
sentences=sent_tokenize(raw_text)
print(sentences)

vocab = {}#vocab이라는 value 생성 단 값은 초기화 힘
preprocessed_sentences = []#preprocessed_sentences라는 value 생성 단 값은 초기화 함
stop_words = set(stopwords.words('english'))#stop_words라는 value 생성 value에 영어 불용어 단어 객체들을 넣어줌
#set()->new empty set object
#set(iterable)->new set object
#set은 순서가 없으며 고유한 값을 가진다. 그리고 mutable(값이변하는)객체이다. 
for sentence in sentences:
    # 단어 토큰화
    tokenized_sentence = word_tokenize(sentence)#setence라는 value에 넣어있는 단어들을 토큰화 함
    result = []#result라는 value를 생성하되 초기화 함

    for word in tokenized_sentence: 
        word = word.lower() # 모든 단어를 소문자화하여 단어의 개수를 줄인다.
        #value.lower()하면 value에 있는 모든 단어들을 소문자화 한다.
        if word not in stop_words: # 단어 토큰화 된 결과에 대해서 불용어를 제거한다.
            if len(word) > 2: # 단어 길이가 2이하인 경우에 대하여 추가로 단어를 제거한다.
                result.append(word)#만약 단어길이가 2이상이면 result라는 리스트 value에 word에 있는 단어를 추가한다.
                if word not in vocab:
                #if A in B B안에 A가 있으면 true
        
                 #if A not in B B 안에 A가 없으면 true
                #if의 리턴 값이 true 아래의 명령어를 실행
                    vocab[word] = 0 #vocab이라는 딕셔너리의 word카테고리에 0을 대입
                vocab[word] += 1#vocab이라는 딕셔너리의 word 카테고리에 +1값을 추가함
    preprocessed_sentences.append(result) 
    #preprocessed_sentences리스트의 맨뒤 result값을 보냄
print(preprocessed_sentences)
#preprocessed_sentences의 리스트 들을 출력 

print('단어 집합:',vocab)
#단어의 빈도수들 출력

print(vocab["barber"])
#barber이라는 단어의 빈도수 출력

vocab_sorted=sorted(vocab.items(),key=lambda x:x[1], reverse= True)
print(vocab_sorted)

word_to_index={}
i=0
for (word,frequnecy) in vocab_sorted :
    if frequnecy > 1 :
        i=i+1
        word_to_index[word]=i
print(word_to_index)

vocab_size=5
words_frequency=[word for word, index in word_to_index.items() if index >= vocab_size + 1]
for w in words_frequency:
    del word_to_index[w]
print(word_to_index)

#불용어 제거
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords#불용어 패키지 불러오기
from nltk.tokenize import word_tokenize

input_sentence="We should all study hard for the exam."
stop_words=set(stopwords.words('english'))
#불용어 영어단어들을 배열에 저장
word_tokens=word_tokenize(input_sentence)
#우리가 input_sentence에 넣은 문장을 토큰화 하는 과정 근데 띄워쓰기 기준으로 토큰화를 진행함
result=[]#불용어가 아닌 단어들을 저장하는 배열
for w in word_tokens:#불용어 처리하는 과정
    #w변수값이 word_tokens라는 토큰화 된 단어끝까지 끝부분이 올때까지 반복
    #즉 토큰화된 단어 각각마다 비교를해서 전체를 진행
    if w not in stop_words:#만약 각 단어마다 불용어 목록에 없으면
        result.append(w)# w라는 배열리스트의 맨 뒤로 보냄
print(word_tokens)
print(result)

from nltk.stem import WordNetLemmatizer 
#WordNetLemmatizer는 표제어 추출을 사용할때 사용하는 라이브러리 이다

lemmatizer = WordNetLemmatizer()
#lemmatizer라는 변수에 표제어 추출 명령어를 삽입
words=['policy','doing','organization','have','going','love','lives','fly','dies','watched','has','starting']
print('표제어 추출 전:',words)

print('표제어 추출 후:',[lemmatizer.lemmatize(word) for word in words])
#표제어 추출 후에 has는 ha dies는 dy lives는 life로 변경 되었는데
#이렇게되면 이게 뭔 의미의 단어인지 모른다 그렇기 때문에 이 단어의 품사정보를 알아야 정확한 결과가나옴


#정수 인코딩
#dictionary 사용하기 
from nltk.tokenize import sent_tokenize
#Sentence Tokenization는 즉 문장 토큰화라고 의미한다.
#.와 같은 문장을 마치는 문장 끝 부분 콤마를 기준으로 문장을 토큰화한다.
from nltk.tokenize import word_tokenize
#Word Tokenization 단어 토큰화
#기본적으로 단어기준으로 토큰화를 하는 것을 의미하며 띄어쓰기 기준이 된다.
from nltk.corpus import stopwords
#불용어 라이브러리

raw_text="A barber is a person. a barber is good person. a barber is huge person. he Knew A Secret! The Secret He Kept is huge secret. Huge secret. His barber kept his word. a barber kept his word. His barber kept his secret. But keeping and keeping such a huge secret to himself was driving the barber crazy. the barber went up a huge mountain."
#토큰화할 문장을 raw_text라는 변수에 저장
sentences=sent_tokenize(raw_text)
#sentences라는 변수에 문장토큰화 한 값들을 저장
vocab={}
preprocessed_sentences=[]
stop_word=set(stopwords.words('english'))
#stop_word라는 변수에 불용어 단어들중에서 영어로된 단어들을 불러와서 집합으로 저장함
print(sentence)
for sentence in sentences:
    #단어 토큰화 하는 과정 
    tokenized_sentence=word_tokenize(sentence)
    #tokenized_sentece변수에 sentence라는 안에 있는 문장을 wordtokenization진행
    result=[]
    for word in tokenized_setence:
        word=word.lower()#모든 단어를 소문자화하여 단어의 개수를 줄인다.
        if word not in stop_words:#만약 단어들이 불용어 리스트에 있지않으면
            if len(word)>2:#만약 word의 단어길이가 2이상이면
                result.append(word)#word라는 배열 맨 뒤에 보낸다. 2이하면 보내지 않아서 단어길이가 2이하인것들은 다 지운다.
                if word not in vocab:#word리스트에 vocab이 없으면
                    vocab[word]=0#vocab딕셔너리에 해당 단어가 없으면 0처리
                vocab[word]+=1#해당 단어가 나오면 +1을 해줘서 해당 단어가 몇번 나왔는지 딕셔너리에 저장
            preprocessed_sentences.append(result)
print(preprocessed_sentences)

print('단어 집합:',vocab)
#단어 빈도수들을 저장해둔 vocab 딕셔너리 출력
print(vocab["barber"])
#barber 단어의 빈도수 출력
vocab_sorted=sorted(vocab.items(),key=lambda x:x[1],reverse= True)
print(vocab_sorted)
#단어 빈도수가 가장 높은 순서대로 정렬한다.
#sorted(정렬할 데이터 목록들,key 파라미터, reverse 파라미터)
#정렬할 데이터 목록들은 한마디로 내가 정렬하고 싶은데이터 목록들이다
#key 파라미터 같은 경우는 어떠한 기준으로 정렬할지 정하는 key 값이다. 대표적인 예시로 쇼핑몰의 가격,추천수,조회수 등등 이러한 어떠한 기준으로
#reverse같은경우는 올림차수로 정렬할거냐 내림차수로 정렬할거냐 인데 False면 올림 차순 True면 내림차순이다.

word_to_index={}
i=0
for (word, frequnecy)in vocab_sorted:
    if frequnecy>1:
        i=i+1
        word_to_index[word]=i
print(word_to_index)
    
vocab_size=5
words_frequency=[word for word, index in word_to_index.items() if index >= vocab_size+1]

from konlpy.tag import Okt
#Okt라는 한국어 전처리 패키지를 사용
okt=Okt()#konlpy 라이브러리에서 제공하는 'Okt'클래스의 인스턴스를 생성하는 코드
#따라서 okt=Okt()는 한국어 텍스트 데이터를 처리하기 위해 Okt 형태소 분석기 객체를 생성하는 코드다.
#이 클래스의 인스턴스를 생성한 후 ,'morphs()'라는 메소드를 사용하여 한국어 텍스트를 형태소 단위로 분리 할 수 있다.
def build_bag_of_words(document):
    #replace()라는 문법을 사용하여 document(문서)에서 마침표를 제거 한 뒤 제거한 document를 document에 덮어씀
    document=document.replace('.','')
    #okt.morphs(document)를 사용하여 document(문서)의 형태소를 분석하고 문장을 한국어 토큰화를 진행한다.
    tokenized_document=okt.morphs(document)
    #단어 인덱스와 Bag of words의 저장공간인 word_to_index,bow라는 변수를 초기화 한다.
    word_to_index={}
    bow=[]
    #토큰화된 문서에서 각 단어의 등장 횟수를 세어 Bag of Words를 만듭니다.
    for word in tokenized_document:
        if word not in word_to_index.keys():
            #만약에 단어가 등장한 적이 없는 경우, 단어 인덱스를 추가하고 새로운 단어의 등장 횟수를 1로 설정합니다.
            word_to_index[word]=len(word_to_index)
            #이전에 텍스트에 등장한 적이 없는 새 단어에 인덱스를 할당한다.
            #여기서 word_to_index는 텍스트의 각 고유 단어와 해당 인덱스 간의 매핑을 저장하는 python사전이다.

            bow.inser(len(word_to_index)-1,1)
            #새 단어에 대한 "bag-of-words"벡터에 새 항목을 추가한다. bow는 bag of words의 벡터를 나타내는 파이썬 목록이다.
        else:
            #단어가 이미 등장한 경우, 해당 단어의 인덱스를 찾아서 Bag of Words에서 해당 인덱스의 값을 1증가시킵니다.
            index=word_to_index.get(word)#해당 단어(word)의 인덱스를 찾아서 index 변수에 저장 
            bow[index]=bow[index]+1#bow[index]에 bow[index]+1 문을 통하여 기존 index값에 +1을 하여 저장
    return word_to_index,bow#토큰화 한 문장의 단어별 index값과 단어 출현 빈도 bow값을 리턴

doc1="정부가 발표하는 물가상승률과 소비자가 느끼는 물가상승률은 다르다."
vocab,bow=build_bag_of_words(doc1)#doc1을 bac of words화하여 문장을 토큰화하여 단어별로 번호 부여후 vocab에 저장 단어 빈도수 값을 bow에 저장 
print('vocabulary:',vocab )
print('bag of words vector:',bow)

doc2='소비자는 주로 소비하는 상품을 기준으로 물가 상승률을 느낀다.'
vocab,bow=build_bag_of_words(doc2)
print('vocabulary:',vocab)
print('bag of words vector',bow)


#doc1과 doc2를 합친 새로운 doc3문장을 만들어 토큰화 하고 index할당 뒤 bow값도 출력

doc3=doc1+' '+doc2
vocab,bow=build_bag_of_words(doc3)
print(doc3)
print('vocabulary:',vocab)
print('bag of words vector',bow)
from sklearn.feature_extraction.text import CountVectorizer

corpus=['you know I want your love. because I love you']
#영어 문장은 corpus변수에 저장
vector=CountVectorizer()
#CountVectorizer()라는 명령어는 사이킷 런에서 제공하는 툴이며
#이는 단어의 빈도를 count하여 vector로 만들어주는 클래스이다.

print('bag of words vector:',vector.fit_transform(corpus).toarray())
#코퍼스로부터 각 단어의 빈도수 기록
print('vocabulary:',vector.vocabulary_)
#각 단어의 인덱스가 어떻게 부여되었는지를 출력

