import re
import spamcheck

def emails(filename):
    email_list = list()

    email_re = r'[\w.+-]+@[\w-]+\.[\w.-]+'

    with open(filename, 'r') as f:
        buf = f.read()
        regex = re.findall(email_re, buf)
        if regex is not None:
            for match in regex:
                if match not in email_list:
                    email_list.append(match)
    
    print(email_list)

    for mail in email_list:
        res = spamcheck.check(mail, report=True)
        score = res['score']
        report = res['report']

        print(score)
        print(report)