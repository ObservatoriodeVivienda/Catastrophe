# Description
An NGO, [Observatorio del Derecho a la Vivienda][observatorio-web] was
trying to get the cadastre data of México City, but [SEDUVI][seduvi-map]
(the corresponding goverment organization) doesn't have an API to access
this public information.

This repository includes a script to query their database.

[cm-slack]: http://slack.codeandomexico.org/
[cm-twitter]: https://twitter.com/CodeandoMexico
[observatorio-web]: http://www.observatoriodevivienda.org/
[seduvi-map]: http://ciudadmx.df.gob.mx:8080/seduvi/


# Usage
1) Download the script:

```bash
wget https://raw.githubusercontent.com/MrOutis/Catastrophe/master/catastrophe
```

_Make sure the script is runnable_:

```bash
chmod 775 catastrophe
```

2) Run it with a latitude and a longitude:

```bash
./catastrophe 19.401408 -99.201958
```

3) Enjoy your cadastre account :neckbeard:


# Roadmap
- [ ] Write more context info
- [ ] Write some tests
- [ ] Code another script to scrap the cadastre data using [this KMLs][kml-dataset]

[kml-dataset]: http://datos.labcd.mx/dataset?tags=Catastro


# License
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


----------------------------------------------------------------------------


Mr. Outis wrote this script.
If you meet him some day, and you think this stuff is worth it,
you can buy him a beer in return.
<mroutis@protonmail.com>

