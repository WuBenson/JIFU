from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext
from django import template
from website.models import ProjectInfo
from django.conf import settings
from website import forms
from django.core.mail import EmailMessage
from website import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.models import User
import os
import glob

# Create your views here.
def sitemap(request):
    template = get_template('sitemap.xml')
    html = template.render(locals())
    return HttpResponse(html)

def temp(request):
    template = get_template('temp.html')
    html = template.render(locals())
    return HttpResponse(html)

def aboutus(request):
    if 'username' in request.session:
        status = 'login'
        username = request.session['username']
    else:
        status = 'logout'
    template = get_template('aboutus.html')
    nbar = 'contact'
    html = template.render(locals())
    return HttpResponse(html)

def home(request):
    if 'username' in request.session:
        status = 'login'
        username = request.session['username']
    else:
        status = 'logout'
    template = get_template('home.html')
    nbar = 'home'
    html = template.render(locals())
    return HttpResponse(html)

def mail(request):
    if 'username' in request.session:
        status = 'login'
        username = request.session['username']
    else:
        status = 'logout'
    nbar = 'drop'
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            message = "感謝您的來信!"
            user_name = form.cleaned_data['user_name']
            user_city = form.cleaned_data['user_city']
            user_email = form.cleaned_data['user_email']
            user_phone = form.cleaned_data['user_phone']
            user_msg = form.cleaned_data['user_msg']

            mail_body = u'''
            網友姓名 : {}
            居住城市 : {}
            聯絡信箱 : {}
            聯絡電話 : {}
            反映意見 : 如下
            {}'''.format(user_name, user_city, user_email, user_phone, user_msg)
            email = EmailMessage('來自我的網站的網友提供意見', mail_body, user_email, ['jeff80228@gmail.com'])
            email.send()

        else:
            message = "請檢察您輸入的資訊是否正確!"
    else:
        form = forms.ContactForm()
        
    template = get_template('mail.html')
    html = template.render(context=locals(),request=request)
    return HttpResponse(html)

def hire(request):
    if 'username' in request.session:
        status = 'login'
        username = request.session['username']
    else:
        status = 'logout'
    template = get_template('hire.html')
    nbar = 'hire'
    html = template.render(locals())
    return HttpResponse(html)

def service(request):
    if 'username' in request.session:
        status = 'login'
        username = request.session['username']
    else:
        status = 'logout'
    template = get_template('service.html')
    nbar = 'news'
    infos = ProjectInfo.objects.order_by('-id')
    count = len(infos)
    media_url = settings.MEDIA_URL
    html = template.render(locals())
    return HttpResponse(html)

def show(request):
    if 'username' in request.session:
        status = 'login'
        username = request.session['username']
    else:
        status = 'logout'
    template = get_template('showImg.html')
    nbar = 'show'
    html = template.render(locals())
    return HttpResponse(html)

def adduser(request):
    if 'username' in request.session:
        status = 'login'
    else:
        status = 'logout'
    try:
        user = User.objects.get(username="test")
    except:
        user = None
    if user != None:
        message = user.username + "帳號已建立!"
        return HttpResponse(message)
    else:
        user = User.objects.create_user("test", "test@test.com.tw", "aa123456")
        user.first_name="chiacheng"
        user.last_name="wu"
        user.is_staff=True
        user.save()
        return redirect('/admin/')

def album(request):
    if 'username' in request.session:
        status = 'login'
        username = request.session['username']
        return redirect('/adminmain/')
    else:
        status = 'logout'
    nbar = 'show'
    albums = models.AlbumModel.objects.all().order_by('-id')
    totalalbum = len(albums)
    photos = []
    lengths = []
    for album in albums:
        photo = models.PhotoModel.objects.filter(palbum__atitle=album.atitle).order_by('-id')
        lengths.append(len(photo))
        if len(photo) == 0:
            photos.append('')
        else:
            photos.append(photo[0].pimg)
    return render(request, "album.html", locals())

def albumshow(request, albumid=None):
    if 'username' in request.session:
        status = 'login'
        username = request.session['username']
    else:
        status = 'logout'
    album = albumid
    photos = models.PhotoModel.objects.filter(palbum__id=albumid).order_by('-id')
    monophoto = photos[0]
    totalphoto = len(photos)
    return render(request, "albumshow.html", locals())

def albumphoto(request, photoid=None, albumid=None):
    if 'username' in request.session:
        status = 'login'
        username = request.session['username']
    else:
        status = 'logout'
    album = albumid
    photo = models.PhotoModel.objects.get(id=photoid)
    photo.save()
    return render(request, "albumphoto.html", locals())

