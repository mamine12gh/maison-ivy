# -*- coding: utf-8 -*-
import sys
from common import *
from content_analyse import CRITERIA, PARTS, C, total

MOCKUP_URL = "https://claude.ai/artifact/QZkYRYDgmFcEyFKdrbbq9S"
SHOTS = sys.argv[1] if len(sys.argv) > 1 else ""
PAGES = {}  # rempli au 2e passage : id -> page
if len(sys.argv) > 2 and sys.argv[2]:
    import json; PAGES = json.load(open(sys.argv[2]))

OBJ = {"id": ("Identité", "#1E1B2E"), "moi": ("C'est pour moi ?", "#FF5A36"), "crois": ("Je te crois ?", "#2F5BEA"),
       "prix": ("Ça vaut le prix ?", "#E0A800"), "risque": ("Et si ça foire ?", "#1E8A5E"), "action": ("Comment j'achète ?", "#B23A8C")}

def winner(c):
    t = [total(o["scores"]) for o in c["options"]]
    return t.index(max(t)), t

def flow_svg():
    plan = [("1", "Bandeau, logo", "id"), ("2", "Titre et accroche", "moi"), ("3", "Galerie produit", "moi"), ("4", "Preuve et prix", "prix"),
            ("5", "Comment ça marche + bénéfices", "crois"), ("6", "Choix du pack", "prix"), ("7", "Bouton d'achat", "action"),
            ("8", "Galerie d'idées", "moi"), ("9", "Pourquoi c'est différent", "crois"), ("10", "Émotion et moments", "moi"),
            ("11", "Témoignages", "crois"), ("12", "Avis", "crois"), ("13", "FAQ + barre fixe", "risque")]
    fin = [("S0", "Bandeau d'annonce", "id"), ("S1", "En-tête", "id"), ("S2", "Hero + galerie produit", "moi"), ("S3", "Bande de chiffres", "crois"),
           ("S4", "Comment ça marche", "crois"), ("S5", "Galerie d'idées", "moi"), ("S6", "Bénéfices + vue éclatée", "crois"),
           ("S7", "Offre : packs + achat", "prix"), ("S8", "Pourquoi c'est différent", "crois"), ("S9", "Émotion et moments", "moi"),
           ("S10", "Témoignages", "crois"), ("S11", "Avis", "crois"), ("S12", "Promesse 30 jours", "risque"), ("S13", "FAQ", "risque"),
           ("S14", "Dernier appel", "action"), ("S15", "Pied de page", "id")]
    links = [(0, 0), (0, 1), (1, 2), (2, 2), (3, 7), (4, 4), (4, 6), (5, 7), (6, 7), (7, 5), (8, 8), (9, 9), (10, 10), (11, 11), (12, 13)]
    new = {3, 12, 14}
    W, rh, top = 178, 7.6, 10
    H = top + rh * len(fin) + 4
    lx, rx, bw = 0, 106, 72
    o = [f'<svg viewBox="0 0 {W} {H}" width="{W}mm" height="{H}mm" xmlns="http://www.w3.org/2000/svg" font-family="Nunito" font-size="3.1">']
    o.append(f'<text x="{lx}" y="5" font-family="Fredoka" font-weight="600" font-size="3.8" fill="#5F5870">Plan initial (13 blocs Al-Raha)</text>')
    o.append(f'<text x="{rx}" y="5" font-family="Fredoka" font-weight="600" font-size="3.8" fill="#1E1B2E">Proposition finale (16 sections)</text>')
    py = lambda i: top + i * rh * len(fin) / len(plan)
    fy = lambda i: top + i * rh
    for a, b in links:
        y1, y2 = py(a) + 2.8, fy(b) + 2.8
        moved = abs(a - b) > 1 and not (a == 4 and b in (4, 6))
        col = "#E8431F" if moved else "#CFC6D8"
        o.append(f'<path d="M{lx+bw} {y1} C {lx+bw+16} {y1}, {rx-16} {y2}, {rx} {y2}" fill="none" stroke="{col}" stroke-width="{0.7 if moved else 0.45}"/>')
    for i, (n, lab, ob) in enumerate(plan):
        y = py(i)
        o.append(f'<rect x="{lx}" y="{y}" width="{bw}" height="5.6" rx="1.4" fill="#F7F1EA"/><circle cx="{lx+3}" cy="{y+2.8}" r="1.5" fill="{OBJ[ob][1]}"/>')
        o.append(f'<text x="{lx+6}" y="{y+3.9}" fill="#5F5870"><tspan font-weight="800">{n}</tspan>  {e(lab)}</text>')
    for i, (n, lab, ob) in enumerate(fin):
        y = fy(i)
        fill = "#FFF3C9" if i in new else "#FFFFFF"
        o.append(f'<rect x="{rx}" y="{y}" width="{bw}" height="5.6" rx="1.4" fill="{fill}" stroke="#EADFD2" stroke-width=".3"/><circle cx="{rx+3}" cy="{y+2.8}" r="1.5" fill="{OBJ[ob][1]}"/>')
        o.append(f'<text x="{rx+6}" y="{y+3.9}" fill="#1E1B2E"><tspan font-weight="800">{n}</tspan>  {e(lab)}</text>')
        if i in new:
            o.append(f'<text x="{rx+bw-1.5}" y="{y+3.9}" text-anchor="end" font-weight="900" font-size="2.6" fill="#E8431F">NOUVEAU</text>')
    o.append("</svg>")
    leg = " ".join(f'<span class="pill" style="background:{c};color:{"#1E1B2E" if k=="prix" else "#fff"}">{e(l)}</span>' for k, (l, c) in OBJ.items())
    return "".join(o), leg

