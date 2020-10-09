import pygame as pg
import datetime
import time
import json
import requests
from bs4 import BeautifulSoup
import pyautogui
import urllib.parse

pg.init()

pg.display.set_caption(" Open Api ")

json_data = requests.get("http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey=qU6ZiWZWr9TyzBf4CSQePVRrLv656KwyxySrnDDH4o9I71HOfECubfmhWxHeIYMyg6X9yLyogSFQV0ucd9gFpA%3D%3D&numOfRows=25&pageNo=1&sidoName=%EC%84%9C%EC%9A%B8&searchCondition=DAILY&(&_returnType=json)").json()
weather_rescode = requests.get("http://api.openweathermap.org/data/2.5/weather?lat=37&lon=126&appid=313d1d39ded06b928c0612edb94637a7").status_code
dust_rescode = requests.get("http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey=qU6ZiWZWr9TyzBf4CSQePVRrLv656KwyxySrnDDH4o9I71HOfECubfmhWxHeIYMyg6X9yLyogSFQV0ucd9gFpA%3D%3D&numOfRows=25&pageNo=1&sidoName=%EC%84%9C%EC%9A%B8&searchCondition=DAILY&(&_returnType=json)").status_code
load_blue = pg.transform.scale(pg.image.load("image/파란.png"), (130, 45))
botton_image = pg.image.load("image/버튼.png")
load_wd_background = pg.image.load("image/날씨미세배경.png")
wd_background_image = pg.transform.scale(load_wd_background, (400, 490))

main_image_size = (90, 90)
sun_image = pg.transform.scale(pg.image.load("image/태양.png"), main_image_size)
clouds_image = pg.transform.scale( pg.image.load("image/구름많음.png"), main_image_size)
rain_image = pg.transform.scale(pg.image.load("image/비.png"), main_image_size)
cloud_image = pg.transform.scale(pg.image.load("image/구름.png"), (100, 100))
mist_image = pg.transform.scale( pg.image.load("image/안개.png"), main_image_size)
haze_image = pg.transform.scale( pg.image.load("image/안개.png"), main_image_size)

mygu = "강남구"
dust = 0
smalldust = 0
seoultemp = 0
reset_time = 0

news_x_list = [0, 2600] 
grid = [1,1]
gu_list = []

timefont = pg.font.SysFont("malgungothic", 40)
font = pg.font.SysFont("malgungothic", 30)
bigfont = pg.font.SysFont("malgungothic", 39)
smallfont = pg.font.SysFont("malgungothic", 28)
smallsmallfont = pg.font.SysFont("malgungothic", 16)
bus_font = pg.font.SysFont("malgungothic", 15)

t_botton = font.render("구 선택", True, (0,0,0))
t_choose_gu = bigfont.render("구 선택", True, (0,0,0))
t_okay = font.render("확인", True, (0,0,0))
t_station = font.render("정류장 선택", True, (0,0,0))
t_small_intro = bigfont.render("오늘의 날씨", True ,(0,0,0))

okay = False
running = True
change_gu  = True
set_gu = True
set_information_one = True