def login(request):
    message = ''
    if request.method == 'POST':
        name = request.POST['username'].strip()
        password = request.POST['passwd']
        user1 = authenticate(username=name, password=password)
        if user1 is not None:
            if user1.is_active:
                if not 'username' in request.session:
                    request.session['username'] = name
                    request.session.set_expiry(3600)
                auth.login(request, user1)
                return redirect('/adminmain/')
            else:
                message = '帳號未被啟用!'
        else:
            message = '登入失敗'
    return render(request, "login.html", locals())

def logout(request):
    if 'username' in request.session:
        del request.session['username']
    auth.logout(request)
    return redirect('/home/', locals())

def adminmain(request, albumid=None):
    if 'username' in request.session:
        status = 'login'
        username = request.session['username']
    else:
        status = 'logout'
        return redirect('/home/')
    if albumid == None:
        albums = models.AlbumModel.objects.all().order_by('-id')
        totalalbum = len(albums)
        photos = []
        lengths = []
        for album in albums:
            photo = models.PhotoModel.objects.filter(palbum__atitle=album.atitle).order_by('-id')
            lengths.append(len(photo))
            if len(photo) == 0:
                photos.append('')
            else:
                photos.append(photo[0].pimg)
    else:
        album = models.AlbumModel.objects.get(id=albumid)
        photo = models.PhotoModel.objects.filter(palbum__atitle=album.atitle).order_by('-id')
        for photounit in photo:
            os.remove(photounit.pimg.path)
            photounit.delete()
        album.delete()
        return redirect('/adminmain/', locals())
    return render(request, "adminmain.html", locals())

def adminadd(request):
    if 'username' in request.session:
        status = 'login'
        username = request.session['username']
    else:
        status = 'logout'
        return redirect('/home/')
    message = ''
    title = request.POST.get('album_title', '')
    location = request.POST.get('album_location', '')
    desc = request.POST.get('album_desc', '')
    if title == '':
        message = '請填寫名稱'
    else:
        unit = models.AlbumModel.objects.create(atitle=title, alocation=location, adesc=desc)
        unit.save()
        return redirect('/adminmain/')
    return render(request, "adminadd.html", locals())

def adminfix(request, albumid=None, photoid=None, deletetype=None):
    if 'username' in request.session:
        status = 'login'
        username = request.session['username']
    else:
        status = 'logout'
        return redirect('/home/')
    album = models.AlbumModel.objects.get(id=albumid)
    photos = models.PhotoModel.objects.filter(palbum__id=albumid).order_by('-id')
    totalphoto = len(photos)
    if photoid != None:
        if photoid == 999999:
            album.atitle = request.POST.get('album_title', '')
            album.location = request.POST.get('album_location', '')
            album.adesc = request.POST.get('album_desc', '')
            album.save()
            files = []
            picurl = ["ap_picurl1", "ap_picurl2", "ap_picurl3", "ap_picurl4", "ap_picurl5"]
            for count in range(0,5):
                files.append(request.FILES.get(picurl[count], ''))
            for upfile in files:
                if upfile != '':
                    unit = models.PhotoModel.objects.create(palbum=album, pimg=upfile)
                    unit.save()
            return redirect('/adminfix/' + str(album.id) + '/')
        elif deletetype == 'delete':
            photo = models.PhotoModel.objects.get(id=photoid)
            os.remove(photo.pimg.path)
            photo.delete()
            return redirect('/adminfix/' + str(album.id) + '/')
    return render(request, "adminfix.html", locals())

def test(request):
    if 'username' in request.session:
        status = 'login'
        username = request.session['username']
        return redirect('/adminmain/')
    else:
        status = 'logout'
    nbar = 'show'
    filenum = getfilenum()
    location = getlocation()
    name = getname()
    totalnum = len(filenum)
    n = reversed(range(totalnum))
    z = zip(n, filenum, name, location)
    return render(request, "test.html", locals())

def testshow(request, filename=None, filenum=None):
    fileid = filename
    total = filenum
    title = getname(filename)
    location = getlocation(filename)
    content = getcontent(filename)
    n = range(1, total+1)
    return render(request, "testshow.html", locals())

def testalbum(request, fileid=None, pictureid=None):
    fid = fileid
    pid = pictureid
    pnext = pid + 1
    plast = pid - 1
    total = getfilenum(fid)
    title = getname(fid)
    return render(request, "testalbum.html", locals())

