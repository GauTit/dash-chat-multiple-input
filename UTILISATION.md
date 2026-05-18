# Utilisation — `dash-chat-multi`

Guide pratique pour installer et utiliser le composant `ChatComponentMulti` dans une app Dash. Pour la liste détaillée des modifications par rapport à la lib `dash-chat` originale, voir [changements.md](changements.md).

---

## 1. Installation

### 1.1 Prérequis

- Python 3.9+
- Node.js 18+ et npm
- Un venv Python activé

### 1.2 Installation locale (depuis ce repo)

La lib n'est **pas publiée sur PyPI**. Elle s'installe en mode éditable depuis le dossier source.

```powershell
cd c:\Users\vagoa\Desktop\stage_BPCE\dash\dash-chat-multiple-input

# 1. Dépendances JS
npm install

# 2. Build du bundle JS (~2 min)
npm run build:js

# 3. Génération des wrappers Python
npm run build:py

# 4. Install Python en mode éditable
pip install -e .
```

> Sous Windows, **ne pas utiliser** `npm run build:activated` — le script contient de la syntaxe bash et plante sous PowerShell. Lance `build:js` puis `build:py` séparément.

### 1.3 Vérification de l'install

```powershell
pip show dash-chat-multi
python -c "from dash_chat_multi import ChatComponentMulti; print(ChatComponentMulti)"
```

Tu dois voir `<class 'dash_chat_multi.ChatComponentMulti.ChatComponentMulti'>`.
Si tu vois `<module ...>`, le `__init__.py` du package est manquant — voir [changements.md §3.2](changements.md).

### 1.4 Cohabitation avec la lib officielle

Tu peux installer `dash-chat` (PyPI) à côté du fork sans conflit — les namespaces sont disjoints :

```python
from dash_chat import ChatComponent              # version originale PyPI
from dash_chat_multi import ChatComponentMulti   # fork local (multi + DnD)
```

---

## 2. Import

```python
from dash_chat_multi import ChatComponentMulti
```

Le composant exporté est `ChatComponentMulti` (et **pas** `ChatComponent`). C'est le seul composant exposé par la lib.

---

## 3. Usage minimal

```python
import dash
from dash import callback, html, Input, Output, State
from dash_chat_multi import ChatComponentMulti

app = dash.Dash(__name__)

app.layout = html.Div([
    ChatComponentMulti(
        id="chat-component",
        messages=[],
        supported_input_file_types=[".png", ".jpg", ".pdf", ".doc"],
    )
])


@callback(
    Output("chat-component", "messages"),
    Input("chat-component", "new_message"),
    State("chat-component", "messages"),
    prevent_initial_call=True,
)
def handle_chat(new_message, messages):
    if not new_message:
        return messages

    bot_response = {"role": "assistant", "content": "OK reçu"}
    return messages + [new_message, bot_response]


if __name__ == "__main__":
    app.run(debug=True)
```

L'API est **identique** à `ChatComponent` original — seuls le nom du composant et le nom du package changent. Les exemples du [README](README.md) (OpenAI, persistance, renderers graph/table) fonctionnent à l'identique en remplaçant `ChatComponent` par `ChatComponentMulti`.

---

## 4. Spécificités du fork

Le fork ajoute deux comportements côté UI **sans changer l'API Python** :

### 4.1 Sélection multi-fichiers

- L'utilisateur peut sélectionner plusieurs fichiers d'un coup (Ctrl/Shift+clic).
- Les fichiers s'**accumulent** entre plusieurs sélections — pas d'écrasement.
- Chaque preview a sa croix de suppression individuelle.
- Re-sélectionner le même fichier est possible.

### 4.2 Drag-and-drop

- Drop d'un ou plusieurs fichiers directement sur la zone d'input.
- Le filtre `supported_input_file_types` est respecté côté drop.
- Désactivé pendant que l'assistant répond.
- Cumulatif avec la sélection par bouton.

