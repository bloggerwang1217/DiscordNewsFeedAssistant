import poplib
import os
from email.parser import BytesParser, Parser
from email.policy import default
import json


def get_latest_email():
    user_name = os.environ.get("EMAIL_USERNAME")
    password = os.environ.get("EMAIL_PASSWORD")
    pop3_server = os.environ.get("EMAIL_SERVER", "msa.ntu.edu.tw")

    server = poplib.POP3_SSL(pop3_server, 995)

    server.user(user_name)
    server.pass_(password)

    # num是最後一封
    emails = server.list()[1]
    num = len(emails)

    data = b'\r\n'.join(server.retr(num)[1])


    parsed_data = BytesParser(policy=default).parsebytes(data)

    text = []

    text.append("發件人: " + parsed_data["from"])
    try:
        text.append("收件人: " + parsed_data["to"])
    except:
        text.append("收件人: 未顯示")

    try:
        text.append("標題: " + parsed_data["subject"])
    except:
        text.append("無標題")

    content_list = []
    for part in parsed_data.walk():

        # 如果maintype是multipart，說明是容器（包含正文、附件等）
        if part.get_content_maintype() == 'multipart':
            continue
        elif part.get_content_maintype() == 'text':
            content_list.append("正文:")

            for item in part.get_content().split("\r\n\r\n\r\n"):
                if len(item.strip()) != 0:
                    content_list.append(item.strip())
            break

    text.append(content_list)

    server.quit()

    return text


def check_latest():
    text_list = get_latest_email()
    latest_mail = {}
    with open("save/latest_mail.json") as f:
        latest_mail = json.load(f)

    if latest_mail["sender"] != text_list[0] or latest_mail["receiver"] != text_list[1] or latest_mail["subject"] != text_list[2]:
        with open("save/latest_mail.json", 'w') as f:
            latest_mail["sender"] = text_list[0]
            latest_mail["receiver"] = text_list[1]
            latest_mail["subject"] = text_list[2]
            json.dump(latest_mail, f)
        text_list.insert(0, "**最新信件**")
        return text_list

    else:
        return False 