def choose_bus_station():
    global want_station_asrId, want_station, change_bus_page, want_station_back
    arsId = []
    while True:
        list = []
        want_station = pyautogui.prompt(text="원하는 정류소를 입력하세요", title="정류소 검색")
        if not want_station == None:
            want_station = want_station.strip()
        if want_station == None:
            break
        elif want_station == "":
            pyautogui.alert(text="잘못 입력하셨습니다.", title="오류", button="확인")
        else:
            want_station_back = want_station 
            response = requests.get( "http://ws.bus.go.kr/api/rest/stationinfo/getStationByName?ServiceKey=qU6ZiWZWr9TyzBf4CSQePVRrLv656KwyxySrnDDH4o9I71HOfECubfmhWxHeIYMyg6X9yLyogSFQV0ucd9gFpA%3D%3D&stSrch={}".format(urllib.parse.quote_plus(want_station))).text.encode("utf-8")
            for a in BeautifulSoup(response, "lxml-xml").find_all("itemList"):
                for b in a.find_all("stNm"):
                    if want_station == b.text:
                        list.append(a)
            for a in list:
                for b in a.find_all("arsId"):
                    arsId.append(b.text)
            if arsId == []:
                pyautogui.alert(text="존재하지 않는 역입니다.", title="오류", button="확인")
            else:
                direction_list = []
                for a in arsId[0:2]:
                    station_list = [] #http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid?ServiceKey=qU6ZiWZWr9TyzBf4CSQePVRrLv656KwyxySrnDDH4o9I71HOfECubfmhWxHeIYMyg6X9yLyogSFQV0ucd9gFpA%3D%3D&arsId=25544
                    #for b in BeautifulSoup(requests.get("http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid?ServiceKey=qU6ZiWZWr9TyzBf4CSQePVRrLv656KwyxySrnDDH4o9I71HOfECubfmhWxHeIYMyg6X9yLyogSFQV0ucd9gFpA%3D%3D&arsId={}".format(a)).text.encode("utf-8"), "lxml-xml").find_all("nxtStn"):
                    for b in BeautifulSoup(requests.get("http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid?ServiceKey=vd%2B2nNyF4R6cKQheiYx%2FnBKf3jBbnCburz0CpVI6lma62eC7DKIiVCvnIP8geQzI3muGUuDjvcWrKCKzrzyQhw%3D%3D&arsId={}".format(a)).text.encode("utf-8"), "lxml-xml").find_all("nxtStn"):
                        station_list.append(b.text)
                    how_many = 0
                    for a in enumerate(station_list):
                        if how_many < station_list.count(a[1]):
                            how_many = a[0]
                        
                    direction_list.append(station_list[how_many])
                if direction_list[0] == pyautogui.confirm(buttons=direction_list, text="방향을 선택하세요", title="정류소 선택"):
                    want_station_asrId = arsId[0]
                else:
                    want_station_asrId = arsId[1]
                change_bus_page = 0
                break

def set_bus_information():
    global bus_list, bus_response, bus_xml_data
    #bus_url = "http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid?ServiceKey=qU6ZiWZWr9TyzBf4CSQePVRrLv656KwyxySrnDDH4o9I71HOfECubfmhWxHeIYMyg6X9yLyogSFQV0ucd9gFpA%3D%3D&arsId={}".format(want_station_asrId)
    bus_url = "http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid?ServiceKey=vd%2B2nNyF4R6cKQheiYx%2FnBKf3jBbnCburz0CpVI6lma62eC7DKIiVCvnIP8geQzI3muGUuDjvcWrKCKzrzyQhw%3D%3D&arsId={}".format(want_station_asrId)
    bus_response = requests.get(bus_url).text.encode("utf-8")
    bus_xml_data = BeautifulSoup(bus_response, 'lxml-xml').find_all("itemList")
    bus_list = []
    for bus in enumerate(bus_xml_data):
        bus_list.append([bus[1].find("rtNm").text])
        bus_list[bus[0]].append(want_station_back)
        bus_list[bus[0]].append(bus[1].find("sectNm").text.split("~")[0])
        if bus[1].find("stationNm1") == None:
            bus_list[bus[0]].append("운행종료")
        else:
            bus_list[bus[0]].append(bus[1].find("stationNm1").text)
        if bus[1].find("arrmsg1").text == "운행종료":
            bus_list[bus[0]].append("운행종료")
        else:
            bus_list[bus[0]].append(bus[1].find("arrmsg1").text.split("분")[0])
        if bus_list[bus[0]][3] == bus_list[bus[0]][1]:
            bus_list[bus[0]].append(0)
        elif bus_list[bus[0]][3] == bus_list[bus[0]][2]:
            bus_list[bus[0]].append(1)
        else:
            bus_list[bus[0]].append(2)
        bus_list[bus[0]].append(load_blue)
    for a in range(3):
        for bus in bus_list:
            if bus[3] == "운행종료":
                bus_list.remove(bus)

    # bus_list[0] 버스번호 bus_list[1] 고덕역  bus_list[2] 현재 위치  bus_list[3] 전역 bus_list[4] 남은 시간(분) bus_list[5]위치 0 ~ 2 bus_list[6] 버스 이미지

def set_news():
    global news, t_news, news2
    news_url = "https://www.yna.co.kr/"
    news_response = requests.get(news_url).text.encode("utf-8")
    news_soup = BeautifulSoup(news_response, 'html.parser')
    news_first_pasing = news_soup.find_all("div", class_ = "list-type063")
    news_list = []
    for a in news_first_pasing:
        for b  in a.find_all("strong", class_ = "tit-news"):
            news_list.append(b.text)
    news = ""
    news2 = ""
    for a in news_list[:3]:
        news = "{}     {}".format(news,a)
    for a in news_list[4:]:
        news2 = "{}     {}".format(news2,a)
  
