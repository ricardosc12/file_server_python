import os
import base64

def getFiles(dir = ''):
    try:
        files = os.listdir(dir)
        return {
            'status':True,
            'dados':list(map(lambda x: x, files)),
            'mensagem':'Listado com sucesso !'
        }
    except NotADirectoryError:
        return {'status':False,'mensagem':'Não é um diretório !'}
    except FileNotFoundError:
        return {'status':False,'mensagem':'Não é um arquivo !'}
    except PermissionError:
        return {'status':False,'mensagem':'Sem permissão de acesso !'}

def getFile_(file):
    try:
        file = open(file,'rb')
        binary = file.read()
        base64_ = base64.b64encode(binary).decode('utf-8')
        return {'status':True,'dados':{
            'content':base64_,
        }}
    except FileNotFoundError:
        return {'status':False,'mensagem':'Não é um arquivo !'}
    except PermissionError:
        return {'status':False,'mensagem':'Sem permissão de acesso !'}
    except:
        return {'status':False,'mensagem':'Erro inesperado !'}



def getConfig(IP,PORT):
    try:
        page = open('./config.txt','r')
        file = page.readlines()
        str_ = ''
        public = False
        port = PORT
        for line in file:
            try:
                line = line.replace('\n','')
                if(line[0]=="#" or line[0] == ''): continue
                values = line.split('=')
                config = values[0]
                value = "=".join(values[1:])
                if(config=='HOST' and 'local' in value): 
                    value = value.replace('local',IP)
                if(config=="PUBLIC"):
                    public=True if value=='true' else False
                    continue
                if(config=="PORT"):
                    port = value
                    continue
                str_ = str_+"let {} = '{}'\n".format(config,value)
            except:
                continue
        return public,str_,port
    except FileNotFoundError:
        print(" \n[*] - Arquivo de configuração ausente, criando...")
        path = "./config.txt"
        try:
            os.mkdir("./temp")
            temp = open("./temp/hello.txt","w")
            temp.write(" [*] - Hello World !\n")
            temp.close()
        except:
            pass
        with open(path, "w") as config_file:
            config_file.writelines([
            "PORT=789\n",
            "HOST=local:789\n",
            "PATH=./temp\n",
            "PUBLIC=false\n",
            "#Exemplo com ngrok\n",
            "#--comand: ngrok http 789\n",
            "#PORT=789\n",
            "#HOST=0c94-45-178-248-62.ngrok.io\n",
            "#PATH=./temp\n",
            "#PUBLIC=true\n",
            "#Exemplo\n",
            "#PATH=C:/Users/user/Documents\n",
            ])
            config_file.close()
        return False,"let HOST='{}:789'\nlet PATH='./temp'".format(IP), 789
    except:
        return public,"let HOST='127.0.0.1:789'\nlet PATH='./temp'",port
