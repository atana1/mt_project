from collections import deque


with open("hindencorp05.plaintext") as f:
    store_en = deque
    store_hi = deque
    store_seg = deque
    for line in f:
        source_id, seg, align_q, en_sen, hi_sen = line.split("\t")
        store_en.append(en_sen)
        store_hi.append(hi_sen)
        store_seg.append(seg)

eng_sent = []
hin_sent = []
for item in store_seg:
    ec, hc = item.split("-")
    en_sent = []
    hi_sent = []
    for i in xrange(ec):
        en_sent.append(store_en.popleft())
    for i in xrange(hc):
        hi_sent.append(store_hi.popleft())
    if len(en_sent) == 1:
        eng_sent.append(en_sent[0])
    else:
        new_sent = "".join()
    if len(hi_sent) == 1:
        hin_sent.append(hi_sent[0])

#for item in store_en:
#    print item


