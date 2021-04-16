import telebot
import time
import requests
import random
import json
import http.client
import mimetypes
from codecs import encode

TELEGRAM_TOKEN = "1706269133:AAEVfwrvBS4gKNeoq4Nc8n0RNZV3WhyO8UU"
bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)
r = requests.get("https://pastebin.com/raw/7VzfGkkS").text
c = "".join(str(r)).split("\n")
l = random.choice(c)
@bot.message_handler(commands=['start'])
def hi(message):
    bot.reply_to(message, "اهلا بك في بوت رفع اسئلة الى موقع Bartleby من فضلك قم بارسال صورة السؤال اللذي تريد رفعه")
@bot.message_handler(content_types=['photo'])
def send_welcome(message):
    bot.reply_to(message, "Wait to post your question . . . [-]")
    raw = message.photo[-1].file_id
    path = raw + ".jpg"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file)
    conn = http.client.HTTPSConnection("nk6xemh85d.execute-api.us-east-1.amazonaws.com")
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=data;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("{\"questionText\":\"<p></p>\",\"subjectShortName\":\"chemical-engineering\"}"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=uploads; filename={0}'.format('')))
    fileType = mimetypes.guess_type('photo/' + path)[0] or 'application/octet-stream'
    dataList.append(encode('Content-Type: {}'.format(fileType)))
    dataList.append(encode(''))
    with open(path, 'rb') as f:
        dataList.append(f.read())
    dataList.append(encode('--' + boundary + '--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
        'Content-Disposition': f'form-data; name="uploads"; filename=f"{path}"',
        'Authorization': f'Bearer {l}',
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    conn.request("POST", "/prod/user/qna-question", payload, headers)
    res = conn.getresponse()
    data = res.read()
    vv = data.decode("utf-8")
    m = json.loads(vv)
    id = m['data']['questionId']
    if ('"message":"Question successfully posted."') in data.decode("utf-8"):
        bot.reply_to(message,"Successfully uploaded to Chemical Engineering [+]\n\n\nTime : "+str(time.time_ns())+"\n\n\nLink : https://www.bartleby.com/questions-and-answers/chemical-engineering/" + id)
    else:
        bot.reply_to(message, "Failed ...")




bot.polling()