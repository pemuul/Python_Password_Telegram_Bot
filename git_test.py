from github import Github
import hashlib

class GitTest:
    def __init__(self):
        self.g = Github("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")
        self.repo = self.g.get_user().get_repo('Test')

    def get_uset(self):
        user = self.g.get_user()
        return(str(user.login))

    def test_repo_name(self):
        pass
        #self.g.

    def get_content(self, file_name='README.md'):
        contents = self.repo.get_contents(file_name)
        return contents.decoded_content.decode('utf-8')

    def write_content(self, content, file_name='README.md'):
        contents = self.repo.get_contents(file_name)
        #self.repo.update_file(file_name, "", content, contents.sha, branch="test")
        self.repo.update_file(contents.path, '', content, contents.sha)

if __name__ == '__main__':
    gt = GitTest()
    print(gt.get_content())
    gt.write_content('jjjjjjjj', 'test/unit_test.txt')