import itchat
import os
from PIL import Image
from threading import Thread

itchat.auto_login(hotReload=True, enableCmdQR=True)
MyUserName = itchat.search_friends(nickName='啦啦啦被煮')[0]['UserName']

DealDict = []


@itchat.msg_register(itchat.content.PICTURE)
def image_reply(msg):
    msg.download(msg.fileName)
    gif_file_name = msg.fileName+'.gif'
    if msg.FromUserName in DealDict:
        return '您有图片正在处理，请稍后重试'
    elif len(DealDict) >= 4:
        return '当前处理用户超过4人，请稍后重试'
    DealDict.append(msg.FromUserName)
    try:
        image = Image.open(msg.fileName)
        if image.format == 'GIF':
            return '这张图片可以直接存表情哦'
        w, h = image.size
        if w > 500:
            image = image.resize((500, int(h * 500 / w)), Image.ANTIALIAS)
        w, h = image.size
        if h > 500:
            image = image.resize((int(w * 500 / h), 500), Image.ANTIALIAS)
        image.save(gif_file_name, 'GIF')
        itchat.send_image(gif_file_name, toUserName=msg.FromUserName)
        itchat.send(msg.User['NickName'] + '发送了一张图片', toUserName=MyUserName)
        itchat.send_image(gif_file_name, toUserName=MyUserName)
        os.remove('./'+gif_file_name)
    except:
        return '图片转换失败'
    finally:
        DealDict.remove(msg.FromUserName)
        os.remove('./'+msg.fileName)


@itchat.msg_register(itchat.content.TEXT)
def text_redirect(msg):
    itchat.send(msg.User['NickName'] + ' : ' + msg.Text, toUserName=MyUserName)


Thread(target=itchat.run).start()
Thread(target=itchat.run).start()
Thread(target=itchat.run).start()
Thread(target=itchat.run).start()
Thread(target=itchat.run).start()
