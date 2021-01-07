import json

class UsersController:
    def __init__(self, filepath):
        self.filepath = filepath

        self.open_users()

    def open_users(self):
        self.users = json.loads(open(self.filepath, 'r').read())

    def save_users(self):
        open(self.filepath, 'w').write(json.dumps(self.users))

    def add_user(self, username, user_id, ref):
        if self.user_does_not_exist(user_id):
            user = {
            'id': len(self.users) + 1,
            'username': username,
            'user_id': user_id,
            'ref': ref,
            'balance': 100
            }

            self.users.append(user)

            self.save_users()
        
    def find_user_by_user_id(self, user_id):
        for user in self.users:
            if user['user_id'] == user_id:
                return user

        return None

    def user_does_not_exist(self, user_id):
        for user in self.users:
            if user['user_id'] == user_id:
                return False

        return True

    def change_balance(self, user_id, balance):
        print('cb')
        for user in self.users:
            if user['user_id'] == user_id:
                user['balance'] = balance

        print('cb post')

        self.save_users()
        print('save data')