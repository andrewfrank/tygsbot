import logging
import requests

requests_url = "https://tygs.dsmz.de/user_requests/show"
results_url = "https://tygs.dsmz.de/user_results/show"

def _get_json(url):
    session = requests.Session()
    r = session.get(url)
    return r.json()

class Submission:
    def __init__(
            self, 
            email, 
            files=[None], 
            accessions=["AGSE01000001-AGSE01000004"], 
            restrict=False,
        ):

        genomes_count = len(files) + len(accessions)
        if genomes_count > 20:
            raise ValueError(f"{genomes_count} submitted; TYGS limit is 20")

        self.email = email
        self.files = files
        self.accessions = accessions
        self.restrict = restrict

    def _submit(self):
        # TODO: this payload doesn't work yet
        url = "http://tygs.dsmz.de/user_requests/new"
        payload = {
            "user_request[accession_number_batch]":self.accessions,
            "user_request[email]":self.email
        }
        r = requests.post(url, data=payload)
        print(r)

class Results:
    def __init__(self, guid):
        self.guid = guid

    def status(self):
        url = f"{requests_url}/status/{self.guid}"
        return _get_json(url)

    def identification(self):
        url = f"{results_url}/identification_table_json/{self.guid}"
        return _get_json(url)

# testing
guid = "3da2e199-82af-440d-b178-f3fda71cc299"
results = Results(guid)

status = results.status()
print(status)

identification = results.identification()
print(identification)