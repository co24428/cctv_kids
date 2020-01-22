from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

cursor = connection.cursor()
#BLOB 읽기용
from base64 import b64encode # byte배열을 base64로 변경함.
import pandas as pd
from .models import cctv_data # 해당 모델에 직접 연결, SQL 안써도 되게끔
from .models import article
from .models import user_table
from .models import favorite
from .models import article_scrap
import time

import pandas as pd
import glob

# graph
import matplotlib.pyplot as plt
import io # byte로 변환
import base64 # byte배열을 base64로 변경함.
from matplotlib import font_manager, rc # 한글 폰트 적용
from django.db.models import Sum, Max, Min, Count, Avg

# Create your views here.


def big_addr_list():
    rows_tmp = cctv_data.objects.all().values("big_addr")
    tmp = set()
    for i in rows_tmp:
        tmp.add(i['big_addr'])
    b_addr_list = list(tmp)
    b_addr_list.sort()
    return b_addr_list

def small_addr_list(big_addr):
    rows_tmp = cctv_data.objects.all().values("small_addr")
    tmp = set()
    for i in rows_tmp:
        tmp.add(i['small_addr'])
    s_addr_list = list(tmp)
    s_addr_list.sort()
    return s_addr_list

def chart_total(request):

    font_name = font_manager.FontProperties\
        (fname='C:/Windows/Fonts/gulim.ttc').get_name() # 폰트읽기
    rc('font', family=font_name) # 폰트적용
    plt.rcParams['figure.figsize']= (14, 4)

    if request.method == 'GET':
        
        # row = cctv_data.objects.big_addr.values("전라북도") => 어트리뷰트에 속한 값을 모두 가져오는 것
        # SELECT * FROM cctv WHERE big_addr='전라북도'
        addr_list = cctv_data.objects.all().values("big_addr")
        

        big_set = set()
        for tmp in addr_list:
            if tmp['big_addr'] == "소재지 미상" or tmp['big_addr'] == "충청북도청주시" or tmp['big_addr'] == "용인구":
                continue
            big_set.add(tmp['big_addr'])

        big_list = list(big_set)
        big_list.sort()
        # addr_list = ['서울특별시','인천광역시','경기도','강원도','울산광역시','경상북도','경상남도','부산광역시','대구광역시','전라북도', '전라남도','충청남도','충청북도']
        list_for_yn = list()
        for tmp_addr in big_list:

            row = cctv_data.objects.filter(big_addr=tmp_addr).values("cctv_yn")

            tmp = []

            for i in row:
                tmp.append(str(i['cctv_yn']))
                # print(tmp)

            print ("total : ",len(tmp))
            print ("Y : ",tmp.count("Y"))
            print ("N : ",tmp.count("N"))

            tot = len(tmp)
            y_num = tmp.count("Y")

            y_percent = round((y_num / tot) * 100,2)
            list_for_yn.append(y_percent)
            

        plt.title("< CCTV 도별 설치 비율 >")
        plt.xlabel("< 도 >")
        plt.ylabel("< 퍼센트 >")
    
        plt.bar(big_list,list_for_yn)

        plt.draw()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img_url = base64.b64encode(img.getvalue()).decode()

        plt.close()


        list_for_num =list()
        for tmp_addr1 in big_list:
            row1 = cctv_data.objects.filter(big_addr=tmp_addr1).aggregate(Avg("cctv_num"))
            list_for_num.append(row1['cctv_num__avg'])
        
        plt.title("< CCTV 설치대수 평균 >")
        plt.xlabel("< 도 >")
        plt.ylabel("< 평균 >")

        plt.bar(big_list,list_for_num)
        plt.draw()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img_url1 = base64.b64encode(img.getvalue()).decode()

        plt.close()

    return render(request, "chart/total.html", \
        {"graph1":'data:;base64,{}'.format(img_url), "graph2":'data:;base64,{}'.format(img_url1), \
          "big_list":big_list  })

