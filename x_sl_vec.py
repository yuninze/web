from time import time
from pprint import pprint as pr
import logging
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer,TfidfVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.datasets import fetch_20newsgroups

#stdout logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(Levelname)s %(message)s")

# Author: Olivier Grisel <olivier.grisel@ensta.org>
#         Lars Buitinck
#         Chyi-Kwei Yau <chyikwei.yau@gmail.com>
# License: BSD 3 clause

n_samples = 10000
n_features = 10000
n_components = 10000
n_top_words = 10

def plot_map(data)->None:
    ax=sns.heatmap(data,annot=True,fmt='d',linewidths=.5,cmap='viridis',vmax=500)
    ax.set_xticklabels(set_fontfamily="JetBrains Mono")
    ax.set_yticklabels(set_fontfamily="JetBrains Mono")
    plt.show()
    return None

def plot_top_words(model,feature_names,n_top_words,title):
    fig,axes=plt.subplots(nrows=2,ncols=5,figsize=(30,15),sharex=True)
    axes=axes.flatten()
    for topic_idx,topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[: -n_top_words - 1 : -1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]
        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f"Topic {topic_idx +1}", fontdict={"fontsize": 30})
        ax.invert_yaxis()
        ax.tick_params(axis="both", which="major", labelsize=20)
        for i in "top right left".split():
            ax.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=40)
    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
    plt.show()

# Load the 20 newsgroups dataset and vectorize it. We use a few heuristics
# to filter out useless terms early on: the posts are stripped of headers,
# footers and quoted replies, and common English words, words occurring in
# only one document or in at least 95% of the documents are removed.

print("Loading dataset...")
t0 = time()
data, _ = fetch_20newsgroups(
    shuffle=True,
    random_state=1,
    remove=("headers", "footers", "quotes"),
    return_X_y=True,
)
data_samples = data[:n_samples]
print(f"done in {time()-t0}")

# Use term frequency for LDA.
print("Extracting tf features for LDA...")
tf_vectorizer = CountVectorizer(
    max_df=0.9, min_df=1, max_features=n_features, stop_words="english")
t0 = time()
tf = tf_vectorizer.fit_transform(data_samples)
print(f"done in {time()-t0}")

# Use tf-idf features for NMF.
print("Extracting tf-idf features for NMF...")
tfidf_vectorizer = TfidfVectorizer(
    max_df=0.9, min_df=1, max_features=n_features, stop_words="english")
t0 = time()
tfidf = tfidf_vectorizer.fit_transform(data_samples)
print(f"done in {time()-t0}")

# Fit the NMF model
print(
    "Fitting the NMF model (Frobenius norm) with tf-idf features, "
    "n_samples=%d and n_features=%d..." % (n_samples, n_features)
)
t0 = time()
nmf = NMF(n_components=n_components, random_state=1, alpha=0.1, l1_ratio=0.5).fit(tfidf)
print(f"done in {time()-t0}")


tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
plot_top_words(
    nmf, tfidf_feature_names, n_top_words, "Topics in NMF model (Frobenius norm)"
)

# Fit the NMF model
print(
    "\n" * 2,
    "Fitting the NMF model (generalized Kullback-Leibler "
    "divergence) with tf-idf features, n_samples=%d and n_features=%d..."
    % (n_samples, n_features),
)
t0 = time()
nmf = NMF(
    n_components=n_components,
    random_state=1,
    beta_loss="kullback-leibler",
    solver="mu",
    max_iter=1000,
    alpha=0.1,
    l1_ratio=0.5,
).fit(tfidf)
print("done in %0.3fs." % (time() - t0))

tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
plot_top_words(
    nmf,
    tfidf_feature_names,
    n_top_words,
    "Topics in NMF model (generalized Kullback-Leibler divergence)",
)

print(
    "\n" * 2,
    "Fitting LDA models with tf features, n_samples=%d and n_features=%d..."
    % (n_samples, n_features),
)
lda = LatentDirichletAllocation(
    n_components=n_components,
    max_iter=5,
    learning_method="online",
    learning_offset=50.0,
    random_state=0,
)
t0 = time()
lda.fit(tf)
print("done in %0.3fs." % (time() - t0))

tf_feature_names = tf_vectorizer.get_feature_names_out()
plot_top_words(lda, tf_feature_names, n_top_words, "Topics in LDA model")

#get categories
cat=[]

while True:
    cat_input=input(f"category: ")
    if not cat_input:
        break
    cat.append(cat_input)
    print(f"added->{cat_input}")
print(f"categories->{len(cat)}")

if not len(cat)==0:
    print(cat)
    #dataset sklearn.datasets.fetch_20newsgroups
    src=fetch_20newsgroups(categories=cat)
    print(f"{len(src.filenames)} documents")
    #sequences of text feature extractor
    pl=Pipeline(
        [("vc",CountVectorizer()),
        ("tfidf",TfidfTransformer()),
        ("clf",SGDClassifier())]
    )
    params={
        #"vc__ngram_range":((1,1),(2,2)), #n-grams
        "vc__max_df":([.8,.9]), #have the highest tf
        #"vc__min_df":(), #have the lowest tf
        "vc__max_features":(None,10,10_000,10_0000), #only uses top-ranked vocabs
        "tfidf__norm":("l2","l1"),
        #"tfidf__use_idf":(True,False),
        #"tfidf__smooth_idf":(True,False),
        "clf__max_iter":(100,200),
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
        print(f"done in {(time()-t0)}s")
        print(f"Best score: {grid_search.best_score_}")
        best_params=grid_search.best_estimator_.get_params()
        for q in sorted(params.keys()):
            print(f"\t{q}: {best_params[q]}")
else:
    raise Exception(f"{cat=}")

#https://scikit-learn.org/stable/modules/classes.html#module-sklearn.decomposition
#plotting 함수 제작
#decomposition method 선택(dim reduction용)
#tf-idf
#raw term count
#이제 이걸 LDA 하든지 해서 decompositioning함