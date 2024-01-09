import datetime
import shutil
import sqlite3
from os import remove, mkdir
from os.path import exists, join

import click
import jinja2
from jinja2 import FileSystemLoader

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


def run_query(database, query, obj=None):
    with sqlite3.connect(database) as con:
        cur = con.cursor()

        if obj:
            cur.execute(query, obj)
        else:
            cur.execute(query)

        con.commit()

        return cur.fetchall()


@click.group(help="Stechuhr is a CLI tool to keep time of your working hours.")
def cli():
    pass


@cli.command(name="in", help="Clock in.")
@click.option("-d", "--database", help="Database file. Defaults to 'stechuhr.db'.", default="stechuhr.db")
@click.option("-t", "--time", help="Clock in with given time. Format: YYYY-MM-DD HH:mm:ss. Defaults to now.")
def clock_in(database, time: str):
    time = time if time else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return run_query(database, INSERT_CLOCK_IN, (time,))


@cli.command(name="out", help="Clock out.")
@click.option("-d", "--database", help="Database file. Defaults to 'stechuhr.db'.", default="stechuhr.db")
@click.option("-t", "--time", help="Clock out with given time. Format: YYYY-MM-DD HH:mm:ss. Defaults to now.")
def clock_out(database, time: str):
    time = time if time else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    (identifier, in_time, out_time) = run_query(database, GET_LATEST_ENTRY)[0]

    if out_time:
        click.echo("WARNING: The latest entry already has a clock out time.")
        click.echo("Did you forget to clock in?.")
        click.echo("A new entry will be created with only a clock out time.")

        return run_query(database, INSERT_CLOCK_OUT, (time,))

    t = (
        in_time,
        time,
        identifier
    )
    return run_query(database, UPDATE_CLOCK_IN_OUT, t)


@cli.command(name="print", help="Print Stechuhr data.")
@click.option("-d", "--database", help="Database file. Defaults to 'stechuhr.db'.", default="stechuhr.db")
def print_db(database):
    pprint(run_query(database, SELECT_ALL))


def pprint(lines: list[(int, datetime, datetime)]) -> None:
    click.echo("ID\tIn\t\t\tOut")
    for (identifier, in_time, out_time) in lines:
        click.echo(f"{identifier}\t{in_time}\t{out_time}")


@cli.command(name="update", help="Update entry with id IDENTIFIER.")
@click.argument("identifier", type=int, required=True)
@click.option("-d", "--database", help="Database file. Defaults to 'stechuhr.db'.", default="stechuhr.db")
@click.option("-i", "--in-time", help="Clock in with given time. Format: YYYY-MM-DD HH:mm:ss")
@click.option("-o", "--out-time", help="Clock out with given time. Format: YYYY-MM-DD HH:mm:ss")
def update_entry(database, identifier, in_time, out_time):
    if not identifier:
        click.echo("Specify which entry to update using --identifier ID.")
        return

    if in_time:
        run_query(database, UPDATE_CLOCK_IN, (in_time, identifier))

    if out_time:
        run_query(database, UPDATE_CLOCK_OUT, (out_time, identifier))


@cli.command(name="new", help="Create new Stechuhr.")
@click.option("-d", "--database", help="Database file. Defaults to 'stechuhr.db'.", default="stechuhr.db")
def new_db(database):
    if exists(database):
        c = input(f"File {database} already exists. Do you want to overwrite it? [y/N]: ")
        if c.lower() == "y":
            remove(database)
        else:
            return

    open(database, "w").close()
    run_query(database, CREATE_TABLE_TIME)


def _build_csv(database) -> str:
    s = "id,in,out\n"
    for (identifier, in_time, out_time) in run_query(database, SELECT_ALL):
        s += f"{identifier},{in_time},{out_time}\n"

    return s


def _render_jinja_template(template_path: str, data: dict) -> str:
    env = jinja2.Environment(loader=FileSystemLoader("."))
    template = env.get_template(template_path)
    return template.render(data)


