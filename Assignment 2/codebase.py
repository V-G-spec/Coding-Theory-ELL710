# %%
"""
## Imports
"""

# %%
import math
import copy

# %%
"""
## Generation
### Not Required
"""

# %%
# • k input sequences enter from the left;
# • n output sequences produced by external mod-2 adders
# • Input sequence u = (u0, u1, u2, ...)
# • Output sequence v = (v0(0), v0(1), v1(0), v1(1), ...)
# • v(0)= g1+g2
# • v(1)= g1
# • Impulse response sequences: u = (1, 0, 0, 0, ...) produces output
#     • g(0) = 0, 1, 1
#     • g(1) = 0, 1, 0
# • v(0) = u_(l-1) + u_(l-2) = u*g(0)
# • v(1) = u_(l-1) = u*g(1)
#   * is a discrete convolution
    
# n = 2, k = 1, m = 2, C (constraint length) = n*(m+1) = 6 (# output bits)
#     Let length of input stream be 4 (Remember to flush out while encoding 
#     and prolly truncate while decoding)
#     Size of G: [4 x n(m+4)] = [4 x 12]
# • G = [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0;
#        0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0;
#        0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0;
#        0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0] 

# %%
# G = [[0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0]]
# G

# %%
# u = np.array([1, 0, 1, 1])
# print(u.dot(G)%2)

# %%
"""
## Viterbi Decoding
"""

# %%
def getOutnSt(curr_st, inp):
    if curr_st=='00':
        if inp=='0':
            new_st = '00'
            outp = '00'
        elif inp=='1':
            new_st = '10'
            outp = '11'
    elif curr_st=='01':
        if inp=='0':
            new_st = '00'
            outp = '00'
        elif inp=='1':
            new_st = '10'
            outp = '11'
    elif curr_st=='10':
        if inp=='0':
            new_st = '01'
            outp = '10'
        elif inp=='1':
            new_st = '11'
            outp = '01'
    elif curr_st=='11':
        if inp=='0':
            new_st = '01'
            outp = '10'
        elif inp=='1':
            new_st = '11'
            outp = '01'
    return new_st, outp


def hamwt(str1, str2):
    assert(len(str1)==len(str2))
    assert(len(str1)==2)
    ct = 0
    for i in range(2):
        if str1[i]!=str2[i]:
            ct+=1
    return ct

def adderr(codew, errloc):
    if (errloc<0):
        return codew
    # Assume even input digits
    l = list(codew)
    assert(len(codew)>errloc)
    if l[errloc]=='0':
        l[errloc]='1'
    else:
        l[errloc] = '0'
    return ''.join(l)

def ViterbiMin(trellDict):
    minval = math.inf
    decoded = ""
    for k,v in trellDict.items():
        if v<minval:
            minval=v
            decoded = k
    return decoded, minval

def decodeViterbiGreedy(code):
    assert(len(code)%2==0)
    output = ""
    # trellisDict = {}
    prevStateDict = {'00': 0, '01': math.inf, '10': math.inf, '11': math.inf}
    currStateDict = {}
    while(len(code)>0):
        curr_code = code[:2]
        prev_state, minHamm = ViterbiMin(prevStateDict)
        # print(prev_state)
        next_poss_state1, next_poss_op1 = getOutnSt(prev_state, '0')
        next_poss_state2, next_poss_op2 = getOutnSt(prev_state, '1')
        
        diff1 = hamwt(next_poss_op1, curr_code)
        if next_poss_state1 in currStateDict:
            if minHamm + diff1 < currStateDict[next_poss_state1]:
                currStateDict[next_poss_state1] = minHamm + diff1
        else:
            currStateDict[next_poss_state1] = minHamm + diff1

        diff2 = hamwt(next_poss_op2, curr_code)
        if next_poss_state2 in currStateDict:
            if minHamm + diff2 < currStateDict[next_poss_state2]:
                currStateDict[next_poss_state2] = minHamm + diff2
        else:
            currStateDict[next_poss_state2] = minHamm + diff2

        curr_state, minHamm = ViterbiMin(currStateDict)
        curr_poss_state1, curr_poss_op1 = getOutnSt(prev_state, '0')
        curr_poss_state2, curr_poss_op2 = getOutnSt(prev_state, '1')
        if curr_state == curr_poss_state1:
            output += curr_poss_op1
        elif curr_state == curr_poss_state2:
            output += curr_poss_op2

        prevStateDict = copy.deepcopy(currStateDict)
        currStateDict = {}
        code = code[2:]
    return output



def decodeViterbiRec(code, init_state='00'):
    assert(len(code)%2==0)
    if len(code)==0:
        return '', 0
    else:
        curr_code = code[:2]
        code = code[2:]
        chan1st, chan1op = getOutnSt(init_state, '0')
        chan2st, chan2op = getOutnSt(init_state, '1')
        hlp1cod, hlp1 = decodeViterbiRec(code, chan1st)
        hlp2cod, hlp2 = decodeViterbiRec(code, chan2st)
        chan1wt = hamwt(chan1op, curr_code) + hlp1
        chan2wt = hamwt(chan2op, curr_code) + hlp2
        if (chan1wt>chan2wt):
            return chan2op+hlp2cod, chan2wt
        else:
            return chan1op+hlp1cod, chan1wt


def compareFromOrig(orig, decoded):
    assert(len(orig)==len(decoded))
    for i in range(len(orig)):
        if orig[i]!=decoded[i]:
            print("Nop, work hard for audit pass in major")
            return
    print("Yep, we did it! Easy NP for me, yeyy. Maybe I should have credited this course, I love it")
    return 

# %%
"""
## Testing!
"""

# %%
init_code = '11011011'
for i in range(len(init_code)):
    err_loc = i
    print("Raw Code:", init_code)
    print("Adding Error")
    code = adderr(init_code, err_loc)
    print("Erroneous Code:", code)
    decoded1 = decodeViterbiGreedy(code)
    decoded2, decwt = decodeViterbiRec(code)
    print("Viterbi decoded code by greedy algorithm:", decoded1)
    print("Result for Greedy:")
    compareFromOrig(init_code, decoded1)
    print("Viterbi decoded code by recursive algorithm:", decoded2)
    print("Result for Recursive:")
    compareFromOrig(init_code, decoded2)
    print("----------------------------------------------")

# %%
