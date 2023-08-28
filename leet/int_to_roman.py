#!/usr/bin/python3

class Solution(object):
    numerals = ['I', 'V', 'X', 'L', 'C', 'D', 'M']

    def toRoman(self, n, i):
        if n <= 3:
            return self.numerals[i] * n;
        elif n >= 5 and n <= 8:
            return self.numerals[i+1] + self.numerals[i] * (n-5)
        elif n == 4:
            return self.numerals[i] + self.numerals[i+1]
        elif n == 9:
            return self.numerals[i] + self.numerals[i+2]
        else:
            return ''

    def intToRoman(self, num):
        """
        :type num: int
        :rtype: str
        """
        out = ""
        n = num
        for i in range(3, -1, -1):
            x = n // 10**i
            out += self.toRoman(x, 2 * i)
            n -= x * 10**i
        return out

s = Solution()
print(s.intToRoman(1994))