def _build_html(database, template_path):
    entries = run_query(database, SELECT_ALL)

    template_data = {
        "entries": [
            {
                "id": identifier,
                "in_time": datetime.datetime.strptime(in_time, "%Y-%m-%d %H:%M:%S") if in_time else None,
                "out_time": datetime.datetime.strptime(out_time, "%Y-%m-%d %H:%M:%S") if out_time else None
            }
            for (identifier, in_time, out_time) in entries]
    }

    html = _render_jinja_template(template_path, template_data)

    return html


@cli.command(name="export", help="Export data.")
@click.option("-d", "--database", help="Database file. Defaults to 'stechuhr.db'.", default="stechuhr.db")
@click.option("-f", "--format", "export_format", help="Export format.", default="csv",
              type=click.Choice(['CSV', 'HTML'], case_sensitive=False))
@click.option("-o", "--out", help="Output path. Defaults to stdout.")
@click.option("-t", "--template",
              help="Path to jinja template for html export. Defaults to './templates/default.jinja'",
              default="./templates/default.jinja")
def export(database, export_format: str, out: str, template: str):
    export_data = None

    if export_format.lower() == "csv":
        export_data = _build_csv(database)

    elif export_format.lower() == "html":
        export_data = _build_html(database, template)

    if out:
        with open(out, "w") as f:
            f.write(export_data)
    else:
        click.echo(export_data)


@cli.command(name="archive", help="Archive Stechuhr.")
@click.option("-d", "--database", help="Database file. Defaults to 'stechuhr.db'.", default="stechuhr.db")
@click.option("--archive-dir", help="Path to archive directory. Defaults to './archive/'", default="./archive/")
def archive(database, archive_dir):
    if not exists(archive_dir):
        mkdir(archive_dir)

    timestamp = datetime.datetime.now().isoformat().replace(" ", "_")
    shutil.copy(database, str(join(archive_dir, timestamp + "_" + database)))


@cli.command(name="reset", help="Reset Stechuhr.")
@click.option("-d", "--database", help="Database file. Defaults to 'stechuhr.db'.", default="stechuhr.db")
def reset(database, no_interact: bool = False):
    if no_interact:
        run_query(database, DELETE_ALL)
        return

    c = input(f"Are you sure you want to reset {database}? [y/N]: ")
    if c.lower() == "y":
        run_query(database, DELETE_ALL)


@cli.command(name="delete", help="Delete Stechuhr entry.")
@click.argument("identifier", type=int, required=True)
@click.option("-d", "--database", help="Database file. Defaults to 'stechuhr.db'.", default="stechuhr.db")
def delete_entry(database, identifier):
    if not identifier:
        click.echo("Specify which entry to delete using --identifier ID.")
        return

    run_query(database, DELETE_BY_ID, (identifier,))


@cli.command(name="merge", help="Merge Stechuhr with Stechuhr TO_MERGE.")
@click.argument("TO_MERGE", type=str, required=True)
@click.option("-d", "--database", help="Database file. Defaults to 'stechuhr.db'.", default="stechuhr.db")
def merge(database, to_merge):
    for (_, in_time, out_time) in run_query(to_merge, SELECT_ALL):
        if in_time:
            clock_in(database, in_time)

        if out_time:
            clock_out(database, out_time)


@cli.command(name="sort", help="Sort Stechuhr entries by clock in time.")
@click.option("-d", "--database", help="Database file. Defaults to 'stechuhr.db'.", default="stechuhr.db")
def sort(database):
    ordered_entries = run_query(database, SELECT_ALL_ORDERED_TIMEWISE)
    run_query(database, DELETE_ALL)

    for (_, in_time, out_time) in ordered_entries:
        if in_time:
            clock_in(database, in_time)

        if out_time:
            clock_out(database, out_time)


def recursive_help(cmd, parent=None):
    ctx = click.core.Context(cmd, info_name=cmd.name, parent=parent)
    print(cmd.get_help(ctx))
    print()
    commands = getattr(cmd, 'commands', {})
    for sub in commands.values():
        recursive_help(sub, ctx)


@cli.command(hidden=True)
def dumphelp():
    recursive_help(cli)


if __name__ == '__main__':
    cli()
