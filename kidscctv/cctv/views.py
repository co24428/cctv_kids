from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
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
    print(big_addr_list())
    print(small_addr_list("경상남도"))

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
    
    group_names = ['Y_group', 'N_group']
    group_sizes = [Y_num, N_num]
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
    plt.title("Pie graph test", fontsize=20)

    plt.draw()
    img = io.BytesIO() # img에 byte배열로 보관
    plt.savefig(img, format="png") # png파일 포맷으로 저장
    img_url = base64.b64encode(img.getvalue()).decode()
    plt.close() # 그래프 종료

    return render(request, "chart/total.html",{"graph1":'data:;base64,{}'.format(img_url)})

def chart_circleplt(request):
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
    
    group_names = ['Y_group', 'N_group']
    group_sizes = [Y_num, N_num]
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
    plt.title("Pie graph test", fontsize=20)

    plt.draw()
    img = io.BytesIO() # img에 byte배열로 보관
    plt.savefig(img, format="png") # png파일 포맷으로 저장
    img_url = base64.b64encode(img.getvalue()).decode()
    plt.close() # 그래프 종료

    return render(request, "chart/circleplt.html",{"graph1":'data:;base64,{}'.format(img_url)})


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