def set_dust_level():
    global dust, dust_level, t_dust_color
    try:
        if dust < 31:
            dust_level = "좋음"
            t_dust_color = (0, 0, 255)
        elif dust > 30 and dust < 81:
            dust_level = "보통"
            t_dust_color = (0, 255, 0)
        elif dust> 80 and dust < 151:
            dust_level = "나쁨"
            t_dust_color = (255, 255, 0)
        elif dust> 150:
            dust_level = "매우나쁨"
            t_dust_color = (255, 0, 0)
    except:
        dust_level = ""
        t_dust_color = (0,0,0)

def set_smalldust_level():
    global smalldust, smalldust_level, t_smalldust_color
    
    try:
        if smalldust < 16:
            smalldust_level = "좋음"
            t_smalldust_color = (0, 0, 255)
        elif smalldust > 15 and smalldust < 35:
            smalldust_level = "보통"
            t_smalldust_color = (0, 255, 0)
        elif smalldust > 34 and smalldust < 76:
            smalldust_level = "나쁨"
            t_smalldust_color = (255, 255, 0)
        elif smalldust > 75:
            smalldust_level = "매우나쁨"
            t_smalldust_color = (255, 0, 0)
    except:
        smalldust_level = ""
        t_smalldust_color = (0,0,0)

def set_weather():
    global seoulweather, main_image
    if weather_json_data['weather'][0]['main'] == "Clear":
        seoulweather = "맑음"
        main_image = sun_image
    if weather_json_data['weather'][0]['main'] == "Clouds":
        seoulweather = "구름 많음"
        main_image = clouds_image
    if weather_json_data['weather'][0]['main'] == "Drizzle":
        seoulweather = "이슬비"
    if weather_json_data['weather'][0]['main'] == "Rain":
        seoulweather = "비"
        main_image = rain_image
    if weather_json_data['weather'][0]['main'] == "Mist":
        seoulweather = "안개"
        main_image = mist_image
    if weather_json_data['weather'][0]['main'] == "Haze":
        seoulweather = "안개"
        main_image = haze_image

def set_information():
    global okay, mygu, response, json, url, seoul, dust, smalldust, datatime, json_data, weather_url, response2, weather_json_data, seoulweather, main_image, seoultemp, set_gu
    if set_gu:
        seoul = json_data['list']
        for a in seoul:
            gu_list.append(a['cityName'])
        set_gu = False

    weater_response = requests.get("http://api.openweathermap.org/data/2.5/weather?lat=37&lon=126&appid=313d1d39ded06b928c0612edb94637a7")
    dust_response = requests.get("http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey=qU6ZiWZWr9TyzBf4CSQePVRrLv656KwyxySrnDDH4o9I71HOfECubfmhWxHeIYMyg6X9yLyogSFQV0ucd9gFpA%3D%3D&numOfRows=25&pageNo=1&sidoName=%EC%84%9C%EC%9A%B8&searchCondition=DAILY&(&_returnType=json)")
    json_data = dust_response.json()
    weather_json_data = weater_response.json()
    seoul = json_data['list']
    set_weather()
    for gu in seoul:
        if mygu == gu['cityName']:
            okay = True
            print_information = False
            datatime = gu['dataTime']

            if gu['pm10Value'] == "":
                dust = "정보없음"
            else:
                if dust == int(gu['pm10Value']):
                    pass
                else:
                    dust = int(gu['pm10Value'])
                    print_information = True
            if gu['pm25Value'] == "":
                smalldust = "정보없음"
            else:
                if smalldust == int(gu['pm25Value']):
                        pass
                else:
                    smalldust = int(gu['pm25Value'])
                    print_information = True

            if seoultemp != (int(weather_json_data['main']['temp']) - 273) :
                seoultemp = (int(weather_json_data['main']['temp']) - 273)
                print_information = True
            if print_information:
                print_write()
            break
    set_dust_level()
    set_smalldust_level()