def chart_big(request):

    font_name = font_manager.FontProperties\
        (fname='C:/Windows/Fonts/gulim.ttc').get_name() # 폰트읽기
    rc('font', family=font_name) # 폰트적용
    plt.rcParams['figure.figsize']= (14, 4)


    if request.method == 'GET':

        big = request.GET.get("big", "경상남도")

        if big == "경기도":
            plt.rcParams['figure.figsize']= (15, 4)


        test3 = list()
        addr_list = cctv_data.objects.filter(big_addr=big).values("small_addr")
        

        tmp_set = set()
        for tmp in addr_list:
            if tmp['small_addr'] != "시흥로":
                tmp_set.add(tmp['small_addr'])
                # tmp['small_addr'][:len(tmp['small_addr'])-1]
            else:
                continue

        tmp_list = list(tmp_set)
        tmp_list.sort()

        tmp_min_list = list()
        for i in tmp_list:
            tmp_min_list.append(i[:len(i)-1])
        
        tmp_list_tuple = list()
        for i in range(0,len(tmp_list),2):
            try:
                tmp_tuple = (tmp_list[i], tmp_list[i+1])
                tmp_list_tuple.append(tmp_tuple)
            except:
                tmp_tuple = (tmp_list[i],)
                tmp_list_tuple.append(tmp_tuple)

        # tmp_min_list_tuple = list()
        # for i in range(0,len(tmp_min_list),2):
        #     if tmp_min_list[i+1]:
        #         tmp_min_tuple = tuple(tmp_min_list[i], tmp_min_list[i+1])
        #         tmp_min_list_tuple.append(tmp_min_tuple)
        #     else:
        #         tmp_min_tuple = tuple(tmp_min_list[i])
        #         tmp_min_list_tuple.append(tmp_min_tuple)

        


        for tmp_addr in tmp_list:
            row2 = cctv_data.objects.filter(big_addr=big , small_addr=tmp_addr).values("cctv_yn")
            
            list1 = list()
            for i in row2:
                list1.append(i['cctv_yn'])

            tot = len(list1)
            y_num = list1.count("Y")
            y_percent = round((y_num / tot) * 100,2)
            test3.append(y_percent)

        plt.title("< CCTV 설치여부 >")
        plt.xlabel("X축")
        plt.ylabel("Y축")
        if big =="경기도":
            plt.bar(tmp_min_list,test3)
        else:
            plt.bar(tmp_list,test3)

        plt.draw()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img_url = base64.b64encode(img.getvalue()).decode()

        plt.close()

        # ##############
        test2 = list()

        for tmp_addr2 in tmp_list:
            row1 = cctv_data.objects.filter(big_addr=big , small_addr=tmp_addr2).aggregate(Avg("cctv_num"))

            test2.append(row1['cctv_num__avg'])
            
        print(test2)

        
        plt.title("CCTV 설치대수")
        plt.xlabel("X축")
        plt.ylabel("Y축")
        
        if big =="경기도":
            plt.bar(tmp_min_list,test2)
        else:
            plt.bar(tmp_list,test2)

        plt.draw()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img_url1 = base64.b64encode(img.getvalue()).decode()

        plt.close()
    
  


        return render(request, 'chart/big.html',\
             {"graph1":'data:;base64,{}'.format(img_url), "graph2":'data:;base64,{}'.format(img_url1), "small_list":tmp_list_tuple, "big": big})

