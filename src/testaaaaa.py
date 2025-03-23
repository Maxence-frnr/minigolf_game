import numpy as np

def projection_orthogonale(P, S1, S2):
    """Projette le point P sur le segment [S1, S2]"""
    S1, S2, P = np.array(S1), np.array(S2), np.array(P)
    segment = S2 - S1
    projection = S1 + np.dot(P - S1, segment) / np.dot(segment, segment) * segment
    # Vérifier si P' est sur le segment
    t = np.dot(P - S1, segment) / np.dot(segment, segment)
    if 0 <= t <= 1:
        return projection
    else:
        return None  # Projection hors du segment

def distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def detect_collision_face(P, r, rectangle):
    """
    Détecte avec quelle face du rectangle (A, B, C, D) la boule P (rayon r) a collisionné.
    rectangle = [A, B, C, D]
    """
    faces = [("AB", rectangle[0], rectangle[1]), 
             ("BC", rectangle[1], rectangle[2]), 
             ("CD", rectangle[2], rectangle[3]), 
             ("DA", rectangle[3], rectangle[0])]

    closest_face = None
    min_distance = float('inf')

    for name, S1, S2 in faces:
        P_proj = projection_orthogonale(P, S1, S2)
        if P_proj is not None:
            d = distance(P, P_proj)
            if d <= r and d < min_distance:
                min_distance = d
                closest_face = (name, S1, S2)

    # Vérification des sommets si aucune arête détectée
    if closest_face is None:
        for i, vertex in enumerate(rectangle):
            d = distance(P, vertex)
            if d <= r:
                return f"Collision avec le sommet {chr(65+i)}"

    return f"Collision avec la face {closest_face[0]}" if closest_face else "Pas de collision"

# Exemple d'utilisation
rectangle = [(144.199, 103.349), (230.801, 53.3494), (255.801, 96.6506), (169.199, 146.651)]  # Rectangle ABCD
P = (200, 140)  # Centre de la boule
r = 10  # Rayon de la boule
print(detect_collision_face(P, r, rectangle))
