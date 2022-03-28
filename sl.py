from pprint import pprint as pr
from time import time
import logging

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.datasets import fetch_20newsgroups

#stdout logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(Levelname)s %(message)s")

#get categories
cat=[
    "alt.atheism",
    "talk.religion.misc",
]
while True:
    cat_input=input(f"category: ")
    if not cat_input:
        break
    cat.append(cat_input)
    print(f"added: {cat_input}")
print("Loaded categories: %d" % len(cat))

if not len(cat)==0:
    print(cat)

    #dataset sklearn.datasets.fetch_20newsgroups
    src=fetch_20newsgroups(categories=cat)
    print(f"{len(src.filenames)} documents")

    #sequences of text feature extractor
    pl=Pipeline(
        [
            ("vc",CountVectorizer()),
            ("tfidf",TfidfTransformer()),
            ("clf",SGDClassifier())
        ]
    )

    #parameters will give better power but will increase processing time
    params={
        "vc__max_df":(0.5,0.75,1.0),
        "vc__max_features":(None,5_000,10_000,50_000),
        "vc__ngram_range":((1,1),(2,2)), #unigrams or bigrams
        "tfidf__use_idf":(True,False),
        "tfidf__norm":("l1","l2"),
        "clf__max_iter":(20,50,),
        "clf__alpha":(0.00_001,0.00_0001),
        "clf__penalty":("l2","elasticnet"),
    }

    if __name__=="__main__":
        #mp requires the fork to a __main__ protected block
        #find the best params for feature extractions and classifier
        grid_search=GridSearchCV(pl,params,n_jobs=-1,verbose=1)

        print("pipeline: ",[q for q,_ in pl.steps])
        print("params: ")
        pr(params)
        t0=time()
        grid_search.fit(src.data,src.target)
        print("done in %0.3fs" % (time()-t0))

        print("Best score: %0.3f" % grid_search.best_score_)
        best_params=grid_search.best_estimator_.get_params()
        for q in sorted(params.keys()):
            print(f"\t{q}: {best_params[q]}")
else:
    raise Exception(f"{cat=}")

