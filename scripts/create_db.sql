-- Script SQL de création de la base de données
-- Usage: psql -U postgres -d ml_api_db -f scripts/create_db.sql

CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    age FLOAT NOT NULL,
    revenu_mensuel FLOAT NOT NULL,
    nombre_experiences_precedentes FLOAT,
    annees_dans_l_entreprise FLOAT,
    satisfaction_employee_environnement FLOAT,
    note_evaluation_precedente FLOAT,
    note_evaluation_actuelle FLOAT,
    satisfaction_employee_nature_travail FLOAT,
    satisfaction_employee_equipe FLOAT,
    satisfaction_employee_equilibre_pro_perso FLOAT,
    heure_supplementaires INTEGER,
    nombre_participation_pee FLOAT,
    nb_formations_suivies FLOAT,
    distance_domicile_travail FLOAT,
    niveau_education FLOAT,
    frequence_deplacement FLOAT,
    annees_depuis_la_derniere_promotion FLOAT,
    genre VARCHAR(10),
    departement VARCHAR(50),
    statut_marital VARCHAR(20),
    domaine_etude VARCHAR(50),
    poste VARCHAR(50),
    a_quitte_entreprise INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(id),
    input_data JSONB NOT NULL,
    prediction INTEGER NOT NULL,
    label VARCHAR(50) NOT NULL,
    probabilite_depart FLOAT NOT NULL,
    satisfaction_globale FLOAT,
    indicateur_surcharge INTEGER,
    model_version VARCHAR(20) DEFAULT '0.1.0',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index pour accélérer les requêtes
CREATE INDEX IF NOT EXISTS idx_predictions_created_at ON predictions(created_at);
CREATE INDEX IF NOT EXISTS idx_predictions_prediction ON predictions(prediction);
CREATE INDEX IF NOT EXISTS idx_employees_departement ON employees(departement);
