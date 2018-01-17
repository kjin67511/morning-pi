# morning-pi #

라즈베리파이에서 (서울)버스 도착 알림, 날씨정보를 LCD에 표시하는 프로젝트입니다.

* 버스 도착정보 표시 
   * 남은 시간 및 남은 정류장수를 표시
* 날씨 정보 표시
   * 현재 날씨 / 12시간 후 날씨 예보
* 미세먼지 정보 표시
   * PM10 / PM2.5 
   * 임계치 초과시 경고 LED ON 
* 30초 마다 정보를 갱신
* 버튼을 누르면 30분간 재 실행
* 알람 기능


![morning-pi](https://i.imgur.com/tzn3CF2.jpg)

### 버스정보
3m(3)/12m(8) : 3분 후 3 정류장 전 / 12분 후 8 정류장 전     

### 날씨정보
-2L/4L : 현재 영상2도 흐림 / 12시간 후 영상4도 흐림
1L/3R60 : 현재 영하1도 흐림 / 12시간 후 영상3도 60%확률 비

날씨 코드
* S : 맑음
* L : 흐림
* Rxx : 비 xx% 확률
* W : 눈

### 미세먼지정보
105/86 : PM10 미세먼지 105, PM2.5 미세먼지 86

## 1. 요구사항

### 준비물

* 라즈베리파이
* GPIO 스위치
* 16x2 LCD
* LED 1개

### 추가모듈

```
sudo apt-get update
sudo apt-get install build-essential python-dev python-smbus python-pip
sudo pip install RPi.GPIO grequests
```
[Adafruit_Python_Char_LCD](https://github.com/adafruit/Adafruit_Python_CharLCD) 

```
git clone https://github.com/adafruit/Adafruit_Python_CharLCD.git
cd Adafruit_Python_CharLCD/
sudo python setup.py install
```

## 2. 설정정보 요구사항
### 2.1 공공데이터포털 API 인증키

[공공데이터포털](https://www.data.go.kr) 가입 후 다음 서비스 신청 

로그인 후 링크 클릭
* [동네예보정보조회서비스](https://www.data.go.kr/subMain.jsp#/L3B1YnIvcG90L215cC9Jcm9zTXlQYWdlL29wZW5EZXZEZXRhaWxQYWdlJEBeMDgyTTAwMDAxMzBeTTAwMDAxMzUkQF5wdWJsaWNEYXRhRGV0YWlsUGs9dWRkaTo5ZWQzZTRlMS0zNjU0LTQzN2EtYTg2Yi1iODg4OTIwMzRmOTAkQF5wcmN1c2VSZXFzdFNlcU5vPTE4MDI5NDckQF5yZXFzdFN0ZXBDb2RlPVNUQ0QwMQ==)
* [노선정보조회 서비스(서울특별시)](https://www.data.go.kr/subMain.jsp#/L3B1YnIvcG90L215cC9Jcm9zTXlQYWdlL29wZW5EZXZEZXRhaWxQYWdlJEBeMDgyTTAwMDAxMzBeTTAwMDAxMzUkQF5wdWJsaWNEYXRhRGV0YWlsUGs9dWRkaTplZGU4Y2E4Yy05NGJjLTQ5NTktYWFiOS1mNTAyMTAzN2I0NmYkQF5wcmN1c2VSZXFzdFNlcU5vPTE4MDY1MDUkQF5yZXFzdFN0ZXBDb2RlPVNUQ0QwMQ==)
* [정류소정보조회 서비스(서울특별시)](https://www.data.go.kr/subMain.jsp#/L3B1YnIvcG90L215cC9Jcm9zTXlQYWdlL29wZW5EZXZEZXRhaWxQYWdlJEBeMDgyTTAwMDAxMzBeTTAwMDAxMzUkQF5wdWJsaWNEYXRhRGV0YWlsUGs9dWRkaTozMjA1NjhiNS1jZDBmLTQyODAtOGI5Ny1iZjUxMmYxNWZlNDkkQF5wcmN1c2VSZXFzdFNlcU5vPTE4MDY1MjAkQF5yZXFzdFN0ZXBDb2RlPVNUQ0QwMQ==)
* [대기오염정보 조회 서비스](https://www.data.go.kr/subMain.jsp#/L3B1YnIvcG90L215cC9Jcm9zTXlQYWdlL29wZW5EZXZEZXRhaWxQYWdlJEBeMDgyTTAwMDAxMzBeTTAwMDAxMzUkQF5wdWJsaWNEYXRhRGV0YWlsUGs9dWRkaTo3MDkxMTBlNy1kN2IxLTQ0MjEtOTBiYS04NGE2OWY5ODBjYWJfMjAxNjA4MDgxMTE0JEBecHJjdXNlUmVxc3RTZXFObz0yMDc1Nzk3JEBecmVxc3RTdGVwQ29kZT1TVENEMDE=)

각 서비스 별 '일반인증키' 복사

### 2.2 버스노선 ID

인터넷 브라우저를 열고 주소 창에 다음 입력
```http://ws.bus.go.kr/api/rest/busRouteInfo/getBusRouteList?serviceKey=인증키&strSrch=버스노선번호```

* 인증키 : 공공데이터포털에서 노선정보조회 서비스를 위해 발급받은 인증키
* 버스노선번호 : 원하는 버스번호 입력

Request가 정상적으로 처리되면, 해당 버스노선과 일치하는 버스노선정보를 반환함. 
**```<busRouteId>```** (버스노선 ID)값 복사

예) 601번 버스
```
<itemList>
    <busRouteId>100100086</busRouteId>
    <busRouteNm>601</busRouteNm>
    <corpNm>다모아 02-376-2300</corpNm>
    <edStationNm>혜화역</edStationNm>
    <firstBusTm>20170219040000</firstBusTm>
    <firstLowTm>20151125040800</firstLowTm>
    <lastBusTm>20170219231000</lastBusTm>
    <lastBusYn></lastBusYn>
    <lastLowTm>20150717231000</lastLowTm>
    <length>51.7</length>
    <routeType>3</routeType>
    <stStationNm>개화동</stStationNm>
    <term>6</term>
</itemList>
```

### 2.3 정류정 ID

[다음지도](http://map.daum.net/)에서 버스노선번호 입력하면 정류소별 ID(5자리)를 알아낼 수 있음, 네이버지도에서는 제공하지 않음

예) 종로1가 역: 01012

![](https://i.imgur.com/AwQkkYo.png)

### 2.4 날씨위치좌표 XY

[동네예보정보조회서비스](https://www.data.go.kr/subMain.jsp#/L3B1YnIvcG90L215cC9Jcm9zTXlQYWdlL29wZW5EZXZEZXRhaWxQYWdlJEBeMDgyTTAwMDAxMzBeTTAwMDAxMzUkQF5wdWJsaWNEYXRhRGV0YWlsUGs9dWRkaTo5ZWQzZTRlMS0zNjU0LTQzN2EtYTg2Yi1iODg4OTIwMzRmOTAkQF5wcmN1c2VSZXFzdFNlcU5vPTE4MDI5NDckQF5yZXFzdFN0ZXBDb2RlPVNUQ0QwMQ==) 첨부 기술문서에 포함되어 있는 ```동네예보조회서비스_격자_위경도.xlsx``` 엑셀파일에서 원하는 지역의 좌표x, 좌표y를 획득

예) 종로구 : (X) 60, (Y) 127



### 2.5 미세먼지 측정소

[에어코리아](https://www.airkorea.or.kr/realSearch) 에서 측정소명 알아내기

예) 청계천로
![](https://i.imgur.com/gtBLjJI.png)


## 3. config 파일
```
interval: 실행 중 얼마나 자주 업데이트 하는가 (초)
duration: 한번 실행 시 얼마나 오래 동작 하는가 (초) 
input_pin: 누르면 실행시키는 스위치의 GPIO핀 번호
station_id: 정류소 ID 입력
nx: 날씨위치 X좌표
ny: 날씨위치 Y좌표
station_name: 미세먼지 측정소
pm10_threshold: PM10 미세먼지 임계치
pm25_threshold: PM2.5 미세먼지 임계치
led_pin: 미세먼지 임계치 초과시 경고 LED ON GPIO핀 번호 
bus: 공공데이터포털에서 정류소정보조회를 위해 발급받은 인증키
weather: 공공데이터포털에서 동네예보정보조회서비스를 위해 발급받은 인증키
dust: 공공데이터포털에서 대기오염정보조회를 위해 발급받은 인증키
rs, en, d4, d5, d6, d7: LED에 사용되는 GPIO핀 번호
schedule: 스위치 입력 상관없이 해당시각에 실행(1회)
``` 

## 4. 참조
LED 설정 참조하기 : [참조1](https://learn.adafruit.com/drive-a-16x2-lcd-directly-with-a-raspberry-pi?view=all) [참조2](http://www.rasplay.org/?p=7268)

## 5. 실행

```
python main.py

# 백그라운드 실행하기
nohup python main.py &
```


