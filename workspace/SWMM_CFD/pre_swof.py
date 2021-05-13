import os,para
fieldname='U'
patchname='inlet'
filename='data2'
init=para.init

os.system('rm -rf comms')
os.system('cp -f changeDictionaryDict openfoam/system/') 
with open('openfoam/system/changeDictionaryDict','a') as f1:
    f1.writelines(fieldname)
    f1.writelines('{boundaryField{')

    f1.writelines('~'+patchname+';')
    f1.writelines(patchname+'{')

    f1.writelines('type '+'externalCoupled;')
    f1.writelines('commsDir        "comms";')
    f1.writelines('file '+filename+';')
    f1.writelines('initByExternal '+str(init)+';')

    f1.writelines('}')
    f1.writelines('}}')
    f1.writelines('\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //')

os.system('changeDictionary -case openfoam')