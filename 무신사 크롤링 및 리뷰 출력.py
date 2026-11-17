#라이브러리/모듈 호출
from tkinter import *
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from PIL import ImageTk, Image
from io import BytesIO
import re

max_review = 300           #리뷰를 30페이지까지 인식
max_object = 6          #상품 갯수



#B리스트 안에 A값이 몇 번째 index에 있는지 출력해주는 함수
def index_(list_value,list):
    for index, list in enumerate(list):   
        if list_value == list:
            return index
           


#시작 페이지 설정
def start_window():
    global window
    window = Tk()
    window.title("무신사 상품#####")
    window.geometry("2000x3000")

    label_title = Label(window, text="무신사 상품#####")
    label_title.place(x=10, y=10)
    label_title.configure(font=50)

    label_search = Label(window, text="상품명:")
    label_search.place(x=300, y=20)
    
    global entry_search
    entry_search = Entry(window, width=25)
    entry_search.place(x=350, y=20)

    for i in range(int(max_object/3)):
        for j in range(3):
            label= Label(window, text="[" + str((j+1)+(i*3))  +"]")
            label.place(x=50+430*(j), y=180+300*(i))

            label= Label(window, text="[상품명]")
            label.place(x=50+430*(j), y=200+300*(i))

            label = Label(window, text="[가격]")
            label.place(x=50+430*(j), y=220+300*(i))

            label = Label(window, text="[리뷰 수]")
            label.place(x=50+430*(j), y=240+300*(i))

            label= Label(window, text="[평점]")
            label.place(x=50+430*(j), y=260+300*(i))

            label = Label(window, text="[Ai 리뷰]")
            label.place(x=50+430*(j), y=280+300*(i))


    global no_url
    no_url = "https://as2.ftcdn.net/v2/jpg/04/99/93/31/1000_F_499933117_ZAUBfv3P1HEOsZDrnkbNCt4jc3AodArl.jpg"

    # 이미지 다운로드
    response = requests.get(no_url)
    image_data = response.content

    # 이미지 열기
    image = Image.open(BytesIO(image_data))

    # 이미지 크기 조정
    image = image.resize((90, 110))

    # 이미지를 TK 이미지로 변환
    tk_image = ImageTk.PhotoImage(image)

    # 이미지를 라벨에 표시
    labels = []
    for i in range(int(max_object/3)):
        for j in range(3):
            for k in range(3):
                label = Label(window, image=tk_image)
                label.image = tk_image
                label.place(x=50+(j*430)+(k*110), y=70+(i*300))
                labels.append(label)

start_window()

# 키 입력 함수:
def click():
    #함수 선언
    global text
    global names
    global prices
    global links
    global review_cnts
    global score_ratings
    global hearts
    global images
    global reviews
    global session_obj
    global qs


    #함수 초기화
    text = entry_search.get()  # 텍스트 엔트리 위젯으로부터 입력한 텍스트를 수집
    names=[]
    prices=[]
    links=[]
    review_cnts=[]
    score_ratings=[]
    hearts=[]
    qs=[[] for _ in range(max_object)]
    images=[[] for _ in range(max_object)]
    reviews=[[] for _ in range(max_object)]
    session_obj = requests.Session()

    #상품 데이터 크롤링 하기
    value_crawl()

    #리뷰 데이터 크롤링 하기
    review_crawl()

    #이미지 데이터 크롤링 하기
    image_crawl()

    #데이터 excel로 업로드
    XLSX_upload()
    XLSX_2_upload()

    #창 데이터 초기화
    reset_upload()

    #데이터를 창에 업로드
    for i in range(int(max_object/3)):
        for j in range(3):
            value_upload(window,(i*3)+j, 140+430*(j), 200+300*(i))      #크롤링한 데이터 업로드
            
            for k in range(3):
                image_upload(window,images[(i*3)+j][k], 50+(j*430)+(k*110), 70+(i*300))    #크롤링한 이미지 업로드


