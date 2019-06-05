# -!- coding: utf-8 -!-
import time
import jieba
import thulac
import io

with io.open("Output.txt","r",encoding = "utf8") as f:
    text = f.read()
start_time_jieba = time.time()
seg_list = jieba.cut(text)
with io.open("cut_jieba.txt","w",encoding = "utf8") as f:
    f.write(" ".join(seg_list))
print("Total running time of jieba: {}".format(time.time() - start_time_jieba))

with io.open("Output.txt","r",encoding = "utf8") as f:
    text = f.read()
start_time_thulac = time.time()
thu1 = thulac.thulac(seg_only = True)
cut_text = thu1.cut(text,text=True)
with io.open("cut_thulac.txt","w",encoding = "utf8") as f:
    f.write(cut_text)
print("Total running time of thulac: {}".format(time.time() - start_time_thulac))
#thu1.cut_f("input.txt","output.txt")
