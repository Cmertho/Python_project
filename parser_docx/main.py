import docx
import collections
import re

re_cap = re.compile("[\n]")


class Reconstruction(object):
    def __init__(self):
        self.construct, self.re_construct = {}, [""]

    def config(self, doc):
        document = docx.Document(doc)
        for para in document.paragraphs:
            for r in para.runs:
                if r.font.bold:
                    text = re_cap.sub(" ", r.text)
                    if len(self.re_construct) > 3:
                        self.configuration_text(self.re_construct)
                        self.re_construct[0] = ''.join(self.re_construct[0] + text)
                    else:
                        self.re_construct[0] = ''.join(self.re_construct[0] + text)

                elif r.font.italic:
                    text = re_cap.sub(" ", r.text)
                    self.re_construct.append(text)
                    self.re_construct.append(text)
                else:
                    text = re_cap.sub(" ", r.text)
                    self.re_construct.append(text)

                try:
                    self.re_construct.remove(" ")
                    self.re_construct.remove("")
                except ValueError:
                    pass
        return self.construct

    def sort_dict(self, items):
        col = [k for k, i in collections.Counter(items[1:]).items() if i > 1]
        b = [j + 1 for j, z in enumerate(sorted(set(self.re_construct[1:]))) if z in col]
        return b if len(b) >= 2 else ", ".join(str(b[0]))

    def configuration_text(self, items):
        try:
            item = self.sort_dict(items)
            items = sorted(set(items[1:]))
            items.append(item)
            items.insert(0, self.re_construct[0])
            items.append(1 if len(item) == 1 else 2)
            self.construct[len(self.construct) + 1] = [i for i in items]
            self.re_construct.clear()
            self.re_construct.append("")
            return self.construct
        except IndexError:
            return 0


main = Reconstruction()
print(main.config('name.docx')) # name .docx file
