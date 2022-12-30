#!/usr/bin/python3
def longestPalindrome( s: str) -> str:
    lp = 0
    mlp = 0
    mli = 0
    li = 0
    for c in range(0, len(s)):
        if lp == 0:
            lp = 1
            li = 0
        else:
            if c - lp - 1 == 0:
                lp = 1
                li = c - 1
            if c - lp - 1 >= 0 and s[c] == s[c - lp - 1]:
                lp += 2
                li -= 1
            elif c - 1 >= 0 and s[c] == s[c - 1]:
                lp += 1
            else:
                lp = 1
                li = c

        #
        # elif lp == 1:
        #     if c - 1 >= 0 and s[c] == s[c - 1]:
        #         lp += 1
        #     elif c - 2 >= 0 and s[c] == s[c - 2]:
        #         lp += 2
        #         li -= 1
        #     else:
        #         li += 1
        # else:
        #     #print(c-lp-1)
        #     if c-lp-1 >=0 and s[c] == s[c - lp - 1]:
        #         lp += 2
        #         li -= 1
        #     elif c-lp >=0 and s[c] == s[c-lp]:
        #         lp += 1
        #     else:
        #         lp = 1
        #         li = c
        if lp > mlp:
            mlp = lp
            mli = li
        #print('current index:',c,lp,li,mlp,mli,(c-lp-1))
    return s[mli:mli + mlp]

print(longestPalindrome('cbbd'))
print(longestPalindrome('babad'))
print(longestPalindrome('abba'))
print(longestPalindrome('findnitianhere'))
print(longestPalindrome('apqjpwedlhmvvpexxnntxheeynxmgzwxhnhfdvziuxnuusymklgcacndoyhqkoahnkyaikohwkmnuphipftmzmihvmoetskioeypwjujvvusaxynzxxdugnebsisrtgeujkqkgwjuplijhluumqcdurovyjsbowmnqndejwkihzbbdyxjunkduyqeihektaknbmkzgnnmgywylulxwyywrvieqfenjeljofkqqqisdjsbfkvqgahxwkfkcucvrbbpyhwkfztjdboavtfynrudneieelwlcezqsuhmllcsadcnoyemsfdlrijoyj'))
print(longestPalindrome('ccc'))
print(longestPalindrome("aacabdkacaa"))