def comp_html(c):
    wi, t = winner(c)
    letters = "ABC"
    head = "".join(f'<th style="{"background:#E8431F" if i==wi else ""}">Option {letters[i]}{" · retenue" if i==wi else ""}<br><span style="font-family:Fredoka;font-size:10pt;font-weight:600">{e(o["name"])}</span></th>' for i, o in enumerate(c["options"]))
    def row(label, key):
        cells = "".join(f'<td style="{"background:#FFF1EC" if i==wi else ""}">{e(o[key])}</td>' for i, o in enumerate(c["options"]))
        return f'<tr><td style="font-weight:800;background:#FBF4EC">{label}</td>{cells}</tr>'
    rows = row("Ce que c'est", "desc") + row("Forces", "plus") + row("Faiblesses", "minus") + row("Pertinence", "pert")
    sc = ""
    for k, (name, w, _) in enumerate(CRITERIA):
        cells = "".join(f'<td class="num" style="{"background:#FFF1EC" if i==wi else ""}">{"●"*o["scores"][k]}<span style="color:#DDD3C6">{"●"*(5-o["scores"][k])}</span></td>' for i, o in enumerate(c["options"]))
        sc += f'<tr><td style="background:#FBF4EC">{name} <span class="muted">({w} %)</span></td>{cells}</tr>'
    tot = "".join(f'<td class="num" style="font-family:Fredoka;font-size:12pt;font-weight:700;{"background:#E8431F;color:#fff" if i==wi else ""}">{v}/100</td>' for i, v in enumerate(t))
    sc += f'<tr><td style="font-weight:900;background:#FBF4EC">Score pondéré</td>{tot}</tr>'
    princ = "".join(f"<li>{e(p)}</li>" for p in c["principles"])
    test = f'<p class="test"><b>À tester ensuite :</b> {e(c["test"])}</p>' if c["test"] else ""
    srt = sorted(t, reverse=True)
    return f'''<div class="comp" id="c-{c["id"]}">
<h3><span class="mk">§c-{c["id"]}§</span><span class="pill i">{c["id"]}</span> {e(c["title"])} <span class="muted small" style="font-family:Nunito;font-weight:700">· {e(c["objection"])}</span></h3>
<ul class="small muted" style="margin-bottom:1.5mm">{princ}</ul>
<table class="opts"><colgroup><col style="width:17%"><col style="width:27.6%"><col style="width:27.6%"><col style="width:27.6%"></colgroup>
<thead><tr><th>Critère</th>{head}</tr></thead><tbody>{rows}{sc}</tbody></table>
<p><b>Analyse comparative.</b> {e(c["analysis"])} <span class="muted">Écart avec la 2e option : {srt[0]-srt[1]} points.</span></p>
<div class="decision"><span class="lab">Décision</span><span>{e(c["decision"])}</span></div>{test}</div>'''

