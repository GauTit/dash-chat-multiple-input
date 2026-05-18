# Changements — fork `dash-chat-multi`

Ce document liste **tous les changements** apportés à la lib `dash-chat` originale dans le cadre du fork `dash-chat-multi`, et explique comment installer / rebuilder le fork localement pour pouvoir l'utiliser côte à côte avec la version officielle.

---

## 1. Nouvelles fonctionnalités

### 1.1 Sélection multi-fichiers

L'attribut `multiple` est activé sur l'input file. L'utilisateur peut sélectionner plusieurs fichiers en une fois (Ctrl+clic ou Shift+clic dans le sélecteur), ou ajouter des fichiers en plusieurs lots successifs — les fichiers s'**accumulent** (pas d'écrasement).

- Chaque preview a sa propre croix de suppression individuelle.
- À l'envoi, tous les fichiers sont convertis en base64 en parallèle (`Promise.all`) et empaquetés dans un seul message avec un tableau de blocs `attachment`.
- Re-sélectionner le même fichier est possible (l'input est reset après chaque upload).

Implémenté dans :
- [src/private/ChatMessageInput.js](src/private/ChatMessageInput.js) — state `selectedFiles`, fonction `addFiles`, handlers `handleFileUpload` / `handleRemoveFile`
- [src/lib/components/ChatComponentMulti.js](src/lib/components/ChatComponentMulti.js) — state `attachment`, sérialisation `Promise.all` dans `handleSendMessage`

### 1.2 Drag-and-drop natif

On peut désormais glisser-déposer un ou plusieurs fichiers directement sur la zone d'input :

- Retour visuel : bordure pointillée bleue + fond légèrement teinté quand on survole la zone.
- Filtre `accept` respecté côté drop (les fichiers non supportés sont ignorés).
- Désactivé pendant que l'assistant est en train de répondre (`showTyping`).
- Cumulatif avec la sélection par bouton (on peut drop puis cliquer pour ajouter d'autres fichiers).

Implémenté dans :
- [src/private/ChatMessageInput.js](src/private/ChatMessageInput.js) — state `isDragging`, fonction `filterByAccept`, handlers `handleDragOver` / `handleDragEnter` / `handleDragLeave` / `handleDrop`
- [src/styles/chatStyles.css](src/styles/chatStyles.css) — classe `.dragging`

---

## 2. Renommages (cohabitation avec la lib originale)

Pour permettre l'installation simultanée de `dash-chat` et de ce fork, tout a été renommé :

| Ancien                    | Nouveau                    |
| ------------------------- | -------------------------- |
| npm `dash-chat`           | `dash-chat-multi`          |
| Python `dash_chat`        | `dash_chat_multi`          |
| Composant `ChatComponent` | `ChatComponentMulti`       |
| Bundle `dash_chat.min.js` | `dash_chat_multi.min.js`   |
| Dossier `dash_chat/`      | `dash_chat_multi/`         |
| Chunk webpack `dash_chat-shared` | `dash_chat_multi-shared` |

### Fichiers source touchés par le renommage

- [package.json](package.json) — `name` + script `build:py`
- [webpack.config.js](webpack.config.js) — nom du chunk partagé (hardcodé ligne 100)
- [MANIFEST.in](MANIFEST.in) — chemins des artefacts inclus dans le sdist
- [_validate_init.py](_validate_init.py) — variable `components_package`
- [src/lib/components/ChatComponent.js](src/lib/components/ChatComponentMulti.js) → **renommé** en `ChatComponentMulti.js` + identifiants internes mis à jour (const, propTypes, default export, JSDoc)
- [src/lib/index.js](src/lib/index.js) — import + export
- [src/demo/App.js](src/demo/App.js) — import + usage

---

## 3. Corrections de bugs

### 3.1 PropTypes invalide dans `messages.content`

[src/lib/components/ChatComponentMulti.js](src/lib/components/ChatComponentMulti.js) (autour de la ligne 337)

**Bug pré-existant** dans la lib originale : utilisation de `PropTypes.oneOf(shape, object)` au lieu de `PropTypes.oneOfType([shape, object])`. `oneOf` attend une liste de valeurs *littérales* (strings/nombres), pas d'autres validateurs `PropTypes`. La nouvelle version de Dash valide plus strictement et plante `dash-generate-components` avec :

```
AttributeError: 'str' object has no attribute 'get'
```

**Fix** : remplacer `oneOf` par `oneOfType` avec liste entre crochets.

```js
// Avant (cassé)
PropTypes.arrayOf(
    PropTypes.oneOf(
        PropTypes.shape({ ... }),
        PropTypes.object
    )
)

// Après
PropTypes.arrayOf(
    PropTypes.oneOfType([
        PropTypes.shape({ ... }),
        PropTypes.object,
    ])
)
```

### 3.2 `__init__.py` manquant après rebuild

Si tu supprimes le dossier `dash_chat_multi/` avant de rebuild (pour faire un clean install), `dash-generate-components` régénère les wrappers (`ChatComponentMulti.py`, `_imports_.py`) **mais pas le `__init__.py`** — il s'attend à ce qu'il existe déjà.

Sans `__init__.py`, Python résout `from dash_chat_multi import ChatComponentMulti` comme **le module** `ChatComponentMulti.py`, et l'instanciation `ChatComponentMulti(...)` plante avec :

```
TypeError: 'module' is not callable
```

**Fix** : un `__init__.py` complet est maintenant versionné dans [dash_chat_multi/__init__.py](dash_chat_multi/__init__.py). Si tu fais un clean total du dossier, restaure-le depuis le repo avant le `pip install -e .`.

---

## 4. Installation locale

### Prérequis

- Python 3.9+
- Node.js 18+ et npm
- Un venv activé

### Première installation (clean)

```powershell
cd c:\Users\vagoa\Desktop\stage_BPCE\dash\dash-chat-multiple-input

# 1. Désinstaller l'ancien package éditable s'il existe
pip uninstall dash-chat -y
pip uninstall dash-chat-multi -y

# 2. (optionnel) Nettoyer les artefacts de build
Remove-Item -Recurse -Force dash_chat -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force dash_chat.egg-info -ErrorAction SilentlyContinue

# 3. Installer les dépendances npm
npm install

# 4. Builder le bundle JS (lent : ~2 min)
npm run build:js

# 5. Générer les wrappers Python depuis les sources JS
npm run build:py

# 6. Installer en mode éditable
pip install -e .
```

> ⚠️ **Ne pas utiliser `npm run build:activated`** sur Windows : le script utilise une syntaxe bash (`. venv/bin/activate || venv\scripts\activate`) qui plante sous PowerShell. Lance `build:js` et `build:py` séparément, en t'assurant que ton venv est activé.

### Rebuild après modification du code source

- **Modif d'un composant React (logique, propTypes)** → rebuild JS + wrappers Python :
  ```powershell
  npm run build:js
  npm run build:py
  ```
- **Modif uniquement du CSS ou d'un fichier non-component** → rebuild JS seulement :
  ```powershell
  npm run build:js
  ```
- **Modif des propTypes uniquement** → rebuild Python seulement :
  ```powershell
  npm run build:py
  ```

L'install éditable (`pip install -e .`) garde la lib synchronisée — pas besoin de réinstaller à chaque rebuild, sauf si tu as supprimé/recréé le dossier `dash_chat_multi/`, auquel cas :

```powershell
pip install -e . --force-reinstall --no-deps
```

### Vérification

```powershell
pip show dash-chat-multi
python -c "from dash_chat_multi import ChatComponentMulti; print(ChatComponentMulti)"
```

Tu dois voir `<class 'dash_chat_multi.ChatComponentMulti.ChatComponentMulti'>` (pas `<module ...>`).

---

## 5. Cohabitation avec la lib originale

Une fois le fork installé, tu peux ajouter la version officielle PyPI à côté sans conflit :

```powershell
pip install dash-chat
```

Les deux libs vivent dans des namespaces séparés :

```python
from dash_chat import ChatComponent              # version originale (PyPI)
from dash_chat_multi import ChatComponentMulti   # fork local (multi + DnD)
```

---

## 6. Usage minimal

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

### Format du message envoyé

**Sans pièce jointe** — `content` est une simple string :

```python
{"role": "user", "id": 1700000000000, "content": "salut"}
```

**Avec une ou plusieurs pièces jointes** — `content` est une liste de blocs typés :

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

---

## 7. Limitations connues (non corrigées dans ce fork)

- **Fuite mémoire sur les previews d'images** : `URL.createObjectURL` est appelé inline dans le render sans `revokeObjectURL`. Avec beaucoup d'images, ça scale en `O(N × renders)`. À corriger avec un `useMemo` + cleanup `useEffect`.
- **État dupliqué** entre `selectedFiles` (local à `ChatMessageInput`) et `attachment` (dans `ChatComponentMulti`). Fragile mais fonctionnel tant que les setters sont appelés en paire.
- **`handleSend` de MessageInput** passe `(value, selectedFiles)` à `onSend`, mais `handleSendMessage` ignore ses arguments et lit l'état du parent. API trompeuse, pas un bug actif.
- **Pas de dédup** : sélectionner deux fois le même fichier le duplique.
- **Pas de limite de taille / nombre** : le base64 multiplie la taille par ~1.33, attention avec de gros fichiers.
- **Drop de dossier non géré** : `dataTransfer.files` est vide ou partiel selon le navigateur, comportement standard.
- **Bug indépendant dans `persistence_type`** ([ChatComponentMulti.js:101-106](src/lib/components/ChatComponentMulti.js#L101-L106)) : la branche `"session"` est morte (typo `=== "local"` au lieu de `=== "session"`).
- **Script `build:activated` cassé sous Windows** : syntaxe bash, ne marche qu'en WSL ou Linux/Mac.

---

## 8. Diffs des modifications de code

Cette section liste, fichier par fichier, les modifications concrètes apportées au code (au-delà de ce qui existait déjà dans le fork multi-files pré-existant).

### 8.1 `src/private/ChatMessageInput.js` — drag-and-drop

**Diff du bloc states + handlers d'upload** :

```diff
  const fileInputRef = useRef(null);
  const [selectedFiles, setSelectedFiles] = useState([]);
+ const [isDragging, setIsDragging] = useState(false);
+
+ const addFiles = (newFiles) => {
+     if (newFiles.length === 0) return;
+     const updated = [...selectedFiles, ...newFiles];
+     setSelectedFiles(updated);
+     setAttachment(updated);
+ };

  const handleFileUpload = (event) => {
-     const newFiles = Array.from(event.target.files);
-     if (newFiles.length === 0) return;
-
-     // Mode cumulatif : on append aux fichiers déjà sélectionnés
-     const updated = [...selectedFiles, ...newFiles];
-     setSelectedFiles(updated);
-     setAttachment(updated);
-
-     // Reset l'input pour permettre de re-sélectionner le même fichier
+     addFiles(Array.from(event.target.files));
      event.target.value = "";
  };
+
+ const filterByAccept = (files) => {
+     if (!accept || accept === "*/*") return files;
+     const acceptList = Array.isArray(accept) ? accept : accept.split(",");
+     const normalized = acceptList.map((t) => t.trim().toLowerCase()).filter(Boolean);
+     if (normalized.length === 0 || normalized.includes("*/*")) return files;
+     return files.filter((f) => {
+         const fileType = (f.type || "").toLowerCase();
+         const fileName = f.name.toLowerCase();
+         return normalized.some((t) => {
+             if (t.endsWith("/*")) return fileType.startsWith(t.slice(0, -1));
+             if (t.startsWith(".")) return fileName.endsWith(t);
+             return fileType === t;
+         });
+     });
+ };
+
+ const handleDragOver = (e) => {
+     e.preventDefault();
+     e.stopPropagation();
+ };
+
+ const handleDragEnter = (e) => {
+     e.preventDefault();
+     e.stopPropagation();
+     if (showTyping) return;
+     setIsDragging(true);
+ };
+
+ const handleDragLeave = (e) => {
+     e.preventDefault();
+     e.stopPropagation();
+     if (e.currentTarget.contains(e.relatedTarget)) return;
+     setIsDragging(false);
+ };
+
+ const handleDrop = (e) => {
+     e.preventDefault();
+     e.stopPropagation();
+     setIsDragging(false);
+     if (showTyping) return;
+     const dropped = Array.from(e.dataTransfer.files || []);
+     addFiles(filterByAccept(dropped));
+ };
```

**Diff du container JSX** :

```diff
- <div className="message-input-container" style={customStyles}>
+ <div
+     className={`message-input-container ${isDragging ? "dragging" : ""}`}
+     style={customStyles}
+     onDragOver={handleDragOver}
+     onDragEnter={handleDragEnter}
+     onDragLeave={handleDragLeave}
+     onDrop={handleDrop}
+ >
```

### 8.2 `src/styles/chatStyles.css` — style du drop zone

```diff
  .message-input-container {
      width: 100%;
      margin-top: 10px;
      border: 1px solid;
      border-radius: 10px;
+     transition: outline-color 0.15s ease, background-color 0.15s ease;
  }

+ .message-input-container.dragging {
+     outline: 2px dashed #c6117e;
+     outline-offset: -4px;
+     background-color: rgba(0, 123, 255, 0.06);
+ }
+
  .message-input-container .disabled {
      background-color: #efefef4d;
      ...
  }
```

### 8.3 `package.json` — renommage npm + build:py

```diff
- "name": "dash-chat",
+ "name": "dash-chat-multi",
  "version": "0.3.0",
- "description": "A chat component for Dash",
+ "description": "A chat component for Dash (multi-file + drag-and-drop fork)",
```

```diff
- "build:py": "dash-generate-components ./src/lib/components dash_chat -p package-info.json",
+ "build:py": "dash-generate-components ./src/lib/components dash_chat_multi -p package-info.json",
```

### 8.4 `webpack.config.js` — chunk partagé hardcodé

```diff
                      shared: {
                          chunks: 'all',
                          minSize: 0,
                          minChunks: 2,
-                         name: 'dash_chat-shared'
+                         name: 'dash_chat_multi-shared'
                      }
```

### 8.5 `MANIFEST.in` — chemins des artefacts

```diff
- include dash_chat/dash_chat.min.js
- include dash_chat/dash_chat.min.js.map
- include dash_chat/metadata.json
- include dash_chat/package-info.json
+ include dash_chat_multi/dash_chat_multi.min.js
+ include dash_chat_multi/dash_chat_multi.min.js.map
+ include dash_chat_multi/metadata.json
+ include dash_chat_multi/package-info.json
  include README.md
  include package.json
```

### 8.6 `_validate_init.py` — nom du package à valider

```diff
- components_package = "dash_chat"
+ components_package = "dash_chat_multi"
```

### 8.7 `src/lib/components/ChatComponent.js` → `ChatComponentMulti.js`

- Fichier **renommé** (move) : `ChatComponent.js` → `ChatComponentMulti.js`
- Remplacement global de l'identifiant à l'intérieur du fichier :

```diff
- const ChatComponent = ({
+ const ChatComponentMulti = ({
      ...
  });
- ChatComponent.propTypes = { ... };
+ ChatComponentMulti.propTypes = { ... };
- export default ChatComponent;
+ export default ChatComponentMulti;
```

(toutes les occurrences `ChatComponent` du JSDoc/exemples ont aussi été remplacées)

### 8.8 `src/lib/components/ChatComponentMulti.js` — fix PropTypes (autour ligne 337)

```diff
  content: PropTypes.oneOfType([
      PropTypes.arrayOf(
-         PropTypes.oneOf(
+         PropTypes.oneOfType([
              PropTypes.shape({
                  type: PropTypes.oneOf(["text", "attachment", "table", "graph"]).isRequired,
                  props: PropTypes.object,
              }),
-             PropTypes.object
-         )
+             PropTypes.object,
+         ])
      ),
      PropTypes.string,
      PropTypes.object,
  ]).isRequired,
```

### 8.9 `src/lib/index.js` — export

```diff
  /* eslint-disable import/prefer-default-export */
- import ChatComponent from './components/ChatComponent';
+ import ChatComponentMulti from './components/ChatComponentMulti';

  export {
-     ChatComponent
+     ChatComponentMulti
  };
```

### 8.10 `src/demo/App.js` — import + usage du composant de demo

```diff
- import { ChatComponent } from '../lib';
+ import { ChatComponentMulti } from '../lib';

  ...
-         <ChatComponent
+         <ChatComponentMulti
              setProps={setProps}
              {...state}
          />
```

### 8.11 `dash_chat_multi/__init__.py` — fichier recréé manuellement

Fichier **régénéré** (perdu lors du clean du dossier `dash_chat/`). Contenu identique au template Dash standard, avec deux substitutions :

```diff
- {"relative_package_path": "dash_chat.min.js", "namespace": package_name},
+ {"relative_package_path": "dash_chat_multi.min.js", "namespace": package_name},
  {
-     "relative_package_path": "dash_chat.min.js.map",
+     "relative_package_path": "dash_chat_multi.min.js.map",
      "namespace": package_name,
      "dynamic": True,
  },
```

Fichier complet versionné dans le repo — voir [dash_chat_multi/__init__.py](dash_chat_multi/__init__.py).

### 8.12 `app.py` (hors lib) — import dans le projet utilisateur

```diff
- from dash_chat import ChatComponent
+ from dash_chat_multi import ChatComponentMulti

  ...
-     ChatComponent(
+     ChatComponentMulti(
          id="chat-component",
          messages=[],
          supported_input_file_types=[".png", ".jpg", ".pdf", ".doc"]
      )
```

> ℹ️ La ligne `supported_input_file_types=[...]` était déjà présente avant le fork — elle n'a pas été ajoutée par le renommage.

---

## 9. Historique des changements

| Date         | Type         | Description |
| ------------ | ------------ | ----------- |
| pré-fork     | feat         | Sélection multi-fichiers + accumulation + suppression individuelle |
| 2026-05-13   | feat         | Drag-and-drop natif sur la zone d'input |
| 2026-05-13   | refactor     | Renommage complet `dash_chat` → `dash_chat_multi` / `ChatComponent` → `ChatComponentMulti` |
| 2026-05-13   | fix          | `PropTypes.oneOf(...)` → `PropTypes.oneOfType([...])` dans `messages.content` |
| 2026-05-13   | docs         | Création de `changements.md` |
| 2026-05-18   | fix          | Restauration du `__init__.py` du package Python (perdu après clean) |
| 2026-05-18   | docs         | `changements.md` complété (fixes + historique + commandes Windows) |