def getfilenum(index=None):
    filenum = [8,6,5,7,5,6,6,10,5,7,6,3,9,7,8,
        5,10,5,6,7,6,4,9,8,5,9,12,9,13,8,18,26,8,5,
        8,5,15,15,5,4,5,8,7,6,6,4,6,4,9,10,8,6,7,14
    ]
    
    if index != None:
        return filenum[index]
    else:
        filenum.reverse()
        return filenum

def getname(index=None):
    name = [
            "永信建設-新建案→R5新世界",
            "嘉義朴子市農會-稻穀烘乾中心",
            "高雄市原生植物園",
            "穎明工業股份有限公司-新建廠房&週邊環境工程營造",
            "岡山螺絲廠大老闆私人招待所",
            "國立台南高級工業職業學校",
            "萬吉山妍---全新登場心之境界綠嵐院墅(萬吉建設)",
            "湧盛電機股份有限公司",
            "崙上教會",
            "宗鉦企業股份有限公司",
            "永信建設-明頂大鎮-人行道",
            "第一場工場在屏東林邊",
            "茂新營造-廠區水泥塊板吊掛安裝",
            "路竹新建養護之家-透水磚、緣石鋪設工程",
            "路竹私人工作室停車空間-連鎖磚、界石鋪設工程",

            "A、B、C、D區停車格施工",
            "透水通風設計、拒蚊爬蟲動物騷擾、景觀再造活化",
            "宅院前透水散熱步道",
            "停車場植草磚&路緣石施工",
            "萬吉建設-里港建案",
            "拾光旅宿-植草磚工程",
            "甲頂營造公司-德陽軍艦委外經營管理案管理中心興建工程",
            "名威營造有限公司 FIGHT. K 教會",
            "偉倡營造有限公司- 土城仔排水整治工程",
            "芳源號營造股份有限公司-岡山魚市場新建工程",
            "泛亞工程建設股份有限公司-站前廣場及周邊景觀工程",
            "滿福庭建設有限公司-《豐邑築石》",
            "大型畜牧養豬場 地坪紅磚鋪設",
            "何董-住宅別墅庭院高壓磚地坪工程",
            "橋頭家賀-大港建設股份有限公司",
            "私人百坪住家別墅(低調奢華)---蔬果批發大商 施董",
            "碳佐麻里精品燒肉(時代店)",
            "天時地利人和三村集會所活動中心",
            "高雄市政府警察局湖內分局田寮分駐所",
            "林先生住家別墅",
            "萬吉建設股份有限公司-美濃雙峰段透天案",
            "杉林區家信仰中心-樂善堂周邊客家生活環境改造工程",
            "曾先生住家別墅",
            "台南市大勇街道連鎖磚翻新工程",
            "台南市忠義路一段連鎖磚翻新工程",
            "台南市胡美街177巷道平板磚鋪設工程",
            "台南市文祥街道平板磚鋪設工程",
            "107年度台南市孔廟南門路道路損壞搶修工程",
            "107年度台南市日新里活動中心門前廣場舊磚翻新工程(甲頂營造有限公司)",
            "台南市善化區-廠房新建工程高壓磚鋪設 (綠建材) (建築法申請跑照程序用)",
            "台南市安定區7-11善安門市",
            "甲頂營造有限公司",
            "佳里工業區大型廠房-利晉工程股份有限公司",
            "高雄市立大寮國民中學校舍改建第三期工程(升富營造有限公司)",
            "護理之家新建大樓周邊景觀",
            "里港鄉某砂石大廠(二期追加施做工程)",
            "知名豬隻畜牧大型養殖場",
            "美濃區代書庭園",
            "潮洲機廠整地及配合工程"

       ]

    if index != None:
        return name[index]
    else:
        name.reverse()
        return name

