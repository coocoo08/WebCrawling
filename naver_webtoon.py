'''
    * 네이버 웹툰 페이지 크롤링 (bs4)
        - 요일별 폴더에 각각의 이미지를 다운로드
        - 타이틀번호, 요일, 제목, 링크 내용으로 csv 파일 생성

    * 크롤링 순서
        <div class="thumb">인 항목을 추출함
        반복문 사용
            <a> 태그의 href 속성을 읽어 옴
                replace()
                split()
            <img> 태그
                title 속성을 읽어 와서 제목으로 처리함

        리스트에 추가함
        해당 이미지를 각 요일 폴더에 이미지로 저장함

        데이터 프레임 만들어 CSV 파일로 저장함
'''
import os

from urllib.request import urlopen
from bs4 import BeautifulSoup
from pandas import DataFrame

myparser = 'html.parser'
myurl = 'https://comic.naver.com/webtoon/weekday'
response = urlopen(myurl)
soup = BeautifulSoup(response, myparser)

weekday_dict = {'mon':'월요일', 'tue':'화요일', 'wed':'수요일',
                'thu':'목요일', 'fri':'금요일', 'sat':'토요일',
                'sun':'일요일'}

myfolder = 'c:\\Users\\0_0N\\Desktop\\ezen_webtoon\\'

try:
    if not os.path.exists(myfolder):           # 폴더 생성
        os.mkdir(myfolder)

    for mydir in weekday_dict.values():
        mypath = myfolder + mydir
        if os.path.exists(mypath):
            pass
        else:       #'월요일'부터 '일요일'까지 폴더 생성
            os.mkdir(mypath)
except FileExistsError as err:
    pass    # 오류를 무시하고 넘김

'''
save_file() : 웹 페이지에 존재하는 이미지를 로컬 컴퓨터에 저장하기 위한 함수
              <img src=''>는 웹 페이지에 존재하는 이미지 경로임
              'mon', 'thu', 등 요일 정보 저장
'''
def save_file(mysrc, myweekday, mytitle):
    image_file = urlopen(mysrc)
    filename = myfolder + myweekday + '\\' + mytitle + '.jpg'

    myfile = open(filename, mode='wb')
    myfile.write(image_file.read())     # 이미지로 저장됨

mylist = []     # 데이터를 저장할 리스트

mytarget = soup.find_all('div', attrs={'class' : 'thumb'})
print('만화 총 갯수 : %d' % (len(mytarget)))
for weekday_target in mytarget:
    myhref = weekday_target.find('a').attrs['href']
    myhref = myhref.replace('/webtoon/list?', '')
    result = myhref.split('&')
    mytitltid = result[0].split('=')[1]
    myweekday = result[1].split('=')[1]
    myweekday = weekday_dict[myweekday]
    # print(mytitltid + '/' + myweekday)

    imgtag = weekday_target.find('img')
    # print(imgtag)
    mysrc = imgtag.attrs['src']
    mytitle = imgtag.attrs['title'].strip()
    mytitle = mytitle.replace('?', '')
    # print(mytitle + '/' + mysrc)

    mytuple = tuple([mytitltid, myweekday, mytitle, mysrc])
    mylist.append(mytuple)

    # 이미지 저장함수
    save_file(mysrc, myweekday, mytitle)

print(mylist)

myframe = DataFrame(mylist, columns=['타이틀 번호', '요일', '제목', '링크'])
filename = 'ezen_cartoon.csv'
myframe.to_csv(filename, encoding='UTF-8', index=False)
print(filename + '파일로 저장함')
print('\n finished')














