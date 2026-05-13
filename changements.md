# Changements — fork `dash-chat-multi`

Ce document décrit les modifications apportées par rapport à la lib `dash-chat` originale, et comment installer le fork en local pour pouvoir l'utiliser côte à côte avec la version officielle.

---

## 1. Nouvelles fonctionnalités

### 1.1 Sélection multi-fichiers

L'attribut `multiple` est activé sur l'input file. L'utilisateur peut sélectionner plusieurs fichiers en une fois (Ctrl+clic ou Shift+clic dans le sélecteur), ou ajouter des fichiers en plusieurs lots successifs — les fichiers s'**accumulent** (pas d'écrasement).

- Chaque preview a sa propre croix de suppression individuelle.
- À l'envoi, tous les fichiers sont convertis en base64 en parallèle (`Promise.all`) et empaquetés dans un seul message avec un tableau de blocs `attachment`.
- Re-sélectionner le même fichier est possible (l'input est reset après chaque upload).

### 1.2 Drag-and-drop natif

On peut désormais glisser-déposer un ou plusieurs fichiers directement sur la zone d'input :

- Retour visuel : bordure pointillée bleue + fond légèrement teinté quand on survole la zone.
- Filtre `accept` respecté côté drop (les fichiers non supportés sont ignorés).
- Désactivé pendant que l'assistant est en train de répondre (`showTyping`).
- Cumulatif avec la sélection par bouton (on peut drop puis cliquer pour ajouter d'autres fichiers).

---

## 2. Renommages

Pour permettre la coexistence avec la lib `dash-chat` officielle, tout a été renommé :

| Ancien                | Nouveau                  |
| --------------------- | ------------------------ |
| npm `dash-chat`       | `dash-chat-multi`        |
| Python `dash_chat`    | `dash_chat_multi`        |
| Composant `ChatComponent` | `ChatComponentMulti` |
| Bundle `dash_chat.min.js` | `dash_chat_multi.min.js` |

### Fichiers source modifiés par le renommage

- `package.json` — `name` + script `build:py`
- `webpack.config.js` — nom du chunk partagé
- `MANIFEST.in` — chemins des artefacts inclus dans le sdist
- `_validate_init.py` — nom du package validé
- `src/lib/components/ChatComponent.js` → renommé en `ChatComponentMulti.js` + identifiants internes mis à jour
- `src/lib/index.js` — export
- `src/demo/App.js` — import et usage

### Fichiers source modifiés pour le DnD

- `src/private/ChatMessageInput.js` — state `isDragging`, fonction `addFiles`, handlers `onDragOver` / `onDragEnter` / `onDragLeave` / `onDrop`, filtre `accept`
- `src/styles/chatStyles.css` — classe `.dragging`

---

## 3. Installation locale

### Prérequis

- Python 3.9+
- Node.js 18+ et npm
- Un venv activé

### Étapes

```powershell
cd c:\Users\vagoa\Desktop\stage_BPCE\dash\dash-chat-multiple-input

# 1. Désinstaller l'ancien package éditable s'il existe
pip uninstall dash-chat -y

# 2. Supprimer les artefacts de build de l'ancien nom
Remove-Item -Recurse -Force dash_chat -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force dash_chat.egg-info -ErrorAction SilentlyContinue

# 3. Installer les dépendances npm (si pas déjà fait)
npm install

# 4. Builder la lib (génère le dossier dash_chat_multi/)
npm run build:activated
# ou, si le venv est déjà activé :
# npm run build

# 5. Installer en mode éditable
pip install -e .
```

### Vérification

```powershell
pip show dash-chat-multi
python -c "from dash_chat_multi import ChatComponentMulti; print(ChatComponentMulti)"
```

---

## 4. Cohabitation avec la lib originale

Une fois le fork installé, tu peux ajouter la version officielle à côté sans conflit :

```powershell
pip install dash-chat
```

Les deux libs vivent dans des namespaces séparés :

```python
from dash_chat import ChatComponent              # version originale (PyPI)
from dash_chat_multi import ChatComponentMulti   # fork local (multi + DnD)
```

---

## 5. Usage minimal

```python
import dash
from dash import callback, html, Input, Output, State
from dash_chat_multi import ChatComponentMulti

app = dash.Dash(__name__)

app.layout = html.Div([
    ChatComponentMulti(
        id="chat-component",
        messages=[],
        supported_input_file_types=[".png", ".jpg", ".pdf", ".doc"]
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

    if isinstance(new_message["content"], list):
        for item in new_message["content"]:
            if item["type"] == "attachment":
                print(f"Fichier reçu : {item['fileName']} ({item['fileType']})")

    bot_response = {"role": "assistant", "content": "OK reçu"}
    return messages + [new_message, bot_response]


if __name__ == "__main__":
    app.run(debug=True)
```

Format du message envoyé quand il y a des pièces jointes :

```python
{
    "role": "user",
    "id": 1700000000000,
    "content": [
        {"type": "text", "text": "voici les documents"},
        {"type": "attachment", "file": "data:image/png;base64,...", "fileName": "photo.png", "fileType": "image/png"},
        {"type": "attachment", "file": "data:application/pdf;base64,...", "fileName": "rapport.pdf", "fileType": "application/pdf"},
    ]
}
```

Sans pièce jointe, `content` reste une simple `str`.

---

## 6. Rebuild après modification du code source

Si tu modifies un fichier dans `src/` :

```powershell
npm run build:activated
```

L'install éditable (`pip install -e .`) garde la lib synchronisée automatiquement — pas besoin de réinstaller à chaque rebuild.

---

## 7. Limitations connues (non corrigées dans ce fork)

- **Fuite mémoire sur les previews d'images** : `URL.createObjectURL` est appelé inline dans le render sans `revokeObjectURL`. Avec beaucoup d'images, ça scale en `O(N × renders)`. À corriger avec un `useMemo` + cleanup `useEffect`.
- **État dupliqué** entre `selectedFiles` (local à `ChatMessageInput`) et `attachment` (dans `ChatComponentMulti`). Fragile mais fonctionnel tant que les setters sont appelés en paire.
- **Pas de dédup** : sélectionner deux fois le même fichier le duplique.
- **Pas de limite de taille / nombre** : le base64 multiplie la taille par ~1.33, attention avec de gros fichiers.
- **Drop de dossier non géré** : `dataTransfer.files` est vide ou partiel selon le navigateur, comportement standard.
- **Bug indépendant dans `persistence_type`** ([ChatComponentMulti.js:101-106](src/lib/components/ChatComponentMulti.js#L101-L106)) : la branche `"session"` est morte (typo `=== "local"` au lieu de `=== "session"`).
