def get_dict(filename='../data/pku_training_words.utf8'):
    """读取字典"""
    d = {}
    d['_t_'] = 0.0
    with open(filename, "r") as f:
        for line in f:
            word = line.split('\n')[0]
            d['_t_'] += 1
            d[word] = 1
    return d
d = get_dict()


def build_graph(s, big_dict):
    l = len(s)
    # 邻接矩阵，用dict实现
    adj = {}
    for i in range(l+1):
        adj[i] = {}
    for i in range(l):
        adj[i][i+1] = 1
    for size in range(2, l+1):
        for start in range(l+1):
            if start + size <= l and s[start: start+size] in big_dict:
                # 所有权值（长度）都直接选用1
                adj[start][start+size] = 1
    return adj



def row_equal(row_1, row_2):
    """判断信息记录表中某两行是否重复"""
#     print(row_1, row_2)
    return row_1[1] == row_2[1] and row_1[2][0] == row_2[2][0] and row_1[2][1] == row_2[2][1]

def keep_n_min(candidates, n, length_index=1):
    """保留前N小的所有路径"""
    candidates = sorted(candidates, key=lambda x: x[length_index])
    last_one = -1
    count = 0
    last = -1
    for i, one in enumerate(candidates):
        if one[length_index] != last_one:
            last_one = one[length_index]
            count += 1
            if count > n:
                last = i
                break
    if last != -1:
        candidates = candidates[:last]
    index = 0
    # 更新路径编号
    last_len = -1
    del_indices = []
    for i, row in enumerate(candidates):
        if i > 0 and row_equal(candidates[i], candidates[i-1]):
            del_indices.append(i)
        if row[length_index] != last_len:
            last_len = row[length_index]
            index += 1
        candidates[i][0] = index
    for i in del_indices[::-1]:
        del candidates[i]
    return candidates

def get_tables_by_adj(adj, n):
    """使用类似Dijkstra的贪心算法获得信息表"""
    l = len(adj)
    tables = [[[1, 0, (0, 0)]]]  # 第0个table实际上用不到，这里初始化用于占位
    for cur in range(1, l):
        candidates = []
        i = 0
        for pre in range(cur):
            if cur in adj[pre]:  # 存在从结点pre指向结点cur的边
                for row in tables[pre]:
                    candidates.append([i, row[1] + 1, (pre, row[0])])
        # 保留长度前N小的所有candidate到table
        table = keep_n_min(candidates, n)
        tables.append(table)
    return tables

def core_retro(s, cur, pre, path_index, one_res, one_length_res, pre_node_index,tables):
    """回溯的核心函数"""
    one_res.append(s[pre: cur])
    if pre == 0:
        one_length_res.append(one_res[::-1])
    else:
        for one_row in tables[pre]:
            if one_row[0] == path_index:
                core_retro(s, pre, one_row[pre_node_index][0],
                           one_row[pre_node_index][1], one_res, one_length_res, pre_node_index,tables)
                one_res.pop()

def retro_back(s, tables, n, length_index=1, pre_node_index=2):
    """根据信息记录表回溯分词结果"""
    count = 0
    last_len = -1
    res = {}
    l = len(s)
    for row in tables[-1]:
        # 只留长度是前n个的结果
        cur = l
        if row[length_index] != last_len:
            last_len = row[length_index]
            count += 1
            if count > n:
                break
        # 开始回溯
        one_length_res = []
        one_res = []
        # 回溯的核心函数
        core_retro(s, cur, row[pre_node_index][0], row[pre_node_index][1], one_res, one_length_res, pre_node_index,tables)
        if row[length_index] not in res:
            res[row[length_index]] = one_length_res
        else:
            res[row[length_index]] += one_length_res
    return res


def segstr(str):
    adj = build_graph(str, d)
    tables = get_tables_by_adj(adj, 1)
    res = retro_back(str, tables, 1)
    return res

if __name__ == '__main__':
    # test = "他说的的确在理"
    # print(segstr(test))
    testset = open('../data/pku_test.utf8', encoding='utf-8')       #读取测试集
    output = ''

    for line in testset:
        line = line.strip()
        seg = segstr(line)
        seg = list(seg.items())[0][1][0]
        seg = " ".join(seg) + "\n"
        output = output + seg
    outputfile = open('pku_result.utf8', mode='w', encoding='utf-8')
    outputfile.write(output)