#상품 데이터 크롤링 함수
def value_crawl():
    url = "https://www.musinsa.com/search/musinsa/goods?q=" + text + "&list_kind=small&sortCode=emt_high&sub_sort=&page=1&display_cnt=0&saleGoods=false&includeSoldOut=false&setupGoods=false&popular=false&category1DepthCode=&category2DepthCodes=&category3DepthCodes=&selectedFilters=&category1DepthName=&category2DepthName=&brandIds=&price=&colorCodes=&contentType=&styleTypes=&includeKeywords=&excludeKeywords=&originalYn=N&tags=&campaignId=&serviceType=&eventType=&type=popular&season=&measure=&openFilterLayout=N&selectedOrderMeasure=&shoeSizeOption=&groupSale=false&d_cat_cd=&attribute=&plusDeliveryYn="

    response = requests.get(url) #GET 요청 보내기

    html = response.text #응답으로 받은 HTML 가져오기

    soup = BeautifulSoup(html, 'html.parser')

    #상품 정보 가져오기: 이름, 가격, 링크
    abc=soup.find_all(class_="boxed-list-wrapper")
    
    infos = []
    for box in abc:
        info = box.find_all(class_="article_info")
        infos.extend(info)

    for info in infos[:max_object]:
        try:
            #이름 가져오기
            name_title = info.find(class_="list_info")
            name=name_title.find("a").get_text().strip()
            names.append(name)

            #가격 가져오기
            price=info.find(class_="price").get_text().strip()
            prices.append(price)          
            

            #상품의 링크 가져오기
            link_element = info.find(class_="list_info")
            link=link_element.find("a").get("href").strip()
            links.append(link)

            #상품에 등록된 총 리뷰 수 가져오기
            review_cnt = info.find(class_="count").get_text()
            review_cnts.append(review_cnt)


        except NoSuchElementException:
                print('Exception')

    #상품의 주소로부터 해당 상품 코드 추출하기
    global review_numbers
    review_numbers = [link.split('/')[-1] for link in links]



#리뷰 크롤링 함수
def review_crawl():
    
    for review_number in review_numbers:

        url="https://goods.musinsa.com/api/goods/v2/review/list?goodsNo=" + review_number + "&similarNo=0&type=style&itemCategoryCode=017042"
        response = session_obj.get(url, headers={"User-Agent": "Mozilla/5.0"})
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        infos=soup.find_all(class_="korSub")
        for info in infos[:3]:
            try:
                q=info.get_text()
                q = re.findall(r'\d+', q)
                q = ''.join(q)
                qs[index_(review_number,review_numbers)].append(q)
            except:
                print("Exception")

        review_all_cnt=0
        for i in (range(3)):
            for page in range(1,int(qs[index_(review_number,review_numbers)][i])+2):
                if review_all_cnt >= max_review:
                    break
                #해당 상품의 자바스크립트로된 HTML 리뷰의 URL 주소
                if i==0:
                    url="https://goods.musinsa.com/api/goods/v2/review/style/list?similarNo=0&sort=new&selectedSimilarNo=" + review_number + "&page=" + str(page) + "&goodsNo="+review_number+"&_=1685145377685" #무신사 리뷰 데이터 사이트
                #https://goods.musinsa.com/api/goods/v2/review/style/list?similarNo=0&sort=new&selectedSimilarNo=810034&page=1&goodsNo=810034&_=1685145377685
                elif i==1:
                    url="https://goods.musinsa.com/api/goods/v2/review/photo/list?similarNo=0&sort=new&selectedSimilarNo="+review_number+"&page=" + str(page) + "&goodsNo="+review_number+"&_=1685604860061"
                elif i==2:
                    url="https://goods.musinsa.com/api/goods/v2/review/goods/list?similarNo=0&sort=new&selectedSimilarNo="+review_number+"&page=" + str(page) + "&goodsNo="+review_number+"&_=1685604860063"

                #크롤링 방지 사이트를 우회해서 크롤링
                response = session_obj.get(url, headers={"User-Agent": "Mozilla/5.0"})

                #HTML 받음
                html = response.text

                #HTML을 파싱함
                soup = BeautifulSoup(html, 'html.parser')

                #리뷰 text를 가진 class
                infos=soup.find_all(class_="review-contents")

                #한 URL에 10개의 리뷰가 있어 10번 반복
                for info in infos[:10]:
                    try:
                        review=info.find(class_="review-contents__text").get_text().strip()
                        reviews[index_(review_number,review_numbers)].append(review)          
                        review_all_cnt+=1
                    except NoSuchElementException:
                        print('Exception')


                    



