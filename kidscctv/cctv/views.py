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


def chart_total(request):

    file = open("C:/Users/admin/Desktop/project/SchoolZone-2.jpg", "rb")
    img = file.read()
    img64 = b64encode(img).decode("utf-8")
    final_image = "data:;base64,{}".format(img64)

    font_name = font_manager.FontProperties\
        (fname='C:/Windows/Fonts/gulim.ttc').get_name() # 폰트읽기
    rc('font', family=font_name) # 폰트적용
    plt.rcParams['figure.figsize']= (14, 4)



    if request.method == 'GET':
        

        addr_list = cctv_data.objects.all().values("big_addr")
        
        big_set = set()
        for tmp in addr_list:
            if tmp['big_addr'] == "소재지 미상" or tmp['big_addr'] == "충청북도청주시" or tmp['big_addr'] == "용인구" or tmp['big_addr'] == "대구광역시?서구?원대동3가":
                continue
            big_set.add( tmp['big_addr'] )

        big_list = list(big_set)
        big_list.sort()

        list_for_yn = list()
        for tmp_addr in big_list:
            
            row = cctv_data.objects.filter(big_addr=tmp_addr).values("cctv_yn")

            tmp = []

            for i in row:
                tmp.append(str(i['cctv_yn']))

            tot = len(tmp)
            y_num = tmp.count("Y")

            y_percent = (y_num / tot) * 100
            list_for_yn.append(y_percent)
            

        plt.title("< CCTV 도별 설치 비율 >")
        plt.xlabel("< 도 >")
        plt.ylabel("< 퍼센트 >")
    
        plt.bar(big_list,list_for_yn, color='gold')

        plt.draw()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img_url = base64.b64encode(img.getvalue()).decode()

        plt.close()
        #####################################################

        list_for_num =list()
        for tmp_addr1 in big_list:
            row1 = cctv_data.objects.filter(big_addr=tmp_addr1).aggregate(Avg("cctv_num"))
            list_for_num.append(row1['cctv_num__avg'])
        
        plt.title("< CCTV 설치대수 평균 >")
        plt.xlabel("< 도 >")
        plt.ylabel("< 평균 >")

        plt.bar(big_list,list_for_num ,color='gold')
        plt.draw()
        img = io.BytesIO()
        plt.savefig(img, format='png')  
        img_url1 = base64.b64encode(img.getvalue()).decode()

        plt.close()

    return render(request, "chart/total.html", \
        {"graph1":'data:;base64,{}'.format(img_url), "graph2":'data:;base64,{}'.format(img_url1), \
          "big_list":big_list ,"image": final_image})

def chart_big(request):

    file = open("C:/Users/admin/Desktop/project/SchoolZone-2.jpg", "rb")
    img = file.read()
    img64 = b64encode(img).decode("utf-8")
    final_image = "data:;base64,{}".format(img64)

    font_name = font_manager.FontProperties\
        (fname='C:/Windows/Fonts/gulim.ttc').get_name()
    rc('font', family=font_name)
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
            else:
                continue

        tmp_list = list(tmp_set)
        tmp_list.sort()
        ###########################
        tmp_min_list = list()
        for i in tmp_list:
            tmp_min_list.append(i[:len(i)-1])
        ########################
        tmp_list_tuple = list()
        for i in range(0,len(tmp_list),2):
            try:
                tmp_tuple = (tmp_list[i], tmp_list[i+1])
                tmp_list_tuple.append(tmp_tuple)
            except:
                tmp_tuple = (tmp_list[i],)
                tmp_list_tuple.append(tmp_tuple)

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
            plt.bar(tmp_min_list,test3, width=0.5, bottom=0.25, align='center',label='A', color='gold',linewidth=0.5)
        else:
            plt.bar(tmp_list,test3, width=0.5, bottom=0.25, align='center',label='A', color='gold',linewidth=0.5)

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
            

        
        plt.title("< CCTV 설치대수 >")
        plt.xlabel("X축")
        plt.ylabel("Y축")
        
        if big =="경기도":
            plt.bar(tmp_min_list,test2, width=0.5, bottom=0.25, align='center',label='A', color='gold',linewidth=0.5)
        else:
            plt.bar(tmp_list,test2, width=0.5, bottom=0.25, align='center',label='A', color='gold',linewidth=0.5)

        plt.draw()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img_url1 = base64.b64encode(img.getvalue()).decode()

        plt.close()
    
  


        return render(request, 'chart/big.html',\
             {"graph1":'data:;base64,{}'.format(img_url), "graph2":'data:;base64,{}'.format(img_url1), "small_list":tmp_list_tuple, "big": big, "image": final_image })

