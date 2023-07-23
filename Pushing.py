
from datetime import date
from git import Repo

repo_path = r'C:\Users\Victorus\PycharmProjects\Fixed2\Personal\CCG2'
repo = Repo(repo_path)

repo.index.add(['screenings'])
repo.index.commit(f'Screenings update {date.today()}')

repo.remotes.origin.set_url('https://github.com/145211/Cinema-City-Planner')

origin = repo.remote(name='origin')

origin.push()
