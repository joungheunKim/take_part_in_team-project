# 팀소개 웹페이지 만들기
## 프로젝트 목표

1.메인 페이지 구현 

2.팀 참여 버튼으로 정보입력하기, 정보에 포함되는 내용 이름, 나이, 취미, 블로그주소, 한마디, 사진 포함

3.메인화면에 팀 개인 정보노출, 클릭시 팀 개인화면 출력

4.올린 정보 수정 및 삭제

를 기본 목표로 삼는다.

## 구현 내용
메인페이지, 개인페이지, 팀참가페이지간의 이동

### 고민했던 부분
a테그를 사용하여 a href= "card.html"로 이동을 구현하려 하였으나
a테그는 하이퍼링크를 정의 할 때 사용 함으로 적합하지 않았다.

그래서 html 페이지간의 이동이 가능한 location.href = "이동할페이지주소"를 사용하여 해결 하기로 하였다.
메인 html에서 개인 카드로 넘어가는 버튼생성
```
<button type="button" onclick="location.href='/gocard'">
</button>
```
으로 gocard라는 값을 주고 app.py 백엔드에서
```
@app.route('/gocard')
def gocard():
    return render_template('card.html')
 ```
gocard 라는 값이 들어왔을때 card.html을 리턴해주는 방법으로 구현에 성공하였다.

## 구현 내용
팀 개인페이지에서 선택한 한명분의 정보만 노출
### 고민했던 부분
1.각자의 개인 페이지를 만들어 한명의 정보만 노출되게 하고 싶었다.
하지만 개인의 html을 만드는 것은 번거롭고, 추가생성되는 팀원의 페이지는 만들어 놓지 않았기에 계속만드는 일을 했어야했다.
그래서 개인페이지를 하나만들고, 메인 페이지에서 선택한 한명의 정보만 가져와 페이지를 구성하는 방법이 필요했다.

2.처음에는 MongoDB에서 자동으로 생성해주는 ObjectId 타입의 '_id'컬럼을 사용하려 했으나  해당 타입이 string이 아닌 관계로 jsonString으로 프론트에 전달하기 위해서는 String 타입으로 변경해주는 작업이 추가적으로 필요했다.
하지만 MongoDB에서 데이터를 find할 때 ObjectId를 사전에 String타입으로 가져오는 방법이 없어 iteration을 통해 따로 ObjectId 타입을 변경해주는 추가 작업이 필요했는데 이 기능들을 구현하기에는 기술력도 받쳐주지않고 다른 기능을 구현하는 시간이 부족하여 간단한 방법을 찾아보았다.

3.
```
<button type="button" onclick="location.href='/gocard/${name}'"><span class="ir">더보기</span></button>
 ```
메인페이지에 노출되는 작은 미니카드에서 개인카드로 넘어가는 버튼에서 가져온 이름${name}을 사용하였다.
```
@app.route('/gocard/<memberNamed>')
def gocard(memberNamed):
  only_memberd = list(db.teams.find({'name':memberNamed},{'_id':False}))
    
  return render_template('card.html',only = only_memberd)
```
<memberNamed>라는 값으로 받아 Mongodb에서 name 값이 같은 정보만 불러와서
  card.html에 only라는 값으로 정보를 주기로 하였다.
  
이 방법은 문제점은 혹여나 이름이 같은 팀원의 경우 값이 1개만 나오는 것이 아니기에 문제가 될 수 있다.
  하지만 완벽한 기술을 구현하기에는 시간이 부족하여 이러한 방법을 선택했다.
  
```
  <h5 class="card-title"></h5>
                        <p class="card-text">나이 : </p>
                        <p class="card-text">취미 : </p>
                        <p class="card-text" >블로그 : </p>
                        <p class="card-text" style="margin-top: 10px;">부트캠프 다짐 : </p>
  ```
  만들어 놓은 기본틀에 {{only[0].값}}으로 필요한 값만 넣어주면 된다.
  ```
  <h5 class="card-title">{{only[0].name}}</h5>
                        <p class="card-text">나이 : {{only[0].age}}</p>
                        <p class="card-text">취미 : {{only[0].hobby}}</p>
                        <p class="card-text" >블로그 : {{only[0].blog}}</a></p>
                        <p class="card-text" style="margin-top: 10px;">부트캠프 다짐 : {{only[0].comment}}</p>
  ```
