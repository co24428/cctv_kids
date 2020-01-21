from selenium import webdriver
import urllib. request
import time
import cx_Oracle as oci

conn = oci.connect('admin_mpj/1234@192.168.99.100:32764/xe', encoding="UTF-8", nencoding="UTF-8")
cursor = conn.cursor()

options = webdriver.ChromeOptions()

options.add_argument('headless')
options.add_argument("disable-gpu")   
options.add_argument("lang=ko_KR")    
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

# 각자 경로 맞춰서
driver = webdriver.Chrome("C:\\Users\\admin\\Desktop\\python_crawling\\python_crawling\\chromedriver.exe", chrome_options=options)

# 20개 
# 1페이지
url1 = "http://www.newsis.com/search/schlist/?val=%25EC%2596%25B4%25EB%25A6%25B0%25EC%259D%25B4%25EB%25B3%25B4%25ED%2598%25B8%25EA%25B5%25AC%25EC%2597%25AD&sort=acc&jo=sub&bun=all_bun&sdate=&term=allday&edate=&s_yn=Y&catg=1&t=1&page=1&"
# 2페이지
url2 = "http://www.newsis.com/search/schlist/?val=%25EC%2596%25B4%25EB%25A6%25B0%25EC%259D%25B4%25EB%25B3%25B4%25ED%2598%25B8%25EA%25B5%25AC%25EC%2597%25AD&sort=acc&jo=sub&bun=all_bun&sdate=&term=allday&edate=&s_yn=Y&catg=1&t=1&page=2&"
# 3페이지
url3 = "http://www.newsis.com/search/schlist/?val=%25EC%2596%25B4%25EB%25A6%25B0%25EC%259D%25B4%25EB%25B3%25B4%25ED%2598%25B8%25EA%25B5%25AC%25EC%2597%25AD&sort=acc&jo=sub&bun=all_bun&sdate=&term=allday&edate=&s_yn=Y&catg=1&t=1&page=3&"
url_list = [url1, url2, url3]
# url_list = [url1]

title = list()
link = list()
content = list()
reporter = list()
date = list()

for url in url_list:
    driver.get(url)

    print("start")



    articles = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[3]/ul')
    article = articles.find_elements_by_class_name('bundle')
    for tmp in article:
        title.append(tmp.find_element_by_tag_name("a").text.replace("'", " "))
        link.append(tmp.find_element_by_tag_name("a").get_attribute("href"))
        content.append( (tmp.find_element_by_class_name("txt1").text[:100].replace("'", " ") + "..."))
        reporter_date = tmp.find_element_by_class_name('date').text.split("|")
        reporter.append(reporter_date[0].strip())
        date.append(reporter_date[1].strip())


# print("="*50)
# print("title")
# print("="*50)
# for i in title:
#     print(i)

# print("="*50)
# print("reporter")
# print("="*50)
# for i in reporter:
#     print(i)

# print("="*50)
# print("date") # YYYY.MM.DD HH:MI
# print("="*50)
# for i in date:
#     print(i)

# print("="*50)
# print("content")
# print("="*50)
# for i in content:
#     print(i)

# print("="*50)
# print("link")
# print("="*50)
# for i in link:
#     print(i)


# pdf = open('hello.pdf', 'rb')
# mem_file = io.BytesIO(pdf.read())


thumbnail = list()
for i in range(0,60):
    path = "static/img/art_thumnail/"
    full_path = path + 'newsis' + str(i) + '.png'
    # print(full_path)
    try:
        file = open(full_path, 'rb')
        img = file.read()
        print(len(img))
        thumbnail.append(img)
    except:
        thumbnail.append(None)

# print("="*50)
# print("thumbnail")
# print("="*50)
# for i in thumbnail:
#     print(i)


for i in range(0,60):
    # sql = "INSERT INTO CCTV_ARTICLE(TITLE, PUB_DATE, REPORT, CONTENT, LINK, THUMBNAIL) VALUES('" \
    #     + title[i] +"', TO_DATE('" + date[i] + "', 'YYYY.MM.DD HH24:MI'), '" \
    #     + reporter[i] + "', '" + content[i] + "', '" + link[i] + "', :0 )"
#    
    print("===================================================")
    if thumbnail[i]:
        sql = "INSERT INTO CCTV_ARTICLE(TITLE, PUB_DATE, REPORT, CONTENT, LINK, THUMBNAIL) VALUES('" \
        + title[i] +"', TO_DATE('" + date[i] + "', 'YYYY.MM.DD HH24:MI'), '" \
        + reporter[i] + "', '" + content[i] + "', '" + link[i] + "', :0 )"
        print(sql)

        cursor.execute(sql, [thumbnail[i]])
    else:
        sql = "INSERT INTO CCTV_ARTICLE(TITLE, PUB_DATE, REPORT, CONTENT, LINK) VALUES('" \
        + title[i] +"', TO_DATE('" + date[i] + "', 'YYYY.MM.DD HH24:MI'), '" \
        + reporter[i] + "', '" + content[i] + "', '" + link[i] + "')"
        print(sql)

        cursor.execute(sql)
#

conn.commit()


# 이미지가 필요할 때
# idx = 40
# for i in link:
#     driver.get(i)
#     time.sleep(1)
#     tmp = driver.find_element_by_xpath('//*[@id="textBody"]')
#     img_table = tmp.find_element_by_tag_name('table')
#     try:
#         file = img_table.find_element_by_tag_name('img').get_attribute("src")
#         # path부분 각자 경로 맞게 변경
#         path = "C:/Users/admin/Desktop/project/cctv_kids/kidscctv/static/img/art_thumnail/"
#         file_name = "newsis" + str(idx) + ".png"
#         urllib.request.urlretrieve(file, path + file_name)
#         print("image save!!")
#         idx += 1
#     except Exception as e:
#         idx += 1
#         continue