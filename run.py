import os

from flask_script import Manager
from flask_migrate import MigrateCommand

from chum import create_app
from config import Config
from chum.api.utils import error_response


config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)


@app.errorhandler(404)
def page_not_found(e):
    return error_response(status=404, error='Not found', message='The '
                          'requested URL was not found on the server.  If '
                          'you entered the URL manually please check your '
                          'spelling and try again')


@app.errorhandler(500)
def internal_server_error(e):
    return error_response(status=500, error='Internal server error',
                          message="It is not you. It is me. The server "
                          "encountered an internal error and was unable to "
                          "complete your request.  Either the server is "
                          "overloaded or there is an error in the application")

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def migrations():
    """ 
    Runs a single migrations command that runs entire migrations setup 
    from start. 
    """

    if not os.path.isdir(Config.BASE_DIR + '/migrations/'):
        os.system('python run.py db init')
    else:
        print('\n\tA migrations folder already exists skipping "db '
              'init"...\n')

    os.system('python run.py db migrate')
    os.system('python run.py db upgrade')


@manager.command
def tests():
    """ Runs tests on chum  """

    os.system('nosetests -v --cover-package=chum')


if __name__ == '__main__':
    manager.run()