def chart_small(request):
    font_name = font_manager.FontProperties\
    (fname='C:/Windows/Fonts/gulim.ttc').get_name() # 폰트읽기
    rc('font', family=font_name) # 폰트적용
    plt.rcParams['figure.figsize']= (12, 4)


    if request.method == 'GET':

        big = request.GET.get("big", "부산광역시") 
        small = request.GET.get("small", "기장군")

        test4 = list()
        test5 = list()

        tmp_addr = cctv_data.objects.filter(big_addr=big ,small_addr=small).values("cctv_yn")
        # print(tmp_addr)
        

        tmp = []

        for i in tmp_addr:
            tmp.append(str(i['cctv_yn']))
            # print(tmp)

        tot1 = len(tmp)
        y_num1 = tmp.count("Y")
        y_percent1 = round((y_num1 / tot1) * 100,2)
        test4.append(y_percent1)
    
        print(test4)

        tot2 = len(tmp)
        n_num1 = tmp.count("N")
        n_percent1 = round((n_num1 / tot2) * 100,2)
        test5.append(n_percent1)
    
        print(test5)


        group_names = ['Y', 'N']
        group_sizes = [test4, test5]
        group_colors = ['lightskyblue', 'lightcoral']
        group_explodes = (0, 0) # explode 1st slice
        
        plt.pie(group_sizes,
            explode=group_explodes,
            labels=group_names, 
            colors=group_colors, 
            autopct='%1.2f%%', # second decimal place
            shadow=False, 
            startangle=90,
            textprops={'fontsize': 14}) # text font size
        plt.axis('equal')
        plt.title("< 시군구별 여부 >", fontsize=20)

        plt.draw()
        img = io.BytesIO() # img에 byte배열로 보관
        plt.savefig(img, format="png") # png파일 포맷으로 저장
        img_url = base64.b64encode(img.getvalue()).decode()
        plt.close() # 그래프 종료

        # ###########################################################

        test6 = list()
        test7 = list()

        tmp_addr = cctv_data.objects.filter(big_addr=big ,small_addr=small).values("cctv_num")
        # print(tmp_addr)

        for i in tmp_addr:
            test6.append(str(i['cctv_num']))
        # print(test6)

        tmp_set = set()
        for tmp in test6:
            tmp_set.add(tmp)
        # print(tmp_set)

        tmp_list1 = list(tmp_set)
        for i in range(len(tmp_list1)):
            tmp_list1[i] = int(tmp_list1[i])
        tmp_list1.sort()
        
        for i in range(len(tmp_list1)):
            tmp_list1[i] = str(tmp_list1[i])
    

        for i in tmp_list1:
            num = test6.count(i)
            test7.append(num)
        print(test7)

        plt.title("< 시군구별 대수 비교 >")
        plt.xlabel("< 시군구 >")
        plt.ylabel("< 대수 >")

        plt.bar(tmp_list1,test7,width=0.25, bottom=0.25, align='center',label='A', color='g', edgecolor='gray',linewidth=0.5 )


        plt.draw()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img_url1 = base64.b64encode(img.getvalue()).decode()

        plt.close()

        #   ##################################################
        test8 = list()
        test9 = list()

        tmp_addr = cctv_data.objects.filter(big_addr=big ,small_addr=small).values("sisul")

        for i in tmp_addr:
            test8.append(str(i['sisul']))

        tmp_set = set()
        for tmp in test8:
            tmp_set.add(tmp)

        tmp_list = list(tmp_set)
        tmp_list.sort()
        for i in tmp_list:
            num = test8.count(i)
            test9.append(num)

        plt.title("< 시군구 시설갯수 >")
        plt.xlabel("< 시설 >")
        plt.ylabel("< 갯수 >")

        plt.bar(tmp_list,test9,width=0.25, bottom=0.25, align='center',label='A', color='g', edgecolor='gray',linewidth=0.5 )

        plt.draw()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img_url2 = base64.b64encode(img.getvalue()).decode()

        plt.close()
        
        # small_addr이랑 user_id가 favorite에 있는지 확인
        # bool값으로 전달 (1, 0)
        
        # SELECT NO FROM CCTV_CCTV_DATA  WHERE big_addr='전라남도' and small_addr='고흥군' and rownum <=1
        row2 = cctv_data.objects.filter(big_addr=big, small_addr=small).values('no')
        check_no = row2[0]['no']
        # SELECT * FROM CCTV_FAVORITE WHERE REGION_NO_ID= check_no and USER_ID_ID=request.session['user_id']
        check_fav = ""
        try:
            check_fav = favorite.objects.filter(region_no=check_no, user_id=request.session['user_id'])
            if check_fav:
                check_fav = True
            else:
                check_fav = False
        except:
            pass


    return render(request, 'chart/small.html', \
        {"graph1":'data:;base64,{}'.format(img_url), "graph2":'data:;base64,{}'.format(img_url1),\
         "graph3":'data:;base64,{}'.format(img_url2), "big":big, "small":small, "check_fav": check_fav})