def prac():
    corpus=[
        '50세 여환으로 1995년 Breast Cancer 진단을 받고 수술, 방사선 치료, Chemotherapy 후 완치됐었다. 가족 중 모친은 Ovarian Cancer, 여동생은 Breast Cancer로 사망했으며, 검사 결과 BRCA Mutation이 있는 환자였다. 2013년 4월부터 시작된 Vaginal Bleeding을 CC로 산 부인과 진료 후 난소 혹으로 판정됐다. 복수의 양은 많지 않았으나 CT 결과 Peritoneum에 다량의 종괴가 발견됐고 골반 및 복부 림프선 비대가 발견됐다. 환자는 지속되는 복부 불편감과 통증을 호소했다. 2013년 7월부터 Paclitaxel/Carboplatin을 투여했다. 치료 시작 직 후 환자는 극심한 근육통과 관절통을 호소해 이후 투여에 지장이 발생했다. 이때부터 Oxycodone 5mg를 PO하고 Fentanyl 25ug/hr을 경피 투여 했다. 통증이 심한 경우 Pethidine 25mg IM, Morphine을 정맥점주 했다. Severe N/V',
        'Episodes. 엄마와 담임선생님은 나에게 신뢰를 깼다고 말했다. 나의 기분, 마음 있는 그대로를 이야기해도 말을 들어주는 사람이 없다. 나는 기억을 왜곡할 수 없다. 나의 좋지 않은 기억이 Intact 상태로 다가온다. 기억을 포장할 수 없다. 분명히 이것이야말로 트라우마이다. 누군가에게 물고문을 당한 기억이 있다. 너무나도 충격적이었다. 내가 잘못한 것이 분명히 있다. 그것을 고치고 싶어 안달하지만 결국 실패해서 속상하다. 좋아했던 사람이 있었다. 그 좋아했던 사람이 눈 앞에 나타나서 고생했다고 말해 주는 상상, 이런 것이 이루어졌으면 하는 상상을 나도 하곤 한다. 삼성병원의 의사가 너는 사내새끼가 아니다, 너는 인격장애이다, 거짓말쟁이이다라고 했다. 예전에 배가 아팠다. 독감이 유행했으므로 Oseltamivir 먹었다. 3일 후 맹장이 아팠다. 근처 한림대병원에서 Echo하러 가는 길에 누군가가 담 배를 사달라고 했다. 나는 늙어보이기 때문에 담배를 살 수 있다. 사주려고 했는데 일하던 엄마가 발견하고 못하게 했다. 복통이 심해져 삼성병원으로 갔으나 보호자 없이는 안된다고 했다. 엄마는 돈이 많이 든다며 그냥 가자고 했으나 눈을 떠보니 정신병원이었다. 옆구리가 쑤신다고 말했으나 건강염려증이라고만 했다. 힘들지 않았으면 좋겠다. 남들처럼 살고 싶다. 누군가를 좋아했을 때처럼 평범하게 누 군가를 좋아하고 싶다. 좋아했던 사람을 생각했을 때 너무나도 아련하다. 선생님 제가 횡설수설하죠? 저도 속상해요. 밖에 나가서 꼭 만나요. 전 홍대에서 주로 놀아요. 그림 학원 한번 다녀볼게요. (관계 Breaking 예감, 암시적 발언) > ADHD, BPD',
        '저 산은 미륵산이라고 한다. 저 산에 가본 적은 있는가? (과제도 많고 멀어서 못갔다.) 그럴 것이다. 미륵산은 AD 600년 전 미륵사지 절터로서 지어졌다. 탑의 뚜껑을 열면서 이건 어떻게 지었고 누가 얼마나 내서 지은건지 밝혀지게 되었다. 이 탑은 동방에서 가장 큰 석탑으로 지금은 체르노빌 원전의 보호막 같은 걸 뒤짚어 씌워서 보강하고 있다. (종교는 있는가?) 예배당에 가곤 했다. 가족이 종교는 믿는가? (아버지와 어머니가 믿기는 하지만 거의 가지 않는다. 친가가 기독교 성향이다.) 그런가. (종교나 유적에 대해 잘 아시는 거 같다.) 내 전공은 인류학, 고고학, 신학이다. 이런 게 전문이다. 내 전화번호를 알려주겠다. 010-4816-3554이다. 선생님도 전화번호 적어서 지금 줘라. (갑자기 내 번호가 기억나지 않는다. 나중에 주겠다.) 나중에 윤인재 선생님도 몰래 전화번호 적어서 알려줘라. 몰래 적어줘야 한다. 왜 전화번호 알려주는지 알 것이다. 나중에 퇴원해서 서로 전문 분야에 대해서 이야기하는 기회가 있을 것이다. 또 나는 음악 에도 관심이 있다. 나가면 음악을 하려고 한다. 눈에서 무언가가 배출되고 있다. 눈이 좋아지는 과정이다. (실제로는 아무것도 나오고  있지 않다.)',
        '안녕하세요? 저녁은 많이 드셨나요? 네, 많이 먹었습니다. 이거 좀 봐주세요. (쪽지를 건냄) 쪽지에는 악성 인물들과 얽히지 말라는  스스로에게 쓴 편지글이 쓰여져 있다. > 서원석이라는 정신분열증을 앓고 있는 친구가 스스로를 괴롭힌다. 그는 90kg의 거구로서 자신이 살고 있는 아파트에 아무 때나 찾아와 초인종을 연달아 누르고 빵을 사왔다는 거짓말을 큰 소리로 지르며 자신을 괴롭혔다. 서원석은  컴퓨터에 능통하여 전 시의 CCTV를 들여다보고 있을 뿐만 아니라 병원, 시청, 각종 소상점도 속속들이 감시하고 있다. 특히 그는 성적인 이야기를 잘 한다. 신동에 있는 59피자의 사장님이 예쁘다면서 섹스를 한번 하고 싶다는 이야기를 한다. 동해반점 안주인이 예쁘다면서 보면서 자위행위를 했다는 이야기를 한다. 삼푸 나이트클럽과 CGV에 스트레스를 풀기 위해 불을 지르겠다는 이야기를 한다. 미장원 아 줌마가 단골 대학생과 이상한 짓을 하는 것을 보여주었다. 그는 스스로에게만 정신분열증 증상을 표출한다. 말이 잘 맞지 않는 것이다. 우원증이라는 증상 말이다. 정신분열증 증상의 하나인데, 30초에서 1분 이내 조리있게 설명할 수 있는 것을 횡설수설 하면서 몇 십 분이고 이야기하는 것이다. 그는 자신의 보호자 행세를 하며 스스로를 위대한 능력의 소유자 또는 신, 천재라고 표현한다. 생각하고 싶지도 않은 임주호와 안장환과 같은 인물의 이야기를 자꾸만 내게 들려준다. 이 도시의 모든 시민은 악마이지만 착한 사람도 있다는 소리를 한다. 이 모든 얘기는 저와 선생님만의 비밀입니다. 의사한테 이야기하지 마세요.',
        '세팅된 나의 모습을 보면 선생님의 변화가 느껴진다. 평소 냉정한 척 하는 타입이지만 나를 보며 얼굴을 새빨갛게 한다. 내 앞에서는 왠지 다정해지고 다감하게 언어를 구사한다. 특히, 스스로 지켜보는 앞에서는 다른 환자에게 달달한 목소리로 대하려는 것이 전부 보인 다. 평소 자기 얘기는 전부 털어놓는 상대인데, 늘 나를 신경써주고 조언해주려는 모습이 보인다. 결국 다정다감한 그 선생님의 모습에 좋아하게 될 수밖에 없었다. 그를 좋아한다. 인간 대 인간으로 그가 다가왔다. 다음 면담을 기다리고 있다. 단 둘만의 마주침의 위해서 이다. 내가 그의 과외학생이었다면 하는 생각을 하곤 한다.',
        '그저께는 생일이었다. 그러나 내색하지 않았다. 그를 골려주고 싶었다. 일부러 남자 간호사와 친밀하게 보이려고 했는데 아니다다를까 얼굴이 빨개지는 그의 모습을 볼 수 있었다. 예전에는 폴리클과 단 둘이 있을 때 폴리클에게 쌀쌀맞게 대하며 자신과의 밀접함을 강조 하려는 태도를 보였다. 나에 대한 친밀함을 과시하려는 것이 분명했다.',
        '면담하면서 팩폭을 당했다. 스스로를 가감없이 드러냈다. 그러나 그는 임의로 나의 말을 막히게 했다. 나는 울었다. 날 울려놓고 쑤셔놓고 후벼파고 나한테 안와? 좋아해놓고 안와? 나를 좋아하는 거 먼저 티 내놓고 안와? 이런 것이 너무 짜증났다. 일부러 누워 있었다. 그러나 머릿속에는 그에 대한 생각으로 가득했다. 기다렸다. 스스로의 흠을 드러낸 것이 화났다. 그러면서 장난으로 나의 이야기를 중단시킨 그가 괘씸했다. 오늘 면담을 세 번 했다. 솔직히 여섯 시 넘으면 전부 퇴근하므로 면담하러 올 사람 없다. 그러나 그는 날 좋아하 기에 올지도 모른다. 그래서 저녁을 먹고 다시 세팅을 했다. 혹시나 하고 기다리며 오늘 당직이 누구인지를 물었다. 아니다다를까 그였 다. RN이 환자가 좋아하는 그 선생님이라고 말했지만 열심히 정색하며 아무렇지도 않게 그렇냐고 대답했다. 모든 것은 나의 설계이다.  과연 나를 울려놓고 스스로 올까, 말까? 생각했다. 지금껏 기다리는 중 안오기만 해봐... 하는 생각이 든다. 그렇지만 안오면 어떡해?  하는 생각도 든다. 그러나 먼저 좋아한 건 그쪽이다. 회진은 분명히 늦게 시작될 것이다. 왜냐하면 그 선생님은 나와의 면담 시간을 최 대한으로 하고 싶기 때문이다.',
        '다른 남자와의 친밀함을 모사함으로써 선생님의 반응을 확인하고 싶다. 그가 질투하는 모습을 보고 싶다. 오늘 회진 시간에 모든 것을 결정하겠다. 퇴원 전까지 모든 관계를 정리하겠다. 그와의 관계를 미세하게나마 이어나갈 것인지, 아니면 모든 것을 끝낼 것인지.'
    ]

    #set vectorizer
    cursor=CountVectorizer()
    #fit source
    data=cursor.fit_transform(corpus)
    #get analyzer as target
    anal=cursor.build_analyzer()
    #get feature names
    cursor.get_feature_names_out()
    #CSR matrix to ndarray
    data.toarray()
    #get column index of specific feature
    cursor.vocabulary_.get("정신분열증")
    return None