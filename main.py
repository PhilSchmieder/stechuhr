import argparse
import datetime
import shutil
import sqlite3
from os import remove, mkdir
from os.path import exists, join

SELECT_ALL = ("SELECT * FROM time")
SELECT_ALL_ORDERED_TIMEWISE = ("SELECT * FROM time ORDER BY begin")
GET_LATEST_ENTRY = "SELECT * FROM time ORDER BY id DESC LIMIT 1"
GET_ENTRY_BY_ID = "SELECT * FROM time WHERE id = ?"
INSERT_CLOCK_IN = "INSERT INTO time(begin) VALUES(?)"
INSERT_CLOCK_OUT = "INSERT INTO time(end) VALUES(?)"
INSERT_CLOCK_IN_OUT = "INSERT INTO time(begin, end) VALUES(?, ?)"
UPDATE_CLOCK_IN_OUT = "UPDATE time SET begin = ?, end = ? WHERE id = ?"
UPDATE_CLOCK_IN = "UPDATE time SET begin = ? WHERE id = ?"
UPDATE_CLOCK_OUT = "UPDATE time SET end = ? WHERE id = ?"
CREATE_TABLE_TIME = "create table time ( id integer primary key autoincrement, begin datetime, end datetime);"
DELETE_ALL = "delete from time"
DELETE_BY_ID = "delete from time where id = ?"


def run_query(db_file, query, obj=None):
    with sqlite3.connect(db_file) as con:
        cur = con.cursor()

        if obj:
            cur.execute(query, obj)
        else:
            cur.execute(query)

        con.commit()

        return cur.fetchall()


def clock_in(db_file, time: str):
    time = time if time else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return run_query(db_file, INSERT_CLOCK_IN, (time,))


def clock_out(db_file, time: str):
    time = time if time else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    (identifier, in_time, out_time) = run_query(db_file, GET_LATEST_ENTRY)[0]

    if out_time:
        print("WARNING: The latest entry already has a clock out time.")
        print("Did you forget to clock in?.")
        print("A new entry will be created with only a clock out time.")

        return run_query(db_file, INSERT_CLOCK_OUT, (time,))

    t = (
        in_time,
        time,
        identifier
    )
    return run_query(db_file, UPDATE_CLOCK_IN_OUT, t)


def print_db(db_file):
    pprint(run_query(db_file, SELECT_ALL))


def pprint(lines: list[(int, datetime, datetime)]) -> None:
    print("ID\tIn\t\t\tOut")
    for (identifier, in_time, out_time) in lines:
        print(f"{identifier}\t{in_time}\t{out_time}")


def update_entry(db_file, identifier, in_time, out_time):
    if not identifier:
        print("Specify which entry to update using --identifier ID.")
        return

    if in_time:
        run_query(db_file, UPDATE_CLOCK_IN, (in_time, identifier))

    if out_time:
        run_query(db_file, UPDATE_CLOCK_OUT, (out_time, identifier))


def new_db(db_file):
    if exists(db_file):
        c = input(f"File {db_file} already exists. Do you want to overwrite it? [y/N]: ")
        if c.lower() == "y":
            remove(db_file)
        else:
            return

    open(db_file, "w").close()
    run_query(db_file, CREATE_TABLE_TIME)


def _export_csv(db_file, export_out):
    with open(export_out, "w") as f:
        f.write("id,in,out\n")
        for (identifier, in_time, out_time) in run_query(db_file, SELECT_ALL):
            f.write(f"{identifier},{in_time},{out_time}\n")


def export(db_file, export_format: str, export_out: str):
    if not export_out:
        print("Specify where to export to using --export-out FILENAME.")
        return

    if export_format.lower() == "csv":
        _export_csv(db_file, export_out)


def archive(database, archive_dir):
    if not exists(archive_dir):
        mkdir(archive_dir)

    timestamp = datetime.datetime.now().isoformat().replace(" ", "_")
    shutil.copy(database, str(join(archive_dir, timestamp + "_" + database)))


def reset(db_file, no_interact: bool = False):
    if no_interact:
        run_query(db_file, DELETE_ALL)
        return

    c = input(f"Are you sure you want to reset {db_file}? [y/N]: ")
    if c.lower() == "y":
        run_query(db_file, DELETE_ALL)


def delete_entry(db_file, identifier):
    if not identifier:
        print("Specify which entry to delete using --identifier ID.")
        return

    run_query(db_file, DELETE_BY_ID, (identifier,))


def create_parser():
    parser = argparse.ArgumentParser(prog='Stechuhr', description='Keep time on your working hours')

    parser.add_argument("action",
                        choices=["new", "in", "out", "print", "update", "delete", "export", "archive", "reset",
                                 "merge", "sort"], nargs="?", default="print")
    parser.add_argument("--in-time", help="Clock in with given time. Format: YYYY-MM-DD HH:mm:ss")
    parser.add_argument("--out-time", help="Clock out with given time. Format: YYYY-MM-DD HH:mm:ss")
    parser.add_argument("--identifier", help="ID of the entry you want to update/delete.", type=int)
    parser.add_argument("--database", help="Specify database file.", default="stechuhr.db")
    parser.add_argument("--to-merge", help="Path to database to merge.")
    parser.add_argument("--archive-dir", help="Directory to store archived databases.", default="./archive/")
    parser.add_argument("--export-format", help="Format to export database in.", nargs="?", choices=["CSV", "PDF"],
                        default="CSV")
    parser.add_argument("--export-out", help="Path to export to.")

    return parser


def merge(db_file, to_merge):
    for (_, in_time, out_time) in run_query(to_merge, SELECT_ALL):
        if in_time:
            clock_in(db_file, in_time)

        if out_time:
            clock_out(db_file, out_time)


def sort(db_file):
    ordered_entries = run_query(db_file, SELECT_ALL_ORDERED_TIMEWISE)
    run_query(db_file, DELETE_ALL)

    for (_, in_time, out_time) in ordered_entries:
        if in_time:
            clock_in(db_file, in_time)

        if out_time:
            clock_out(db_file, out_time)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    if args.action == "new":
        new_db(args.database)
    elif args.action == "in":
        clock_in(args.database, args.in_time)
    elif args.action == "out":
        clock_out(args.database, args.out_time)
    elif args.action == "print":
        print_db(args.database)
    elif args.action == "update":
        update_entry(args.database, args.identifier, args.in_time, args.out_time)
    elif args.action == "delete":
        delete_entry(args.database, args.identifier)
    elif args.action == "export":
        export(args.database, args.export_format, args.export_out)
    elif args.action == "archive":
        archive(args.database, args.archive_dir)
    elif args.action == "reset":
        reset(args.database)
    elif args.action == "merge":
        merge(args.database, args.to_merge)
    elif args.action == "sort":
        sort(args.database)
