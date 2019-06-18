import sys
import unicodedata
import os


def get_messages(filename, user="goncaloraposo"):
    try:
        with open(filename, 'r', errors='ignore') as f:
            text = f.readline()
    except IOError:
        print(filename, "doesn't exit")
        return

    keyword = '_2lek _2lel">'
    text = text.split(keyword)
    text = text[1:]

    username = ""
    othername = ""

    for line in text:
        name = get_name(line)
        temp = only_text(name)
        if temp==user:
            username = name
        else:
            othername = name
            other = temp

        if username and othername:
            break

    filepath = "./messages_processed/"
    dirname = os.path.dirname(filepath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    new_filename = other+'_'+user

    with open(filepath+new_filename+"_E"+".txt", 'w') as fe, \
            open(filepath+new_filename+"_D"+".txt", 'w') as fd:

            for start in range(0, len(text)):
                name = get_name(text[start])
                if name==username:
                    break

            nlines = len(text)
            phrases = [[], []]
            write = False

            for i in range(start, nlines):
                line = text[i]
                name = get_name(line)

                if name==username:
                    if write:
                        save_phrases(fe, fd, phrases)
                        phrases = [[], []]
                        write = False

                    phrases[1].append(get_phrase(line))

                else:
                    write = True
                    phrases[0].append(get_phrase(line))

            save_phrases(fe, fd, phrases)

    print("Processed ", filename)


def save_phrases(fe, fd, phrases):
    phrases[0].reverse()
    phrases[1].reverse()
    phrases[0] = ' '.join(phrases[0])
    phrases[1] = ' '.join(phrases[1])

    if filter_phrases(phrases):
        fe.write(phrases[0]+'\n')
        fd.write(phrases[1]+'\n')


def filter_phrases(phrases):
    for phrase in phrases:
        if not phrase or phrase.isspace():
            return 0
    return 1


def only_text(str_in):
    str_out = ''.join(c for c in str_in if c.isalnum())
    str_out = str_out.lower()
    str_out = remove_accents(str_out)
    return str_out


def remove_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


def get_name(line):
    keyword = '</div><div '
    end = line.find(keyword)
    if end<0:
        return ''
    else:
        return line[:end]


def get_phrase(line):
    keyword1 = '_2let"><div><div></div><div>'
    start = line.find(keyword1)+len(keyword1)
    keyword2 = '</div>'
    end = line.find(keyword2, start)
    phrase = line[start:end]
    phrase = format_link(phrase)
    phrase = phrase.replace('<br />', '')   # removes newlines

    return phrase


def format_link(phrase):
    keyword1 = '<a href="'
    while True:
        start = phrase.find(keyword1)
        if start is -1:
            break

        keyword2 = '">'
        end = phrase.find(keyword2, start)

        keyword3 = '</a>'
        rest = phrase.find(keyword3, end)+len(keyword3)

        phrase = phrase[:start]+phrase[start+len(keyword1):end]+phrase[rest:]

    return phrase


if len(sys.argv)<2:
    for root, _, files in os.walk('./messages_unprocessed'):
        for file in files:
            get_messages(os.path.join(root, file))
else:
    get_messages(sys.argv[1])
