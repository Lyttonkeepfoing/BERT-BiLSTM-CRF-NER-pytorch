# BERT-BiLSTM-CRF模型

### 输入数据格式请处理成BIO格式，如下：
```
彭	B-name
小	I-name
军	I-name
认	O
为	O
，	O
国	O
内	O
银	O
行	O
现	O
在	O
走	O
的	O
是	O
台	B-address
湾	I-address

温	B-name
格	I-name
的	O
球	O
队	O
终	O
于	O
```

### 在中文CLUENER2020的eval集上的结果如下：
```
processed 50260 tokens with 3072 phrases; found: 3363 phrases; correct: 2457.█
accuracy:  94.08%; precision:  73.06%; recall:  79.98%; FB1:  76.36
          address: precision:  54.63%; recall:  63.27%; FB1:  58.63  432
             book: precision:  77.02%; recall:  80.52%; FB1:  78.73  161
          company: precision:  72.58%; recall:  81.22%; FB1:  76.65  423
             game: precision:  78.27%; recall:  89.15%; FB1:  83.36  336
       government: precision:  75.36%; recall:  85.43%; FB1:  80.08  280
            movie: precision:  82.19%; recall:  79.47%; FB1:  80.81  146
             name: precision:  84.35%; recall:  89.25%; FB1:  86.73  492
     organization: precision:  71.15%; recall:  79.29%; FB1:  75.00  409
         position: precision:  74.46%; recall:  79.45%; FB1:  76.87  462
            scene: precision:  65.77%; recall:  69.86%; FB1:  67.75  222
```