def chart_favorite(request):
    big = request.GET.get("big", "") 
    small = request.GET.get("small", "")

    # SELECT * FROM CCTV_USER_TABLE WHERE user_id=request.session['user_id']
    row1 = user_table.objects.get(user_id=request.session['user_id'])
    print(row1)
    fav_usr = row1

    # GET 1개 -= 객체
    #     여러개 - 에러 안뱉음

    # filter 1개 = 그 데이터
    #        여러개 = 객체의 리스트


    # SELECT NO FROM CCTV_CCTV_DATA  WHERE big_addr='전라남도' and small_addr='고흥군' and rownum <=1
    row2 = cctv_data.objects.filter(big_addr=big, small_addr=small)
    fav_reg = row2[0]
    print(fav_usr)
    # print(fav_reg)

    print(type(request.session['user_id']))
    obj = favorite()
    obj.region_no = fav_reg
    obj.user_id = fav_usr
    obj.save()  
    # INSERT INTO CCTV_FAVORITE(REGION_NO_ID, USER_ID_ID) VALUES ( fav_reg , request.session['user_id'] )

    return redirect("/cctv/chart/small?big="+ big + "&small=" + small)

def chart_unfavorite(request):
    big = request.GET.get("big", "") 
    small = request.GET.get("small", "")

    # SELECT NO FROM CCTV_CCTV_DATA  WHERE big_addr='전라남도' and small_addr='고흥군' and rownum <=1
    row2 = cctv_data.objects.filter(big_addr=big, small_addr=small).values('no')
    check_no = row2[0]['no']

    # DELETE FROM CCTV_FAVORITE WHERE REGION_NO_ID= check_no and USER_ID_ID=request.session['user_id']
    favorite.objects.get(region_no=check_no, user_id=request.session['user_id']).delete()
    return redirect("/cctv/chart/small?big="+ big + "&small=" + small)


def chart_barplt(request):
    rows_tmp = cctv_data.objects.filter(big_addr="강원도").values("cctv_yn")
    tmp = list()
    for i in rows_tmp:
        tmp.append(i['cctv_yn'])
    tmp.sort()
    print(tmp)
    total = len(tmp)
    Y_num = 0; N_num = 0
    for i in tmp:
        if i =="Y":
            Y_num += 1
        elif i == "N":
            N_num += 1
    print(total)
    print(Y_num)
    print(N_num)
    


    x = ['total', 'Y', 'N']
    y = [total, Y_num, N_num]
    plt.bar(x,y)
    plt.title("please")
    plt.xlabel("X축")
    plt.ylabel("Y축")

    plt.draw()
    img = io.BytesIO() # img에 byte배열로 보관
    plt.savefig(img, format="png") # png파일 포맷으로 저장
    img_url = base64.b64encode(img.getvalue()).decode()
    plt.close() # 그래프 종료

    return render(request, "chart/barplt.html",{"graph1":'data:;base64,{}'.format(img_url)})


def chart_list(request):
    print(big_addr_list())
    print(small_addr_list("경상남도"))

    # rows = cctv_data.objects.filter(big_addr="경상남도", small_addr="김해시")
    rows = cctv_data.objects.filter(big_addr="경상남도")
    print(rows)
    return render(request, 'chart/list.html',{"list":rows}) 


def article_insert(request):
    """
        나중에 혼자서 합시다~~~
    """
    return HttpResponse("Dont try this")

