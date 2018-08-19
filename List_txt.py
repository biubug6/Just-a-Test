import os 

path = ''

filenames = os.listdir(path)
filenames.sort()
with open('query.txt', 'w') as f:
    for name in filenames:
        st = name.split('_')
        id = int(st[0])
        cam = int(st[1][1])
        nameq = os.path.join('query', name)
        context = '{:04d} {:02d} {}\n'.format(id, cam, name1)
        f.write(context)
print ('finish!')
