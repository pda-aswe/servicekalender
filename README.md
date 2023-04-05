# Kalender-Service

## Datenstruktur des Topics appointment/next
```json
{
   "start":"2023-04-04T22:00:00+02:00",
   "end":"2023-04-04T22:00:00+02:00",
   "id":"<ID-DES-TERMINS>",
   "summary":"<TITEL-DES-TERMINS>",
   "location":"<STRING-MIT-DEM-STANDORT>",
   "status":"<STATUS MEIST confirmed>"
}
```
Anfrage durch: `req/appointment/next`


## Datenstruktur des Topics appointment/create
```json
{
   "start":"2023-04-04T22:00:00+02:00",
   "end":"2023-04-04T22:00:00+02:00",
   "summary":"<TITEL-DES-TERMINS>",
   "location":"<STRING-MIT-DEM-STANDORT>"
}
```
Der Key location ist optional.

## Datenstruktur des Topics appointment/delete
```json
{
   "id":"<ID-DES-TERMINS>"
}
```

## Datenstruktur des Topics appointment/update
```json
{
   "start":"2023-04-04T22:00:00+02:00",
   "end":"2023-04-04T22:00:00+02:00",
   "summary":"<TITEL-DES-TERMINS>",
   "location":"<STRING-MIT-DEM-STANDORT>",
   "id":"<ID-DES-TERMINS>"
}
```
Jeder Key ist optional außer id. Dadurch können nur bestimmte sachen im Termin angepasst werden.

## Datenstruktur des Topics req/appointment/range
```json
{
   "start":"2023-04-04T22:00:00+02:00",
   "end":"2023-04-04T22:00:00+02:00"
}
```

## Datenstruktur des Topics appointment/range
```json
{
   "start":"2023-04-04T22:00:00+02:00",
   "end":"2023-04-04T22:00:00+02:00",
   "events":[
      {
         "start":"2023-04-04T22:00:00+02:00",
         "end":"2023-04-04T22:00:00+02:00",
         "id":"<ID-DES-TERMINS>",
         "summary":"<TITEL-DES-TERMINS>",
         "location":"<STRING-MIT-DEM-STANDORT>",
         "status":"<STATUS MEIST confirmed>"
      },
      {
         "start":"2023-04-04T22:00:00+02:00",
         "end":"2023-04-04T22:00:00+02:00",
         "id":"<ID-DES-TERMINS>",
         "summary":"<TITEL-DES-TERMINS>",
         "location":"<STRING-MIT-DEM-STANDORT>",
         "status":"<STATUS MEIST confirmed>"
      }
   ]
}
```
Liste aller Events geordnet nach Start des Termins.