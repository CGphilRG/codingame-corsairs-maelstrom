> 🇬🇧 [English version](README.md)

# Corsairs of the Maelstrom — Projet CodinGame Multiplayer SDK

Un puzzle multijoueur algorithmique basé sur la **cinématique inertielle à masse variable**, la **navigation dans un champ de vecteurs tourbillonnant (Maelström)** et la **balistique prédictive**, développé avec le **CodinGame Game Engine (`4.7.7`)** en **3 divisions progressives** (**Bois 3 → Bois 2 → Bois 1**).

---

## 1. Commandes Rapides

### Lancer le Viewer Web Local (`http://localhost:8888/test.html`)
```bash
cd corsairs-maelstrom-sdk
mvn test-compile exec:java -Dexec.mainClass="Main" -Dexec.classpathScope="test"
```

### Lancer le Banc de Simulation Rapide (Sans Serveur Web)
```bash
cd corsairs-maelstrom-sdk
mvn test-compile exec:java -Dexec.mainClass="Main" -Dexec.classpathScope="test" -Dexec.args="--simulate"
```

---

## 2. Structure du Projet

* [`pom.xml`](pom.xml) : Configuration Maven avec `core`, `module-entities`, `module-tooltip`, `module-endscreen`, `module-toggle` et `runner` (`4.7.7`).
* [`config/config.ini`](config/config.ini) : Paramètres du jeu (`type=multi`, `min_players=2`, `max_players=2`).
* [`config/stub.txt`](config/stub.txt) : Générateur de code d'entrée/sortie multi-langages.
* [`config/statement_en.html.tpl`](config/statement_en.html.tpl) & [`config/statement_fr.html.tpl`](config/statement_fr.html.tpl) : Énoncés HTML filtrés en anglais et en français pour chaque division.
* `config/level1/Boss.java`, `config/level2/Boss.java`, `config/level3/Boss.java` : Boss progressifs par division *(conservés en local uniquement et exclus via `.gitignore`)*.
* [`src/main/java/com/codingame/game/Referee.java`](src/main/java/com/codingame/game/Referee.java) : Arbitre physique complet, champ tourbillonnaire du Maelström, livraison d'or au Port et onde de choc des canons.

---

## 3. Liens

* **Contribution CodinGame** : https://www.codingame.com/contribute/view/158647b537dec10e539706b149bde5a6c7442f
* **Jouer dans l'IDE CodinGame** : https://www.codingame.com/ide/demo/1605692ff7906372a45b3320918ac8fbdaaa75f
* **Portail GitHub Pages (6 Puzzles)** : https://cgphilrg.github.io/codingame-sdk-puzzles/
