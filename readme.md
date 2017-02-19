# morning-pi #

라즈베리파이에서 (서울)버스 도착 알림, 날씨정보를 LCD에 표시하는 프로젝트입니다.

* 정류에 도착하는 버스의 남은 시간 및 남은 정류장수를 표시
* 원하는 위치에 현재 날씨 상태 및 12시간후 날씨 예보를 표시
* 30초 마다 정보를 갱신
* 버튼을 누르면 30분간 재 실행

![morning-pi](http://i.imgur.com/WHF5RHo.jpg)

### 버스정보
5m(3)/22m(13) : 5분 후 3 정류장 전 / 22분 후 13 정류장 전     

### 날씨정보
-1°L/3°R60 : 현재 영하1도 흐림 /12 시간 후 영상 3도 60%확률 비

날씨 코드

* S : 맑음
* L : 흐림
* R : 비
* W : 눈


## 준비물

* 라즈베리파이
* GPIO 스위치
* 16x2 LCD

## 설치 요구사항

* [Adafruit_Python_Char_LCD](https://github.com/adafruit/Adafruit_Python_CharLCD)
* pip install grequests
* 공공데이터포털 API 인증키
* 설정 정보: 버스노선 ID, 정류장 ID, 날씨위치좌표XY

## 공공데이터 API 사용 신청하기

[공공데이터포털](https://www.data.go.kr) 가입 후 다음 API 신청

* 동네예보정보조회서비스
* 노선정보조회 서비스 (서울특별시)
* 정류소정보조회 서비스 (서울특별시)


## 설정 정보 알아내기

### 버스노선 ID

http://ws.bus.go.kr/api/rest/busRouteInfo/getBusRouteList?serviceKey=인증키&strSrch=버스노선번호

인증키 : 공공데이터포털에서 노선정보조회 서비스를 위해 발급받은 인증키

버스노선번호 : 원하는 버스번호 입력


HTTP Request가 정상적으로 처리되면, 해당 버스노선과 일치하는 버스노선정보를 반환함. 버스노선 ID는  <busRouteId>에 들어있음

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

### 정류소 ID

[다음지도](http://map.daum.net/)에서 버스노선번호 입력하면 정류소별 ID(5자리)를 알아낼 수 있음, 네이버지도에서는 제공하지 않음

예) 종로1가 역: 01190


### 날씨위치좌표

공동네예보정보조회서비스 기술문서에 포함되어 있는 동네예보조회서비스_격자_위경도 엑셀파일에서 원하는 지역의 좌표x, 좌표y를 획득

예) 종로구 : (X) 60, (Y) 127


## config 파일

* interval: 설정시간 간격 마다 리프레시 (초)
* duration: 설정시간동안 실행
* input_pin: 스위치 입력받을 GPIO핀 번호
* station_id: 정류소 ID 입력
* nx: 날씨위치 X좌표
* ny: 날씨위치 Y좌표
* bus: 공공데이터포털에서 정류소정보조회를 위해 발급받은 인증키
* weather: 공공데이터포털에서 동네예보정보조회서비스를 위해 발급받은 인증키
* rs, en, d4, d5, d6, d7: [참조1](https://learn.adafruit.com/drive-a-16x2-lcd-directly-with-a-raspberry-pi?view=all) [참조2](http://www.rasplay.org/?p=7268)


## 다음버전

정해진 시각에 실행되는 기능
