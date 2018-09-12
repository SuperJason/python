#!/usr/bin/env python3
"""
    patterns statistics of colorful glass balls lottery

    20 balls, 4 colors(red, yellow, green, blue), 5 balls per color
    grab 1 ball per time and grab 10 times
    statistic the probability of every pattern
"""

import random

def grab_ten_balls():
    r = 0
    y = 0
    g = 0
    b = 0
    red = ['red','red','red','red','red']
    yellow = ['yellow','yellow','yellow','yellow','yellow']
    green = ['green','green','green','green','green']
    blue = ['blue','blue','blue','blue','blue']
    balls = red + yellow + green + blue
    for i in range(10):
        ball = random.randrange(len(balls))
        #print("balls: " + str(balls))
        #print("len: " + str(len(balls)) + ", ball: " + str(ball) + ", color: " + balls[ball])
        if balls[ball] == 'red': 
            r = r + 1
            del(balls[ball])
        elif balls[ball] == 'yellow':
            y = y + 1
            del(balls[ball])
        elif balls[ball] == 'green':
            g = g + 1
            del(balls[ball])
        elif balls[ball] == 'blue':
            b = b + 1
            del(balls[ball])
    x = [r, y, g, b]
    x.sort()
    x.reverse()
    return x

def patterns_statics(cnt=1000):
    patterns = {}
    for i in range(cnt):
        pattern = grab_ten_balls()
        if str(pattern) in patterns:
            p, c = patterns[str(pattern)]
            c = c + 1
            p = float(c)/cnt
            patterns[str(pattern)] = p, c
        else:
            c = 1
            p = float(c)/cnt
            patterns[str(pattern)] = p, c

    return patterns

def patterns_statics_show(times=4, sorted_by='keys'):
    print("times: " + str(10**times) + "(10**" + str(times) + ")")
    patterns = patterns_statics(10**times)

    print("patterns\tprobabilitys\tcount")
    # sorted by keys
    if sorted_by == 'keys':
#        sorted_patterns_list = \
#                [(k,patterns[k]) for k in sorted(patterns.keys(), reverse=True)]
        sorted_patterns_list = \
                sorted(patterns.items(), key=lambda x:x[0], reverse=True)
    # sorted by values
    elif sorted_by == 'value':
        sorted_patterns_list = sorted(patterns.items(), key=lambda x:x[1][0])
    cnt = 0
    for p, c in sorted_patterns_list:
        cnt = cnt + 1
        s = p[1] + p[4] + p[7] + p[10]
        print("%2d> %s\t%6.3f%%\t\t%8d"%(cnt, s, c[0]*100, c[1]))

def random_static(cnt=1000):
    patterns = {}
    for i in range(cnt):
        pattern = random.randrange(20)
        if pattern in patterns:
            p, c = patterns[pattern]
            c = c + 1
            p = float(c)/cnt
            patterns[pattern] = p, c
        else:
            c = 1
            p = float(c)/cnt
            patterns[pattern] = p, c

    return patterns

def random_static_show(times=4):
    print("times: " + str(10**times) + "(10**" + str(times) + ")")
    patterns = random_static(10**times)

    print("patterns\tprobabilitys\tcount")
    sorted_patterns_list = \
            [(k,patterns[k]) for k in sorted(patterns.keys())]
    cnt = 0
    for p, c in sorted_patterns_list:
        cnt = cnt + 1
        print("%2d> %2d\t\t%2.3f%%\t\t%8d"%(cnt, int(p), c[0]*100, c[1]))


# Following result takes about 20 minites
# times: 100000000(10**8)
# patterns        probabilitys   count
#  1> 5500         0.003%         3344
#  2> 5410         0.325%       325289
#  3> 5320         1.299%      1298885
#  4> 5311         1.626%      1626422
#  5> 5221         3.246%      3245912
#  6> 4420         1.625%      1624950
#  7> 4411         2.029%      2029334
#  8> 4330         3.245%      3245040
#  9> 4321        32.470%     32469560
# 10> 4222        10.828%     10828108
# 11> 3331        10.824%     10823602
# 12> 3322        32.480%     32479554

# Following result takes about 20 minites
# times: 100000000(10**8)
# patterns        probabilitys   count
#  1> 5500         0.003%         3265
#  2> 5410         0.325%       324594
#  3> 5320         1.299%      1299075
#  4> 5311         1.623%      1622909
#  5> 5221         3.247%      3247176
#  6> 4420         1.624%      1623695
#  7> 4411         2.030%      2030253
#  8> 4330         3.245%      3244983
#  9> 4321        32.480%     32480487
# 10> 4222        10.825%     10824749
# 11> 3331        10.823%     10823249
# 12> 3322        32.476%     32475565

if __name__ == '__main__':
#    print(grab_ten_balls())
    patterns_statics_show(6, 'value')
#    random_static_show(6)