def print_write():
        #print("\n-----------------------------\n\n서울의 현재온도 : {}\n\n서울의 날씨 : {}\n\n{}의 미세먼지 농도 : {}\n\n{}의 초미세먼지 농도 : {}\n\n-----------------------------".format(seoultemp, seoulweather, mygu, dust ,mygu, smalldust))
        write = False
        dustfile = open("미세먼지기록.txt", "r")
        all_lines = dustfile.readlines()
        for line in all_lines:
            if line == "{}시에 측정한 서울의 온도는 {} 날씨는 {} {}의  미세먼지농도는 {}, 초미세먼지농도는 {}입니다.\n".format( datatime,seoultemp, seoulweather, mygu,dust, smalldust ):
                pass
                write = False
            else:
                write = True
        dustfile.close()
        if write:
            dustfile = open("미세먼지기록.txt", "a")
            dustfile.write("{}시에 측정한 서울의 온도는 {} 날씨는 {} {}의  미세먼지농도는 {}, 초미세먼지농도는 {}입니다.\n\n".format( datatime,seoultemp, seoulweather, mygu,dust, smalldust ))
            dustfile.close()    

def set_time():
    global now, year, month, day, hour, minute, second
    now = datetime.datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime("%d")
    hour = now.strftime('%H')
    minute = now.strftime('%M')
    second= now.strftime('%S')

def d_background():
    screen.fill((84, 195, 255))
    screen.blit(wd_background_image, (50, 120))
    screen.blit(t_time, (220, 30))
    screen.blit(botton_image, (140, 520))
    screen.blit(botton_image, (620, 520))
    screen.blit(t_station, (653, 535))
    screen.blit(t_news, (news_x_list[0], 630))
    screen.blit(t_news2, (news_x_list[1], 630))

def render_text():
    global t_dust_level, t_smalldust_level, t_dust, t_smalldust, t_seoulweather, t_seoultemp, t_time, t_news, t_news2
    t_dust_level = smallfont.render(dust_level, True, t_dust_color)
    t_smalldust_level = smallfont.render(smalldust_level, True, t_smalldust_color)
    t_dust = smallfont.render("{} 미세먼지 : {}".format(mygu, dust), True, (0,0,0))
    t_smalldust = smallfont.render("{} 초미세먼지 : {}".format(mygu, smalldust) ,True, (0,0,0))
    t_seoulweather = smallfont.render("서울의 현재날씨 : {}".format(seoulweather), True, (0,0,0)) 
    t_seoultemp = smallfont.render("서울의 현재온도 : {}".format(seoultemp), True, (0,0,0))
    t_time = timefont.render("{}년 {}월 {}일 {}시 {}분 {}초".format(year, month, day, hour,minute, second), True, (0,0,0))
    t_news = font.render(news, True, (0,0,0))
    t_news2 = font.render(news2, True, (0,0,0))

