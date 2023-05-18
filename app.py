from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@joungheun.fsxjost.mongodb.net/?retryWrites=true&w=majority')
db =client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gojoin')
def gojoin():
    return render_template('join.html')

@app.route('/gocard/<memberNamed>')
def gocard(memberNamed):
    only_memberd = list(db.teams.find({'name':memberNamed},{'_id':False}))
    
    return render_template('card.html',only = only_memberd)


@app.route("/teams", methods=["POST"])
def teams_post():
    name_receive = request.form['name_give']
    age_receive = request.form['age_give']
    hobby_receive = request.form['hobby_give']
    blog_receive = request.form['blog_give']
    comment_receive = request.form['comment_give']
    image_receive = request.form['image_give']
    
    doc = {
        'name':name_receive,
        'age':age_receive,
        'hobby':hobby_receive,
        'blog':blog_receive,
        'comment':comment_receive, 
        'image':image_receive
    }
    db.teams.insert_one(doc)

    return jsonify({'msg':'저장 완료!'})

@app.route("/teams", methods=["GET"])
def teams_get():
    all_teams = list(db.teams.find({},{'_id':False}))
    return jsonify({'result': all_teams})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)