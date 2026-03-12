# NebuleAir WiFi

![Logo NebuleAir](https://aircarto.fr/images/NebuleAir/LogoNebuleAir.png)

## Présentation

Le NebuleAir WiFi est un capteur de qualité de l'air connecté en WiFi.

## Caractéristiques

- **Microcontrôleur** : ESP32
- **Capteur de particules fines** : NextPM (fabricant : Tera Sensor) - mesure des PM1, PM2.5 et PM10

## Configuration WiFi

Au démarrage, le capteur crée un réseau WiFi temporaire pour permettre sa configuration.

1. **Connectez-vous au réseau WiFi** du capteur :
    - Nom du réseau : `nebuleair-xxxxx`
    - Mot de passe : `nebuleaircfg`

    !!! warning "Réseau temporaire"
        Ce réseau n'est actif que quelques minutes après le démarrage du capteur.

2. **Accédez à la page de configuration** en ouvrant votre navigateur à l'adresse : [http://192.168.4.1/](http://192.168.4.1/)

    ![Page de configuration WiFi](https://nebuleair.fr/img/config1.PNG)

3. **Sélectionnez votre réseau WiFi domestique** et entrez le mot de passe
4. Cliquez sur **Sauvegarder et redémarrer**
5. Le capteur redémarre et se connecte à votre réseau WiFi. Le réseau `nebuleair-xxxxx` disparaît.

### Accès aux données

Une fois connecté, rendez-vous sur [Mon NebuleAir](https://nebuleair.fr/monNebuleAir.html) avec :

- Le **nom du capteur** et le **token** gravés sur le plexiglass de l'appareil

### Géolocalisation

Depuis l'interface Mon NebuleAir, géolocalisez votre capteur via l'onglet dédié :

- Entrez une adresse ou déplacez manuellement le marqueur sur la carte
- Validez la localisation pour que le capteur apparaisse sur [OpenAirMap](https://openairmap.fr)

## Installation

Le NebuleAir WiFi peut être fixé de deux manières à l'aide de colliers de serrage :

### Fixation horizontale

Utilisez deux colliers de serrage sur les attaches latérales (haut droit et haut gauche).

![Fixation horizontale](https://nebuleair.fr/img/nebuleAirFixation_horizontale.jpg)

### Fixation verticale

Utilisez deux colliers de serrage sur les attaches centrales.

![Fixation verticale](https://nebuleair.fr/img/nebuleAirFixation_verticale.jpg)