def add_csv():
    # C:/Users/admin/Desktop/project/cctv_kids/kidscctv/static/csv
    # path = r'C:/Users/admin/Desktop/python_crawling/python_crawling/project/resources' # use your path
    path = 'C:/Users/admin/Desktop/project/cctv_kids/kidscctv/static/csv'
    # path = 'C:/Users/admin/Desktop/project/cctv_kids/kidscctv/static/csv_tmp'
    all_files = glob.glob(path + "/*.csv")

    li = []

    for filename in all_files:
        try:
            df = pd.read_csv(filename, index_col=None, header=0, encoding="euc-kr")
        except:
            df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    return frame


def chart_insert(request):
    frame = add_csv()
    # 168번째 행 가져오기
    # print(frame.iloc[168]) 
    # 필요한 열 가져오기
    # print( frame.loc[:, ['CCTV설치대수', 'CCTV설치여부', '소재지지번주소', '시설종류']] )
    # 168, 170번째 행 / 필요한 열 가져오기
    # print( frame.loc[[168, 170], ['CCTV설치대수', 'CCTV설치여부', '소재지지번주소', '시설종류']] )

    # addr = frame.loc[:, ['소재지지번주소']].values[0][0].split(" ")
    big_addr = list()
    small_addr = list()
    sisul = list()
    cctv_yn = list()
    cctv_num = list()
    
    # big_addr / small_addr
    addr = frame.loc[:, ['소재지지번주소']].values
    for tmp in addr:
        try:
            big_addr.append(tmp[0].split(" ")[0])
            small_addr.append(tmp[0].split(" ")[1])
        except:
            big_addr.append("소재지 미상")
            small_addr.append("소재지 미상")

    # cctv_yn
    cctvYN = frame.loc[:, ['CCTV설치여부']].fillna("N").values
    for tmp in cctvYN:
        data = ""
        if tmp[0] == "설치":
            data = "Y"
        elif tmp[0] == "미설치":
            data = "N"
        else:
            data = tmp[0].upper()
        cctv_yn.append(data)

    #cctv_num
    cctvNum = frame.loc[:, ['CCTV설치대수']].fillna(0).values
    for tmp in cctvNum:
        cctv_num.append(int(tmp[0]))

    #sisul
    sisul_all = frame.loc[:, ['시설종류']].fillna(0).values
    for tmp in sisul_all:
        sisul.append(tmp[0])

    # for i in range(0, len(sisul)):
    #     print(i)
    #     obj = cctv_data()
    #     obj.big_addr = big_addr[i]
    #     obj.small_addr = small_addr[i]
    #     obj.cctv_yn = cctv_yn[i]
    #     obj.cctv_num = cctv_num[i]
    #     obj.sisul = sisul[i]
    #     obj.save()

    return HttpResponse("Dont try this")

# 메인 - 준형
def main_index(request):
    if request.method == 'GET':
        return render(request, 'main/index.html')

@csrf_exempt 
def main_join(request):
    if request.method == 'GET':
        return render(request, 'main/join.html')
    elif request.method == 'POST':
        if request.POST["password"] == request.POST["password1"]:
            obj = user_table()
            obj.user_id = request.POST['user_id']
            obj.name = request.POST['name']
            obj.password = request.POST['password']
            obj.age = request.POST['age']
            obj.home = request.POST['home']
            obj.save()
            """
            ar = [request.POST['user_id'], request.POST['name'], request.POST['password'], request.POST['age'], request.POST['home']]
            sql = "INSERT INTO MEMBER(ID,NAME,PW,AGE,HOME) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql,ar)
            """
            return redirect("/cctv/main/index")
        else:
            return render(request, 'main/join.html', {'error': 'Incorrect password'})

