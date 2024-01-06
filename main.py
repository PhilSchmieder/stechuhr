import datetime
import sqlite3
import argparse

SELECT_ALL = ("SELECT * FROM time")
GET_LATEST_ENTRY = "SELECT * FROM time ORDER BY id DESC LIMIT 1"
INSERT_CLOCK_IN = "INSERT INTO time(begin) VALUES(?)"
INSERT_CLOCK_OUT = "INSERT INTO time(end) VALUES(?)"
INSERT_CLOCK_IN_OUT = "INSERT INTO time(begin, end) VALUES(?, ?)"
UPDATE_CLOCK_IN_OUT = "UPDATE time SET begin = ?, end = ? WHERE id = ?"


def run_query(db_file, query, obj=None):
    with sqlite3.connect(db_file) as con:
        cur = con.cursor()

        if obj:
            cur.execute(query, obj)
        else:
            cur.execute(query)

        con.commit()

        return cur.fetchall()


def clock_in(db_file, time=datetime.datetime.now()):
    t = (
        time.strftime("%Y-%m-%d %H:%M:%S"),  # '2007-01-01 10:00:00'
    )
    return run_query(db_file, INSERT_CLOCK_IN, t)


def clock_out(db_file, time=datetime.datetime.now()):
    (identifier, in_time, out_time) = run_query(db_file, GET_LATEST_ENTRY)[0]

    if out_time:
        print("WARNING: The latest entry already has a clock out time.")
        print("A new entry will be created with only a clock out time.")

        t = (
            time.strftime("%Y-%m-%d %H:%M:%S"),  # '2007-01-01 10:00:00'
        )

        return run_query(db_file, INSERT_CLOCK_OUT, t)

    t = (
        in_time,
        time.strftime("%Y-%m-%d %H:%M:%S"),  # '2007-01-01 10:00:00'
        identifier
    )
    return run_query(db_file, UPDATE_CLOCK_IN_OUT, t)


def create_parser():
    parser = argparse.ArgumentParser(
        prog='Stechuhr',
        description='Keep time on your working hours')

    parser.add_argument("-i", help="Clock in now.", action="store_true")
    parser.add_argument("-o", help="Clock out now.", action="store_true")
    parser.add_argument("--in-time", help="Clock in with given time.")
    parser.add_argument("--out-time", help="Clock out with given time.")
    parser.add_argument("-p", "--print", help="Print time database.", action="store_true")
    parser.add_argument("--database", help="Specify database file.", default="stechuhr.db")

    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    if args.i:
        clock_in(args.database)
        exit()

    if args.o:
        clock_out(args.database)
        exit()

    if args.print:
        print("ID\tIn\t\t\tOut")
        for (identifier, in_time, out_time) in run_query(args.database, SELECT_ALL):
            print(f"{identifier}\t{in_time}\t{out_time}")
        exit()

    # if no other action is specified, print times
    print("ID\tIn\t\t\tOut")
    for (identifier, in_time, out_time) in run_query(args.database, SELECT_ALL):
        print(f"{identifier}\t{in_time}\t{out_time}")
    exit()
