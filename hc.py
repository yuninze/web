import pandas as pd
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans,AgglomerativeClustering

costco0=pd.read_csv("c:/code/costco.csv").iloc[:,2:]
costco0.index.name="clientidx"
costco1=pd.DataFrame(
    normalize(costco0),columns=costco0.columns)
costco1.head(n=3)

plt.figure(figsize=(13,13))

plt.subplot(311)
gram=sch.dendrogram(sch.linkage(costco1,method="ward"))
plt.title("dendrogram")

blok0=AgglomerativeClustering(
    n_clusters=2,affinity="euclidean",linkage="ward"
    ).fit_predict(costco1)
plt.subplot(312)
plt.scatter(costco1.Milk,costco1.Fresh,c=blok0)
plt.title("AC Milk:Fresh")

blok1=KMeans(
    n_clusters=2,random_state=94056485
    ).fit_predict(costco1)
plt.subplot(313)
plt.scatter(costco1.Milk,costco1.Fresh,c=blok1)
plt.title("KMeans Milk:Fresh")