import poplib
import os
from email.parser import BytesParser, Parser
from email.policy import default
import json
from bs4 import BeautifulSoup


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

    # Get subject and clean up email address in parentheses
    try:
        subject = parsed_data["subject"]
        # Remove email address in parentheses at the end
        if subject.endswith(")"):
            subject = subject[:subject.rfind("(")].strip()
        text.append("標題: 「" + subject + "」")
    except:
        text.append("無標題")

    content_list = []
    content_added = False
    for part in parsed_data.walk():
        # 如果maintype是multipart，說明是容器（包含正文、附件等）
        if part.get_content_maintype() == 'multipart':
            continue
        elif part.get_content_maintype() == 'text':
            content = part.get_content()
            content_type = part.get_content_type()

            # If HTML, parse with BeautifulSoup
            if content_type == 'text/html':
                soup = BeautifulSoup(content, 'html.parser')
                # Remove script and style tags
                for script in soup(["script", "style"]):
                    script.decompose()
                content = soup.get_text()

            # Clean up content: replace multiple line breaks
            content = content.replace('\r\n\r\n\r\n', '\n\n')
            content = content.replace('\r\n', '\n')

            # Remove email addresses and spam patterns
            lines = content.split('\n')
            cleaned_lines = []
            for line in lines:
                # Skip lines that are just email addresses
                if '@' in line and len(line.replace('@', '').replace('.', '')) < 30:
                    continue
                # Skip lines with "邀請對象" section or attendee lists
                if any(skip_text in line for skip_text in ['邀請對象', '查看所有', '回覆', '由於你是', '轉寄', '來自 Google']):
                    continue
                # Skip very long URLs
                if 'https://' in line and len(line) > 100:
                    continue
                cleaned_lines.append(line)

            # Keep structure: preserve 1-2 blank lines for readability
            content = '\n'.join(cleaned_lines)
            # Remove excessive blank lines (3+) but keep 1-2 for paragraph breaks
            while '\n\n\n' in content:
                content = content.replace('\n\n\n', '\n\n')

            # Limit length to avoid flooding (first 1500 chars)
            if len(content) > 1500:
                content = content[:1500] + "\n...(內容過長，已截斷)"

            if content.strip():
                content_list.append("正文:\n" + content.strip())
                content_added = True
            break

    if not content_added:
        content_list.append("正文: (無內容或無法解析)")

    text.extend(content_list)

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

            # Get subject and clean up email address in parentheses
            try:
                subject = parsed_data["subject"]
                # Remove email address in parentheses at the end
                if subject.endswith(")"):
                    subject = subject[:subject.rfind("(")].strip()
                text.append("標題: 「" + subject + "」")
            except:
                text.append("無標題")

            content_list = []
            content_added = False
            for part in parsed_data.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                elif part.get_content_maintype() == 'text':
                    content = part.get_content()
                    content_type = part.get_content_type()

                    # If HTML, parse with BeautifulSoup
                    if content_type == 'text/html':
                        soup = BeautifulSoup(content, 'html.parser')
                        # Remove script and style tags
                        for script in soup(["script", "style"]):
                            script.decompose()
                        content = soup.get_text()

                    # Clean up content: replace multiple line breaks
                    content = content.replace('\r\n\r\n\r\n', '\n\n')
                    content = content.replace('\r\n', '\n')

                    # Remove email addresses (common spam pattern)
                    lines = content.split('\n')
                    cleaned_lines = []
                    for line in lines:
                        # Skip lines that are just email addresses
                        if '@' in line and len(line.replace('@', '').replace('.', '')) < 30:
                            continue
                        # Skip lines with "邀請對象" section or attendee lists
                        if any(skip_text in line for skip_text in ['邀請對象', '查看所有', '回覆', '由於你是', '轉寄', '來自 Google']):
                            continue
                        # Skip very long URLs
                        if 'https://' in line and len(line) > 100:
                            continue
                        cleaned_lines.append(line)

                    # Keep structure: preserve 1-2 blank lines for readability
                    content = '\n'.join(cleaned_lines)
                    # Remove excessive blank lines (3+) but keep 1-2 for paragraph breaks
                    while '\n\n\n' in content:
                        content = content.replace('\n\n\n', '\n\n')

                    # Limit length to avoid flooding (first 1500 chars)
                    if len(content) > 1500:
                        content = content[:1500] + "\n...(內容過長，已截斷)"

                    if content.strip():
                        content_list.append("正文:\n" + content.strip())
                        content_added = True
                    break

            if not content_added:
                content_list.append("正文: (無內容或無法解析)")

            text.extend(content_list)
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