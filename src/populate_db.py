import csv
import os
from models import *
from app import db
from datetime import datetime


def populate_license(directory):
    path = os.path.join(os.getcwd(), os.path.join(
        directory, 'input-license.csv'))
    with open(path) as input_file:
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


def populate_component(directory):
    path = os.path.join(os.getcwd(), os.path.join(
        directory, 'input-component-info.csv'))
    with open(path) as input_file:
        read_csv = csv.reader(input_file, delimiter='|')
        for row in read_csv:
            name = row[0]
            version = row[1]
            created_by = row[2]
            pub_date = row[3]
            pub_date = datetime.strptime(pub_date, '%B %d, %Y')
            pub_date = pub_date.strftime('%Y-%m-%d')
            origin = row[4]
            source_url = row[5]
            license_expression = row[6]
            ext_link = row[7]
            c = Component(name, version, created_by, pub_date,
                    origin, source_url, license_expression, ext_link)
            db.session.add(c)
            db.session.commit()

def populate_component_conn(directory):
    path = os.path.join(os.getcwd(), os.path.join(
        directory, 'input-component-relationship.csv'))
    with open(path) as input_file:
        read_csv = csv.reader(input_file, delimiter='|')
        for row in read_csv:
            input_c1_name = row[0]
            c1 = Component.query.filter_by(name=input_c1_name).first()
            input_c2_name = row[2]
            c2 = Component.query.filter_by(name=input_c2_name).first()
            c1.components.append(c2)
            db.session.commit()


if __name__ == '__main__':
    # Recreate DB
    db.drop_all()
    db.create_all()

    directory = 'dataset'
    populate_license(directory)
    populate_component(directory)
    populate_component_conn(directory)
