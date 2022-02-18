import poplib
import os
from email.parser import BytesParser, Parser
from email.policy import default
import json


def get_latest_email(return_list = False):
    user_name = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]
    pop3_server = os.environ["SERVER"]

    server = poplib.POP3_SSL(pop3_server, 995)

    server.user(user_name)
    server.pass_(password)

    # num是最後一封
    emails = server.list()[1]
    num = len(emails)

    data = b'\r\n'.join(server.retr(num)[1])


    parsed_data = BytesParser(policy=default).parsebytes(data)

    text = []

    text.append("發件人:" + parsed_data["from"])
    text.append("收件人:" + parsed_data["to"])
    text.append("內容:" + parsed_data["subject"])

    for part in parsed_data.walk():

        # 如果maintype是multipart，說明是容器（包含正文、附件等）
        if part.get_content_maintype() == 'multipart':
            continue
        elif part.get_content_maintype() == 'text':
            text.append("----------")
            text.append(part.get_content())

    server.quit()

    if return_list:
        return text
    else:
        return '\n'.join(text)


def check_latest():
    text_list = get_latest_email(True)
    latest_mail = {}
    with open("save/latest_mail.json") as f:
        latest_mail = json.load(f)
    if latest_mail["sender"] != text_list[0] or latest_mail["receiver"] != text_list[1] or latest_mail["content"] != text_list[2]:
        with open("save/latest_mail.json") as f:
            latest_mail["sender"] = text_list[0]
            latest_mail["receiver"] = text_list[1]
            latest_mail["content"] = text_list[2]
            json.dump(latest_mail, f)
        return "**最新信件**\n"+'\n'.join(text_list)
    else:
        return False 