from flask import Flask, request, render_template, session, redirect, abort
from utils import query
from utils.getHomeData import *
from utils.getSearchData import *
from utils.getTimeData import *
from utils.getRateData import *
from utils.getMapData import *
from utils.getTypeData import *
from utils.getActorsData import *
from utils.getTableData import *
from utils.getCommentsData import *

app = Flask(__name__)
app.secret_key = 'this is session_key you know ?'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        request.form = dict(request.form)

        def filter_fn(item):
            return request.form['email'] in item and request.form['password'] in item

        users = query.querys('select * from user', [], 'select')
        filter_user = list(filter(filter_fn, users))

        if len(filter_user):
            session['email'] = request.form['email']
            return redirect('/home')
        else:
            return render_template('passwordError.html', message='邮箱或者密码错误')


@app.route('/loginOut')
def loginOut():  # 退出登录清除session
    session.clear()
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        request.form = dict(request.form)
        # 第一次密码和第二次密码是否相同
        if request.form['password'] != request.form['passwordChecked']:
            return render_template("passwordError.html", message='输入的两次密码不相同')

        def filter_fn(item):
            return request.form['email'] in item

        users = query.querys('select * from user', [], 'select')
        filter_list = list(filter(filter_fn, users))
        if len(filter_list):
            return render_template('passwordError.html', message='用户已被注册')
        else:
            query.querys('insert into user(email,password) values(%s,%s)',
                         [request.form['email'], request.form['password']])
            return redirect('/login')


@app.route('/home', methods=['GET', 'POST'])
def home():
    email = session.get('email')
    maxMovieLen, maxRate, maxActors, maxCountry, maxTypes, maxLang = getHomeData()
    typeEchartsData = getTypesEchartsData()
    row, columns = getRateEchartsData()
    tableData = getTableData()
    return render_template(
        'index.html',
        email=email,
        maxMovieLen=maxMovieLen,
        maxRate=maxRate,
        maxActors=maxActors,
        maxCountry=maxCountry,
        maxTypes=maxTypes,
        maxLang=maxLang,
        typeEchartsData=typeEchartsData,
        row=row,
        columns=columns,
        tableData=tableData

    )


# @app.route('/movie/<movieName>')
# def movie(movieName):
#     movieUrl = getMovieUrlByName(movieName)
#     return render_template('movie.html', movieUrl=movieUrl)


@app.route('/search/<movieName>', methods=['GET', 'POST'])
def search(movieName):
    email = session.get('email')
    if request.method == 'GET':
        resultData = getMovieDetailById(movieName)
    else:
        request.form = dict(request.form)
        resultData = getMovieDetailBySearchWord(request.form['searchWord'])
    return render_template('search.html', resultData=resultData, email=email)


@app.route('/time')
def time():
    row, columns = getYearData()
    movieTimeData = getMovieTimeData()
    email = session.get('email')
    return render_template('time.html', email=email, row=row, columns=columns, movieTimeData=movieTimeData)


@app.route('/rate/<type>', methods=['GET', 'POST'])
def rate(type):
    email = session.get('email')
    typeList = getAllType()
    row, columns = getAllRateDataByType(type)
    yearMeanRow, yearMeanColumns = getYearMeanData()
    if request.method == 'GET':
        starData, searchName = getStars("边水往事")
    else:
        request.form = dict(request.form)
        starData, searchName = getStars(request.form['searchIpt'])

    return render_template('rate.html',
                           email=email,
                           typeList=typeList,
                           type=type,
                           row=row,
                           columns=columns,
                           starData=starData,
                           searchName=searchName,
                           yearMeanRow=yearMeanRow,
                           yearMeanColumns=yearMeanColumns
                           )


@app.route('/map')
def map():
    email = session.get('email')
    row, columns = getMapData()
    langRow, langColumns = getLangData()
    return render_template('/map.html', email=email, row=row, columns=columns, langRow=langRow, langColumns=langColumns)


@app.route('/type_m')
def type_m():
    email = session.get('email')
    typesData = getTypeData()
    return render_template('type_m.html', email=email, typesData=typesData)


@app.route('/actor')
def actor():
    email = session.get('email')
    row, columns = getDirectorsDataTop20()
    actorsRow, actorsColumns = getActorsDataTop20()
    return render_template('actor.html', email=email, row=row, columns=columns,
                           actorsRow=actorsRow, actorsColumns=actorsColumns)


@app.route('/table/<movieName>')
def table(movieName):
    email = session.get('email')
    tableData = getTableDataByTablePage()
    if movieName != '0':
        delMovieByMovieName(movieName)
        return redirect('/table/0')
    return render_template('table.html', email=email, tableData=tableData)


@app.route('/comments', methods=['GET', 'POST'])
def comments():
    email = session.get('email')
    if request.method == 'GET':
        return render_template('comments.html', email=email)
    else:
        resSrc,searchName = getCommentsImage(dict(request.form)['searchIpt'])
        return render_template('comments.html', email=email, resSrc=resSrc, searchName=searchName)


@app.route('/title')
def title():
    email = session.get('email')
    return render_template('title.html', email=email)

@app.route('/summary')
def summary():
    email = session.get('email')
    return render_template('summary.html', email=email)


@app.route('/actorName')
def actorName():
    email = session.get('email')
    return render_template('actorName.html', email=email)


@app.before_request
def before_request():
    pat = re.compile(r'^/static')
    if re.search(pat, request.path) or request.path in ['/login', '/register']:
        return
    # uname = session.get('email')
    # if uname:
    #     return None
    # return redirect('/login')
    uname = session.get('email', None)
    if uname:
        return None
    abort(401)  # 401 Unauthorized


@app.route('/')
def allRequest():
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
