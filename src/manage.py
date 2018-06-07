# -------------------------------------------------------------------
# SPDX-License-Identifier: GPL-3.0-or-later
# See GPL-3.0-or-later in the Licenses folder for license information
# -------------------------------------------------------------------

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