def build():
    b = []
    b.append(cover("Analyse des options · Landing page", "Bobiko : 36 décisions pour une page qui convertit",
                   "Trois options par élément, comparées et notées, jusqu'à la proposition finale",
                   "Préparé le 12 octobre 2026 pour la boutique Shopify Maison Ivy.<br>Suite du « Plan de landing page · Imprimante à stickers vocale » (11/10/2026).<br>Maquette interactive : " + MOCKUP_URL))
    # sommaire
    toc = [("part", "Lire ce document", None), ("", "1. L'essentiel en une page", "ess"), ("", "2. La méthode d'évaluation", "meth"),
           ("", "3. Tableau de synthèse des 36 décisions", "synth")]
    for code, name, _ in PARTS:
        toc.append(("part", f"Partie {code} · {name}", None))
        for c in C:
            if c["part"] == code:
                toc.append(("", f'{c["id"]} · {c["title"]}', "c-" + c["id"]))
    toc += [("part", "Conclusion", None), ("", "4. Ce qui change par rapport au plan", "diff"), ("", "5. Contrôle final : grille 10/10 et 12 règles", "ctrl"),
            ("", "6. Tests A/B et indicateurs", "ab"), ("", "7. La maquette en images", "shots")]
    rows = ""
    for kind, name, anchor in toc:
        if kind == "part":
            rows += f'<tr class="part"><td colspan="2">{e(name)}</td></tr>'
        else:
            rows += f'<tr><td><a href="#{anchor}">{e(name)}</a></td><td class="pg">{PAGES.get(anchor, "")}</td></tr>'
    b.append(f'<section class="chapter"><h1>Sommaire</h1><table class="toc">{rows}</table></section>')

    # essentiel
    wins = [(c, winner(c)) for c in C]
    b.append(f'''<section class="chapter" id="ess"><p class="kicker">1</p><h1>L'essentiel en une page</h1>
<p class="lead">Ce document applique le plan du 11 octobre à chaque élément de la landing. Pour chacun, trois options réalistes sont décrites, notées sur cinq critères pondérés par leur effet sur la conversion, puis comparées. L'option qui gagne devient la proposition finale, décrite en détail dans le second document (« Proposition finale ») et construite dans la maquette interactive.</p>
<div class="grid3" style="margin:4mm 0">
<div class="box ink" style="margin:0"><p style="font-family:Fredoka;font-size:22pt;font-weight:700;color:#FFC83D;margin:0">36</p><p>éléments décidés, de l'identité à la barre fixe</p></div>
<div class="box ink" style="margin:0"><p style="font-family:Fredoka;font-size:22pt;font-weight:700;color:#FFC83D;margin:0">108</p><p>options comparées sur 5 critères</p></div>
<div class="box ink" style="margin:0"><p style="font-family:Fredoka;font-size:22pt;font-weight:700;color:#FFC83D;margin:0">{round(sum(max(t) for _, (_, t) in wins)/len(wins))}/100</p><p>score moyen des options retenues</p></div></div>
<h2>Les 8 décisions qui pèsent le plus</h2>
{table(["Décision", "Retenu", "Pourquoi ça convertit"], [
 ["Nom", "<b>Bobiko</b> (bobiko.fr libre)", "Profil sonore idéal (B→K, sons ronds) ; papoto.com et papoto.fr déjà pris : risque juridique écarté."],
 ["Titre", "<b>« S'il peut le dire, ça l'imprime. »</b>", "Mot pour mot l'accroche des pubs : le visiteur sait en 1 seconde qu'il est au bon endroit."],
 ["Média du hero", "<b>Vidéo muette 8 s</b>, poster photo action", "Montre le sticker qui sort (preuve sensorielle) sans risque de chargement."],
 ["Ordre des blocs", "<b>Montrer avant de vendre</b>", "Galerie d'idées remontée en 4e position : l'angle est prouvé avant qu'on parle d'argent."],
 ["Packs", "<b>79 / 99 / 149 €</b>, Créatif présélectionné", "Effet de compromis : le pack du milieu devient l'évidence ; chiffre de gauche bas."],
 ["Économie affichée", "<b>Valeur des éléments séparés</b>", "Ancrage aussi fort qu'un prix barré, mais vrai et légal (directive Omnibus)."],
 ["Inversion du risque", "<b>« Essayez-le 30 jours »</b>", "Transforme l'achat en essai ; répond au dernier doute avant la FAQ."],
 ["Urgence", "<b>Date limite réelle de Noël</b>", "La seule urgence honnête de la saison ; aucun faux minuteur."],
], widths=["18%", "30%", "52%"])}
<div class="box blue"><b>Comment lire la suite.</b> Chaque fiche suit le même ordre : les principes du plan qui s'appliquent, le tableau des trois options (description, forces, faiblesses, pertinence, puis les scores), l'analyse comparative, la décision et, si utile, le test A/B à lancer ensuite. La colonne orange est toujours l'option retenue.</div>
</section>''')

    # méthode
    crit_rows = [[f"<b>{n}</b>", f"{w} %", e(d)] for n, w, d in CRITERIA]
    svg, leg = flow_svg()
    b.append(f'''<section class="chapter" id="meth"><p class="kicker">2</p><h1>La méthode d'évaluation</h1>
<p>Chaque option reçoit une note de 1 à 5 sur cinq critères. Les poids traduisent la consigne : <b>chaque décision doit servir le taux de conversion</b>. La conversion directe pèse donc le plus ; la confiance vient ensuite parce qu'une vente obtenue par un artifice revient en retour, en litige ou en refus publicitaire.</p>
{table(["Critère", "Poids", "Ce qu'on mesure"], crit_rows, widths=["20%", "10%", "70%"])}
<figure>{hbars([(n, w) for n, w, _ in CRITERIA], maxv=40, unit=" %", w=150, label_w=30)}<figcaption><b>Figure 1.</b> Poids des critères. Score pondéré = somme (note × poids) ÷ 5, sur 100.</figcaption></figure>
<h2>Les sources des principes</h2>
<ul><li><b>Le plan du 11/10/2026</b> : ses 12 règles d'or, ses 13 blocs, sa grille de contrôle et ses recommandations de marque.</li>
<li><b>Les guides Kolenda</b> cités dans le plan (Copywriting, E-commerce, Pricing, UX, Visual Attention, Color, Fonts, Brand Names, Advertising, Packaging).</li>
<li><b>La méthode Al-Raha</b> : la page suit l'ordre des 5 objections, et ses erreurs à ne pas reproduire.</li>
<li><b>Le droit applicable</b> : directive Omnibus (prix barrés), normes jouets, RGPD (voix d'enfants), règles publicitaires Meta.</li></ul>
<h2>La page suit les objections</h2>
<p>Le schéma compare l'ordre du plan et l'ordre retenu. Les liens orange signalent les blocs qui ont changé de place ; les cases jaunes, les sections ajoutées.</p>
<figure>{svg}<figcaption><b>Figure 2.</b> Du plan à la proposition finale. Couleur du point = objection levée : {leg}</figcaption></figure>
<div class="box cream"><b>Limites.</b> Les notes sont des jugements d'expert fondés sur les sources ci-dessus, pas des mesures. Elles servent à décider vite et de façon cohérente ; les tests A/B de la partie 6 les confronteront aux chiffres réels. Quand deux options sont proches (moins de 5 points), la fiche le signale et propose un test.</div>
</section>''')

    # synthèse
    srows = []
    for c, (wi, t) in wins:
        s = sorted(t, reverse=True)
        srows.append([f'<b>{c["id"]}</b>', e(c["title"]), e(c["options"][wi]["name"]), f"{max(t)}", f"+{s[0]-s[1]}"])
    b.append(f'''<section class="chapter" id="synth"><p class="kicker">3</p><h1>Tableau de synthèse des 36 décisions</h1>
<p>Une ligne par élément : l'option retenue, son score et son avance sur la deuxième. Une avance faible indique un test A/B prioritaire.</p>
{table(["ID", "Élément", "Option retenue", "Score", "Avance"], srows, widths=["8%", "30%", "44%", "9%", "9%"], num_cols=(3, 4))}
</section>''')

    for code, name, intro in PARTS:
        b.append(f'<section class="chapter"><p class="kicker">Partie {code}</p><h1>{e(name)}</h1><p class="lead">{e(intro)}</p>')
        for c in C:
            if c["part"] == code:
                b.append(comp_html(c))
        b.append("</section>")

    # différences
    b.append(f'''<section class="chapter" id="diff"><p class="kicker">4</p><h1>Ce qui change par rapport au plan</h1>
<p>L'analyse confirme l'essentiel du plan. Six points s'en écartent, chaque fois pour une raison de conversion ou de conformité.</p>
{table(["Sujet", "Le plan disait", "La proposition finale", "Pourquoi"], [
 ["Nom", "[MARQUE] à choisir parmi 5 pistes", "<b>Bobiko</b>", "Meilleur profil sonore libre ; Papoto déjà déposé en .com et .fr."],
 ["Ordre", "Galerie d'idées en 8e bloc, prix en 4e", "Galerie d'idées en 4e section, offre en 7e", "Prouver l'angle avant de parler d'argent."],
 ["Pack présélectionné", "Kit Fratrie (2 machines, 149 €)", "Kit Créatif (1 machine, 99 €)", "La plupart des familles achètent une machine ; l'effet de compromis favorise le milieu."],
 ["Pack haut", "Kit Créatif à 109 €", "Kit Créatif à 99 €, Fratrie en ancre haute", "Rester sous 100 € ; écart de 20 € seulement avec l'entrée."],
 ["Prix barré", "Prix barré réel, au plus 1,3 à 1,5 fois", "Valeur des éléments vendus séparément", "Au lancement il n'existe pas de prix antérieur : un prix barré serait illégal (Omnibus)."],
 ["Sections ajoutées", "—", "Bande de chiffres, promesse 30 jours, dernier appel", "Preuve concrète tôt, inversion du risque, fin de défilement justifiée."],
], widths=["15%", "25%", "27%", "33%"])}
</section>''')

    # contrôle
    grid = [["1", "Titre = bénéfice concret", "« S'il peut le dire, ça l'imprime. » + sous-titre geste"],
            ["2", "Image n°1 = produit en usage", "Vidéo 8 s, poster photo action (IMG-01/02)"],
            ["3", "Avis cohérents, dont un nuancé", "Un seul nombre d'avis partout ; avis 4★ « seul bémol »"],
            ["4", "Prix mis en scène", "« Seulement 99 € », valeur des éléments, économie, assurances dessous"],
            ["5", "Remise crédible", "Économie = somme réelle des éléments vendus seuls (1,36×)"],
            ["6", "Pack recommandé présélectionné", "Kit Créatif coché, badge « Notre recommandation »"],
            ["7", "3 bénéfices + mécanisme", "S6 : « … grâce à … » ×3 + vue éclatée"],
            ["8", "Zéro fausse urgence", "Seulement la date limite réelle de Noël"],
            ["9", "Bouton à la 1re personne, répété", "« Je veux mon Bobiko → » ×6 + barre fixe"],
            ["10", "Paiement simple", "Apple Pay, Google Pay, PayPal, 3× sans frais"]]
    rules = [["Même message que la pub", "Oui (titre identique)"], ["Titre ≤ 8 mots, centré enfant", "Oui (7 mots)"], ["Image n°1 = produit en action", "Oui"],
             ["Montrer, pas affirmer", "Oui (galerie d'idées en 4e)"], ["IA en coulisse", "Oui (une ligne en S4)"], ["Pack présélectionné, ≤ 4 choix", "Oui (3 packs)"],
             ["« Seulement » + économie + ancrage crédible", "Oui"], ["Bouton à la 1re personne + barre fixe", "Oui"], ["Assurance plutôt que pression", "Oui"],
             ["Avis vrais et nuancés", "Oui (masqués sous 10 avis)"], ["Les 5 objections dans l'ordre", "Oui (figure 2)"], ["Jamais « Stickerbox »", "Oui"]]
    b.append(f'''<section class="chapter" id="ctrl"><p class="kicker">5</p><h1>Contrôle final</h1>
<h2>Grille « Ecom Method » : 10/10</h2>
{table(["#", "Point de contrôle", "Où la proposition le remplit"], grid, widths=["6%", "34%", "60%"])}
<h2>Les 12 règles d'or du plan</h2>
{table(["Règle", "Respectée ?"], rules, widths=["60%", "40%"])}
<div class="box yellow"><b>Ce qui reste à vérifier avant la mise en ligne.</b> Tous les éléments soulignés en pointillés dans la maquette sont des exemples : nombre de stickers par rouleau, dimensions, poids, autonomie, âge minimum, traitement de la voix, filtres de l'IA, date limite de Noël, note et nombre d'avis. Le second document en donne la liste complète.</div>
</section>''')

    ab = [["1", "Titre : « S'il peut le dire, ça l'imprime » / « Il l'imagine, il le dit, ça l'imprime »", "Clic sur le 1er bouton, profondeur de défilement"],
          ["2", "Hero : vidéo 8 s / photo action seule", "Clic sur le 1er bouton, vitesse (LCP)"],
          ["3", "Prix d'entrée : 79 € / 69 €", "Taux de commande × marge"],
          ["4", "Pack présélectionné : Créatif / Fratrie", "Panier moyen, taux de commande"],
          ["5", "Galerie d'idées : statique / avec champ interactif", "Temps passé, ajout au panier"],
          ["6", "Boutons de section : défilement / tiroir de choix", "Ajout au panier"]]
    b.append(f'''<section class="chapter" id="ab"><p class="kicker">6</p><h1>Tests A/B et indicateurs</h1>
<p>Les tests sont classés par effet attendu. Un seul test à la fois, au moins 1 000 sessions par variante ou deux semaines, et toujours le même indicateur principal.</p>
{table(["#", "Test", "Indicateur principal"], ab, widths=["6%", "64%", "30%"])}
<h2>Tableau de bord minimal</h2>
<ul><li><b>Clic sur le premier bouton</b> et défilement jusqu'à l'offre : la page accroche-t-elle ?</li>
<li><b>Ajout au panier</b> et <b>paiement terminé</b> : l'offre et le paiement convainquent-ils ?</li>
<li><b>Part du Kit Créatif</b> et panier moyen : la présélection fonctionne-t-elle ?</li>
<li><b>Retours et réclamations</b> : la page promet-elle ce que le produit tient ?</li></ul>
</section>''')

    shots = ""
    if SHOTS:
        shots = f'''<div class="grid3">
<figure><img class="shot" style="max-height:200mm;object-fit:contain" src="file://{SHOTS}/f-hero.png"><figcaption><b>Premier écran mobile.</b> Titre, note, média, sous-titre.</figcaption></figure>
<figure><img class="shot" style="max-height:200mm;object-fit:contain" src="file://{SHOTS}/f-ideas.png"><figcaption><b>Galerie d'idées.</b> Phrase d'enfant → sticker réel.</figcaption></figure>
<figure><img class="shot" style="max-height:200mm;object-fit:contain" src="file://{SHOTS}/f-offer.png"><figcaption><b>Offre.</b> Kit Créatif présélectionné.</figcaption></figure></div>'''
    b.append(f'''<section class="chapter" id="shots"><p class="kicker">7</p><h1>La maquette en images</h1>
<p>La maquette interactive applique toutes les décisions de ce document. Les packs, la barre fixe, le tiroir panier, les filtres d'avis et la FAQ fonctionnent. Le bouton « Afficher les annotations » en haut de la page affiche, au-dessus de chaque section, l'objection levée et les leviers utilisés.</p>
<p><b>Lien :</b> <a href="{MOCKUP_URL}">{MOCKUP_URL}</a></p>{shots}</section>''')
    return page("Analyse des options · Landing Bobiko", "".join(b))

if __name__ == "__main__":
    open(sys.argv[3] if len(sys.argv) > 3 else "analyse.html", "w", encoding="utf-8").write(build())
