# Description
In the [Slack][cm-slack] of [Codeando México][cm-twitter],
someone from an ONG asked for help to scrap some data.

This time, [SEDUVI's cadastral map][seduvi-map] was the target.

This repository includes my effort to help
[Observatorio del Derecho a la Vivienda][observatorio-web].

[cm-slack]: http://slack.codeandomexico.org/
[cm-twitter]: https://twitter.com/CodeandoMexico
[observatorio-web]: http://www.observatoriodevivienda.org/
[seduvi-map]: http://ciudadmx.df.gob.mx:8080/seduvi/

# Do it yourself
1. Get a KML from [here][kml-dataset].

2. Extract a latitude/longitude from your KML.

```bash
grep '<coordinates>.*</coordinates>' -m 1 doc.kml |
awk '{print $3}' |
cut -d ','
```
_Note: The latitude is a negative number_

3. Download the **catastrophe** script and make it runnable:
```bash
wget https://raw.githubusercontent.com/MrOutis/Catastrophe/master/catastrophe &&
chmod 775 catastrophe
``

3. Run the following to get the cadastre account:
```bash
# replace `lat` and `lon` with the output of step 2
./catastrophe lat lon
```

4. ????

5. **PROFIT!!!**

Now, to make the scraper, you need to iterate over your KML,
getting one latitude and longitude of each polygon, and
for each one, run `catastrope lat lon`.

This implementation is language agnostic, you only need a
computer capable of run `bash` and `awk`.

[kml-dataset]: http://datos.labcd.mx/dataset?tags=Catastro

# Roadmap
- [] Write a better README
- [] Write the rest of the roadmap