#상품 이미지, 평점 크롤링 함수
def image_crawl():

    for review_number in review_numbers:
        #특정 상품을 클릭한 페이지 URL
        url = "https://www.musinsa.com/app/goods/" + review_number

        #크롤링 방지 사이트를 우회해서 크롤링
        response = session_obj.get(url, headers={"User-Agent": "Mozilla/5.0"})

        html = response.text 

        #HTML을 파싱함
        soup = BeautifulSoup(html, 'html.parser')

        #상품 이미지 주소를 포함한 class
        abc=soup.find_all(class_="product_thumb")

        infos = []
        for box in abc:
            info = box.find_all("li")
            infos.extend(info)



        for info in infos[:3]:
            try:
                image=info.find("img").get("src").strip()
                if image is not None:
                    images[index_(review_number,review_numbers)].append("http:"+ image)
                else:
                    images[index_(review_number,review_numbers)].append(no_url)
            
            except NoSuchElementException:
                images[index_(review_number,review_numbers)].append(no_url)

        while(len(images[index_(review_number, review_numbers)])<3):
            images[index_(review_number, review_numbers)].append(no_url)

        #평점 크롤링
        score_rating=soup.find(class_="prd-score__rating").get_text()
        score_ratings.append(score_rating)


#데이터 값 excel에 업로드 함수
def XLSX_upload():
    data = [["상품명", "가격", "링크", "리뷰 수", "리뷰"]]

    for i in range(len(names)):
        row = [names[i],prices[i],links[i],review_cnts[i]]
        for review in reviews[i]:
                row.append(review)
        data.append(row)

    df = pd.DataFrame(data)
    filename = "data.xlsx"
    df.to_excel(filename, index=False)

#데이터 값 excel에 업로드 함수(인공지능 데이터)
def XLSX_2_upload():
    data = []

    for i in range(max_review):
        row = []
        for j in range(6):
            try:
                reviews[j][i] is not None and reviews[j][i]
                row.append(reviews[j][i])
            except:
                row.append(' ')
        data.append(row)

    df = pd.DataFrame(data)
    filename = "data2.xlsx"
    df.to_excel(filename, index=False)



#window창 각 데이터 값 리셋(재검색 할 시 데이터 값 겹침 방지)
def reset_upload():
    for i in range(2):
        for j in range(3):
            label= Label(window, text="                                                                                            ")
            label.place(x=100+430*(j), y=200+300*(i))

            label = Label(window, text="                                                                                           ")
            label.place(x=100+430*(j), y=220+300*(i))

            label = Label(window, text="                                                                                           ")
            label.place(x=100+430*(j), y=240+300*(i))

            label= Label(window, text="                                                                                            ")
            label.place(x=100+430*(j), y=260+300*(i))

            label = Label(window, text="                                                                                           ")
            label.place(x=100+430*(j), y=280+300*(i))



#크롤링한 값 업로드 함수
def value_upload(tk_object, index, X, Y):
    label= Label(window, text= names[index])
    label.place(x=X, y=Y)

    label = Label(window, text=prices[index])
    label.place(x=X, y=Y+20)

    label = Label(window, text=review_cnts[index])
    label.place(x=X, y=Y+40)

    label= Label(window, text=score_ratings[index] + "/5.0")
    label.place(x=X, y=Y+60)

    label = Label(window, text="AI:\"#############\"")
    label.place(x=X, y=Y+80)



#크롤링한 이미지 업로드 함수
def image_upload(tk_object,adress,X, Y):
    url = adress
    # 이미지 다운로드
    response = requests.get(url)
    image_data = response.content

    # 이미지 열기
    image = Image.open(BytesIO(image_data))

    # 이미지 크기 조절
    image = image.resize((90, 110))

    # 이미지를 TK 이미지로 변환
    tk_image = ImageTk.PhotoImage(image)


    # 이미지를 라벨에 표시
    label = Label(tk_object, image=tk_image)
    label.image = tk_image
    label.place(x = X, y = Y)


# 제출 버튼 추가
Button(window, text="제출", width=5, command=click).place(x=550, y=16)


window.mainloop()