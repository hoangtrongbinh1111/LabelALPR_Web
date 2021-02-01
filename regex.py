import re


dong1 = ["(^[0-9]{2,2})(A{1,1}|D{1,1})$", "(^[0-9]{2,2})[-]([A-Z]{2,2})$", "(^[0-9]{2,2})([A-Z]{2,2})$",
         "^[A-Z]{2,2}$", "^[0-9]{2,2}[-][0-9]{3,3}$"]
dong2 = ["^[0-9]{3,3}[.][0-9]{2,2}$", "^[0-9]{4,4}$", "^[0-9]{3,3}[.][0-9]{2,2}$", "^[0-9]{2,2}[-][0-9]{2,2}$", "^[A-Z]{2,2}[-][0-9]{3,3}$"]
#matching : 1 - 1, 2 - 2, 3 - 3, 4 - 4, 5 - 5

def check2dong(str1, str2):
    for rex in range(0, 4, 1):
        if re.search(dong1[rex], str1):
            if re.search(dong2[rex], str2):
                return True
    return False

def check1dong(str_):
    for rex in range(0, 4, 1):
        s1 = dong1[rex]
        s2 = dong2[rex]
        ss = s1[:len(s1)-1] + "[-]"+s2[1:]
        print(ss)
        if re.search(ss, str_):
            return True
    return False

print(check2dong("00A", "000.00"))
print(check1dong("00A-000.00"))