def getlocation(index=None):
    location = [
                "高雄鳳山福誠3街",
                "嘉義-朴子市",
                "高雄市政德路",
                "高雄市湖內區",
                "高雄市-岡山區",
                "台南市-永康區",
                "九如鄉",
                "前鎮加工出口區",
                "屏東縣長治鄉",
                "台南關廟",
                "高雄市鳳山區-頂明路",
                "屏東著名建設公司：萬吉建設",
                "台南市-城西垃圾焚化廠",
                "高雄市-路竹區中華路",
                "高雄市-路竹區仁愛路",

                "高雄市-楠梓高中",
                "高雄市-大社區大智街-醫師自用別墅",
                "屏東縣-內埔鄉和興路 透天民宿",
                "高雄市-彌陀區 安永生物科技公司(新廠）",
                "屏東縣-里港鄉 永豐路二段",
                "台南市-安平區 安北路",
                "台南市-安平區 安億路121號",
                "高雄市-橋頭區 (鄰青埔捷運站)",
                "台南市安南區安清路一段",
                "高雄市岡山區嘉新東路1巷",
                "鳳山火車站-高雄市鳳山區曹公路68號",
                "屏東縣萬丹鄉廣安路230巷68弄",
                "高雄市路竹區-下坑",
                "高雄市杉林區",
                "高雄市橋頭區瑞祥二街17號",
                "美濃區外六寮",
                "高雄市前鎮區南一路85號",
                "屏東縣枋寮鄉建興路260號",
                "高雄市田寮區崗安路71-2號",
                "高雄市美濃區廣興街林宅",
                "高雄市美濃區雙峰段",
                "高雄市杉林區桐竹路241號",
                "高雄市美濃區曾宅",
                "台南市大勇街",
                "台南市忠義路一段",
                "台南市湖美街177巷道",
                "台南市文祥街",
                "台南市南門路",
                "台南市南區利南街136號",
                "台南市善化區",
                "台南市安定區蘇林村7號",
                "台南市西港區",
                "台南市佳里工業區",
                "高雄市大寮區進學路150號",
                "屏東縣內埔鄉昭勝路安平1巷1號",
                "屏東縣里港鄉",
                "高雄市路竹區下坑",
                "高雄市美濃區",
                "屏東縣潮州鎮"

           ]

    
    if index != None:
        return location[index]
    else:
        location.reverse()
        return location

