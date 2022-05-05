import os, time
from sys import platform, argv

virstrs = []
virfiles = []
supfiles = []
done_dirs = []
unopenable = []

def check_dir(the_dir):
    global unopenable
    cur_dir = the_dir
    unopenablele = []
    vir_strs = []
    vir_files = []
    sup_files = []
    newline = False
    scaned_files = []
    samples_file = 'virstrings.txt'
    f = open(samples_file, 'r')
    virstrings = f.read().split('\n')
    f.close()
    for a, aa, filenames in os.walk(cur_dir, topdown=True):
        for file in filenames:
            if file != __file__ or samples_file:
                try:
                    if argv[1] == 'fast':
                        time.sleep(0.05)
                    elif argv[1] == 'slow':
                        time.sleep(1)
                except:
                    time.sleep(0.5)
                if platform == 'linux':
                    full_file = str(a) + '/' + str(file)
                elif platform == 'windows':
                    full_file = str(a) + '\\' + str(file)
                scaned_files = scaned_files + [file]
                if file.endswith('.py') or file.endswith('.pym'):
                    try:
                        f = open(full_file, 'r')
                        data = f.read().split('\n')
                        f.close()
                    except:
                        if unopenablele == []:
                            unopenablele = [full_file]
                        else:
                            unopenablele = unopenablele + [full_file]
                        continue
                    for i in virstrings:
                        for a in data:
                            if i in a:
                                vir_strs = vir_strs + [file + ':' + ''.join(virstrings[i:il])]

    breaknt = False
    if len(vir_strs) > 0:
        for i in range(len(vir_strs)):
            time.sleep(0.1)
            il = i + 1
            filename = ''.join(''.join(vir_strs[i:il]).split(':')[0:1])
            vir_files = vir_files + [filename]
    f = open('virnames.txt')
    data = f.read().split('\n')
    f.close()
    sup_files = []
    for i in data:
        for a in scaned_files:
            if i in a:
                if sup_files != []:
                    sup_files = sup_files + [a]
                else:
                    sup_files = [a]
    cur_dir = [cur_dir]
    if unopenablele != []:
        return vir_strs, vir_files, sup_files, cur_dir, unopenablele
    else:
        return vir_strs, vir_files, sup_files, cur_dir, unopenable


def stoper(filename, dirs):
    quarentined_files = []
    for i in quarentined_files:
        if filename == i:
            breaknt = True
            break
        else:
            quarentined_files = quarentined_files + [filename]
    if quarentined_files == []:
        quarentined_files = quarentined_files + [filename]
    try:
        f = open(filename, 'a+')
        data = f.read().split('\n')
        for i in data:
            da = encode(i)
            f.write(da + '\n')
        f.close()
    except:
        if platform == 'linux':
            print(f'can\'t open potential malware file {filename}, delete it yourself.')
        elif platform == 'windows':
            print(f'can\'t open potential malware file {filename}, delete it yourself.')

if platform == 'windows':
    userprofile = os.popen('echo %userprofile%')
    dirs_to_check = [x[0] for x in os.walk(userprofile)]

if platform == 'linux':
    dirs_to_check = [x[0] for x in os.walk('/home')] + [x[0] for x in os.walk('/tmp')]

for dirs in dirs_to_check:

    if virstrs == []:
        if supfiles == []:
            if virfiles == []:
                if done_dirs == []:
                    virstrs, virfiles, supfiles, done_dirs, unopenable = check_dir(dirs)
                    continue
    
    a, b, c, d, e = check_dir(dirs)
    virstrs = virstrs + a; virfiles = virfiles + b; supfiles = supfiles + c; done_dirs = done_dirs + d; unopenable = unopenable + e

if virstrs != []:
    print('\npotentialy dangrous strings in python files:')
    for i in virstrs:
        print(i)
    print('\n')
if virfiles != []:
    print('disabling files')
    for i in virfiles:
        stoper(i, dirs)

prev_file = ''
if supfiles != []:
    print('suspiously named files (won\'t disable)')
    for i in supfiles:
        if prev_file != i:
            print(i)
            prev_file = i
    print('\n')

if unopenable != []:
    unopenable = len(unopenable)

if virfiles == virstrs:
    print(f'no virus files found in {unopenable} files\n')
else:
    print('scaned', unopenable, 'files\n')
print(f'scaned {len(done_dirs)} directories')
