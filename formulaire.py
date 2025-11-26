def afficher_titre():
    """Affiche le titre du formulaire"""
    print("=" * 40)
    print("FORMULAIRE D'INSCRIPTION")
    print("=" * 40)
    print()

def demander_nom():
    """Demande le nom de l'utilisateur"""
    while True:
        nom = input("Entrez votre nom : ").strip()
        if nom != "":
            return nom
        print("❌ Le nom ne peut pas être vide. Réessayez.")

def demander_prenom():
    """Demande le prénom de l'utilisateur"""
    while True:
        prenom = input("Entrez votre prénom : ").strip()
        if prenom != "":
            return prenom
        print("❌ Le prénom ne peut pas être vide. Réessayez.")

def demander_age():
    """Demande l'âge de l'utilisateur"""
    while True:
        age = input("Entrez votre âge : ").strip()
        if age != "" and age.isdigit():
            return age
        print("❌ L'âge doit être un nombre valide. Réessayez.")

def demander_email():
    """Demande l'email de l'utilisateur"""
    while True:
        email = input("Entrez votre email : ").strip()
        if email != "":
            return email
        print("❌ L'email ne peut pas être vide. Réessayez.")

def afficher_resume(nom, prenom, age, email):
    """Affiche un résumé des informations saisies"""
    print()
    print("=" * 40)
    print("RÉSUMÉ DE VOS INFORMATIONS")
    print("=" * 40)
    print(f"Nom : {nom}")
    print(f"Prénom : {prenom}")
    print(f"Âge : {age}")
    print(f"Email : {email}")
    print("=" * 40)
    print("✅ Formulaire complété avec succès!")

def main():
    """Fonction principale qui gère le formulaire"""
    afficher_titre()
    
    nom = demander_nom()
    prenom = demander_prenom()
    age = demander_age()
    email = demander_email()
    
    afficher_resume(nom, prenom, age, email)

# Lancer le programme
if __name__ == "__main__":
    main()