def chart_small(request):

    file = open("C:/Users/admin/Desktop/project/SchoolZone-2.jpg", "rb")
    img = file.read()
    img64 = b64encode(img).decode("utf-8")
    final_image = "data:;base64,{}".format(img64)



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
    
        tot2 = len(tmp)
        n_num1 = tmp.count("N")
        n_percent1 = round((n_num1 / tot2) * 100,2)
        test5.append(n_percent1)

        group_names = ['Y', 'N']
        group_sizes = [test4, test5]
        group_colors = ['gold', 'beige']
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

        plt.title("< 시군구별 대수 비교 >", fontsize=20)
        plt.xlabel("< 시군구 >")
        plt.ylabel("< 대수 >")

        plt.bar(tmp_list1,test7,width=0.5, bottom=0.25, align='center',label='A', color='gold',linewidth=0.5 )


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

        plt.title("< 시군구 시설갯수 >" , fontsize=20)
        plt.xlabel("< 시설 >")
        plt.ylabel("< 갯수 >")

        plt.bar(tmp_list,test9,width=0.25, bottom=0.25, align='center',label='A', color='gold' ,linewidth=0.5 )

        plt.draw()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img_url2 = base64.b64encode(img.getvalue()).decode()

        plt.close()

        
            # row1 = cctv_data.objects.filter(big_addr=tmp_addr1).aggregate(Avg("cctv_num"))

        # #### 시설 그래프 c3용
        sisul_list = tmp_list
        sisul_num  = test9
        sisul_y    = list()

        # SELECT cctv_yn FROM cctv_data WHERE big_addr=경상남도 and small_addr=김해시 and sisul=유치원
        for one in sisul_list:
            tmp = cctv_data.objects.filter(big_addr=big ,small_addr=small, sisul=one, cctv_yn="Y").count()
            sisul_y.append(tmp)



        
        # small_addr이랑 user_id가 favorite에 있는지 확인
        # bool값으로 전달 (1, 0)
        
        # SELECT NO FROM CCTV_CCTV_DATA  WHERE big_addr='전라남도' and small_addr='고흥군' and rownum <=1
        row2 = cctv_data.objects.filter(big_addr=big, small_addr=small).values('no')
        check_no = row2[0]['no']
        # SELECT * FROM CCTV_FAVORITE WHERE REGION_NO_ID= check_no and USER_ID_ID=request.session['user_id']
        check_fav = False
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
         "graph3":'data:;base64,{}'.format(img_url2), "big":big, "small":small, "check_fav": check_fav, \
         "image": final_image , "y": y_num1 , "n": tot1-y_num1, \
         "sisul_list": sisul_list, "sisul_num": sisul_num, "sisul_y": sisul_y  })

def chart_favorite(request):
    big = request.GET.get("big", "") 
    small = request.GET.get("small", "")

    row1 = user_table.objects.get(user_id=request.session['user_id'])
    fav_usr = row1

    row2 = cctv_data.objects.filter(big_addr=big, small_addr=small)
    fav_reg = row2[0]

    obj = favorite()
    obj.region_no = fav_reg
    obj.user_id = fav_usr
    obj.save()  
    return redirect("/cctv/chart/small?big="+ big + "&small=" + small)

def chart_unfavorite(request):
    big = request.GET.get("big", "") 
    small = request.GET.get("small", "")

    row2 = cctv_data.objects.filter(big_addr=big, small_addr=small).values('no')
    check_no = row2[0]['no']

    favorite.objects.get(region_no=check_no, user_id=request.session['user_id']).delete()
    return redirect("/cctv/chart/small?big="+ big + "&small=" + small)

def add_csv():
    path = 'C:/Users/admin/Desktop/project/cctv_kids/kidscctv/static/csv'
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
    addr = frame.loc[:, ['소재지지번주소']].values # 경상남도 김해시 ~~
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
        rows1 = article_scrap.objects.filter(user_id=request.session['user_id']).values("article_no")

        scr_no_list = list()
        for i in rows1:
            scr_no_list.append( i["article_no"] )
        


        return render(request, 'main/mypage.html', {"scr_no_list":scr_no_list})

@csrf_exempt
def main_idfind(request):
    if request.method == 'GET':
        return render(request, 'main/idfind.html')
    elif request.method == 'POST':
        na = request.POST['name']
        ag = request.POST['age']
        ar = [na,ag]
        print(ar)
        sql = """
            SELECT USER_ID, NAME, AGE
            FROM CCTV_USER_TABLE
            WHERE name=%s AND age=%s
        """
        cursor.execute(sql, ar)
        data = cursor.fetchone()
        print(data)

        if data:
            return render(request, 'main/login.html', {'user_id': data[0]})
            #return redirect('/cctv/main/idsuccess')
        else:
            return render(request, 'main/idfind.html', {'error': 'Incorrect Information'})
        
