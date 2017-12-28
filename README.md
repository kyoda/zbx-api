# zabbix-api


## PREPARE

+ some json files

## EXEC

```
python main.py
```


## Severity of the trigger. 

```
Possible values are: 
0 - (default) not classified; 
1 - information; 
2 - warning; 
3 - average; 
4 - high; 
5 - disaster.
```

## Media Object severity

```
Trigger severities to send notifications about. 

Severities are stored in binary form with each bit representing the corresponding severity. For example, 12 equals 1100 in binary and means, that notifications will be sent from triggers with severities warning and average. 

Refer to the trigger object page for a list of supported trigger severities.
```

6 digits?

```
disaster, high, average, warning, information, not classified
```

### Example

+ average and warning (001100)
  - `001100 = 12`
+ all
 - `111111 = 2*5 + 2*4 + 2*3 + 2*2 + 2*1 + 2*0 = 32 + 16 + 8 + 4 + 2 + 1 = 63`

