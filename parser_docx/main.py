import docx
import re
import collections


class ReadDox(object):
    construct, reconstruct, main_container = {}, [], []

    def read_file(self, doc):

        document = docx.Document(doc)

        for para in document.paragraphs:
            for r in para.runs:
                if r.font.bold:
                    if not self.reconstruct:
                        self.reconstruct.append(re_cap.sub(" ", para.text))
                    else:
                        self.configuration_text(self.reconstruct)
                        self.reconstruct.clear()
                        self.reconstruct.append(re_cap.sub(" ", para.text))

                elif r.font.italic:
                    text = re_cap.sub(" ", para.text)
                    self.reconstruct.append(text)
                    self.reconstruct.append(text)
                else:
                    text = re_cap.sub(" ", para.text)
                    self.reconstruct.append(text)
                break
        return self.construct

    def sort_dict(self, items):
        col = [k for k, i in collections.Counter(items).items() if i > 1]
        b = [j + 1 for j, z in enumerate(sorted(set(self.reconstruct[1:]))) if z in col]
        return b if len(b) >= 2 else ", ".join(str(b[0]))

    def configuration_text(self, items):
        try:
            item = self.sort_dict(items)
            items_text = sorted(set(items[1:]))
            while len(items_text) < 5:
                items_text.append("")
            items_text.append(item)
            items_text.insert(0, self.reconstruct[0])
            items_text.append(1 if len(item) == 1 else 2)
            self.construct[len(self.construct) + 1] = [i for i in items_text]
            self.reconstruct.clear()
            self.reconstruct.append("")
            return 1
        except IndexError:
            return 0


re_cap = re.compile("[\n]")

if __name__ == "__main__":
    main = ReadDox()
    a = main.read_file('test_component/tester.docx')
    for i in a:
        print(i, a[i])