def getcontent(index=None):
    content = [
			"人行道地磚鋪設、路緣石鋪設",
            "採用特別圍牆磚樣式→仿岩千面磚",
            "圍牆磚施工- 完工現況",
            "路緣石、連鎖磚 -鋪設(含工含料)",
            "全區鋪設約1000平方公尺進口花崗石材",
            "鈑金科教室鋪設磨石磚（採用水泥黏貼工法）",
            "高壓連鎖磚及植草磚 車道庭園景觀工程",
            "基地整理、襯砂 緣石、平板磚鋪設施工",
            "基地開挖、整理 土方廢棄物清除",
            "基地整理、襯沙 拆除舊磚、重鋪平板新磚(20x20cm)",
            "基地整理、襯沙、夯實 鋪設平板磚(30x30、60x30 cm) 含工含材料（統包工程）",
            "施工項目：圍牆(百歲磚)",
            "基地整理、襯沙、吊掛安裝 安裝1米 x 1米 (四方)水泥塊板 專業機具與經驗豐富師傅 合力施工",
            "基地整理、襯二分沙 20 x 20 x 6 (cm) 平板透水磚 (附綠建材、環保標章證明) 燁昇工程行 專業山貓機具襯沙 協力施工",
            "基地整理、襯二分沙、24x12x 6 (cm) BM連鎖磚、地界泥作土水補強",

            "界石、路緣石、車阻、平板磚、含工帶料、機具，全方位服務",
            "庭院維護、花草樹木移栽整修(含運棄)、連鎖磚鋪設、含工帶料、機具，全方位服務施工",
            "景觀地坪美化、平板磚鋪設",
            "景觀地坪美化、植草磚鋪設回沃土與植草(含工帶料、機具，全方位服務施工)",
            "圍牆磚(百歲磚）施工(景觀圍牆綠化 增添溫暖簡樸生活風)",
            "植草磚24x24x8 連工帶料植草施工(景觀綠化 增添旅宿青翠生活風)",
            "高壓混凝土透水磚20*20*6(環保標章)，四百多平方公尺山貓整地，鋪面施工",
            "30*30*6 高壓透水磚 ， 客製熊造型鋪面、收邊界石施工工程(含磚、襯沙、機具)",
            "40*60*15 坡崁(連鎖式)植草磚，含回沃土植草",
            "100*20/15*27 cm 路緣石施工",
            "透水混凝土底層(綠建材)、鋪設高壓透水地磚(綠建材)、公分化粧蓋板磚裁切黏貼",
            "[含工帶料] 圍牆磚(百歲磚) 施工、空心磚(口字磚) 施工",
            "地坪-紅磚鋪設黏貼 施工 (含工帶料、機具，全方位服務施工)",
            "[含工帶料] 混鋪 高壓連鎖磚施工、邊界石施工",
            "[含工帶料] 24*24*8植草磚(螃蟹磚)、圍牆磚(百歲磚)",
            "[含工帶料] 規劃設計、基地回填夯實整理、挖掘埋設路緣石界隔、60*30*6、30*30*6、20*20*6平板磚鋪設",
            "1.水準高程測量、放樣 2.數百米路緣石劃分法定停車格位區隔收邊 3.數百立方級配回填、注水澆灌、壓路機反覆行走夯實 4.特殊施作工法三角磚 廣場步道舖面 5.法定透水車格植草磚鋪設(含回沃土、植草) 6.店前廣場出入口轉彎角施工 7.周邊人行步道修繕整理 8.食材新鮮、料風味美、環境佳",
            "平板磚、路緣石、界石(含料施工)、收邊路緣石施作、60*60*6高壓平板磚鋪設",
            "30*30*6平板磚損壞拆除，基礎重新整理補修(半天)",
            "景觀規劃造型設計、路緣界石鋪設、30*30*6高壓平板磚鋪設(含山貓基底整理、級配粒料底層夯實、襯二分砂石、水泥)",
            "[含工帶料] 39*9.5*9cm圍牆百歲磚施作(含上層帽蓋)、磚柱灌漿",
            "1.步道及休憩廣場鋪面2.客庄廣場及入口鋪面3.花台、樹穴界石，路緣石施作4.圓形休憩廣場鋪面(山貓基底整理、級配粒料底層夯實、襯二分砂石、水泥、沙)",
            "景觀規劃造型設計、路緣界石鋪設、高壓平板磚鋪設(含山貓基底整理、級配粒料底層夯實、襯二分砂石、水泥)",
            "24*12*6 (cm) 高壓連鎖磚施工",
            "24*12*6 (cm) 高壓連鎖磚施工",
            "20*20*8 (cm) 高壓噴砂平板磚施工",
            "24*12*6 (cm) 高壓連鎖磚施工",
            "1.舊磚拆除 2.夯實強化基底耐重承受度 3.基底襯沙整平 4.20*20*8(cm) 高壓平板磚磚鋪設",
            "1.舊磚拆除運棄 2.基地基礎整理 3.高程測量(洩水方向、坡度) 4.襯沙整平 3. 24*12*6高壓連鎖磚鋪設",
            "基地整地、鋪設“綠建材”高壓平板磚20*20*6、附備-綠建材文件證明 (建築法申請跑照程序用，後續拆除)",
            "1.基地基礎整理 2.高程測量(洩水方向、坡度) 3.界石埋設 4.襯沙整平 5. 24*12*6高壓連鎖磚鋪設 6.平板夯實、人工掃縫",
            "1.基地山貓整地、磚料二次搬運 2.高程測量(洩水方向、坡度) 3.襯砂壓尺整平 4. 20*10*6 洗石子界石埋設黏固 5. 24*24*8 植草烏龜磚鋪設 6.人工沃土回沃、植栽草皮",
            "1.基地整地、磚料搬運 2.高程測量(洩水方向、坡度) 3.襯砂、整平 4. 24*24*8植草磚鋪設",
            "1.基地基礎整理 2.高程測量(洩水方向、坡度) 3.界石、路緣石埋設 4.襯沙整平 5. 24*12*6高壓連鎖磚、10*10*6高壓磚鋪設 6.平板夯實、人工掃縫",
            "1.基地基礎整理 2.高程測量(洩水方向、坡度) 3.路緣石埋設 4.襯沙、乾拌水泥砂整平 5. 10*10*6高壓磚鋪設 6.平板夯實、人工掃縫",
            "1.基地基礎整理 2.高程測量(洩水方向、坡度) 3.路緣石埋設 4.襯二分砂石整平 5. 20*20*8高壓磚鋪設 6.平板夯實、人工掃縫 7.仿岩面花台磚疊砌(圍牆磚一期工程)",
            "1.基地基礎整理 2.高程測量(洩水方向、坡度) 3.紅磚收邊 4.蓄水養護 5..基底整平 6. 窯燒紅磚鋪面 7.澆灌養護 8.機具整面、人工掃縫",
            "1.基地基礎整理 2.高程測量(洩水方向、坡度) 3.界石埋設 4.襯二分砂石整平 5. 24*24*6高壓連鎖磚鋪設 6.平板夯實、人工掃縫",
            "1.RC基座整平 2.高程測量 3.防崁磚運移 4.機具帶特工吊掛安裝 5. 輔具校準調整 6.卵石裝填 7.背擋回填"
          ]

    
    if index != None:
        return content[index]
    else:
        content.reverse()
        return content