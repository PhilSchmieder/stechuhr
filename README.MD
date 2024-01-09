# Stechuhr
_Stechuhr_ (IPA: [ˈʃtɛçˌʔuːɐ̯]) is german for _punch clock_.

Stechuhr is a CLI tool to keep time of your working hours.  


## Usage
```shell
Usage: cli [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  archive   Archive Stechuhr.
  delete    Delete Stechuhr entry.
  dumphelp
  export    Export data.
  in        Clock in.
  merge     Merge Stechuhr with Stechuhr TO_MERGE.
  new       Create new Stechuhr.
  out       Clock out.
  print     Print Stechuhr data.
  reset     Reset Stechuhr.
  sort      Sort Stechuhr entries by clock in time.
  update    Update entry with id IDENTIFIER.

Usage: cli in [OPTIONS]

  Clock in.

Options:
  -d, --database TEXT  Database file. Defaults to 'stechuhr.db'.
  -t, --time TEXT      Clock in with given time. Format: YYYY-MM-DD HH:mm:ss.
                       Defaults to now.
  --help               Show this message and exit.

Usage: cli out [OPTIONS]

  Clock out.

Options:
  -d, --database TEXT  Database file. Defaults to 'stechuhr.db'.
  -t, --time TEXT      Clock out with given time. Format: YYYY-MM-DD HH:mm:ss.
                       Defaults to now.
  --help               Show this message and exit.

Usage: cli print [OPTIONS]

  Print Stechuhr data.

Options:
  -d, --database TEXT  Database file. Defaults to 'stechuhr.db'.
  --help               Show this message and exit.

Usage: cli update [OPTIONS] IDENTIFIER

  Update entry with id IDENTIFIER.

Options:
  -d, --database TEXT  Database file. Defaults to 'stechuhr.db'.
  -i, --in-time TEXT   Clock in with given time. Format: YYYY-MM-DD HH:mm:ss
  -o, --out-time TEXT  Clock out with given time. Format: YYYY-MM-DD HH:mm:ss
  --help               Show this message and exit.

Usage: cli new [OPTIONS]

  Create new Stechuhr.

Options:
  -d, --database TEXT  Database file. Defaults to 'stechuhr.db'.
  --help               Show this message and exit.

Usage: cli export [OPTIONS]

  Export data.

Options:
  -d, --database TEXT      Database file. Defaults to 'stechuhr.db'.
  -f, --format [CSV|HTML]  Export format.
  -o, --out TEXT           Output path. Defaults to stdout.
  -t, --template TEXT      Path to jinja template for html export. Defaults to
                           './templates/default.jinja'
  --help                   Show this message and exit.

Usage: cli archive [OPTIONS]

  Archive Stechuhr.

Options:
  -d, --database TEXT  Database file. Defaults to 'stechuhr.db'.
  --archive-dir TEXT   Path to archive directory. Defaults to './archive/'
  --help               Show this message and exit.

Usage: cli reset [OPTIONS]

  Reset Stechuhr.

Options:
  -d, --database TEXT  Database file. Defaults to 'stechuhr.db'.
  --help               Show this message and exit.

Usage: cli delete [OPTIONS] IDENTIFIER

  Delete Stechuhr entry.

Options:
  -d, --database TEXT  Database file. Defaults to 'stechuhr.db'.
  --help               Show this message and exit.

Usage: cli merge [OPTIONS] TO_MERGE

  Merge Stechuhr with Stechuhr TO_MERGE.

Options:
  -d, --database TEXT  Database file. Defaults to 'stechuhr.db'.
  --help               Show this message and exit.

Usage: cli sort [OPTIONS]

  Sort Stechuhr entries by clock in time.

Options:
  -d, --database TEXT  Database file. Defaults to 'stechuhr.db'.
  --help               Show this message and exit.

Usage: cli dumphelp [OPTIONS]

Options:
  --help  Show this message and exit.
```
