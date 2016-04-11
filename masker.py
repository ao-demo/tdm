import psycopg2
from faker import Faker
import os
import traceback
import psycopg2.extras
import random
import string


def connect_db():
    db_name = os.getenv('COMPANY_NAME', 'apporbit')
    user = os.getenv('POSTGRES_USER', 'odoo')
    passwd = os.getenv('POSTGRES_PASSWORD', 'odoo')
    host = os.getenv('DB_TIER', 'ds2db')

    conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(db_name,
                                                                                       user,
                                                                                       host,
                                                                                       passwd))
    return conn


def get_records(query):
    conn = connect_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query)
    rows = cur.fetchall()

    return rows


def update_passports(rows):
    conn = connect_db()
    cur = conn.cursor()
    for row in rows:
        if row[1]:
            cur.execute("UPDATE hr_employee SET passport_id='{0}' WHERE id={1}".format(row[1], row[0]))
    conn.commit()
    cur.close()


def update_bank_accounts(rows):
    conn = connect_db()
    cur = conn.cursor()
    for row in rows:
        if row[1]:
            cur.execute("UPDATE res_partner_bank SET acc_number='{0}' WHERE id={1}".format(row[1], row[0]))
    conn.commit()
    cur.close()


def mask_passports():
    rows = get_records("SELECT id, passport_id FROM hr_employee WHERE passport_id IS NULL OR  passport_id is NOT NULL")
    print "Rows for passport are " + str(rows)
    for row in rows:
        if row[1]:
            row[1] =  ''.join(random.choice(string.digits) for _ in range(8))

    print "Passport rows after masking " + str(rows)
    update_passports(rows)


def mask_bank_account():
    rows = get_records("SELECT id, acc_number FROM res_partner_bank WHERE acc_number IS NULL OR  acc_number is NOT NULL")
    print "Rows for bank accounts are " + str(rows)
    for row in rows:
        if row[1]:
            row[1] = ''.join(random.choice(string.digits) for _ in range(10))

    print "Bank account rows after masking " + str(rows)
    update_bank_accounts(rows)


def mask_data():
    try:
        mask_passports()
        mask_bank_account()

        with open("/tmp/result", 'w') as outf:
            outf.write("success")
    except:
        print "Failed to mask data"
        traceback.print_exc()

        with open("result", 'w') as outf:
            outf.write("failure")

if __name__ == '__main__':
    mask_data()
