from flask import Flask, request, render_template, redirect, url_for

# from flask_mysqldb import MySQL
# import MySQLdb.cursors
import numpy as np
import re
import pickle
import translators.server as tss
from db_connection import add_prediction, get_data

app = Flask(__name__)


model = pickle.load(open("RFmodel.pkl", "rb"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    features = [float(i) for i in request.form.values()]
    array_features = [np.array(features)]
    prediction = model.predict(array_features)
    # predict = re.sub(r"[^A-Za-z0-9]+", " ", prediction[0])

    match prediction:
        case "Drug_Reaction":
            disease = "Эмийн урвал"
            tailbar = "Эмийн гаж нөлөө (ADR) нь эм ууснаас үүдэлтэй гэмтэл юм. ADR нь эмийг нэг тунгаар эсвэл удаан хугацаагаар хэрэглэсний дараа эсвэл хоёр ба түүнээс дээш эмийг хослуулан хэрэглэсний үр дүнд үүсч болно."
            sergiileh = "цочроохоо болих, хамгийн ойрын эмнэлэгтэй зөвлөлдөх, эм хэрэглэхээ зогсоох, дагаж мөрдөх "
        case "Malaria":
            disease = "Хумхаа"
            tailbar = "Anopheles шумуулд хазуулсан эсвэл бохирдсон зүү, цус сэлбэх замаар халдварладаг Plasmodium овгийн эгэл биетний шимэгчээр үүсгэгддэг халдварт өвчин. Falciparum malaria бол хамгийн аюултай төрөл юм."
            sergiileh = "Ойролцоох эмнэлэгт хандаарай тослог хоол, ногооны бус хоол хүнс, шумуулнаас хол байлга"
        case "Allergy":
            disease = "Харшил"
            tailbar = "Харшил гэдэг нь таны биед хор хөнөөлгүй гадны бодист үзүүлэх дархлааны тогтолцооны хариу үйлдэл юм. Үүнд зарим хоол хүнс, цэцгийн тоос, гэрийн тэжээвэр амьтдын үс зэрэг орно. Таны дархлааны тогтолцооны үүрэг бол хортой эмгэг төрүүлэгчтэй тэмцэх замаар таныг эрүүл байлгах явдал юм."
            sergiileh = "каламины хучаастай хэсгийг боолтоор түрхэж загатнаа шахах мөс ашиглана "
        case "Hypothyroidism":
            disease = "Гипотиреодизм"
            tailbar = "Бамбай булчирхайн үйл ажиллагаа бага эсвэл бага бамбай булчирхай гэж нэрлэгддэг гипотиреодизм нь бамбай булчирхай нь хангалттай хэмжээний бамбай булчирхайн даавар үүсгэдэггүй дотоод шүүрлийн системийн эмгэг юм."
            sergiileh = "стрессийг багасгах дасгал хөдөлгөөн эрүүл хооллолт зөв унт "
        case "Psoriasis":
            disease = "Psoriasis"
            tailbar = "Psoriasis бол мөнгөлөг хайрсаар бүрхэгдсэн зузаан, улаан, товойсон толбо үүсгэдэг нийтлэг арьсны өвчин юм. Тэд хаана ч гарч болох боловч ихэнх нь хуйх, тохой, өвдөг, нуруун дээр гарч ирдэг. Psoriasis нь хүнээс хүнд дамжих боломжгүй. Заримдаа энэ нь нэг гэр бүлийн гишүүдэд тохиолддог."
            sergiileh = "гараа савантай бүлээн усаар угаана, давстай ванны даралтыг ашиглан цус алдалтыг зогсооно "
        case "GERD":
            disease = "GERD"
            tailbar = "Ходоодны улаан хоолойн сөргөө өвчин буюу GERD нь улаан хоолой ба ходоодны хоорондох булчингийн цагираг болох улаан хоолойн доод сфинктер (LES)-д нөлөөлдөг хоол боловсруулах эмгэг юм. Олон хүмүүс, түүний дотор жирэмсэн эмэгтэйчүүд GERD-ийн улмаас зүрхний шарх, ходоодны хүчиллэгээр өвддөг."
            sergiileh = "Өөх тостой халуун ногоотой хоолноос зайлсхийх Хоол идсэний дараа хэвтэхээс зайлсхийж, жингээ хэвийн хэмжээнд байлга"
        case "Chronic_cholestasis":
            disease = "Архаг холестаз"
            tailbar = "Архаг холестатик өвчин нь нялх, бага нас, насанд хүрсэн үед тохиолддог бөгөөд ихэнх тохиолдолд цөсний хучуур эдэд анхдагч гэмтэл учруулдаг цөсний хүчлийг элэгнээс гэдэс рүү дамжуулах чадваргүй байдаг."
            sergiileh = (
                "хүйтэн банн загатнаа арилгах эм Эмчтэй зөвлөлдөнө үү эрүүл хооллоорой"
            )
        case "hepatitis_A":
            disease = "Гепатит А"
            tailbar = "Гепатит А нь гепатит А вирусээр үүсгэгддэг элэгний гоц халдварт өвчин юм. Энэ вирус нь үрэвслийг үүсгэдэг, элэгний үйл ажиллагаанд нөлөөлдөг хэд хэдэн төрлийн гепатитын вирүсийн нэг юм."
            sergiileh = "Өөх тостой халуун ногоотой хоол хүнс хэрэглэхээс зайлсхийж гараа угаахдаа хамгийн ойрын эмнэлэгт хандаарай"
        case "Osteoarthristis":
            disease = "Остеоартрит"
            tailbar = "Остеоартрит нь үе мөчний хамгийн түгээмэл хэлбэр бөгөөд дэлхий даяар сая сая хүмүүст нөлөөлдөг. Энэ нь таны ясны үзүүрийг зөөлрүүлдэг хамгаалалтын мөгөөрс нь цаг хугацааны явцад элэгдэх үед үүсдэг."
            sergiileh = "ацетаминофен зөвлөгөө хамгийн ойрын эмнэлэг давстай ванныг дагаж мөрдөөрэй"
        case "(vertigo)_Paroymsal__Positional_Vertigo":
            disease = "(толгой эргэх) Пароймсал байрлалын вертиго"
            tailbar = "Хоргүй пароксизмаль байрлалын толгой эргэх (BPPV) нь толгой эргэх хамгийн түгээмэл шалтгаануудын нэг юм - гэнэт эргэлдэж байгаа эсвэл толгойн дотор тал нь эргэлдэж байгаа мэдрэмж юм. Хоргүй пароксизмаль байрлалын толгой эргэх нь бага зэргийн болон хүчтэй толгой эргэх шинж тэмдэг илэрдэг."
            sergiileh = "хэвтэх биеийн гэнэтийн өөрчлөлтөөс зайлсхийх толгойн огцом хөдөлгөөнөөс зайлсхийх амрах"
        case "Hypoglycemia":
            disease = "Гипогликеми"
            tailbar = "Гипогликеми нь цусан дахь сахарын хэмжээ (глюкоз) хэвийн хэмжээнээс доогуур байх нөхцөл юм. Глюкоз бол таны биеийн эрчим хүчний гол эх үүсвэр юм. Гипогликеми нь ихэвчлэн чихрийн шижингийн эмчилгээтэй холбоотой байдаг. Гэхдээ бусад эмүүд болон янз бүрийн эмгэгүүд - маш ховор тохиолддог - чихрийн шижингүй хүмүүст цусан дахь сахарын хэмжээг бууруулдаг."
            sergiileh = "тал дээр хэвтэх судасны лугшилтанд үзлэг хийх чихэрлэг ундаа эмчээс зөвлөгөө авах"
        case "Acne":
            disease = "Батга"
            tailbar = "Батга нь үсний уутанцар (үсний уутанцар ба тэдгээрийг дагалддаг өөхний булчирхай) -ын бөглөрөл, үрэвслийн үр дүнд комедон, папуляц, идээт үрэвсэл, зангилаа ба/эсвэл цист үүсэхийг хэлнэ. Нүүр болон их биеийн дээд хэсэгт батга үүсдэг. Энэ нь ихэвчлэн өсвөр насныханд нөлөөлдөг."
            sergiileh = "усанд орох хоер удаа өөх тос хэрэглэхээс зайлсхий халуун ногоотой хоол ус их хэмжээгээр уух хэт олон бүтээгдэхүүнээс зайлсхий"
        case "Diabetes":
            disease = "Чихрийн шижин"
            tailbar = "Чихрийн шижин нь цусан дахь глюкоз буюу цусан дахь сахарын хэмжээ хэт өндөр байх үед үүсдэг өвчин юм. Цусан дахь глюкоз нь таны эрчим хүчний гол эх үүсвэр бөгөөд таны идэж буй хоол хүнсээр дамждаг. Нойр булчирхайгаас ялгардаг инсулин даавар нь хоол хүнснээс агуулагдах глюкозыг таны эсэд орж энерги болгон ашиглахад тусалдаг."
            sergiileh = "тэнцвэртэй хоолны дэглэм дасгал эмч хүртэл дагаж зөвлөгөө байх"
        case "Impetigo":
            disease = "Импетиго"
            tailbar = "Импетиго (im-puh-TIE-go) нь ихэвчлэн нярай болон хүүхдүүдэд нөлөөлдөг арьсны халдварт өвчин юм. Импетиго нь ихэвчлэн нүүр, ялангуяа хүүхдийн хамар, амны эргэн тойронд, гар, хөл дээр улаан шарх хэлбэрээр илэрдэг. Шарх нь хагарч, зөгийн балны өнгөтэй царцдас үүсдэг."
            sergiileh = "нөлөөлөлд өртсөн хэсгийг бүлээн усанд дэвтээнэ антибиотик хэрэглэх нойтон шахсан даавуугаар арчдасыг арилгана эмчид хандаарай"
        case "Hypertension":
            disease = "Гипертензи"
            tailbar = "Цусны даралт ихсэх (HTN эсвэл HT) нь цусны даралт ихсэх (HBP) гэж нэрлэгддэг цусны даралт ихсэх нь артерийн цусны даралт байнга нэмэгдэж байдаг урт хугацааны эрүүл мэндийн эмгэг юм. Цусны даралт ихсэх нь ихэвчлэн шинж тэмдэг үүсгэдэггүй."
            sergiileh = "бясалгал давстай усанд орох нь стрессийг бууруулдаг зөв унтах"
        case "Peptic_ulcer_diseae":
            disease = "Пепсины шархлаа өвчин"
            tailbar = "Пепсины шархлааны өвчин (PUD) нь ходоодны дотоод салст бүрхэвч, нарийн гэдэсний эхний хэсэг, заримдаа улаан хоолойн доод хэсэг юм. Ходоодны шархыг ходоодны шарх гэж нэрлэдэг бол гэдэсний эхний хэсэг нь арван хоёр гэдэсний шархлаа юм."
            sergiileh = "Өөх тостой халуун ногоотой хоолноос зайлсхийх Пробиотик хоол хүнс хэрэглэх Сүүнээс татгалзах архи согтууруулах ундааг хязгаарлах"
        case "Dimorphic_hemorrhoids(piles)":
            disease = "Диморфик цусархаг (овоо)"
            tailbar = "Hemorrhoids буюу hemorrhoids нь шулуун гэдсээр суваг дахь судасны бүтэц юм. Тэдний ... Бусад нэрс, Цусархаг, овоо, геморройдын өвчин ."
            sergiileh = "өөх тостой халуун ногоотой хоол идэхгүй байх шуламны давстай бүлээн усанд орох, алвера шүүс хэрэглэх"
        case "Common_Cold":
            disease = "Ханиад"
            tailbar = "Ханиад нь хамар, хоолойн вируст халдвар юм (амьсгалын дээд замын). Энэ нь ихэвчлэн хор хөнөөлгүй байдаг ч тийм мэдрэмж төрдөггүй. Олон төрлийн вирус нь ханиад үүсгэдэг."
            sergiileh = "С витаминаар баялаг ундаа ууж, уураар ууж, хүйтэн хоол идэхээс зайлсхийх, халууныг барих"
        case "Chicken_pox":
            disease = "Салхин цэцэг"
            tailbar = "Салхин цэцэг нь салхин цэцэг (VZV) -ээр үүсгэгддэг гоц халдварт өвчин юм. Энэ нь загатнах, цэврүүтэх мэт тууралт үүсгэдэг. Тууралт эхлээд цээж, нуруу, нүүрэн дээр гарч, дараа нь бүх биед тархаж, 250-500 загатнах цэврүү үүсгэдэг."
            sergiileh = "усанд орохдоо неем хэрэглэх, нялцан навч хэрэглэх, вакцин хийлгэх, олон нийтийн газраас зайлсхийх"
        case "Cervical_spondylosis":
            disease = "Умайн хүзүүний нугалам"
            tailbar = "Умайн хүзүүний нугалам гэдэг нь хүзүүн дэх нугасны дискэнд нөлөөлдөг насжилттай холбоотой элэгдэл, урагдал гэсэн ерөнхий нэр томъёо юм. Диск нь шингэн алдаж, агших тусам ясны ирмэг (ясны салаа) дагуух ясны төсөөлөл зэрэг остеоартритын шинж тэмдэг илэрдэг."
            sergiileh = "Халаалтын дэвсгэр эсвэл хүйтэн боодол хэрэглэх, дасгал хийх, өвдөлт намдаах эм уух, эмчээс зөвлөгөө аваарай"
        case "Hyperthyroidism":
            disease = "Гипертиреодизм"
            tailbar = "Гипертиреодизм (бамбай булчирхайн хэт идэвхжил) нь бамбай булчирхай нь тироксин гормоныг хэт их хэмжээгээр үйлдвэрлэдэг үед үүсдэг. Гипертиреодизм нь таны биеийн бодисын солилцоог хурдасгаж, санамсаргүйгээр жин хасах, зүрхний цохилт хурдан эсвэл тогтмол бус байдалд хүргэдэг."
            sergiileh = "эрүүл хоол идээрэй массаж хийх нимбэгний бальзам хэрэглэх цацраг идэвхт иодын эмчилгээ"
        case "Urinary_tract_infection":
            disease = "Шээсний замын халдвар"
            tailbar = "Шээсний замын халдвар: Бөөр, шээсний суваг, давсаг, шээсний сүвний халдвар. Товчилсон UTI. Шээсний замын үрэвсэлтэй хүн бүрт шинж тэмдэг илэрдэггүй ч байнга шээх хүсэл, шээх үед өвдөх, түлэгдэх зэрэг нийтлэг шинж тэмдгүүд байдаг."
            sergiileh = "их хэмжээний ус уух, витамин С-ийн хэрэглээг нэмэгдүүлэх, цангис жимсний шүүс уух, пробиотик уух"
        case "Varicose_veins":
            disease = "Хелийн судлууд"
            tailbar = "Судас нь томорч, мушгирсан, ихэвчлэн арьсаар тодорхой харагддаг товойсон, хөх өнгийн судас хэлбэрээр илэрдэг. Варикозын судлууд нь өндөр настнуудад, ялангуяа эмэгтэйчүүдэд ихэвчлэн тохиолддог бөгөөд ялангуяа хөлөнд илэрдэг."
            sergiileh = "Хавтгай хэвтээд хөлөө дээш өргөх, венийн судсыг шахах тос түрхэж удаан зогсохгүй"
        case "AIDS":
            disease = "Хүний дархлал хомсдолын вирус "
            tailbar = "Дархлалын олдмол хомсдолын хам шинж (ДОХ) нь хүний дархлал хомсдолын вирус (ХДХВ)-аас үүдэлтэй архаг, амь насанд аюул учруулж болзошгүй өвчин юм. ХДХВ нь таны дархлааны системийг гэмтээснээр таны биеийн халдвар, өвчинтэй тэмцэх чадварт саад болдог."
            sergiileh = "нээлттэй тайралтаас зайлсхий, хэрэв боломжтой бол эмчийн хяналтан дор хувцас өмс"
        case "Paralysis_(brain_hemorrhage)":
            disease = "Саажилт (тархины цус алдалт)"
            tailbar = "Тархины доторх цус алдалт (ICH) нь тархины эдэд гэнэт цус орж, тархинд гэмтэл учруулдаг. Шинж тэмдэг нь ихэвчлэн ICH үед гэнэт гарч ирдэг. Үүнд толгой өвдөх, сулрах, төөрөгдөл, саажилт, ялангуяа таны биеийн нэг талд орно."
            sergiileh = "массаж эрүүл хооллох дасгал хийх эмчтэй зөвлөлдөх"
        case "Typhoid":
            disease = "Хижиг"
            tailbar = "Salmonella typhi бактерийн халдвараас үүдэлтэй халууралтаар тодорхойлогддог цочмог өвчин. Халууралт нь халуурах, толгой өвдөх, өтгөн хатах, бие сулрах, жихүүдэс хүрэх, булчин өвдөх зэрэг шинж тэмдгүүдтэй байдаг. Суулгалт нь ховор тохиолддог бөгөөд бөөлжих нь ихэвчлэн хүчтэй байдаггүй."
            sergiileh = "өндөр илчлэг хүнсний ногоо идээрэй"
        case "Hepatitis_B":
            disease = "Гепатит В"
            tailbar = "Гепатит В нь таны элэгний халдвар юм. Энэ нь эрхтэний сорвижилт, элэгний дутагдал, хорт хавдар үүсгэдэг. Хэрэв эмчлэхгүй бол үхэлд хүргэж болзошгүй. Энэ нь гепатитын В вирустэй хүний цус, ил шарх, биеийн шингэнд хүрэх үед халдварладаг."
            sergiileh = (
                "Хамгийн ойрын эмнэлгээс зөвлөгөө аваарай, эрүүл эм уух хэрэгтэй"
            )
        case "Fungal_infection":
            disease = "Мөөгөнцрийн халдвар"
            tailbar = "Хүний биед мөөгөнцрийн халдвар нь бие махбодын зарим хэсгийг эзэлдэг бөгөөд дархлааны системд хэт их ачаалал өгөх үед мөөгөнцрийн халдвар үүсдэг. Мөөгөнцөр нь агаар, хөрс, ус, ургамалд амьдардаг. Хүний биед байгалиасаа амьдардаг мөөгөнцөр бас байдаг. Олон микробын нэгэн адил тустай мөөгөнцөр, хортой мөөгөнцөр байдаг."
            sergiileh = (
                "Халдвар авсан газрыг хуурай байлгаж, цэвэр даавуугаар угаана уу"
            )
        case "Hepatitis_C":
            disease = "Гепатит C"
            tailbar = "Цус сэлбэх (ховор тохиолддог), гемодиализ, зүү зүүгээр дамждаг гепатит С вирусын (HCV) улмаас элэгний үрэвсэл. Гепатит С-ийн элэгний гэмтэл нь элэгний хатуурал, түүний хүндрэл, түүнчлэн хорт хавдар үүсгэдэг."
            sergiileh = "Хамгийн ойрын эмнэлгийн вакцинд хамрагдаж, эрүүл эм ууна уу"
        case "Migraine":
            disease = "Мигрень"
            tailbar = "Мигрень нь ихэвчлэн толгойн нэг талд хүчтэй цохилж, лугших мэдрэмжийг үүсгэдэг. Энэ нь ихэвчлэн дотор муухайрах, бөөлжих, гэрэл, дуу чимээнд хэт мэдрэг байдал дагалддаг. Мигрень халдлага хэдэн цагаас хэдэн өдөр хүртэл үргэлжилдэг бөгөөд өвдөлт нь таны өдөр тутмын үйл ажиллагаанд саад болохуйц хүчтэй байж болно."
            sergiileh = "Бясалгал стрессийг бууруулах наранд полороид шил хэрэглэх эмчээс зөвлөгөө аваарай"
        case "Bronchial_Asthma":
            disease = "Гуурсан хоолойн багтраа"
            tailbar = "Гуурсан хоолойн багтраа нь уушгины амьсгалын замыг хавдаж, нарийсгахад хүргэдэг эрүүл мэндийн эмгэг юм. Энэ хавантай холбоотойгоор агаарын зам нь илүүдэл салиа үүсгэдэг бөгөөд амьсгалахад хэцүү байдаг бөгөөд энэ нь ханиалгах, амьсгал богиносох, амьсгал давчдах зэрэгт хүргэдэг. Өвчин нь архагшсан бөгөөд өдөр тутмын ажилд саад болдог."
            sergiileh = "сул хувцаслалт руу шилжих, гүнзгий амьсгаа авах, гохоос холдох, тусламж хайх"
        case "Alcoholic_hepatitis":
            disease = "Архины гепатит"
            tailbar = "Согтууруулах ундааны гепатит нь удаан хугацааны туршид согтууруулах ундаа хэтрүүлэн хэрэглэснээс үүдэлтэй элэгний үрэвсэлт өвчин юм. Мөн хэтрүүлэн ууж, байнга согтууруулах ундаа хэрэглэснээр энэ нь улам хүндэрдэг. Хэрэв та ийм нөхцөл байдал үүсвэл архи уухаа болих хэрэгтэй"
            sergiileh = "Согтууруулах ундааны хэрэглээгээ зогсоох, эмчийн хяналтан дор эм уух хэрэгтэй"
        case "Jaundice":
            disease = "Шарлалт"
            tailbar = "Цусан дахь цөсний пигмент билирубин хэвийн бус өндөр байгаагаас арьс, склера (нүдний цагаан) шар өнгөтэй болно. Шаргал нь бусад эд, биеийн шингэнд хүрдэг. Нэгэн цагт шар өвчнийг 'орбус региус' (хаант өвчин) гэж нэрлэдэг байсан бөгөөд зөвхөн хааны хүрэлт л үүнийг эмчилдэг гэж үздэг."
            sergiileh = "их хэмжээний ус ууж, сүүн ургамал хэрэглэх, жимс жимсгэнэ, эслэг ихтэй хоол хүнс хэрэглэх"
        case "Hepatitis_E":
            disease = "Гепатит_E"
            tailbar = "Гепатит Е вирусын (HEV) халдварын улмаас үүссэн элэгний үрэвслийн ховор хэлбэр. Энэ нь халдвартай хүний хоол хүнс, ундаагаар дамжин халдварладаг ба ялгадас усанд орж болзошгүй газарт халдвартай усаар дамжин халдварладаг. Гепатит Е нь элэгний архаг өвчин үүсгэдэггүй."
            sergiileh = (
                "Согтууруулах ундааны хэрэглээгээ зогсоож, эмчээс эм уух хэрэгтэй"
            )
        case "Dengue":
            disease = "Денге"
            tailbar = "aedes шумуулаар дамждаг флавивирусын (Flavivirus төрлийн Денге вирусын төрөл) үүсгэгддэг, толгой өвдөх, үе мөчний хүчтэй өвдөх, тууралт гарах зэргээр тодорхойлогддог цочмог халдварт өвчин. â€” мөн хугарлын халууралт, денге халууралт гэж нэрлэдэг."
            sergiileh = "Папайя навчны шүүс ууж, өөх тостой халуун ногоотой хоолноос зайлсхийх, шумуулнаас хол байлгах, чийгшүүлэх"
        case "Hepatitis_D":
            disease = "Гепатит D"
            tailbar = "Гепатит D буюу элэгний дельта вирус нь элэгний үрэвсэл үүсгэдэг халдвар юм. Энэ хаван нь элэгний үйл ажиллагааг бууруулж, элэгний сорвижилт, хорт хавдар зэрэг удаан хугацааны элэгний асуудал үүсгэдэг. Нөхцөл байдал нь гепатит D вирусын (HDV) улмаас үүсдэг."
            sergiileh = "Эмчээс зөвлөгөө аваарай эрүүл хооллолтыг дагаж мөрдөөрэй"
        case "Heart_attack":
            disease = "Зүрхний шигдээс"
            tailbar = "Цусны хангамж алдагдсанаас зүрхний булчингийн үхэл. Цусны хангамж алдагдах нь ихэвчлэн зүрхний булчинг цусаар хангадаг артерийн нэг болох титэм артерийн бүрэн бөглөрлийн улмаас үүсдэг."
            sergiileh = "түргэн тусламж дуудах, зажлах эсвэл залгих асприн тайван байх"
        case "Pneumonia":
            disease = "Хатгалгаа"
            tailbar = "Уушгины хатгалгаа нь нэг буюу хоёр уушгины халдвар юм. Бактери, вирус, мөөгөнцөр нь үүнийг үүсгэдэг. Халдвар нь уушгины уушгины уушгинд үрэвсэл үүсгэдэг бөгөөд үүнийг цулцангийн гэж нэрлэдэг. Цуцлагууд нь шингэн юмуу идээ бээрээр дүүрч, амьсгалахад хүндрэлтэй байдаг."
            sergiileh = "эмчтэй зөвлөлдөнө эм амрах хяналт"
        case "Arthritis":
            disease = "Артрит"
            tailbar = "Артрит нь таны нэг буюу хэд хэдэн үе мөчний хавдар, эмзэглэл юм. Үе мөчний үрэвслийн гол шинж тэмдэг нь үе мөчний өвдөлт, хөшүүн байдал бөгөөд нас ахих тусам улам дорддог. Хамгийн түгээмэл үе мөчний үрэвсэл нь остеоартрит ба ревматоид артрит юм."
            sergiileh = (
                "дасгалын хэрэглээ халуун хүйтэн эмчилгээ зүү массаж хийж үзээрэй"
            )
        case "Gastroenteritis":
            disease = "Ходоод гэдэсний үрэвсэл"
            tailbar = "Гастроэнтерит нь хоол боловсруулах замын үрэвсэл, ялангуяа ходоод, бүдүүн, нарийн гэдэсний үрэвсэл юм. Вируст ба бактерийн гаралтай гастроэнтерит нь суулгалт, хэвлийгээр базлах, дотор муухайрах, бөөлжих шинж тэмдэг илэрдэг гэдэсний халдварт өвчин юм."
            sergiileh = "Хатуу хоол идэхээ больж, бага багаар ус уугаад идээрэй"
        case "Tuberculosis":
            disease = "Сүрьеэ"
            tailbar = "Сүрьеэ (сүрьеэ) нь ихэвчлэн сүрьеэгийн микобактерийн (MTB) нянгаар үүсгэгддэг халдварт өвчин юм. Сүрьеэ нь ерөнхийдөө уушгинд нөлөөлдөг ч биеийн бусад хэсгүүдэд нөлөөлдөг. Ихэнх халдвар нь шинж тэмдэггүй байдаг бөгөөд энэ тохиолдолд далд сүрьеэ гэж нэрлэгддэг."
            sergiileh = "амаа таглах эмчтэй зөвлөлдөх эм амрах"

        case _:
            tailbar = "Таамаглах утга олдсонгүй, дахин оролдоно уу !"

    # ca = [np.array(c)]
    # tailbarprediction = tailbarmodel.predict(ca)
    # sergiilehprediction = sergiilehmodel.predict(ca)
    # print(tailbarprediction[0])
    # print(sergiilehprediction[0])
    # tailbarorchuulag = tss.google(tailbarprediction[0], 'en', 'mn')

    # sergiilehorchuulag = tss.google(sergiilehprediction[0], 'en', 'mn')

    return render_template(
        "index.html", disease=disease, tailbar=tailbar, sergiileh=sergiileh
    )


@app.route("/prediction_add", methods=["POST", "GET"])
def AddText():
    if request.method == "POST":
        disease = request.form["disease"]
        tailbar = request.form["tailbar"]
        sergiileh = request.form["sergiileh"]
        # saving all the values to db
        add_new = add_prediction(disease, tailbar, sergiileh)
        return redirect(url_for("home"))
    else:
        return render_template("index.html")


@app.route("/history")
def history():
    all_text = get_data()
    return render_template("history.html", all_text=all_text)


if __name__ == "__main__":
    app.run(debug=True)