def main_login(request):
    if request.method == 'GET':
        return render(request, 'main/login.html')
    elif request.method == 'POST':
        id = request.POST['user_id']
        pw = request.POST['password']
        ar = [id,pw]
        sql = """
            SELECT user_id, password
            FROM CCTV_USER_TABLE
            WHERE user_id=%s AND password=%s
        """
        cursor.execute(sql, ar)
        data = cursor.fetchone()

        if data:
            request.session['user_id'] = data[0]
            request.session['password'] = data[1]
            return redirect("/cctv/main/index")
        return redirect("/cctv/main/login")

@csrf_exempt
def main_logout(request):
    if request.method=='GET' or request.method=='POST':
        del request.session['user_id']
        del request.session['password']
        return redirect('/cctv/main/index')

@csrf_exempt
def main_mypage(request):
    if request.method == 'GET' :
        return render(request, 'main/mypage.html')

# 기사 - 지윤

def article_main(request):
    if request.method == 'GET':
        page = int(request.GET.get("page",1))    
        list1 = article.objects.all()[page*6-6:page*6]
        cnt = article.objects.all().count()
        total = (cnt-1)//6+1    

        # 스크랩 했는지 확인
        # SELECT * FROM ARTICLE_SCRAP WHERE user_id=로그인한 아이디 and art_no=해당 기사 기본키


        return render(request,'article/main.html',{"list":list1, "pages":range(1,total+1,1), "page": page} )

     
def article_scrap1(request):
    no = request.GET.get("no", "") 
    page = request.GET.get("page", "") 

    # SELECT * FROM CCTV_USER_TABLE WHERE user_id=request.session['user_id']

    row1 = user_table.objects.get(user_id=request.session['user_id'])
    print(row1)
    scr_usr = row1

    # SELECT * FROM CCTV_ARTICLE WHERE no=no
    row2 = article.objects.get(no=no)
    print(row2)
    scr_art = row2

    obj = article_scrap()
    # obj.scrap_date = "SYSDATE" # YYYY-MM-DD
    obj.scrap_date = "2020-01-01" # YYYY-MM-DD
    obj.article_no = scr_art 
    obj.user_id = scr_usr
    obj.save()  

    return redirect("/cctv/article/main?page="+page)


def main_myfav(request):

    # SELECT region_no FROM favorite where user_id= sessrion id
    rows = favorite.objects.filter(user_id=request.session['user_id']).values("region_no")
    
    list_tmp = list()
    for i in rows:
        list_tmp.append(i['region_no'])

    # SELECT big_addr, small_addr FROM cctv_data WHERE no in(list_tmp)
    big_list = list()
    small_list = list()
    for i in list_tmp:
        # SELECT big_addr, small_addr FROM cctv_data WHERE no=i
        big_list.append  ( cctv_data.objects.filter(no=i).values("big_addr")[0]["big_addr"] )
        small_list.append( cctv_data.objects.filter(no=i).values("small_addr")[0]["small_addr"] )

    addr_list = list()
    for i in range(len(big_list)):
        addr = big_list[i] + " " + small_list[i]
        addr_list.append(addr)
    
    final_list = list()
    for i in range(len(addr_list) ):
        dic1 = dict()
        dic1["big"] = big_list[i]
        dic1["small"] = small_list[i]
        dic1["addr"] = addr_list[i]
        final_list.append(dic1)
    
    return render(request,'main/myfav.html',{"final":final_list})


def main_myscrap(request):
    # SELECT region_no FROM favorite where user_id= sessrion id
    rows = article_scrap.objects.filter(user_id=request.session['user_id']).values("article_no")

    list_tmp = list()
    for i in rows:
        list_tmp.append(i['article_no'])

    title_list = list()
    link_list = list()
    for i in list_tmp:
        title_list.append( article.objects.filter(no=i).values("title")[0]["title"] )
        link_list.append( article.objects.filter(no=i).values("link")[0]["link"] )
    
    final_list = list()
    for i in range(len(link_list) ):
        dic1 = dict()
        dic1["title"] = title_list[i]
        dic1["link"] = link_list[i]
        final_list.append(dic1)
    
    return render(request,'main/myscrap.html',{"final":final_list})