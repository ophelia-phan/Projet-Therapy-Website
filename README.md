Légende: <br/>
x : pas encore fini/ait <br/>
! : problème non résolu <br/>
~ : en cours <br/>
🗸 : fini et fonctionne <br/>

# Les Point restants à traiter pour le Projet-Therapy-Website (à actualiser régulièrement)


- configurer les Messages d'erreurs pour mail, mot de passe, confirm password (format) : x

    - ajouter un bouton lien vers le profil user si user ou profil thérapeute si thérapeute
    - Bonus : logo du site ? 

- Partie PROFIL USER.html :
    - ajouter un bouton pour permettre au user de supprimer son compte(de la base de données) : x
    - vérifier que le formulaire sur la page user.html marche (update profile datas) : x


- Partie PROFIL PRO USER_PRO.html :
    - vérifier affichage de la photo du thérapeute sur son profil : x
    - vérifier que le formulaire sur la page user_pro.html marche (update profile datas) : x
    - vérifier que le formulaire sur la page user_pro.html marche (update profil picture) : x


- Mise en forme de la page d'accueil :
    - mise en forme des témoignages "fancy way" : x
    - Block "if you need help" avec les boutons associés : x
    - image de fond d'écran du site à choisir : x
    - Titre du site web : x
    - Autres fancy things to add : ...

- Partie FORUM.html à vérifier : 
    - éventuelle mise en forme avec bootstrap (frontend)
  
- Partie THREAD.html à vérifier :
    - éventuellement fonctionnalité liker un commentaire + affichage nombre de likes (ajout d'un attribut dans la classe Comment): x


- Partie Prise de RDV à implémenter :
    - formulaire à redéfinir (revoir les questions) : x A finir 
    - insérer dans le formulaire une liste des thérapeutes disponibles à la consultation (en fonction des spécialités) : x A finir(j'ai ajouter une liste des therapeutes faut juste vir les spécialités à faire)
    - vérifier que le formulaire marche : x DONE🗸
    - vérifier après la prise d'un rdv que le rdv s'affiche sur les profils USER et THERAPEUTE : x
    - Possibilité d'annuler le rdv à implémenter (+ envoi d'un mail ? ou notification ?) : x
    - éventuellement mise en forme bootstrap avec questionnaire déroulant : x


# Les points déjà traités qui fonctionnent :

- Barre de navigation:
    - ajouter le bouton d'accès au forum si user connecté :  🗸
    - Note : quand le user est connecté, le bouton "log out" apparaît 2 fois sur la barre de nav (à changer) : 🗸

- FORUM :
    - add thread (button) : 🗸 
    - affichage des threads : 🗸
    - edit thread : 🗸 
    - delete thread : 🗸
    - ouverture du lien vers un thread sur la page : 🗸
    - ajouter un thread en NON-anonyme + Anonyme : 🗸

- THREAD :
    - ajout bouton "Retour au forum" : 🗸
    - affichage du bon thread : 🗸 
    - add comment : 🗸
    - edit comment : 🗸
    - affichage des commentaires : 🗸
    - delete comment : 🗸
    - Commentaire en NON-anonyme + Anonyme : 🗸

- barre de navigation en fonction si le user est connecté : 🗸
- créer un compte USER : 🗸
- créer un compte Thérapeute : 🗸
- se login comme User, Thérapeute + invalid information : 🗸
- affichage page d'accueil : 🗸
- création de toutes les routes : 🗸
- création de toutes les classes : 🗸


# Points bonus :
- Système de paiement avec Flask
- Système de webchat en ligne avec Flask
- Système d'envoi d'un email de rappel au user 1 jour avant son rdv ou le matin même
