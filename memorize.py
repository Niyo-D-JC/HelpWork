import time
import json
import os
import pickle


PICKLE_DIR = 'pickle_cache'

# Créer le répertoire pour les fichiers pickle s'il n'existe pas
if not os.path.exists(PICKLE_DIR):
    os.makedirs(PICKLE_DIR)

def save_result(key, result):
    pickle_path = os.path.join(PICKLE_DIR, f"{key}.pkl")
    with open(pickle_path, 'wb') as f:
        pickle.dump(result, f)
    return pickle_path

def load_result(pickle_path):
    with open(pickle_path, 'rb') as f:
        return pickle.load(f)

def memoize(func):
    def wrapper(*args):
        # Créer une clé unique basée sur le nom de la fonction et les arguments
        key = f"{func.__name__}-{str(args)}"
        pickle_path = os.path.join(PICKLE_DIR, f"{key}.pkl")
        if os.path.exists(pickle_path):
            # Charger le résultat depuis le fichier pickle si disponible
            
            return load_result(pickle_path)
        else:
            # Sinon, exécuter la fonction et enregistrer le résultat
            result = func(*args)
            save_result(key, result)
            return result
    return wrapper


def memoize_self(exclude_args=None):
    if exclude_args is None:
        exclude_args = []

    def decorator(func):
        def wrapper(self, *args):
            # Exclure les arguments spécifiés de la clé
            filtered_args = tuple(arg for i, arg in enumerate(args) if i not in exclude_args)
            key = f"{self.__class__.__name__}-{func.__name__}-{str(filtered_args)}"
            if os.path.exists(pickle_path):
            # Charger le résultat depuis le fichier pickle si disponible
                return load_result(pickle_path)
            else:
                # Sinon, exécuter la fonction et enregistrer le résultat
                result = func(self, *args)
                save_result(key, result)
                return result
        return wrapper
    return decorator