from urllib import request
from bs4 import BeautifulSoup
import re


class DependencyVisualizer:
    def __init__(self, lib_name) -> None:
        self.dependencies = 0
        self.soap_text = "None"
        self.lib_name = lib_name

    def parsing(self) -> None:
        url = 'https://registry.npmjs.org/' + self.lib_name
        html = request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        self.soap_text = soup.text
        self.dependencies = self.soap_text.count('"dependencies":{')

    def textFormat(self, text: str) -> str:
        text = text.replace('"dependencies":{', self.lib_name + " -> ")
        pattern = r'"|:|\^|~|\d|{|}|\.|\*'
        text = re.sub(pattern, "", text)
        name_visual = self.lib_name + " -> "
        text = text.replace(',', '\n' + name_visual)
        return text

    @property
    def display(self) -> str:
        self.parsing()
        if self.dependencies:
            counter = 0
            begin = 0
            for i in range(self.dependencies - 1):
                begin = self.soap_text.find('"dependencies":{', counter)
                counter = begin + 1
            end = self.soap_text.find('}', counter) + 1
            if not (self.soap_text.find("{", begin) + 2 == end):
                return self.textFormat(self.soap_text[begin:end])
        return "Нет зависимостей"


if __name__ == "__main__":
    while True:
        user_input = input("Введите название библиотеки: ")
        if user_input == "exit":
            break
        console = DependencyVisualizer(user_input)
        print(console.display)
