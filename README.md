# 팀소개 웹페이지 만들기
![api 명세](https://github.com/joungheunKim/take_part_in_team-project/assets/132051740/c2352311-e306-40cc-8937-9e32a5557966)

참여 : 김종현(팀장), 이수현, 김주승
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
하지만 MongoDB에서 데이터를 find할 때 ObjectId를 사전에 String타입으로 가져오는 방법이 없어 iteration을 통해 따로 ObjectId 타입을 변경해주는 추가 작업이 필요했는데 이 기능들을 구현하기에는 기술력도 받쳐주지않고 다른 기능을 구현하는 시간이 부족하여 다른 방법을 찾아보았다.

```
<button type="button" onclick="location.href='/gocard/${name}'"><span class="ir">더보기</span></button>
 ```
메인페이지에 노출되는 작은 미니카드에서 개인카드로 넘어가는 버튼에서 가져온 이름${name}을 사용하였다.

@app.route('/gocard/<memberNamed>')
def gocard(memberNamed):
  only_memberd = list(db.teams.find({'name':memberNamed},{'_id':False}))
    
  return render_template('card.html',only = only_memberd)

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
                        <p class="card-text" >블로그 : {{only[0].blog}}</p>
                        <p class="card-text" style="margin-top: 10px;">부트캠프 다짐 : {{only[0].comment}}</p>
  ```
이때, 블로주소가 표시만되었기에 링크를 걸어주고 싶다고 생각하였고
```
    <p class="card-text" >블로그 : <a href="{{only[0].blog}}">{{only[0].blog}}</a></p>
```
    <a> 태그를 활용하여 하이퍼링크까지 걸어 주었다.
        
## 구현 내용
등록한 정보 삭제

### 과정
먼저 삭제버튼을 만든후 버튼에 member_delete()란 함수를 걸어주었다.
        <button onclick="member_delete()" type="button">팀원 삭제</button>
        
        그리고 
        function member_delete() {
            let name = '{{only[0].name}}'
            fetch(`/teams/${name}`, { method: "DELETE" }).then((res) => res.json()).then((data) => {
                alert(data['msg'])
            })
        }
        
        정보의 name 값을 보내주어
        ```
        @app.route("/teams/<name>", methods=["DELETE"])
            def teams_delete(name):

            db.teams.delete_one({'name':name})

            return jsonify({'msg':'삭제 완료!'})
        ```
        name 값이 같은 데이터를 delete 요청을 보내주었다.
        
        MongoDB에서 자동으로 생성해주는 ObjectId 타입의 '_id'컬럼이 아닌 name이란 값으로 삭제를 하였기에
        같은 개인페이지로 넘어가는 방법과 같이 같은 값을 가진 정보가 삭제될 우려가있다.
        
        추후 'id_'칼럼을 사용하는 방법을 익힐필요가있다고 생각한다.
        
## 구현 내용
        등록된 정보수정
        
        ### 과정
        팀원 수정이라는 이름의 버튼을 생성한 후에 업데이트가 가능한 새페이지로 이동시켜주었다.
        <button onclick="location.href='/goupdate/{{only[0].name}}'" type="button">팀원 수정 </button>
        이때, 개인페이지로 이동과 같은 방식으로 업데이트를 하는 정보값만 새페이지로 보내주었다.
        그후 수정된 값은 POST 방식과 비슷하게 작성하였다
        ```
        <script>
        function updating(){
            let name = $('#name').val();
            let age = $('#age').val();
            let hobby = $('#hobby').val();
            let blog = $('#blog').val();
            let comment = $('#comment').val();
            let image = $('#image').val();

            let formData = new FormData();
            formData.append("name_give", name);
            formData.append("age_give", age);
            formData.append("hobby_give", hobby);
            formData.append("blog_give", blog);
            formData.append("comment_give", comment);
            formData.append("image_give", image);

            fetch('/teamsUpdate/{{onlyone[0].name}}', { method: "UPDATE", body: formData }).then((res) =>   res.json()).then((data) => {
                alert(data['msg'])
                window.location.href = '/'
            })
        }

    </script>

        
        fetch('/teamsUpdate/{{onlyone[0].name}}에서 {{onlyone[0].name}}값을 updateName으로 받아
```

        
@app.route("/teamsUpdate/<updateName>", methods=["UPDATE"])
    def teams_update(updateName):
    name_receive = request.form['name_give']
    age_receive = request.form['age_give']
    hobby_receive = request.form['hobby_give']
    blog_receive = request.form['blog_give']
    comment_receive = request.form['comment_give']
    image_receive = request.form['image_give']
    db.teams.update_one({'name':updateName}, 
        {"$set":{'name':name_receive, 'age':age_receive, 'hobby':hobby_receive,
        'blog':blog_receive,'comment':comment_receive,'image':image_receive}});
    return jsonify({'msg':'수정 완료!'})
```
set 함수로 묶은뒤 {'name':updateName} db에서 name이 updateName와 같은 정보를
현제 보내주는 정보로 업데이트 하게끔 하였다.        
이 역시 위에 구현한 방법들과 같은 이유로 'name' 이름값이 동일한 정보가 있을 경우
같은 이름값의 정보도 수정될 수 있다는 문제점이 있다.

        
## 구현 내용
        이미지 업로드 및 이미지 다운로드
        
### 시행착오들
        input type="file"로 파일을 선택할 수 있는 기능을 추가하여 그 정보를 그대로 db에 저장하면 되는 것인줄 알았다.
        
