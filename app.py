from flask import Flask, render_template, request, flash
import pymysql
from pymysql.connections import DEBUG

# 차후 해야할 부분 : 입력 조건 및 Alert, Pagination, 데이터통계 안된 부분, 검색 다양화, 소셜로그인, 쓰기 삭제 제한 만들기, CNN

db = pymysql.connect(host="database-project.c7coyxstoq3r.ap-northeast-2.rds.amazonaws.com", user="aib03sji", password="aib03sji", db="project", charset="utf8")
curs = db.cursor()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# CREATE
@app.route('/add', methods=['POST', 'GET'])
def add_car():
    if request.method == 'POST':
        sql_create = "INSERT INTO car(model,num1,word,num2,kind) VALUES (%s, %s, %s, %s, %s)"
        curs.execute(sql_create, (request.form['model'], request.form['num1'], request.form['word'], request.form['num2'], request.form['kind']))
        db.commit()
    return render_template('add.html')


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# READ
@app.route('/list', methods=['GET'])
def car_list():
    sql_all = "SELECT * FROM car"
    curs.execute(sql_all)
    rows = curs.fetchall()
    return render_template('list.html', car_list=rows)

# READ (SEARCH)
@app.route('/search', methods=['GET', 'POST'])
def car_search():
    if request.method == 'GET':
        num2 = request.args.get('searchword', default=0000)   # request.form['searchword']
        sql_search = "SELECT * FROM car WHERE num2='{}'".format(num2)
        curs.execute(sql_search)
        searchlist = curs.fetchall()
    return render_template('search.html', search_list=searchlist)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# UPDATE
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'GET':
        id = request.args.get('carid', default=1)
        sql_update = "SELECT * FROM car WHERE id='{}'".format(id)
        curs.execute(sql_update)
        editlist = curs.fetchall()
    return render_template('update.html', edit_list=editlist)

# UPDATE(EDIT)
@app.route('/edit', methods=['GET'])
def edit():
    if request.method == 'GET':
        id = request.args.get('carid', default=1)
        value1 = request.args.get('value1')
        value2 = request.args.get('value2', default=00)
        value3 = request.args.get('value3', default='영')
        value4 = request.args.get('value4', default=0000)
        value5 = request.args.get('value5')

        sql_edit = "UPDATE car SET model='{}', num1='{}', word='{}', num2='{}', kind='{}' WHERE id='{}'".format(value1, value2, value3, value4, value5, id)
        curs.execute(sql_edit)
        db.commit()
    return render_template('edit.html')


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# DELETE
@app.route('/delete')
def del_car():
    if request.method == 'GET':
        id = request.args.get('carid', default=1)
        sql_del = "DELETE FROM car WHERE id = '{}'".format(id)
        curs.execute(sql_del)
        db.commit()
    return render_template('delete.html')


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# DATA ANALYSIS
@app.route('/data2')
def data2():
    count1 = 7 # "SELECT COUNT (CASE WHEN model='K5' THEN 1 END) FROM car"
    # count2 = "SELECT * FROM car"
    # count3 = "SELECT * FROM car"

    return render_template('classification2.html', count1=count1)







''''''''' flask run for EC2 ''''''''''''

flask run --host=0.0.0.0 --port=5000

'''''''''''''''''''''''''''''''''''''''