Aucune prop supplémentaire à activer — les deux comportements sont **toujours actifs**.

---

## 5. Format du message reçu dans le callback

Le callback reçoit `new_message` sous deux formes possibles :

### 5.1 Sans pièce jointe — `content` est une string

```python
{"role": "user", "id": 1700000000000, "content": "salut"}
```

### 5.2 Avec une ou plusieurs pièces jointes — `content` est une liste de blocs

```python
{
    "role": "user",
    "id": 1700000000000,
    "content": [
        {"type": "text", "text": "voici les documents"},
        {
            "type": "attachment",
            "file": "data:image/png;base64,...",
            "fileName": "photo.png",
            "fileType": "image/png",
        },
        {
            "type": "attachment",
            "file": "data:application/pdf;base64,...",
            "fileName": "rapport.pdf",
            "fileType": "application/pdf",
        },
    ],
}
```

> Le bloc `text` est **toujours présent** (même vide) quand il y a des pièces jointes. Itère sur la liste plutôt que de supposer une position fixe.

### 5.3 Pattern de traitement côté callback

```python
def handle_chat(new_message, messages):
    if not new_message:
        return messages

    if isinstance(new_message["content"], list):
        for item in new_message["content"]:
            if item["type"] == "text":
                user_text = item["text"]
            elif item["type"] == "attachment":
                # item["file"] est une data URL base64
                # item["fileName"], item["fileType"] sont les métadonnées
                ...
    else:
        user_text = new_message["content"]

    bot_response = {"role": "assistant", "content": "..."}
    return messages + [new_message, bot_response]
```

---

## 6. Props principales

API identique à `ChatComponent` — voir le [README §Props](README.md) pour la table complète. Les props les plus utiles avec ce fork :

| Prop | Type | Note |
| --- | --- | --- |
| `id` | `string` | Requis pour les callbacks Dash. |
| `messages` | `list` | Initialiser à `[]`. |
| `supported_input_file_types` | `string` ou `list` | Filtre `accept` de l'input — respecté aussi en drag-and-drop. Ex : `[".png", ".jpg", ".pdf"]`. |
| `theme` | `"light"` \| `"dark"` | Thème global. |
| `persistence` | `bool` | Persistance localStorage / sessionStorage. |
| `persistence_type` | `"local"` \| `"session"` | ⚠️ Bug pré-existant : la branche `"session"` est cassée — voir [changements.md §7](changements.md#7-limitations-connues-non-corrigées-dans-ce-fork). |
| `file_attachment_button_config` | `dict` | Customisation du bouton d'attachement (label, icône, style). |
| `send_button_config` | `dict` | Customisation du bouton d'envoi. |

---

## 7. Rebuild après modification de la lib

Si tu modifies le code source du fork :

- **React (logique, propTypes)** → `npm run build:js && npm run build:py`
- **CSS uniquement** → `npm run build:js`
- **propTypes uniquement** → `npm run build:py`

L'install éditable (`pip install -e .`) garde la lib synchronisée — pas besoin de réinstaller. Exception : si tu supprimes/recrées le dossier `dash_chat_multi/`, fais :

```powershell
pip install -e . --force-reinstall --no-deps
```

---

## 8. Exemples complets

Le dossier [usage/](usage/) contient des exemples runnables :

- [usage.py](usage/usage.py) — chat basique
- [usage_with_image.py](usage/usage_with_image.py) — pièces jointes images
- [usage_graph_renderer.py](usage/usage_graph_renderer.py) — réponse contenant un graphe Plotly
- [usage_table_renderer.py](usage/usage_table_renderer.py) — réponse contenant un tableau
- [usage_file_renderer.py](usage/usage_file_renderer.py) — réponse contenant un fichier
- [usage_combine_rendering.py](usage/usage_combine_rendering.py) — combinaison texte + graph + table

Pour les lancer, remplace `ChatComponent` par `ChatComponentMulti` et `dash_chat` par `dash_chat_multi` dans l'import.
