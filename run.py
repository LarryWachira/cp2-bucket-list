import os

from flask_script import Command, Manager

from chum import create_app
from config import Config


class Migrations(Command):
    """ Runs a single migrations command that runs entire migrations setup 
    from start. """

    def run(self):
        if not os.path.isdir(Config.BASE_DIR + '/migrations/'):
            os.system('flask db init')
        else:
            print('\n\tA migrations folder already exists skipping "db '
                  'init"...\n')

        os.system('flask db migrate')
        os.system('flask db upgrade')


config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

manager = Manager(app)

manager.add_command('migrations', Migrations())

if __name__ == '__main__':
    manager.run()
