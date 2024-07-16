#!/usr/bin/python
# Translate srt file to spanish (or any language changing the parameter below)
# pass the srt file name as argument
# first time it will take longer as it has to download the models

import dl_translate as dlt
import pysrt
import sys
import re
import nltk

if(len(sys.argv) < 2):
    print("Need to pass file name : ", len(sys.argv))
    sys.exit()

nltk.download("punkt")

name_f = sys.argv[1]

mt = dlt.TranslationModel("facebook/nllb-200-distilled-600M", device="gpu")
CLEANR = re.compile('<.*?>') 

subs = pysrt.open(name_f)
leng = len(subs)
print ("Lenght " , len(subs))

for i in range(leng):
    text_to = re.sub(CLEANR, '' , (subs[i].text))
    #print("original: " , text_to)
    sents = nltk.tokenize.sent_tokenize(text_to, "english") 
    #print("tokens: " , sents)
    tran = "\n".join(mt.translate(sents, source=dlt.lang.ENGLISH, target=dlt.lang.SPANISH))
    #print("traduccion: " ,tran)
    if 'Qué es eso' not in tran:
       subs[i].text = tran
    else:
        subs[i].text = text_to
    print("%i / %i" % (leng, int(i))  )

subs_es = (name_f[:-3]+ "es.srt")
subs.save(subs_es)

