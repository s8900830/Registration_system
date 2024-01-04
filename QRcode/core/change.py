import hashlib


class mainfunction:

    def _to62(num):
        to62list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
                    'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        sixtwo = []
        while (True):

            rem = num % 62
            sixtwo.append(to62list[int(rem)])
            num = num // 62
            if num == 0:
                break

        return sixtwo

    def hashcode_test(hashcode):
        num = hash(hashcode)
        if num < 0:
            num = 0 - num
        num_hex = mainfunction._to62(num)

        return ''.join(num_hex)

    def change(ourl):
        surl = mainfunction.hashcode_test(ourl)
        return surl
