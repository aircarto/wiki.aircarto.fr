# NebuleAir Pro

![Logo NebuleAir Pro](https://aircarto.fr/images/nebuleair_pro/Logo_NebuleAirPro.png)

## Présentation

Le NebuleAir Pro est la version professionnelle du capteur de qualité de l'air NebuleAir, conçu pour des déploiements en extérieur avec une connectivité cellulaire autonome.

Il est équipé d'un modem 4G **u-blox SARA-R500** qui communique sur les bandes de fréquences **NB-IoT** (Narrowband IoT), permettant une transmission des données sans dépendre d'un réseau WiFi.

## Caractéristiques techniques

### Plateforme

- **Carte mère** : Raspberry Pi Compute Module 4 (CM4)

### Capteurs intégrés de base

| Capteur | Mesure | Paramètres |
|---------|--------|------------|
| **NextPM** (Tera Sensor) | Particules fines | PM1, PM2.5, PM10 |
| **BME280** (Bosch) | Environnement | Température, humidité, pression atmosphérique |

### Capteurs optionnels

Des capteurs supplémentaires peuvent être ajoutés pour étendre les capacités de mesure :

**Sondes gaz Cairsens** (fabricant : [Envea](https://www.envea.global/)) :

- NO2 (dioxyde d'azote)
- O3 (ozone)
- Autres gaz selon les modèles Cairsens disponibles

**Sonomètre** :

- [NSRT mk4](https://convergenceinstruments.com/fr/produit/sonometre-enregistreur-avec-microphone-de-type-1-nsrt_mk4_dev/) (fabricant : Convergence Instruments) - sonomètre enregistreur avec microphone de type 1

### Connectivité

- **Modem** : u-blox SARA-R500
- **Protocole** : NB-IoT (Narrowband IoT)

### Alimentation

Le NebuleAir Pro peut être alimenté de deux manières :

- **Secteur** : alimentation filaire classique
- **Autonome** : pack batterie + panneau solaire

## Installation

L'installation du NebuleAir Pro est simple :

1. **Brancher l'appareil** au câble d'alimentation (adaptateur secteur ou batterie solaire)
2. **L'appareil démarre automatiquement** : les deux LEDs (rouge et verte) clignotent ensemble plusieurs fois
3. **Connexion au réseau mobile** : le modem se connecte automatiquement au réseau NB-IoT disponible
4. **Envoi des données** : les mesures sont transmises toutes les minutes, signalé par le clignotement de la LED verte

!!! info "Carte SIM multi-opérateur"
    La carte SIM intégrée est multi-opérateur. Le choix du réseau est entièrement automatique, aucune configuration n'est nécessaire.

### Indicateurs LED

| LED | Comportement | Signification |
|-----|-------------|---------------|
| Rouge + Verte | Clignotent ensemble | Démarrage de l'appareil |
| Verte | Clignote | Envoi des données en cours |

## Configuration

Aucune configuration n'est nécessaire au démarrage. L'appareil est pré-configuré en usine et se connecte automatiquement au réseau mobile.

## Récupération des données

Il existe deux moyens d'accéder aux données de votre capteur NebuleAir Pro.

!!! tip "Informations nécessaires"
    Le **nom du capteur** et le **token** sont inscrits sur le bon de livraison fourni avec votre capteur. Conservez-le précieusement.

### 1. Interface web MonNebuleAir

Rendez-vous sur [https://nebuleair.fr/monNebuleAir.html](https://nebuleair.fr/monNebuleAir.html) et renseignez :

- **Nom du capteur** : le nom indiqué sur le bon de livraison
- **Token** : le token associé au capteur

![Page de connexion MonNebuleAir](../assets/images/Mon NebuleAir login.png)

Vous accéderez directement à la visualisation de vos données sous forme de graphiques.

![Interface de visualisation des données MonNebuleAir](../assets/images/Mon NebuleAir data.png)

### 2. API AirCarto

Pour une récupération programmatique des données (intégration dans vos propres outils, export, etc.), utilisez l'API AirCarto :

1. Rendez-vous sur la documentation de l'API : [https://api.aircarto.fr/](https://api.aircarto.fr/)
2. Accédez à l'endpoint historique NebuleAir : [https://api.aircarto.fr/#/capteurs/historique_nebuleAir](https://api.aircarto.fr/#/capteurs/historique_nebuleAir)
3. Renseignez les informations de votre capteur (nom et token)

![Interface Swagger de l'API AirCarto](../assets/images/API screen shot .png)

#### Exemple de requête

Pour récupérer les données du capteur `nebuleair-pro142` sur les 2 dernières heures au format JSON :

```
https://api.aircarto.fr/capteurs/dataNebuleAir?capteurID=nebuleair-pro142&start=-2h&end=now&format=JSON
```

!!! warning "Fuseau horaire UTC"
    Les dates envoyées dans la requête et retournées dans la réponse sont en **UTC**. Pensez à convertir si besoin (en France, UTC+1 en hiver, UTC+2 en été).

#### Paramètres de la requête

| Paramètre | Obligatoire | Description | Exemple |
|-----------|:-----------:|-------------|---------|
| `capteurID` | oui | Identifiant du capteur | `nebuleair-pro142` |
| `start` | oui | Date de début de la période. Peut être en **valeur absolue** (date ISO 8601) ou en **relatif** (`-1h` = il y a 1 heure, `-30m` = il y a 30 minutes, `-7d` = il y a 7 jours) | `-2h`, `2026-03-12T06:00:00Z` |
| `end` | oui | Date de fin de la période. Mêmes formats que `start`, avec en plus la valeur `now` pour l'instant présent | `now`, `2026-03-12T08:00:00Z` |
| `format` | non | Format de sortie | `JSON` |
| `freq` | non | Pas de temps pour moyenner les données (intégration). Sans ce paramètre, les données brutes sont retournées (environ 1 mesure/minute) | `1h`, `1d` |

#### Exemple de réponse JSON

```json
[
  {
    "time": "2026-03-12T06:45:41Z",
    "sensorId": "nebuleair-pro142",
    "PM1": 8.3,
    "PM25": 9.2,
    "PM10": 12.4,
    "TEMP": 5.72,
    "HUM": 92.33,
    "PRESS": 987,
    "NOISE": null,
    "COV": null
  },
  {
    "time": "2026-03-12T06:46:42Z",
    "sensorId": "nebuleair-pro142",
    "PM1": 7.7,
    "PM25": 8.5,
    "PM10": 11.5,
    "TEMP": 5.72,
    "HUM": 92.33,
    "PRESS": 987,
    "NOISE": null,
    "COV": null
  },
  {
    "time": "2026-03-12T06:47:43Z",
    "sensorId": "nebuleair-pro142",
    "PM1": 9.5,
    "PM25": 10.6,
    "PM10": 14.3,
    "TEMP": 5.87,
    "HUM": 92.18,
    "PRESS": 987,
    "NOISE": null,
    "COV": null
  },
  {
    "time": "2026-03-12T06:48:43Z",
    "sensorId": "nebuleair-pro142",
    "PM1": 14.3,
    "PM25": 15.8,
    "PM10": 21.4,
    "TEMP": 5.87,
    "HUM": 92.18,
    "PRESS": 987,
    "NOISE": null,
    "COV": null
  }
]
```

| Champ | Description | Unité |
|-------|-------------|-------|
| `time` | Horodatage de la mesure | ISO 8601 (UTC) |
| `sensorId` | Identifiant du capteur | - |
| `PM1` | Particules fines PM1 | µg/m³ |
| `PM25` | Particules fines PM2.5 | µg/m³ |
| `PM10` | Particules fines PM10 | µg/m³ |
| `TEMP` | Température | °C |
| `HUM` | Humidité relative | % |
| `PRESS` | Pression atmosphérique | hPa |
| `NOISE` | Niveau sonore (si disponible) | dB |
| `COV` | Composés organiques volatils (si disponible) | ppb |
