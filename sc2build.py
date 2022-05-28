from bs4 import BeautifulSoup as bs
import requests
import difflib

class Commanders:
    def __init__(self):
        self.address_list = []
        self.truenames = []
        self._get_commanders()

    def _get_commanders(self):
        page = requests.get("https://starcraft2coop.com/")
        HTML_content = bs(page.content, "html.parser")
        commander_container = HTML_content.find(id="commanderList")
        commander_list = commander_container.find_all("img")

        for alt_name in commander_list:
            self.truenames.append(alt_name["alt"].replace(" Portrait", ""))

        commander_list = commander_container.find_all("a")
        for commander_address in commander_list:
            sanitised_names = commander_address["href"].replace("/commanders/", "")
            self.address_list.append(sanitised_names)

def get_build(commander):
    page = requests.get(f"https://starcraft2coop.com/commanders/{commander}")
    HTML_content = bs(page.content, "html.parser")
    build_table = HTML_content.find(class_="buildOrder")
    return build_table.text

def search_commanders(search_term):
    commander_list = Commanders()
    if search_term in commander_list.address_list:
        return search_term
    else: #fuzzy search
        search_results = []
        for commander in commander_list.address_list:
            ratio = difflib.SequenceMatcher(None, search_term, commander).ratio()
            search_results.append([commander, ratio])
        search_results = sorted(search_results, key=lambda l:l[1], reverse=True)
        print(f"Did you mean: {search_results[0][0]}? ({int(search_results[0][1] * 100)}%)")
        return search_results[0][0]


def main():
    commander = search_commanders(input("Commander: "))
    print(get_build(commander))

if __name__ == "__main__":
    main()