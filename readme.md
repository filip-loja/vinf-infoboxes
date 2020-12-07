
# Store modul
* úlohou tohto modulu je indexovanie už spracovaných dát z infoboxov anglickej wikipédie
* následne umožní nad dátami vykonávať vyhľadávanie
* indexovanie aj vyhľadávanie je implementované prostredníctvom PyLucene

## Ovládanie
```
python store <action> [<config-file>]
```
* `<action>` - názov akcie, ktorá sa má vykonať
    * `index` - spustí sa indexovanie vyparsovaných dát
    * `search` - spustí sa vyhľadávanie nad zaindexovanými dátami
* `<config-file>` - cesta ku konfiguračnému JSON súboru (ak nie je zadaná, použije sa súbor `/config.json`)

#### Príklad
```
python store index
python store search 'C:\Development\vinf\project\config.json'
```

#### Konfiguračný súbor
```
{
  "sourceFile": "./source.txt",
  "indexPath": "./index/",
  "queryFile": "./query.json",
  "outputFile": "./result.json",
  "printOutput": true,
  "maxHits": 1000
}
```
* `sourceFile` - textový súbor obsahujúci dáta, ktoré chceme indexovať, každý riadok musí byť validný JSON objekt
* `indexPath` - cesta k priečinku, kam si PyLucene ukladá svoj index, obsah tohto priečinka je vždy vymazaný pred spustením indexovania
* `queryFile` - cesta k JSON súboru, ktorý obsahuje definíciu dopytu nad dátami
* `outputFile` - cesta k JSON súboru, do ktorého sa uložia výsledky vyhľadávania na zákalde dopytu, ktorý je uložený v `queryFile`, pokiaľ tento parameter v súbore prítomný nebude, výsledky vyhľadávania sa neuložia nikam
* `printOutput` - boolovsky prepínač; ak má hodnotu `true`, výsledok dopytu zo súboru `queryFile` sa vypíše aj do konzoly; predvolenou hodnotou je `true`
* `maxHits` - určuje maximálny počet výsledkov vyhľadávacieho dopytu

## Vyhľadávanie
Vyhľadávanie sa vykonáva na základe dopytov, ktoré sú definované v JSON formáte. Dopyty je možné zapisovať viacerými spôsosobmi. Vyhľadávať je možné buď fulltextovo alebo v nasledujúcich poliach:
* `id`
* `name`
* `type`
* `country`
* `population`
* `population_density`
* `area_km2`
* `elevation_m`
* `leader`

### Základné vyhľadávanie
Hľadaný výraz (`term`) sa musí v zadanom poli (`field`) nachádzať celý.
```
{
  "term": "czech",
  "field": "country"
}

```

### Prefixové vyhľadávanie
Obsah zadaného poľa (`field`) musí začínať hľadaným výrazom (`term`).
```
{
  "term": "well",
  "field": "name",
  "prefix": true
}
```

### Fuzzy vyhľadávanie
Hľadaný výraz (`term`) môže obsahovať preklep.
```
{
  "term": "rotedam",
  "field": "name",
  "fuzzy": true
}

```

### Vyhľadávanie podľa intervalu
Dáta v poliach, ktoré obsahujú číselné údaje je možné vyhľadávať aj zadaním intervalu.
```
{
  "term": [100, 200],
  "field": "population_density"
}
```
**Typy intervalov:**
* `"term": [100, 200]` --- *<100, 200>*
* `"term": ["-", 300]` --- *(-INF, 300>*
* `"term": [300, "-"]` --- *<300, INF)*

**Číselné polia:**
* `id`
* `population`
* `population_density`
* `area_km2`
* `elevation_m`

### Fulltextové vyhľadávanie
Textové vyhľadávanie cez všetky polia
```
{
  "term": "brno, matus vallo",
  "field": "fulltext"
}

```

### Zložené vyhľadávanie
Všetky vyššie uvedené typy dopytov je možné navzájom kombinovať prostredníctvom skupín dopytov.
```
{
  "group": "OR",
  "conditions": [
    {
      "term": "hu",
      "field": "country"
    },
    {
      "term": "cz",
      "field": "country"
    }
  ]
}
```
**Typy skupín**
* `OR` - aspoň jeden z dopytov musí byť nájdený
* `AND` - všetky dopyty musia byť nájdené

Skupiny je možné do seba rekurzívne vnárať:
```
{
  "group": "AND",
  "conditions": [
    {
      "group": "OR",
      "conditions": [
        {
          "term": "usa",
          "field": "country"
        },
        {
          "term": "nl",
          "field": "country"
        }
      ]
    },
    {
      "term": [600000, "-"],
      "field": "population"
    }
  ]
}

```

### Filtrovanie polí na vrátenie
Pokiaľ nechceme, aby výsledok dopytu obsahoval všetky polia, ktoré sú pre dané mesto uložené, môžeme špecifikovať len tie, ktoré sa majú vrátiť. Z indexu sa teraz načítajú len zadané polia a nie všetky, ako by tomu bolo v prípade, že by sa atribút `fetch` nepoužil.
```
{
  "term": "czech",
  "field": "country",
  "fetch": ["id", "name", "type"]
}
```
