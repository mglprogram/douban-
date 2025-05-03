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
# sessionId 加密
app.secret_key = 'this is session_key you know ?'


@app.route('/login', methods=['GET', 'POST'])
def login(): # 登录
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        request.form = dict(request.form) # 转换表单数据为字典

        # 定义过滤函数：检查邮箱和密码是否匹配数据库记录
        def filter_fn(item):
            return request.form['email'] in item and request.form['password'] in item

        users = query.querys('select * from user', [], 'select') # 查询所有用户
        filter_user = list(filter(filter_fn, users)) # 过滤匹配的用户

        if len(filter_user): # 如果找到匹配用户
            session['email'] = request.form['email'] # 将邮箱存入session（标记为已登录）
            return redirect('/home') # 重定向到主页
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

        # 定义过滤函数：检查邮箱是否已注册
        def filter_fn(item):
            return request.form['email'] in item

        users = query.querys('select * from user', [], 'select')
        filter_list = list(filter(filter_fn, users))
        # 如果邮箱已存在
        if len(filter_list):
            return render_template('passwordError.html', message='用户已被注册')
        else: # 注册新用户
            # 将新用户插入数据库
            query.querys('insert into user(email,password) values(%s,%s)',
                         [request.form['email'], request.form['password']])
            return redirect('/login')


@app.route('/home', methods=['GET', 'POST'])
def home():
    # 从session获取当前登录用户的email
    email = session.get('email')
    # 获取首页需要的统计数据
    maxMovieLen, maxRate, maxActors, maxCountry, maxTypes, maxLang = getHomeData()
    # 获取电影类型分布数据（用于ECharts图表）
    typeEchartsData = getTypesEchartsData()
    # 获取评分分布数据（用于ECharts图表）
    row, columns = getRateEchartsData()
    # 获取表格展示数据
    tableData = getTableData()
    # 渲染模板并传递所有数据
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


@app.route('/search/<movieName>', methods=['GET', 'POST'])
def search(movieName):
    email = session.get('email')
    if request.method == 'GET':
        # 通过电影名精确查询
        resultData = getMovieDetailById(movieName)
    else:
        # POST请求：通过关键词模糊搜索
        request.form = dict(request.form)
        resultData = getMovieDetailBySearchWord(request.form['searchWord'])
    return render_template('search.html', resultData=resultData, email=email)


@app.route('/time')
def time():
    # 获取年份分布数据（返回年份列表和对应电影数量列表）
    row, columns = getYearData()
    # 获取电影时长分布数据
    movieTimeData = getMovieTimeData()
    email = session.get('email')
    return render_template('time.html', email=email, row=row, columns=columns, movieTimeData=movieTimeData)


@app.route('/rate/<type>', methods=['GET', 'POST'])
def rate(type):
    # 获取用户邮箱和所有电影类型
    email = session.get('email')
    typeList = getAllType()
    # 获取当前类型的评分分布
    row, columns = getAllRateDataByType(type)
    # 获取年度平均评分
    yearMeanRow, yearMeanColumns = getYearMeanData()
    # 处理搜索请求
    if request.method == 'GET':
        starData, searchName = getStars("哪吒之魔童闹海") # 默认搜索
    else:
        request.form = dict(request.form)
        starData, searchName = getStars(request.form['searchIpt']) # 用户输入搜索

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
    # 获取国家分布数据（国家列表和电影数量列表）
    row, columns = getMapData()
    # 获取语言分布数据（语言列表和电影数量列表）
    langRows, langColumns = getLangData()
    print("langRows:", langRows)  # 调试输出
    print("langColumns:", langColumns)
    return render_template('/map.html', email=email, row=row, columns=columns, langRows=langRows, langColumns=langColumns)


@app.route('/type_m')
def type_m():
    email = session.get('email')
    # 获取类型统计数据
    typesData = getTypeData()
    return render_template('type_m.html', email=email, typesData=typesData)


@app.route('/actor')
def actor():
    email = session.get('email')
    # 获取导演TOP20数据
    row, columns = getDirectorsDataTop20()
    # 获取演员TOP20数据
    actorsRow, actorsColumns = getActorsDataTop20()
    return render_template('actor.html', email=email, row=row, columns=columns,
                           actorsRow=actorsRow, actorsColumns=actorsColumns)


@app.route('/table/<movieName>')
def table(movieName):
    email = session.get('email')
    # 获取电影表格数据
    tableData = getTableDataByTablePage()
    # 如果movieName不是'0'（表示有具体电影要删除）
    if movieName != '0':
        # 调用删除函数删除指定电影
        delMovieByMovieName(movieName)
        return redirect('/table/0')
    return render_template('table.html', email=email, tableData=tableData)


@app.route('/comments', methods=['GET', 'POST'])
def comments():
    email = session.get('email')
    # 处理GET请求（首次加载页面）
    if request.method == 'GET':
        # 处理POST请求（用户提交搜索表单）
        return render_template('comments.html', email=email)
    else:
        # 1. 从表单获取搜索关键词
        # 2. 调用getCommentsImage生成词云图片
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


@app.before_request # Flask装饰器，在每次请求前执行此函数
def before_request():
    # 匹配以 / static开头的路径（静态资源）
    pat = re.compile(r'^/static')
    # 2. 检查当前请求路径是否需要跳过认证
    if re.search(pat, request.path) or request.path in ['/','/login', '/register']:
        return # 如果是静态资源或白名单路径，直接放行
    # 3. 获取session中的email（用户登录标识）
    uname = session.get('email')
    if uname:  # 如果用户已登录
        return None  # 放行请求
    return redirect('/login')



@app.route('/')
def allRequest():
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
