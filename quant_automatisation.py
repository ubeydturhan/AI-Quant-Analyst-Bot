# Auteur : Ubeyd TURHAN - 2026
import os
import requests
import yfinance as yf
from bs4 import BeautifulSoup
import time

print("[SYSTEM] Chargement de l'Outil d'Analyse Quant (Version Hybride)...")

# ==========================================
# OUTIL 1 : La Calculatrice de Prix 
# ==========================================
def analyser_prix(ticker):
    print(f"📈 [1/4] Calcul de la tendance des prix pour {ticker}...")
    action = yf.Ticker(ticker)
    historique = action.history(period="7d")
    
    # Le filtre anti-bug (NaN) : on supprime les lignes vides
    historique = historique.dropna()
    
    if historique.empty:
        return f"Impossible de récupérer le prix de {ticker}."
    
    prix_ancien = historique['Close'].iloc[0]
    prix_actuel = historique['Close'].iloc[-1]
    variation_pct = ((prix_actuel - prix_ancien) / prix_ancien) * 100
    
    symbole = "🟢 HAUSSE" if variation_pct > 0 else "🔴 BAISSE"
    
    return f"Le prix actuel de {ticker} est de {round(prix_actuel, 2)} $. Sur les 7 derniers jours, l'action est en {symbole} de {round(variation_pct, 2)} %."

# ==========================================
# OUTIL 2 : L'Agent Textuel 
# ==========================================
# 💡 NOUVEAU : La fonction prend maintenant la tendance_prix en plus du ticker !
def analyser_action(ticker, tendance_prix):
    print(f" [2/4] Récupération des news pour {ticker}...")
    action = yf.Ticker(ticker)
    articles = action.news
    news_texte = ""
    
    headers_web = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36'}

    print(f" [3/4] Aspiration des articles complets pour {ticker}...")
    for i in range(min(3, len(articles))):
        titre = articles[i].get('title') or 'Titre inconnu'
        
        contenu = articles[i].get('content') or {}
        dossier_click = contenu.get('clickThroughUrl') or {}
        dossier_canon = contenu.get('canonicalUrl') or {}
        lien = dossier_click.get('url') or dossier_canon.get('url')
        
        texte_article = "Texte introuvable."
        if lien:
            try:
                reponse_web = requests.get(lien, headers=headers_web, timeout=5)
                soup = BeautifulSoup(reponse_web.text, 'html.parser')
                paragraphes = soup.find_all('p')
                texte_brut = " ".join([p.text for p in paragraphes])
                texte_article = texte_brut[:2500] # RETOUR À 2500 CARACTÈRES !
            except:
                texte_article = "Erreur lors de l'aspiration."

        news_texte += f"--- ARTICLE {i+1} ---\nTITRE: {titre}\nCONTENU: {texte_article}\n\n"

    print(f" [4/4] Analyse IA (Fusion Prix + News) en cours pour {ticker}...")
    api_key = os.getenv("KIMI_API_KEY")
    url = "https://api.moonshot.cn/v1/chat/completions"
    headers_api = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


    prompt_utilisateur = f"""
    CONTEXTE MATHÉMATIQUE (PRIX SUR 7 JOURS) :
    {tendance_prix}

    ACTUALITÉS FONDAMENTALES (3 DERNIERS ARTICLES) :
    {news_texte}

    INSTRUCTIONS D'ANALYSE QUANTITATIVE :
    Tu n'es plus un simple journaliste neutre, tu es un chasseur d'anomalies de marché. 
    1. Filtre le bruit : Ignore la macro-économie globale (guerres, taux d'intérêt, inflation) si ça ne touche pas DIRECTEMENT les fondamentaux de {ticker}.
    2. Analyse la valeur intrinsèque : Les news montrent-elles une entreprise solide (produits, croissance) ou en danger ?
    3. Traque le décalage (L'Alpha) : 
       - Si le prix baisse mais que les fondamentaux sont excellents -> C'est une OPPORTUNITÉ D'ACHAT (Sous-évalué).
       - Si le prix monte mais que les news sont mauvaises -> C'est un RISQUE DE BULLE (Surévalué).
       - Si le prix et les news sont alignés -> La tendance est JUSTIFIÉE.

    Rédige ton rapport en 3 points courts (Fondamentaux, Analyse du décalage, Verdict final avec recommandation claire : Achat Fort, Achat, Conserver, Vendre).
    """

    data = {
        "model": "moonshot-v1-8k",
        "messages": [
            {"role": "system", "content": "Tu es le trader Quant en chef d'un hedge fund agressif. Tu cherches les anomalies entre le prix du marché et la vraie valeur de l'entreprise. Tu réponds UNIQUEMENT en français, de manière tranchante et directe."},
            {"role": "user", "content": prompt_utilisateur}
        ],
        "temperature": 0.3 # On augmente un TOUT PETIT PEU la température pour lui donner une once de libre arbitre d'investissement
    }

    max_essais = 3
    for essai in range(max_essais):
        reponse = requests.post(url, headers=headers_api, json=data)
        
        if reponse.status_code == 200:
            return reponse.json()['choices'][0]['message']['content']
        elif reponse.status_code == 429:
            print(f"    Le cerveau de Kimi surchauffe... Pause de 20 secondes (Tentative {essai + 1}/{max_essais})")
            time.sleep(20)
        else:
            return f"[ERROR] Erreur API : {reponse.status_code}\nExplication : {reponse.text}"
            
    return "[ERROR] Abandon : Le serveur de Kimi est totalement K.O aujourd'hui."

# ==========================================
# LE GRAND TEST (Automatisation)
# ==========================================
if __name__ == "__main__":
    mon_portefeuille = ["MSFT", "AAPL", "NVDA"]

    print("\n [INFO] LANCEMENT DE L'ANALYSE DU PORTEFEUILLE...")

    for ticker in mon_portefeuille:
        # 1. On calcule le prix
        tendance_prix = analyser_prix(ticker)
        
        # 2. On envoie LE PRIX ET LE TICKER à Kimi
        verdict = analyser_action(ticker, tendance_prix)
    
        print("\n" + "="*50)
        print(f"📊 RAPPORT OFFICIEL : {ticker}")
        print("="*50)
        print(verdict)
        print("="*50 + "\n")
    
        print("⏳ Pause de 12 secondes pour ne pas froisser le serveur Kimi...")
        time.sleep(12)
    
    print("✅ TOUT LE PORTEFEUILLE A ÉTÉ ANALYSÉ AVEC SUCCÈS !")