import numpy as np #vektörler ve matrisler üzerinde işlem yapmamızı sağlayan kütüphanedir.
import pandas as pd #datasetini okumaya ve düzenlememizi sağlayan kütüphanedir.



#RNN modelini oluşturmak için keras kullanaağız.
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, GRU, Embedding, CuDNNGRU
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences



#C:\Anaconda3\Lib\site-packages\h5py\__init__.py:37: 'np.float64 == np.dtype(float)'
#from ._conv import register_converters as register_converters

#Datasetimizi tanımlıyoruz
dataset = pd.read_csv('hepsiburada.csv')

#Etiketler ile yorumları ayırıyoruz
target = dataset['Rating'].values.tolist()#başlık altında bulunan tüm etiketleri seçip liste halinde alıyoruz.(0-1 etiketleri)
data = dataset['Review'].values.tolist()#aynı işlemi veriler yani yorumlar içinde yapıyoruz.

#açıklama defterde
cutoff = int(len(data) * 0.80) #elimizdeki verilerin yüzde sekseninin nekadar yaptığını hesaplıyoruz...

#elimizdeki veriyi belirlediğimiz noktadan ikiye ayırıyoruz ve iki farklı değişkene atayacağız. Verielrin yüzde seksenini kapsayan bir index belirliyoruz
x_train, x_test = data[:cutoff], data[cutoff:]
y_train, y_test = target[:cutoff], target[cutoff:]

#------------------------------------------------------------------
# *** TOKENATION ***

num_words = 10000 #kelime haznesinde en fazla kaç kelime olsun.En sık geçen 10000 kelimeyi alacağız nadir geçenleri yok sayacağız...
#tokenleştirme işlemini keras kullanarak yapacağız.
tokenizer = Tokenizer(num_words=num_words) #Tokenizer daki T büyük olmalı // (num_words=num_words) kelime sınırını vermiş oluyoruz bunun yerine none verilirse tüm kelimeler...
tokenizer.fit_on_texts(data) #elimizdeki veriyi tokenleştirelim ve tokenleştireceğimiz verileri veriyoruz

#print(tokenizer.word_index) #kelime haznesini gösterir ve en çok kullanılan başa gelir

#string hallindeki kelimeleri tokenleştirmek için liste içerisinde tokenleştirmek gerekiyor...
x_train_tokens= tokenizer.texts_to_sequences(x_train) # x_train içeirinde eğitim setimiz vardır. Bu kod ile eğitim setimizi tokenleştirmiş olduk...
#print(x_train_tokens[500]) // 500. yorumda bulunan kelimelrin her biri tokenleştirme ile sayıya dönüşmüş durumda...

x_test_tokens= tokenizer.texts_to_sequences(x_test)#bu kodda test setini tokenleştiriyoruz.


num_tokens = [len(tokens) for tokens in x_train_tokens + x_test_tokens] #her yorumunda kaçtane token bulunduğunu görmek için bir liste oluşturuyoruz. hem eğitim setindeki hemde test setindeki yorumları alıyoruz. 
num_tokens=np.array(num_tokens) #liste üzerinde kolay işlem yapabilmek için numpy arraylere dönüştürüyorum. bu sayede numpy'ın kolaylıklarından yararlanıyoruz.

#ortalama bulunan token için: print(np.mean(num_tokens))
#en fazla bulunan token için: print(np.max(num_tokens))

# *** Boyut Belirleme ***
max_tokens= np.mean(num_tokens) + 2 * np.std(num_tokens) #boyutunu hesaplıyoruz ve float bir sonuç buluyoruz...
max_tokens= int(max_tokens) #float çıkan değeri int değerine çeviriyoruz.
#print(max_tokens) #59 token

#59 token yorumların kaç tanesii kapsadığını görmek için: print(np.sum(num_tokens < max_tokens) / len(num_tokens))
#yani 20 tokenlik bir yorum geldiğinde 39 token ekleyip boyutunu 59 a çıkaracapız...

#------------------------------------------------------------------
# *** PADDING ***

#eğitim setindeki verilere padding uygulanıyor...
#x_train_pad= pad_sequences(x_train_tokens, maxlen= max_tokens) #padding işlemini kerasta bulunan pad_sequances ile bu işlem gerçekleşirilebilir. İçerisinde padding eklenecek kelimeler ve token boyutu)

#test setindeki verilere padding uygulanıyor...
#x_test_pad= pad_sequences(x_test_tokens, maxlen=max_tokens)

#tokenleri verip stringleri almak için yazılan fonksiyondur. bunun için word_index işlemi yapılması gerekir.

idx= tokenizer.word_index #'word_index' bir sözlüktür. bu sözlük içerinde kelimeler ve kelimelere karşılık gelen sayılar bulunmaktadır. anahtar-->kelimeler ; değerler-->kelimelere karşılık gelen sayılar.
inverse_map = dict(zip(idx.values(), idx.keys())) #bu kod satırında bu sözlüğü tersine çevireceğiz. anahtar-->kelimelere karşılık gelen sayılar ; değer-->kelimeler.

def tokens_to_string(tokens): #
    words= [inverse_map[token] for token in tokens if token!=0]
    text = ' '.join(words) #daha iyi görünmesi için liste içerisnden çıkarıp text'e atıyoruz.Böylece kelimeler aralarında boşluk bırakılarak ard arda yazılır.
    return text

#yazılan fonksiyonun yorumlar üzerinde tokenleştirilmiş haliyle görmak için: print(tokens_to_string(x_train_tokens[800])) 



