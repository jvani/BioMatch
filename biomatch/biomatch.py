from __future__ import print_function

import os
import sys
import json
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer


class BioMatch(object):
    def __init__(self, directory, slug, data_path):
        """BioMatch is a container for scraping bio data and calculating the
        cosine similarity of the resulting bios and a target string.
        Args:
            directory (str) - Staff directory (i.e., webpage with links to bios).
            slug (str) - Slug where bios live (e.g., ...staff/bios/).
            data_path (str) - Where to save/load scraped data.
            name_tag (str) - html tag for bio names.
            bio_tag (str) - html tag for bios.
        """
        # -- Set variables.
        self.bios = {}
        self.slug = slug
        self.directory = directory
        self.data_path = data_path
        # -- Load data if save to file.
        if os.path.isfile(self.data_path):
            print("BIOS: Loading {}".format(self.data_path))
            with open(self.data_path, "r") as infile:
                self.bios = json.load(infile)
                self.links = self.bios.keys()
        # -- Else test HTML tags.
        else:
            self._bio_links()
            self._tag_test()


    def _bio_links(self):
        """Pull bio urls from a staff directory."""
        # -- Print status.
        print("BIOS: Scraping bio links from staff directory.")
        # -- Get all bio links from directory.
        soup = BeautifulSoup(requests.get(self.directory).text)
        self.links = [hyperlink.get("href") for hyperlink in soup.find_all("a")]
        self.links = filter(lambda x: type(x) == str, self.links)
        self.links = filter(lambda x: x.startswith(self.slug), self.links)


    def _tag_test(self):
        """"""
        # -- Print status.
        print("BIOS: Testing HTML tags on bio page:")
        # -- Scrape a test bio page.
        soup = BeautifulSoup(requests.get(self.links[0]).text)
        # -- Find all tags.
        for tag in ["h1", "h2", "h3", "h4", "h5", "h6", "p"]:
            text = soup.find_all(tag)
            # -- If something was found.
            if len(text) > 0:
                # -- Get the fist text instance.
                text = text[0].get_text()
                # -- Shorten if >40 characters.
                if len(text) > 40:
                    text = text[:40] + "..."
                print("      -- {}: {}".format(tag.rjust(2), text))


    def scrape_bios(self, name_tag="h2", bio_tag="p"):
        """Scrape bio links, pull names and paragraphs.
        Args:
            name_tag (str) - html tag for bio names.
            bio_tag (str) - html tag for bios.
        """
        # -- Print used tags.
        print("BIOS: Name tag <{}>, bio tag <{}>".format(name_tag, bio_tag))
        # -- For each bio.
        for ix, url in enumerate(self.links):
            # -- Print url location.
            text = "/".join(url.split("/")[-3:-1])
            print("BIOS: Scraping .../{}/ ({}/{})                           " \
                .format(text.encode("utf-8"), ix + 1, len(self.links)), end="\r")
            sys.stdout.flush()
            # -- Scrape url.
            soup = BeautifulSoup(requests.get(url).text)
            # -- Pull names.
            name = soup.find_all(name_tag)[0].get_text()
            # -- Pull bios.
            bios = [text.get_text(strip=True).lower() for text in soup.find_all(bio_tag)]
            if len(bios) > 0:
                # -- Remove stopwords.
                bwrd = [item for sublist in [bio.split(" ") for bio in bios] for item in sublist]
                data = [word for word in bwrd if word not in stopwords.words("english")]
                self.bios[url] = {"name": name, "bio": bios, "data": data}
        # -- Write to json.
        with open(self.data_path, "w") as outfile:
            json.dump(self.bios, outfile)


    def cosine_similarity(self, text):
        """Calculate the cosine similarity between scraped bios and a target
        string.
        Args:
            text (str) - target string to find similarity.
        Returns:
            (list) - [names, cosine] biography names and their cosine scores.
        """
        # -- Print status.
        print("BIOS: Calculating cosine similarity:")
        # -- Tokenize text.
        text = " ".join([word for word in text.lower().split(" ")
                          if word not in stopwords.words("english")])
        # -- Pull names.
        names = [bio["name"] for bio in self.bios.values()]
        # -- Pull all bios and append query text to list.
        data = [" ".join(bio["data"]) for bio in self.bios.values()]
        data.append(text)
        # -- Vectorize and calculate cosine similarity.
        tfidf = TfidfVectorizer().fit_transform(data)
        cosine = linear_kernel(tfidf, tfidf)[-1][:-1]
        # -- Find the most similar.
        similar = cosine.argsort()[::-1]
        # -- Print most similar:
        mlen = max([len(names[idx]) for idx in similar[:10]])
        for ii, idx in enumerate(similar[:10]):
            num = (str(ii + 1) + ".").ljust(3)
            name = names[idx].ljust(mlen)
            ptext = "      {} {} (Score: {:.4f})"
            print(ptext.format(num, name.encode("utf-8"), cosine[idx]))
        # -- Return biography names and their corresponding cosine scores.
        return [names, cosine]


if __name__ == "__main__":
    # -- Create BioMatch object with scraped data.
    data_path = os.path.join("..", "data", "idss_bios.json")
    bios = BioMatch(r"https://idss.mit.edu/people/",
                    r"https://idss.mit.edu/staff/",
                    data_path)
    # -- Scrape bios with default HTML tags.
    if not os.path.isfile(data_path):
        bios.scrape_bios(name_tag="h2", bio_tag="p")
    # -- Prompt user for text.
    text = raw_input("BIOS: What is your text?\n")
    # -- Find similarity with mission statement.
    _ = bios.cosine_similarity(text)
