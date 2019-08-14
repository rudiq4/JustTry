# text = 'tralalalal'
#
# f = open('members.txt', 'w')
# f.write(text)
# f.close()

f = open('members.txt', 'r')
line = f.readline()

if not line:
    print('True')

print(len(f.readline()))
print(f.readline()[-1])