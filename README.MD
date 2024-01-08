# Stechuhr
_Stechuhr_ (IPA: [ˈʃtɛçˌʔuːɐ̯]) is german for _punch clock_.

Stechuhr is a CLI tool to keep time of your working hours.  


## Usage
**Create New**  
To create a new stechuhr database, run

```shell
stechuhr new
``` 

This will create a new stechuhr database and store it as the default database.
You may change this using the `--database PATH/TO/STECHUHR/DATABASE` argument.

**Clock in**  
To clock in to a stechuhr, run

```shell
stechuhr in
```

This will clock in to the default stechuhr.
You may change which stechuhr is used with the `--database PATH/TO/STECHUHR/DATABASE` argument.

By default, you will be clocked in at the current time.
You may change this with the `--in-time 'YYYY-MM-DD HH:mm:ss'` argument.

**Clock out**  
To clock out off a stechuhr, run

```shell
stechuhr out
```  

This will clock out of the default stechuhr.
You may change which stechuhr is used with the `--database PATH/TO/STECHUHR/DATABASE` argument.

By default, you will be clocked out at the current time.
You may change this with the `--out-time 'YYYY-MM-DD HH:mm:ss'` argument.

**Print**  
To create a stechuhr database, run `stechuhr print`, or simply `stechuhr`.
This will print the default stechuhr.
You may change which stechuhr is used with the `--database PATH/TO/STECHUHR/DATABASE` argument.

**Update Entry**  
To update an entry in a stechuhr, run

```shell
stechuhr update --identifier ID --in-time 'YYYY-MM-DD HH:mm:ss' --out-time 'YYYY-MM-DD HH:mm:ss'
``` 

This will update the entry `ID` with the given times in the default stechuhr.
You may omit the `--in-time` or `--out-time` argument, if you only want to update one.
You may change which stechuhr is used with the `--database PATH/TO/STECHUHR/DATABASE` argument.

**Delete Entry**  
To delete an entry in a stechuhr, run

```shell
stechuhr update --identifier ID
```

This will delete the entry `ID` in the default stechuhr.
You may change which stechuhr is used with the `--database PATH/TO/STECHUHR/DATABASE` argument.

**Export**  
To export a stechuhr, run

```shell
stechuhr export
```  

This will export the default stechuhr in a CSV format.
You may change the format with the `--export-format FORMAT` argument.
When exporting to HTML a default jinja template is used.
You may change the template with the `--template-path TEMPLATE` argument.
By default, the output gets written to stdout.
You may change this with the `--export-file FILENAME` argument.
You may change which stechuhr is used with the `--database PATH/TO/STECHUHR/DATABASE` argument.

**Archive**  
To archive a stechuhr, run

```shell
stechuhr archive
```  

This will archive the default stechuhr to `./archive/<CURRENT_DATETIME>_<STECHUHR_DB_NAME>.db`.
You may change the archive directory using the `--archive-dir DIR` argument.
You may change which stechuhr is used with the `--database PATH/TO/STECHUHR/DATABASE` argument.

**Reset**  
To reset a stechuhr, run

```shell
stechuhr reset
```  

This will reset the default stechuhr.
You may change which stechuhr is used with the `--database PATH/TO/STECHUHR/DATABASE` argument.

**Merge two**
To merge a stechuhr with another one, run

```shell
stechuhr merge --to-merge PATH/TO/OTHER/STECHUHR
```   

This will reset the stechuhr given by the `--to-merge PATH/TO/OTHER/STECHUHR` argument into the default stechuhr.
You may change which stechuhr is used with the `--database PATH/TO/STECHUHR/DATABASE` argument.

**Sort**  
To sort a stechuhr, run

```shell
stechuhr sort
```

This will sort the default stechuhr according to the clock in times.
This will change the ID's in the underlying database.
You may change which stechuhr is used with the `--database PATH/TO/STECHUHR/DATABASE` argument.