def d_weather_dust():
    if change_gu:
        screen.blit(t_okay, (220, 535))
        screen.blit(t_choose_gu, (190, 140))
        for a in range(5):
            for b in range(5):
                if a + 1 == grid[0] and b + 1 == grid[1]:
                    pg.draw.rect(screen, (255,0,0), [80 +70*a,200 + 60*b ,70, 60], 3)
                else:
                    pg.draw.rect(screen, (0,0,0), [80 + 70*a,200 + 60*b ,70, 60], 2)
        
        for a in enumerate(gu_list):
            t_gu = smallsmallfont.render(a[1], True, (0,0,0))
            if a[0] == 10 or a[0] == 13 or a[0] == 19:
                screen.blit(t_gu, (83 + 70*(a[0]%5), (a[0] // 5) * 60 + 218))
            elif a[0] == 23:
                screen.blit(t_gu, (99 + 70*(a[0]%5), (a[0] // 5) * 60 + 218))
            else:
                screen.blit(t_gu, (92 + 70*(a[0]%5), (a[0] // 5) * 60 + 218))
            b += 1
    else:
        screen.blit(t_botton, (200, 535))
        screen.blit(t_seoultemp, (80, 220)) 
        screen.blit(t_seoulweather, (80, 295))
        screen.blit(t_dust, (80, 370))
        if len(mygu) == 4:
            screen.blit(t_smalldust_level,(390, 445))
            screen.blit(t_dust_level, (380, 370))
        else:
            screen.blit(t_smalldust_level,(375, 445))
            screen.blit(t_dust_level, (360, 370))

        screen.blit(t_smalldust, (80, 445))
        screen.blit(t_small_intro, (145, 140))
        screen.blit(main_image, (350, 200))

def d_bus():
    b = 1
    if not bus_list == []:
        if change_bus_page == 0:
            start_page = 0
        else:
            start_page = change_bus_page*3 - 1
        for bus in bus_list[start_page:start_page+3]:
            pg.draw.line(screen, (0,0,0), (525, 30 +(b *(550/(len(bus_list[start_page:start_page+3]) + 1)))),(925, 30 +  (b *(550/(len(bus_list[start_page:start_page+3]) + 1)))),3)
            if bus[5] == 0:
                for circle in range(2):
                    pg.draw.circle(screen, (0,0,0),((525 + 400*circle), round(30 + (b *(550/(len(bus_list[start_page:start_page+3]) + 1))))), 5)
            else:
                for circle in range(3):
                    pg.draw.circle(screen, (0,0,0),(525 + round((400/2)*circle), round(30 + (b *(550/(len(bus_list[start_page:start_page+3]) + 1))))),5)
            screen.blit(bus[6], (460 + (400/2)*bus[5], (b *(550/(len(bus_list[start_page:start_page+3]) + 1))) - 25 )) 
            cc = 0 
            if bus[5] == 0:
                for station in bus[1:3]:
                    if len(station) > 10:
                        station = station.split(".")[0]
                    t_station_x = (len(station) - 3) * 7
                    t_staion = smallsmallfont.render(station, True, (0,0,0))
                    screen.blit(t_staion, (500 + 400*cc - t_station_x, 50 + (b *(550/(len(bus_list[start_page:start_page+3]) + 1)))))
                    cc += 1
            else:
                for station in bus[1:4]:
                    if len(station) > 10:
                        station = station.split(".")[0]
                    t_station_x = (len(station) - 3) * 7
                    t_staion = smallsmallfont.render(station, True, (0,0,0))
                    screen.blit(t_staion, (500 + (400/2)*cc - t_station_x, 40 + (b *(550/(len(bus_list[start_page:start_page+3]) + 1)))))
                    cc += 1

            if bus[4] == "곧 도착":
                t_left_tile = smallsmallfont.render("   곧 도착".format(bus[4]), True, (0,0,0))
            else:
                t_left_tile = smallsmallfont.render("약 {}분 남음".format(bus[4]), True, (0,0,0))
            screen.blit(bus_font.render(bus[0], True, (0,0,0)), ((510 - (len(bus[0])-3)*5) + (400/2)*bus[5], (b *(550/(len(bus_list[start_page:start_page+3]) + 1))) -5 ))
            screen.blit(t_left_tile, (680 ,80 + (b *(550/(len(bus_list[start_page:start_page+3]) + 1)))))
            b += 1
    else:
        t_no_bus = timefont.render("정보없음", True, (0,0,0))
        screen.blit(t_no_bus, (650, 300))

def update_reset(): 
    global reset_time, change_bus_page
    reset_time += 1
    if reset_time % 20000 == 0:
        set_information()
        set_news()
    if reset_time % 1000 == 0:
        set_bus_information()
    if reset_time % 500 == 0:
        if len(bus_list)//3 == change_bus_page:
            change_bus_page = 0
        else:
            change_bus_page += 1
    for a in range(2):
        news_x_list[a] -= 1
        if news_x_list[a] < -2500:
            news_x_list[a] = 1800

def pygame_event():
    global running, change_gu, mouse_x, mouse_y, grid, mouseclick, mygu, set_information_one
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            if mouse_x >= 140 and mouse_x <= 360 and mouse_y >= 520 and mouse_y <= 594:
                mouseclick = False
                if change_gu:
                    change_gu = False
                    if not gu_list[(grid[1]-1)*5 + grid[0] - 1] == mygu:
                        set_information_one = True
                    mygu = gu_list[(grid[1]-1)*5 + grid[0] - 1]    
                else:
                    change_gu = True
            else:
                mouseclick = True
            if mouseclick and change_gu:
                grid = [((mouse_x - 80) // 70 ) + 1, ((mouse_y - 200)// 60) + 1]
                if grid[0] > 5:
                    grid[0] = 5
                if grid[0] < 1:
                    grid[0] = 1
                if grid[1] > 5:
                    grid[1] = 5
                if grid[1] < 1:
                    grid[1] = 1
            if mouse_x > 640 and mouse_y > 529 and mouse_x < 840 and mouse_y < 586:
                choose_bus_station()
                set_bus_information()
    if set_information_one:
        set_information()
        set_information_one = False

choose_bus_station()
set_bus_information()
set_news()

if dust_rescode == 200 and weather_rescode == 200: 

    screen = pg.display.set_mode((1000, 700))

    while running:

        pygame_event()

        set_time()

        render_text()

        d_background()
        d_weather_dust()
        d_bus()

        update_reset()

        pg.display.update()

else:
    print("오류")