import math
import csv

def lambert93_to_wgs84(x, y):
    """
    Convertit des coordonnées Lambert-93 en WGS84.
    
    :param x: Coordonnée X en Lambert-93.
    :param y: Coordonnée Y en Lambert-93.
    :return: Latitude et longitude en WGS84.
    """
    # Paramètres du système Lambert-93
    e = 0.0818191910428158  # Excentricité de l'ellipsoïde
    n = 0.7256077650532670  # Facteur d'échelle
    C = 11754255.426096     # Constante C
    xs = 700000.0           # Coordonnée X de référence
    ys = 12655612.049876    # Coordonnée Y de référence
    lon_0 = 3.0             # Méridien central en degrés

    # Calcul de la distance et de l'angle
    R = math.sqrt((x - xs)**2 + (y - ys)**2)
    gamma = math.atan((x - xs) / (ys - y))

    # Conversion en latitude
    lat_iso = -1.0 / n * math.log(abs(R / C))
    phi = 2 * math.atan(math.exp(lat_iso)) - math.pi / 2
    
    # Amélioration de la précision par itération
    for _ in range(10):
        phi = 2 * math.atan(
            ((1 + e * math.sin(phi)) / (1 - e * math.sin(phi))) ** (e / 2)
            * math.exp(lat_iso)
        ) - math.pi / 2

    # Calcul de la longitude
    lambda_radians = gamma / n + (lon_0 * math.pi / 180.0)

    # Conversion en degrés
    latitude = phi * 180.0 / math.pi
    longitude = lambda_radians * 180.0 / math.pi

    return latitude, longitude


def main():
    """
    Lit un fichier CSV contenant des coordonnées Lambert-93,
    les convertit en WGS84 et enregistre les résultats dans un nouveau fichier CSV.
    """
    # Demande à l'utilisateur le nom du fichier CSV
    csv_file_in = input("Nom du fichier CSV contenant les coordonnées Lambert-93 : ")
    csv_file_out = csv_file_in + "_WGS84.csv"  # Création du nom du fichier de sortie

    try:
        # Ouvre le fichier CSV en lecture
        with open(csv_file_in, mode="r", newline="", encoding="utf-8") as f_in:
            reader = csv.DictReader(f_in, delimiter=";")  # Lecture du CSV avec séparateur ";"
            fieldnames = reader.fieldnames  # Récupération des noms de colonnes

            # Sélectionne les colonnes utiles
            filtered_fieldnames = [name for name in fieldnames if name and name.strip()]
            output_fieldnames = filtered_fieldnames + ["latitude_wgs84", "longitude_wgs84"]

            # Définit les colonnes X et Y
            x_col_name = fieldnames[0]
            y_col_name = fieldnames[1]

            # Ouvre le fichier CSV en écriture
            with open(csv_file_out, mode="w", newline="", encoding="utf-8") as f_out:
                writer = csv.DictWriter(f_out, fieldnames=output_fieldnames, delimiter=";")
                writer.writeheader()  # Écrit l'en-tête du fichier

                # Convertit chaque ligne du fichier d'entrée
                for row in reader:
                    try:
                        # Récupère X et Y et les convertit en nombres
                        x_val = float(row[x_col_name].replace(",", "."))
                        y_val = float(row[y_col_name].replace(",", "."))

                        # Conversion en WGS84
                        lat, lon = lambert93_to_wgs84(x_val, y_val)

                        # Ajoute les nouvelles coordonnées au fichier
                        row["latitude_wgs84"] = lat
                        row["longitude_wgs84"] = lon
                        writer.writerow(row)

                    except (ValueError, KeyError):
                        # Ignore les lignes avec des données invalides
                        continue

        print(f"Conversion terminée ! Fichier créé : {csv_file_out}")

    except FileNotFoundError:
        print(f"Le fichier {csv_file_in} est introuvable.")
    except Exception as e:
        print(f"Erreur : {e}")


if __name__ == "__main__":
    main()
