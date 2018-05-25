import csv
from models import *
from app import db


def populate_license():
    with open('input-license.csv') as input_file:
        read_csv = csv.reader(input_file, delimiter='|')
        for row in read_csv:
            full_name = row[0]
            identifier = row[1]
            if(row[2] == 'FSF Libre'):
                fsf_free_libre = True
            else:
                fsf_free_libre = False
            if(row[3] == 'OSI approved'):
                osi_approved = True
            else:
                osi_approved = False
            license_category = row[4]
            license_text = row[5]
            l = License(full_name, identifier, fsf_free_libre,
                        osi_approved, license_category, license_text)
            db.session.add(l)
            db.session.commit()

if __name__ == '__main__':
    # Recreate DB
    db.drop_all()
    db.create_all()

    populate_license()
