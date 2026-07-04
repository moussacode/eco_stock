# Eco-Stock API

## Description

Eco-Stock est une API REST développée avec **Django** et **Django REST Framework** permettant de gérer les entrepôts de stockage et les produits alimentaires d'une startup spécialisée dans la logistique du don alimentaire.

L'application permet de centraliser les surplus alimentaires provenant des commerces locaux afin de faciliter leur redistribution avant leur date de péremption.

Le projet a été réalisé dans le cadre d'un atelier sur Django REST Framework.

---

# Fonctionnalités

* Gestion des entrepôts (Warehouse)
* Gestion des produits (Product)
* Authentification JWT avec Simple JWT
* CRUD complet avec ModelViewSet
* Action personnalisée de transfert d'un produit entre deux entrepôts
* Action d'audit permettant d'obtenir le nombre total de produits d'un entrepôt
* Documentation interactive avec Swagger / OpenAPI

---

# Technologies utilisées

* Python 3.12
* Django 6
* Django REST Framework
* Simple JWT
* drf-spectacular (Swagger/OpenAPI)
* SQLite
* Git & GitHub

---

# Installation

## 1. Cloner le projet

```bash
git clone https://github.com/moussacode/eco_stock.git

cd eco_stock
```

---

## 2. Créer un environnement virtuel

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

---

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 4. Appliquer les migrations

```bash
python manage.py migrate
```

---

## 5. Créer un super utilisateur

```bash
python manage.py createsuperuser
```

---

## 6. Lancer le serveur

```bash
python manage.py runserver
```

Le serveur sera disponible à l'adresse :

```
http://127.0.0.1:8000/
```

---

# Authentification JWT

L'API utilise JWT (JSON Web Token).

## Obtenir un token

```
POST /api/token/
```

Exemple de requête :

```json
{
    "username": "admin",
    "password": "mot_de_passe"
}
```

Réponse :

```json
{
    "refresh": "...",
    "access": "..."
}
```

---

## Rafraîchir un token

```
POST /api/token/refresh/
```

Exemple :

```json
{
    "refresh": "..."
}
```

---

## Utiliser le token

Ajouter le token dans l'en-tête HTTP :

```
Authorization: Bearer <access_token>
```

---

# Documentation OpenAPI

Swagger UI :

```
http://127.0.0.1:8000/api/docs/
```

Schéma OpenAPI :

```
http://127.0.0.1:8000/api/schema/
```

---

# Endpoints

## Authentification

| Méthode | Endpoint            | Description                |
| ------- | ------------------- | -------------------------- |
| POST    | /api/token/         | Obtenir un Access Token    |
| POST    | /api/token/refresh/ | Rafraîchir un Access Token |

---

## Warehouses

| Méthode | Endpoint                    | Description                                       |
| ------- | --------------------------- | ------------------------------------------------- |
| GET     | /api/warehouses/            | Liste des entrepôts                               |
| POST    | /api/warehouses/            | Créer un entrepôt                                 |
| GET     | /api/warehouses/{id}/       | Détail d'un entrepôt                              |
| PUT     | /api/warehouses/{id}/       | Modifier un entrepôt                              |
| PATCH   | /api/warehouses/{id}/       | Modifier partiellement un entrepôt                |
| DELETE  | /api/warehouses/{id}/       | Supprimer un entrepôt                             |
| GET     | /api/warehouses/{id}/audit/ | Obtenir le nombre total de produits de l'entrepôt |

---

## Products

| Méthode | Endpoint                 | Description                                  |
| ------- | ------------------------ | -------------------------------------------- |
| GET     | /api/products/           | Liste des produits                           |
| POST    | /api/products/           | Créer un produit                             |
| GET     | /api/products/{id}/      | Détail d'un produit                          |
| PUT     | /api/products/{id}/      | Modifier un produit                          |
| PATCH   | /api/products/{id}/      | Modifier partiellement un produit            |
| DELETE  | /api/products/{id}/      | Supprimer un produit                         |
| POST    | /api/products/{id}/move/ | Transférer un produit vers un autre entrepôt |

---

# Modèles

## Warehouse

| Champ    | Type                 |
| -------- | -------------------- |
| name     | CharField            |
| location | CharField            |
| capacity | PositiveIntegerField |

---

## Product

| Champ           | Type                 |
| --------------- | -------------------- |
| warehouse       | ForeignKey           |
| name            | CharField            |
| quantity        | PositiveIntegerField |
| expiration_date | DateField            |
| status          | TextChoices          |

Valeurs possibles pour **status** :

* available
* reserved
* expired

---

# Règles métier

## Transfert d'un produit

Endpoint :

```
POST /api/products/{id}/move/
```

Le transfert est autorisé uniquement si :

* le produit existe ;
* le nouvel entrepôt existe ;
* le produit n'est pas périmé.

Si le produit est périmé, l'API retourne :

```
HTTP 400 Bad Request
```

---

## Audit d'un entrepôt

Endpoint :

```
GET /api/warehouses/{id}/audit/
```

Cette action retourne :

* le nom de l'entrepôt ;
* sa localisation ;
* sa capacité ;
* le nombre total de produits stockés.

L'agrégation est réalisée avec la fonction ORM `Count`.

---

# Permissions

Les routes de modification sont protégées grâce à :

```
IsAuthenticatedOrReadOnly
```

Les utilisateurs non authentifiés peuvent uniquement consulter les données.

Les utilisateurs authentifiés peuvent :

* créer ;
* modifier ;
* supprimer ;
* transférer un produit.

---

# Codes HTTP utilisés

| Code | Signification |
| ---- | ------------- |
| 200  | OK            |
| 201  | Created       |
| 204  | No Content    |
| 400  | Bad Request   |
| 401  | Unauthorized  |
| 404  | Not Found     |

---

# Structure du projet

```
eco_stock/
│
├── config/
├── inventaire/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── requirements.txt
└── README.md
```

```mermaid
flowchart TD

A[POST /api/products/{id}/move/] --> B[Récupérer le produit]

B --> C{Produit existe ?}

C -- Non --> D[404 Not Found]

C -- Oui --> E{Produit périmé ?}

E -- Oui --> F[400 Bad Request]

E -- Non --> G[Lire le nouvel entrepôt]

G --> H{Entrepôt existe ?}

H -- Non --> I[404 Not Found]

H -- Oui --> J[Changer product.warehouse]

J --> K[product.save()]

K --> L[200 OK<br/>Produit transféré]
```
---

# Auteur

Projet réalisé dans le cadre d'un atelier Django REST Framework.

Développé par **Moussa**.