def main_pwfind(request):
    if request.method == 'GET':
        return render(request, 'main/pwfind.html')
    elif request.method == 'POST':
        na = request.POST['name']
        ag = request.POST['age']
        id = request.POST['user_id']
        ar = [na,ag,id]
        sql = """
            SELECT password
            FROM CCTV_USER_TABLE
            WHERE name=%s AND age=%s AND user_id=%s
        """
        cursor.execute(sql, ar)
        data = cursor.fetchone()
        print(data)
        
        if data:
            return render(request, 'main/login.html', {'user_pw': data[0]})
            #return redirect('/cctv/main/idsuccess')
        else:
            return render(request, 'main/pwfind.html', {'error': 'Incorrect Information'})


# 기사 - 지윤
def article_main(request):
    if request.method == 'GET':

        # ####################################################
        # 세션 유저가 스크랩한 기사 리스트
        # Html 보내고
        # 거기 안에 기사 번호가 있으면
        # 스크랩 버튼 바꿔주기
        # Unscrap url 생성

        page = int(request.GET.get("page",1))    
        list1 = article.objects.all()[page*6-6:page*6]
        cnt = article.objects.all().count()
        total = (cnt-1)//6+1    

        row1 = article_scrap.objects.filter(user_id=request.session['user_id']).values("article_no")
        scr_no_list = list()
        for i in row1:
            scr_no_list.append( i["article_no"] ) # [ 2, 4, 6]

        return render(request,'article/main.html',{"list":list1, "pages":range(1,total+1,1), "page": page, "scr_no_list": scr_no_list} )

def article_scr_list(request):
    blank_list = list()
    scr_no_list = request.GET.get("scr_no_list", blank_list) # "[1,2,3,4,5]"
    if scr_no_list == "[]" or not scr_no_list:
        list1 = list()
    else:
        tmp_list = scr_no_list[1:-1].split(", ") # "[1, 2, 3, 4, 5]" -> ["1", "2", "3"]
        for i in range(len(tmp_list)):
            tmp_list[i] = int(tmp_list[i])

        # User.objects.filter(id__in=[1, 5, 34, 567, 229])
        list1 = article.objects.filter(no__in=tmp_list)

    row1 = article_scrap.objects.filter(user_id=request.session['user_id']).values("article_no")
    scr_no_list = list()
    for i in row1:
        scr_no_list.append( i["article_no"] )

    return render(request,'article/scr_list.html', {"list":list1, "scr_no_list": scr_no_list})

def article_unscrap1_scr(request): 
    no = request.GET.get("no", "") 

    # DELETE FROM article_scrap WHERE article_no= no and USER_ID_ID=request.session['user_id']
    article_scrap.objects.get(article_no=no, user_id=request.session['user_id']).delete()

    rows1 = article_scrap.objects.filter(user_id=request.session['user_id']).values('article_no')
    scr_no_list = list()
    for i in rows1:
        scr_no_list.append( i["article_no"] )
    url = "/cctv/article/scr_list?scr_no_list=["
    for i in scr_no_list:
        url = url + str(i) + ", "
    url = url[:len(url)-2] + "]"
    return redirect(url)

def article_scrap1(request):
    no = request.GET.get("no", "") 
    page = request.GET.get("page", "") 

    # SELECT * FROM CCTV_USER_TABLE WHERE user_id=request.session['user_id']

    row1 = user_table.objects.get(user_id=request.session['user_id'])
    scr_usr = row1

    # SELECT * FROM CCTV_ARTICLE WHERE no=no
    row2 = article.objects.get(no=no)
    scr_art = row2

    obj = article_scrap()
    # obj.scrap_date = "SYSDATE" # YYYY-MM-DD
    # obj.scrap_date = "2020-01-01" # YYYY-MM-DD
    obj.article_no = scr_art 
    obj.user_id = scr_usr
    obj.save()  

    return redirect("/cctv/article/main?page="+page)

def article_unscrap1(request):
    no = request.GET.get("no", "") 
    page = request.GET.get("page", ) 

    # DELETE FROM article_scrap WHERE article_no= no and USER_ID_ID=request.session['user_id']
    article_scrap.objects.get(article_no=no, user_id=request.session['user_id']).delete()
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

