# s = 'we are form sitare university'
# print(w_lst)

def find_ngrams():
    s = str(input("Enter you string :-"))
    w_lst = s.split()
    n = int(input("Enter your n-grama :-"))
    for i in range(len(w_lst)-n+1):
        print(w_lst[i:i+n])
       
find_ngrams()