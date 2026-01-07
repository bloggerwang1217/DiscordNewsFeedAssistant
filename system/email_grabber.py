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
    """Check for new emails since last check"""
    user_name = os.environ.get("EMAIL_USERNAME")
    password = os.environ.get("EMAIL_PASSWORD")
    pop3_server = os.environ.get("EMAIL_SERVER", "msa.ntu.edu.tw")

    try:
        server = poplib.POP3_SSL(pop3_server, 995)
        server.user(user_name)
        server.pass_(password)

        # Get current email count
        emails = server.list()[1]
        current_count = len(emails)

        # Load last checked count
        latest_mail = {}
        with open("save/latest_mail.json") as f:
            latest_mail = json.load(f)

        last_count = latest_mail.get("last_count", current_count)

        # If no new emails, return
        if current_count <= last_count:
            server.quit()
            return False

        # Process new emails (up to 5 most recent to avoid flooding)
        new_emails = []
        start_index = max(last_count + 1, current_count - 4)  # Process at most 5 new emails

        for email_num in range(start_index, current_count + 1):
            data = b'\r\n'.join(server.retr(email_num)[1])
            parsed_data = BytesParser(policy=default).parsebytes(data)

            text = []
            text.append("**新信件**")
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
                if part.get_content_maintype() == 'multipart':
                    continue
                elif part.get_content_maintype() == 'text':
                    content_list.append("正文:")
                    for item in part.get_content().split("\r\n\r\n\r\n"):
                        if len(item.strip()) != 0:
                            content_list.append(item.strip())
                    break

            text.append(content_list)
            new_emails.append(text)

        # Update last count
        latest_mail["last_count"] = current_count
        with open("save/latest_mail.json", 'w') as f:
            json.dump(latest_mail, f)

        server.quit()
        return new_emails if new_emails else False

    except Exception as e:
        print(f"Email check error: {e}")
        return False 