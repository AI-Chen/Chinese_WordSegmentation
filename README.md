# Chinese_WordSegmentation
对经典的基于词典的和基于字的中文方法的实现以及比较
## 评测模型包括
- 最大匹配算法
- N-最短路径算法
- HMM隐马尔科夫模型
- bilstm+crf
## 评测代码
以最大匹配算法为例：
- python max_match/max_match.py
- perl ../score ../data/pku_training.utf8 ../data/pku_test_gold.utf8 max_match/pku_result.utf8 > max_match/score.utf8
- tail -14 max_match/score.utf8
