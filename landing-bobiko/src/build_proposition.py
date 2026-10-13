# -*- coding: utf-8 -*-
"""Document 2 : la proposition finale retenue, élément par élément, avec les prompts d'images."""
import sys, json
from common import *

MOCKUP_URL = "https://claude.ai/artifact/QZkYRYDgmFcEyFKdrbbq9S"
SH = sys.argv[1] if len(sys.argv) > 1 else ""
PAGES = json.load(open(sys.argv[2])) if len(sys.argv) > 2 and sys.argv[2] else {}

def mk(i):
    return f'<span class="mk">§{i}§</span>'

def chap(i, num, title, lead=""):
    l = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<section class="chapter"><p class="kicker">{num}</p><h1>{mk(i)}{title}</h1>{l}'

def shot(name, w="100%", cap=""):
    if not SH:
        return ""
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f'<figure style="margin:0"><img class="shot" style="width:{w}" src="file://{SH}/{name}.png">{c}</figure>'

def kv(rows):
    return "<table class='kv'><colgroup><col style='width:27%'><col></colgroup><tbody>" + "".join(
        f"<tr><td style='font-weight:800;background:#FBF4EC'>{k}</td><td>{v}</td></tr>" for k, v in rows) + "</tbody></table>"

def copy(lines):
    """Bloc de textes exacts : [(rôle, texte)]."""
    return "<div class='copy'>" + "".join(f"<div><span>{e(r)}</span><p>{t}</p></div>" for r, t in lines) + "</div>"

EXTRA_CSS = """
<style>
.copy{border:.3mm solid var(--line);border-radius:2.5mm;overflow:hidden;margin:1mm 0 3mm;break-inside:avoid}
.copy div{display:grid;grid-template-columns:30mm 1fr;border-bottom:.3mm solid var(--line)}
.copy div:last-child{border-bottom:0}
.copy > div > span{background:var(--cream);font-size:7.8pt;font-weight:800;color:var(--muted);padding:1.6mm 2.2mm;text-transform:uppercase;letter-spacing:.04em}
.copy p{margin:0;padding:1.6mm 2.4mm;font-size:9.4pt}
.sec{display:grid;grid-template-columns:50mm 1fr;gap:6mm;align-items:start;margin-top:3mm}
.sec .pic{position:sticky;top:0}
.sec table.kv{font-size:8.6pt;margin-top:0}
.swatch{border-radius:3mm;padding:3mm;min-height:30mm;display:flex;flex-direction:column;justify-content:flex-end;font-size:8.2pt;break-inside:avoid}
.swatch b{font-family:Fredoka;font-size:11pt}
.prompt{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:7.9pt;line-height:1.45;background:#1E1B2E;color:#F3EEF8;border-radius:2.5mm;padding:3mm 3.5mm;white-space:pre-wrap;margin:1.5mm 0 2mm;break-inside:avoid}
.img-card{border:.3mm solid var(--line);border-radius:3mm;padding:3.5mm 4mm;margin:0 0 4mm;break-inside:avoid}
.img-card h3{margin-top:0}
.img-card .meta{font-size:8.3pt;color:var(--muted);margin-bottom:1.5mm}
.img-card .meta b{color:var(--ink)}
.neg{font-size:8.3pt;background:#FFF1EC;border-radius:2mm;padding:1.6mm 2.4mm;margin-bottom:1.6mm}
.post{font-size:8.3pt;color:var(--muted)}
</style>"""

STYLE = """
Photorealistic lifestyle photograph, natural window daylight, warm and soft,
35 mm lens, f/2.8, shallow depth of field, real French family home
(light oak table, off-white walls, a few colorful kid items), saturated but
natural colors with small accents of coral #FF5A36, crayon yellow #FFC83D
and sky blue #2F5BEA, clean uncluttered composition, candid and warm mood.
PRODUCT FIDELITY: the sticker printer must match the attached reference
images EXACTLY - same shape, proportions, colors, button, paper slot,
materials and size. Do not redesign, restyle or add parts to it.
Printed stickers look like thermal prints: pure black line drawing on
white paper, no grey shading, simple and childlike.
No text, no letters, no logos, no watermark anywhere in the image."""

NEG = "Avoid: redesigned or extra product parts, screens added to the product, text or logos, extra or fused fingers, plastic CGI look, studio backdrop, over-perfect catalog look, dark or moody light, adult-looking stickers."

IMAGES = [
 dict(id="IMG-01", t="Photo action (poster du hero)", where="S2 Hero, 1re image ; poster de IMG-02 ; vignette pub", fmt="4:3 · 2400×1800 (recadrages 1:1 et 4:5)", refs="REF-01, REF-02, REF-05 (sticker « chat astronaute »)",
  p="""Use the attached images as the exact product (REF-01, REF-02) and the exact sticker style (REF-05).
Scene: a 6-year-old child's hand (right hand, small, natural nails) peeling a freshly printed sticker
of a cat astronaut from the paper slot of the sticker printer. The printer sits on a light oak kitchen
table, slightly left of center, three-quarter view. Around it: three crayons (blue, yellow, coral),
two already-colored stickers lying flat, a corner of an open drawing notebook.
Camera at the child's eye level, close (the machine fills one third of the frame), slight push toward
the sticker. The sticker is the sharpest point of the image. The child's face is NOT visible, only the
hand and forearm in a striped long-sleeve top. Empty soft background on the right third for text.""",
  post="Garder la même scène comme 1re image de la vidéo IMG-02. Exporter WebP qualité 80, ≤ 180 Ko."),
 dict(id="IMG-02", t="Vidéo héros 8 s en boucle (muette)", where="S2 Hero (autoplay muet), pubs 9:16 en version longue", fmt="4:3 et 9:16 · 8 s · 24 i/s · MP4 H.264 ≤ 1,2 Mo + WebM", refs="Image de départ : IMG-01 ; REF-01, REF-05",
  p="""Image-to-video. Start frame: IMG-01 (attached). Keep the printer identical to the reference images.
0-2 s: a 6-year-old child (face visible, three-quarter, curly brown hair, striped top) leans toward the
printer, presses the big button and says a short sentence, excited, looking at the machine.
2-5 s: the paper slides out of the slot in slow motion (only the paper is slowed, the child moves at
normal speed); the black line drawing of a cat astronaut becomes visible.
5-8 s: the child tears the sticker, holds it up next to their face toward the camera, big surprised
smile, eyes on the sticker. Very slow camera push-in during the whole shot.
Natural daylight, real kitchen, no text, no logos. Loopable: last frame close to the first frame.""",
  post="Sous-titre ajouté au montage (Fredoka, blanc sur pastille encre) : « Un chat astronaute ! ». Pour les pubs : ajouter le son « bzzz » réel de la machine. Démo longue de 30 s (bouton « Voir la démo ») : même tournage, 3 idées enchaînées, filmée avec la vraie machine."),
 dict(id="IMG-03", t="Gros plan : le sticker sort", where="Galerie du hero (vignette 2)", fmt="4:3 · 2000×1500", refs="REF-01, REF-04, REF-05",
  p="""Macro close-up of the paper slot of the exact sticker printer from the references. A strip of thermal
sticker paper is coming out, curling slightly, showing the black line drawing of a dinosaur eating
spaghetti (style of REF-05). Shallow depth of field, the printed lines are tack-sharp, the button is
softly blurred in the foreground. Warm daylight from the left. Light oak table.""",
  post="Peut aussi servir de boucle de 3 s (IMG-06) en image-to-video : « the paper keeps sliding out slowly »."),
 dict(id="IMG-04", t="Kit Créatif complet à plat", where="Galerie du hero, encart « Dans votre boîte »", fmt="1:1 · 2400×2400", refs="REF-01, REF-06, REF-07",
  p="""Top-down flat lay on a warm cream background (#FFF6EC). Neatly arranged with even spacing, like a
knolling photo: the sticker printer from the references in the center; around it 10 thermal paper rolls
in two rows of five, 12 washable markers fanned out, a sticker binder (A5, coral cover), 6 crayons, a
small idea booklet, and the gift box open at the top. Every item fully visible, nothing overlapping.
Soft even daylight, gentle shadows, saturated but true colors.""",
  post="Ajouter au montage de fines étiquettes (Nunito, encre) : « 10 rouleaux », « 12 feutres »… Déclinaisons Découverte (3 rouleaux, 6 crayons) et Fratrie (2 machines) pour IMG-23."),
 dict(id="IMG-05", t="Étape 1 : il appuie et dit son idée", where="S4 Comment ça marche", fmt="4:3 · 1600×1200", refs="REF-01, REF-02 ; IMG-01/02 comme référence de l'enfant",
  p="""Same child as in the reference (curly brown hair, striped top), seen in three-quarter profile, leaning
close to the sticker printer on the kitchen table, index finger pressing the big button, mouth open
mid-sentence, eyes bright and focused on the machine. The printer matches the references exactly.
Eye-level camera, medium close-up, background softly blurred kitchen.""",
  post="Ajouter une bulle de parole (Caveat) en surimpression si l'image est utilisée hors de la maquette."),
 dict(id="IMG-07", t="Étape 3 : il colorie et colle", where="S4 Comment ça marche", fmt="4:3 · 1600×1200", refs="REF-05, REF-06 ; enfant de IMG-01/02",
  p="""Over-the-shoulder view of the same child coloring a printed sticker (cat astronaut, style of REF-05)
with a yellow crayon, half colored, on the light oak table. Next to it, an open notebook already
decorated with four colored stickers. The printer is visible but out of focus in the top-left corner.
Hands natural, small, slightly messy with crayon. Warm daylight."""),
 dict(id="IMG-08 à 13", t="Les 6 stickers de la galerie d'idées", where="S5 Galerie d'idées", fmt="Carré · 1200×1200 chacun · fond blanc", refs="REF-05 = les VRAIS tirages",
  p="""RÈGLE : ces images doivent être de vrais stickers imprimés par la machine.
1. Dire à la machine, en français : « un dinosaure qui mange des spaghettis », « mamie en
   super-héroïne », « une licorne avec une mallette », « un chat astronaute », « une pizza qui fait du
   ski », « papa pirate qui a peur des vagues ». Garder le meilleur de 3 essais.
2. Faire colorier 3 des 6 par un enfant (crayons jaune, corail, bleu).
3. Scanner à plat (600 dpi) ou photographier à la verticale en lumière du jour.
Prompt d'harmonisation (outil d'édition, image = le scan) :
Keep this sticker exactly as it is - same drawing, same lines, same coloring. Only clean the
background to pure white, straighten it, add a very soft drop shadow under the paper and a slight
paper texture. Do not redraw, add or remove any line.""",
  post="Ne jamais générer ces dessins par IA : le client comparera avec ce que sa machine imprime."),
 dict(id="IMG-14", t="Vue éclatée", where="S6 Bénéfices", fmt="1:1 · 2400×2400 · fond crème", refs="REF-01 à REF-04 (intérieur, rouleau, port USB-C)",
  p="""Clean exploded-view product render of the exact sticker printer from the references, floating parts
separated vertically with even gaps on a cream background (#FFF6EC): top shell with the big button,
the microphone module, the thermal print head, the sticker paper roll (57 mm), the rechargeable battery
with USB-C port, the bottom shell. Same colors and materials as the references, soft studio light,
subtle shadows, three-quarter view, photoreal product render, generous margins for callout lines.""",
  post="Les traits de légende et libellés (Micro, Gros bouton, Rouleau thermique 57 mm, Batterie USB-C) sont ajoutés au montage, pas par l'IA. Vérifier la cohérence avec l'intérieur réel (REF-04)."),
 dict(id="IMG-15", t="Échelle : dans une main d'adulte", where="Galerie du hero (vignette 4)", fmt="4:3 · 1600×1200", refs="REF-01, REF-02",
  p="""An adult's hand (a mother's hand, natural manicure, simple ring) holding the exact sticker printer
from the references at chest height, next to a white coffee mug on a kitchen counter, to show its real
size (about 9 x 8 cm). Clean, bright, natural daylight, shallow depth of field."""),
 dict(id="IMG-16", t="Émotion : la cuisine", where="S9 Émotion (grande image)", fmt="4:3 · 2400×1800", refs="REF-01 ; enfant de IMG-01/02",
  p="""Late afternoon in a bright family kitchen. In the foreground, the same child sits at the oak table,
laughing while holding up a freshly printed sticker toward the parent; the sticker printer and crayons
are on the table. In the soft-focus background, a mother in a casual sweater is cooking at the stove,
turning her head with a warm smile toward the child. Golden daylight from a window, steam from a pot,
lived-in but tidy home. The printer matches the references exactly."""),
 dict(id="IMG-17", t="Moment : en voiture", where="S9 Émotion (vignette 1)", fmt="1:1 · 1200×1200", refs="REF-01",
  p="""Back seat of a family car on a sunny road trip, a child in a booster seat holding the sticker printer
on a lap tray, pressing the button and talking, two printed stickers stuck on the window. Bright
daylight through the windows, happy calm mood. The printer matches the references exactly."""),
 dict(id="IMG-18", t="Moment : le mercredi après-midi", where="S9 Émotion (vignette 2)", fmt="1:1 · 1200×1200", refs="REF-01, REF-05",
  p="""Three kids aged 6 to 8 sitting on a colorful rug in a child's bedroom, the sticker printer in the
middle, one child pressing the button while the two others wait excitedly with outstretched hands;
printed stickers scattered on the rug. Natural light, joyful, candid."""),
 dict(id="IMG-19", t="Moment : la carte pour mamie", where="S9 Émotion (vignette 3)", fmt="1:1 · 1200×1200", refs="REF-05 (sticker « mamie en super-héroïne »)",
  p="""Close-up top-down view of a handmade birthday card on a table: a folded coral card with a printed
sticker of a grandmother as a superhero (style of REF-05), colored in yellow and coral, a child's hand
writing with a blue marker, crayons around. Warm daylight.""",
  post="Le texte de la carte est écrit à la main par un vrai enfant au shooting ou ajouté au montage, pas par l'IA."),
 dict(id="IMG-20 à 22", t="Témoignages", where="S10 Témoignages", fmt="16:9 (vidéo 15-30 s) ou 4:3 (photo)", refs="—",
  p="""PAS DE PROMPT : ces images doivent être réelles (clients ou créateurs rémunérés, signalés).
Brief à envoyer aux créateurs :
- Filmer à la maison, lumière du jour, téléphone à la verticale ET à l'horizontale.
- 15 à 30 s : le parent regarde la caméra, dit le prénom et l'âge de l'enfant, raconte UNE scène
  précise (« elle a imprimé toute la famille en super-héros »), puis l'enfant montre ses stickers.
- Montrer le frigo, le cahier ou la carte décorés.
- Pas de script mot à mot ; pas de promesse éducative ou médicale.""",
  post="Mention obligatoire « Collaboration commerciale » pour les créateurs payés."),
 dict(id="IMG-23", t="Vignettes des 3 kits", where="S7 Offre (cartes de packs), barre fixe, panier", fmt="1:1 · 800×800 · fond crème", refs="REF-01, REF-06",
  p="""Three separate square packshots on a flat warm cream background (#FFF6EC), same light, same angle
(slightly from above, 30 degrees), same scale:
(1) KIT DÉCOUVERTE: the sticker printer + 3 paper rolls + 6 crayons, compact group.
(2) KIT CRÉATIF: the sticker printer + 10 paper rolls stacked + 12 markers + coral sticker binder.
(3) KIT FRATRIE: two identical sticker printers side by side + 10 rolls + two crayon boxes.
The printer matches the references exactly. Soft shadow, nothing cropped, no text.""",
  post="Le contenu de chaque vignette doit correspondre exactement à la liste « Dans votre boîte »."),
 dict(id="IMG-24", t="Déballage : la boîte cadeau", where="Galerie du hero (vignette 5), FAQ Noël, pubs de fin d'année", fmt="4:3 · 1600×1200", refs="REF-07 (boîte), REF-01",
  p="""A child's hands lifting the lid of the gift box (design from REF-07, rounded corners, coral and
yellow) on a living-room floor near a decorated Christmas tree, the sticker printer visible inside in
its insert, wrapping paper and a ribbon around. Warm cozy light, festive but natural, not cheesy."""),
 dict(id="IMG-26", t="Concept de boîte cadeau (si pas encore de boîte)", where="Brief fournisseur / emballage", fmt="1:1 · 2000×2000", refs="REF-01 ; logo (fichier SVG fourni)",
  p="""Product packaging concept: a square gift box with generously rounded corners, matte coral (#FF5A36)
with a crayon-yellow (#FFC83D) band, playful hand-drawn black line doodles of a dinosaur, a cat
astronaut and a unicorn around the edges, a large window or illustration of the sticker printer from
the references on the front, leaving a clean empty space at the top for the logo. Three-quarter view
on a cream background, soft shadow. No text.""",
  post="Le logo, le slogan et les mentions légales sont posés ensuite sur le fichier vectoriel, jamais générés."),
 dict(id="IMG-27", t="Image de partage (Open Graph)", where="Aperçu des liens (WhatsApp, Facebook)", fmt="1,91:1 · 1200×630", refs="IMG-01",
  p="""Wide crop of IMG-01 (attached): extend the scene to the left with more oak table and soft
background so the printer and the sticker sit in the right half, leaving the left 55 % calm and empty
for a title. Same light, same colors, nothing added.""",
  post="Ajouter au montage le titre « S'il peut le dire, ça l'imprime. » (Fredoka Bold, encre) et le logo."),
 dict(id="IMG-28", t="Avant / après (pour les pubs)", where="Publicités Meta, éventuellement S8", fmt="4:5 · 1080×1350 (2 images)", refs="Enfant de IMG-01/02, REF-01",
  p="""Two images of the same child in the same living room, same framing.
BEFORE: the child slumped on the sofa staring at a tablet, bored expression, the image fully
desaturated (black and white), dull light.
AFTER: the child sitting up at the table, laughing, holding a freshly printed sticker from the
sticker printer (exact references), crayons and stickers around, warm saturated colors.""",
  post="Réservé aux pubs (cf. analyse S8). Pas de promesse chiffrée sur le temps d'écran."),
]

REFS = [
 ["REF-01", "La machine, face avant", "Fond gris clair uni, lumière du jour diffuse, objectif à hauteur de la machine, 3000 px minimum, net partout."],
 ["REF-02", "La machine de trois quarts", "Même lumière, rotation de 35° ; on doit voir le dessus (fente papier) et un côté."],
 ["REF-03", "La machine de dos et de côté", "Port USB-C, trappe, interrupteur, détails de matière."],
 ["REF-04", "La machine ouverte", "Trappe ouverte avec un rouleau en place ; sert pour la vue éclatée."],
 ["REF-05", "Les vrais stickers", "Scans à plat 600 dpi des 6 idées de la galerie (dont « chat astronaute »), noir et blanc et coloriés."],
 ["REF-06", "Les accessoires", "Rouleaux, crayons, feutres, classeur, guide, photographiés à plat séparément."],
 ["REF-07", "La boîte", "Boîte fermée et ouverte avec calage (ou le concept IMG-26 une fois validé)."],
]

SECTIONS = [
 dict(id="S0", t="Bandeau d'annonce", shot="s00", rows=[
   ("Objectif", "Poser le cadre de service avant tout : livraison, garantie, retour (« Qui me parle ? »)."),
   ("Mobile", "Bande pleine largeur, fond encre #1E1B2E, 36 px de haut, texte crème Nunito 800 13 px, séparateurs « · » jaunes. Statique."),
   ("Ordinateur", "Identique, centré."),
   ("Shopify", "Section « Barre d'annonces » du thème, un seul message, aucun lien."),
  ], copy=[("Texte", "Livraison offerte · Garantie 2 ans · Retour 30 jours")]),
 dict(id="S1", t="En-tête", shot="s01", rows=[
   ("Objectif", "Identifier la marque sans voler l'attention ; aucune sortie."),
   ("Mobile", "64 px de haut. Logo à gauche (30 px de haut). Icône sac à droite (cible 44 × 44 px) avec pastille corail du nombre d'articles, cachée à 0."),
   ("Ordinateur", "Même structure, largeur max 1 120 px."),
   ("Interactions", "Clic logo : remonte en haut. Clic panier : ouvre le tiroir (S17) ; si vide, message « Votre panier est vide : choisissez votre kit » et défilement vers l'offre."),
   ("Shopify", "En-tête simplifié du modèle de page produit : pas de menu, pas de recherche, pas de compte."),
  ], copy=[("Logo", "bobiko (logotype)"), ("Accessibilité", "« bobiko, accueil » · « Ouvrir le panier »")]),
 dict(id="S2", t="Hero (premier écran)", shot="s02", rows=[
   ("Objectif", "« C'est pour moi ? » en 3 secondes : même phrase que la pub, produit en action, prix d'appel, bouton."),
   ("Mobile (ordre)", "Badges → titre (2 lignes) → note → média 16:10,5 (vidéo) + 6 vignettes → sous-titre → ligne de prix → bouton → 3 micro-assurances. Le bouton doit être visible sur un iPhone 13 sans défiler."),
   ("Ordinateur", "2 colonnes : média à gauche (54 %), texte à droite (image à gauche, texte à droite). Titre 60 px."),
   ("Visuels", "IMG-02 (vidéo, autoplay, muet, en boucle, playsinline) avec poster IMG-01 ; vignettes : IMG-01, IMG-03, IMG-04, IMG-15, IMG-24, photo client."),
   ("Interactions", "Le bouton fait défiler en douceur jusqu'à l'offre (#offre). Pulsation légère du bouton 2 fois après 1,2 s, désactivée si « mouvement réduit ». Les vignettes changent le média principal."),
   ("Shopify", "Section hero personnalisée (vidéo + texte) puis galerie produit native ; la vidéo est chargée après le poster (preload=\"none\")."),
  ], copy=[("Badge 1", "180 stickers inclus"), ("Badge 2", "Sans encre"),
           ("Titre H1", "S'il peut le dire,<br><span style='color:#E8431F'>ça l'imprime.</span>"),
           ("Note", "★★★★★ 4,7/5 · [N] avis de parents (lien vers #avis ; masqué sous 10 avis)"),
           ("Sous-titre", "Votre enfant appuie, décrit son idée à voix haute… et tient son sticker <b>5 secondes</b> plus tard. À colorier, à coller partout."),
           ("Prix", "Dès seulement <b>79 €</b> · Livraison offerte"), ("Bouton", "Je veux mon Bobiko →"),
           ("Micro-assurances", "Paiement sécurisé · Expédié sous 24 h · 30 jours pour changer d'avis")]),
 dict(id="S3", t="Bande de chiffres", shot="s03", rows=[
   ("Objectif", "Trois preuves concrètes juste sous le premier écran ; le contraste encre invite à défiler."),
   ("Mise en page", "Fond encre, 3 colonnes égales même sur mobile. Chiffres Fredoka 700, 40-56 px, jaune crayon ; légendes crème Nunito 700 14 px."),
  ], copy=[("Chiffre 1", "5 s — entre l'idée et le sticker"), ("Chiffre 2", "0 — cartouche d'encre, jamais"), ("Chiffre 3", "180 — stickers dans la boîte")]),
 dict(id="S4", t="Comment ça marche", shot="s04", rows=[
   ("Objectif", "Le mécanisme en 3 verbes ; l'IA mentionnée une fois, honnêtement."),
   ("Mobile", "Fond crème. Surtitre + titre centrés. 3 lignes : image carrée 96 px à gauche, numéro, titre, texte à droite. Encadré pointillé pour la note IA."),
   ("Ordinateur", "3 colonnes, images 4:3 au-dessus des textes."),
   ("Visuels", "IMG-05, IMG-06 (boucle 3 s du sticker qui sort, tirée de IMG-02 ou IMG-03), IMG-07."),
   ("Interactions", "Le lien « Où va sa voix ? » ouvre la question correspondante de la FAQ."),
  ], copy=[("Surtitre", "Comment ça marche"), ("Titre H2", "Il le dit. Ça sort. Il colorie."),
           ("Étape 1", "<b>Il appuie et dit son idée</b> · <span class='hand' style='font-size:12pt'>« Un chat astronaute qui mange une glace ! »</span>"),
           ("Étape 2", "<b>Le sticker sort en 5 secondes</b> · Bzzz… la machine dessine son idée et l'imprime en noir et blanc, sans encre."),
           ("Étape 3", "<b>Il le colorie et le colle partout</b> · Cahier, frigo, carte pour mamie : ses idées deviennent de vrais objets."),
           ("Note IA", "Une intelligence artificielle conçue pour les enfants transforme sa phrase en dessin simple, prêt à colorier. <u>Où va sa voix ?</u>")]),
 dict(id="S5", t="Galerie d'idées", shot="s05", rows=[
   ("Objectif", "Prouver l'angle : des phrases absurdes deviennent de vrais stickers."),
   ("Mobile", "Grille 2 colonnes, 6 cartes blanches : phrase en Caveat 22 px → flèche corail → sticker légèrement incliné (±2°) avec ombre douce. Mention sous la grille, puis bouton."),
   ("Ordinateur", "Grille 3 colonnes, stickers de 150 px."),
   ("Visuels", "IMG-08 à IMG-13 : vrais tirages, dont 3 coloriés."),
  ], copy=[("Surtitre", "Ce qu'ils ont dit, ce qui est sorti"), ("Titre H2", "Des idées qu'aucun cahier de stickers ne contient"),
           ("Phrases", "« Un dinosaure qui mange des spaghettis » · « Mamie en super-héroïne » · « Une licorne avec une mallette » · « Un chat astronaute » · « Une pizza qui fait du ski » · « Papa pirate qui a peur des vagues »"),
           ("Mention", "Vrais stickers imprimés par Bobiko, puis coloriés par les enfants."), ("Bouton", "Je veux mon Bobiko →")]),
 dict(id="S6", t="Bénéfices et vue éclatée", shot="s06", rows=[
   ("Objectif", "Chaque promesse avec sa preuve (« … grâce à … »)."),
   ("Mobile", "3 cartes (pastille jaune avec icône, titre Fredoka, « grâce à… » en gris, texte), puis vue éclatée 4:3, 4 légendes en grille 2×2, 3 pastilles encre de mesures, accordéon « Fiche technique complète »."),
   ("Ordinateur", "2 colonnes : vue éclatée carrée à gauche, cartes à droite."),
   ("Visuels", "IMG-14."),
  ], copy=[("Surtitre", "Pourquoi les parents l'adoptent"), ("Titre H2", "Des heures d'invention, sans encre ni tablette"),
           ("Bénéfice 1", "<b>Des idées illimitées</b>, grâce au dessin créé à partir de sa phrase. Chaque idée devient un sticker unique. Impossible d'en faire le tour : il en invente de nouvelles tous les jours."),
           ("Bénéfice 2", "<b>Zéro cartouche</b>, grâce à l'impression thermique. Seul le papier se recharge : 5 rouleaux, soit 300 stickers, pour 25 €."),
           ("Bénéfice 3", "<b>Il crée avec ses mains</b>, grâce au pilotage à la voix. Un bouton, sa voix, des crayons. Pas de tablette à regarder : il parle, il colorie, il colle."),
           ("Légendes", "Micro intégré (il parle, elle écoute) · Un seul gros bouton (utilisable dès 4 ans) · Rouleau thermique (57 mm, sans encre) · Batterie USB-C (4 h d'utilisation)"),
           ("Mesures", "9,4 × 8,1 cm · 280 g · 200 dpi"),
           ("Fiche technique", "Impression thermique noir et blanc 200 dpi · Rouleaux autocollants 57 × 25 mm · Wi-Fi + Bluetooth (réglage unique) · Batterie 1 200 mAh USB-C · Français + 15 langues · CE, EN 71")]),
 dict(id="S7", t="Offre : packs et achat", shot="s07", rows=[
   ("Objectif", "Passer de « est-ce que j'achète ? » à « lequel je prends ? », puis payer en un geste."),
   ("Mobile (ordre)", "Surtitre + titre → encart mini-question → légende « Choisissez votre kit » → 3 cartes radio (Créatif cochée) → boîte d'achat : « Dans votre boîte » (liste chiffrée), total, bouton, paiements express, 3×, 4 assurances, encart Noël."),
   ("Ordinateur", "2 colonnes : question + packs à gauche ; boîte d'achat collante à droite."),
   ("Carte de pack", "Radio 24 px · vignette 64 px (IMG-23) · nom Fredoka 19 px · contenu · ligne verte (stickers et prix unitaire) · prix à droite + pastille d'économie. Carte cochée : bordure corail 2,5 px + halo. Badge encre/jaune « Notre recommandation » sur le Kit Créatif."),
   ("Interactions", "Changer de pack met à jour la liste, le total, l'économie, la mensualité et la barre fixe. La mini-question affiche une réponse en Caveat corail. Le bouton ajoute le pack au panier et ouvre le tiroir (vibration 400 ms sur mobile)."),
   ("Shopify", "Variantes (ou appli de bundles) : 3 options, Créatif par défaut ; paiement express natif ; Alma ou Klarna pour le 3×."),
  ], copy=[("Surtitre / titre", "Votre kit · Prêt pour sa première idée ?"),
           ("Mini-question", "Votre enfant commencerait par… [un dinosaure] [une licorne] [un chat] → « Bonne idée ! « Un dinosaure qui fait du skate » : sorti en 5 secondes. »"),
           ("Kit Découverte", "La machine + 3 rouleaux + 6 crayons · ≈ 180 stickers · 0,44 € le sticker · <b>79 €</b>"),
           ("Kit Créatif", "Notre recommandation · La machine + 10 rouleaux + 12 feutres + classeur à stickers · ≈ 600 stickers · 0,17 € le sticker · <b>99 €</b> · −36 €"),
           ("Kit Fratrie", "2 machines + 10 rouleaux + 2 boîtes de crayons · Soit 74,50 € la machine · <b>149 €</b> · −29 €"),
           ("Dans votre boîte", "Machine Bobiko + 3 rouleaux + 6 crayons 79 € · 7 rouleaux en plus (≈ 420 stickers) 35 € · 12 feutres lavables 12 € · Classeur à stickers 9 € · Guide « 100 idées pour commencer » offert"),
           ("Note", "Valeurs = prix de chaque élément vendu séparément sur maison-ivy.com."),
           ("Total", "Seulement <b>99 €</b> <s>135 €</s> · Vous économisez 36 €"),
           ("Bouton", "Je veux mon Bobiko →"), ("Paiement", "Apple Pay · Google Pay · PayPal · ou en 3 fois sans frais : 3 × 33 €"),
           ("Assurances", "Livraison offerte, 48-72 h · Garantie 2 ans · 30 jours satisfait ou remboursé · Réponse sous 24 h"),
           ("Noël", "Idée cadeau : commandé avant le [18 décembre], livré avant Noël, dans sa boîte prête à offrir.")]),
 dict(id="S8", t="Pourquoi c'est différent", shot="s08", rows=[
   ("Objectif", "Ancrer la valeur face aux deux alternatives réelles."),
   ("Mise en page", "Tableau 4 colonnes ; en-tête de la colonne Bobiko en encre/jaune, cellules Bobiko teintées corail très clair ; pastilles rondes vertes (oui) et grises (non)."),
  ], copy=[("Surtitre / titre", "Comparez · Pourquoi pas un simple cahier de stickers ?"),
           ("Lignes", "Des stickers uniques, inventés par l'enfant (oui / non / non) · Il crée avec ses mains (oui / oui / non) · Sans écran à regarder (oui / oui / non) · Se renouvelle à l'infini (oui / non / oui)")]),
 dict(id="S9", t="Émotion et moments d'usage", shot="s09", rows=[
   ("Objectif", "Vendre le moment ; le parent se projette."),
   ("Mobile", "Grande image 4:3, titre H2, 3 cartes moment (vignette carrée 76 px + titre + phrase), bouton."),
   ("Ordinateur", "Image à gauche (55 %), texte à droite."),
   ("Visuels", "IMG-16, IMG-17, IMG-18, IMG-19."),
  ], copy=[("Titre H2", "Le calme pendant que vous cuisinez. Les rires pendant qu'il invente."),
           ("Moment 1", "<b>En voiture pour les vacances</b> · Un rouleau, des crayons : la route passe en idées."),
           ("Moment 2", "<b>Le mercredi après-midi</b> · Il invente, ses copains réclament chacun leur sticker."),
           ("Moment 3", "<b>La carte d'anniversaire de mamie</b> · Mamie en super-héroïne, coloriée avec amour."),
           ("Bouton", "Je veux mon Bobiko →")]),
 dict(id="S10", t="Témoignages", shot="s10", rows=[
   ("Objectif", "Prouver par des parents qui ressemblent au visiteur."),
   ("Mise en page", "3 cartes (1 colonne mobile, 3 ordinateur) : média 16:9 (vidéo de préférence), citation en gras, signature « Prénom I., parent de Prénom (âge), Ville »."),
   ("Visuels", "IMG-20 à IMG-22 : réels uniquement (voir brief)."),
   ("Règle", "Les citations de la maquette sont des exemples de mise en page. Les remplacer par de vraies paroles, avec accord écrit."),
  ], copy=[("Surtitre / titre", "À la maison · Ce que les parents nous racontent"),
           ("Format de signature", "Sophie M., maman d'Inès (7 ans), Nantes"), ("Bouton", "Je veux mon Bobiko →")]),
 dict(id="S11", t="Avis clients", shot="s11", rows=[
   ("Objectif", "Laisser le visiteur vérifier lui-même."),
   ("Mise en page", "Carte de synthèse (note en grand, étoiles, nombre, barres de répartition), puces de filtre défilant horizontalement, avis en cartes (étoiles, « Achat vérifié », texte, prénom + ville, thème)."),
   ("Règles", "Note réelle seulement ; même nombre d'avis que dans le hero ; au moins un avis 4★ nuancé visible sans filtre ; bloc masqué tant qu'il y a moins de 10 avis ; collecte par e-mail 10 jours après livraison, pas de formulaire sur la page."),
   ("Shopify", "Judge.me (ou Loox) avec filtres par mots-clés et photos."),
  ], copy=[("Surtitre / titre", "Avis vérifiés · Les parents en parlent"), ("Filtres", "Tous · Facile à utiliser · Qualité des dessins · Idée cadeau · Livraison")]),
 dict(id="S12", t="Promesse 30 jours", shot="s12", rows=[
   ("Objectif", "Inverser le risque avant la FAQ."),
   ("Mise en page", "Bande jaune crayon. Sceau rond encre incliné de −8° (« 30 jours pour l'essayer »), titre, phrase, 3 pastilles blanches translucides."),
  ], copy=[("Titre H2", "Essayez-le 30 jours."), ("Texte", "S'il ne fait pas sourire votre enfant, renvoyez-le : on vous rembourse, sans discussion."),
           ("Pastilles", "Garantie 2 ans · Retour simple et suivi · Un humain vous répond sous 24 h")]),
 dict(id="S13", t="FAQ", shot="s13", rows=[
   ("Objectif", "Lever les derniers doutes, logistique d'abord."),
   ("Mise en page", "9 accordéons blancs (cible 56 px), question en Nunito 800, chevron à droite. Tous fermés au chargement."),
   ("Règle", "Les réponses marquées [à valider] doivent être confirmées avec le fournisseur et l'échantillon."),
  ], copy=[("Q1", "<b>Quand vais-je le recevoir ?</b> Votre commande part sous 24 h ouvrées et arrive en 48 à 72 h en France (3 à 5 jours en Belgique et en Suisse). Vous recevez le suivi par e-mail."),
           ("Q2", "<b>Comment se passe un retour ?</b> Vous avez 30 jours pour changer d'avis. Écrivez-nous, on vous envoie l'étiquette de retour, et vous êtes remboursé sous 5 jours après réception."),
           ("Q3", "<b>Est-ce sûr pour mon enfant ? Où va sa voix ?</b> Bobiko est conforme aux normes CE et EN 71 (certificats disponibles sur demande). Sa voix sert uniquement à créer le dessin : [elle est transformée en texte puis effacée, jamais conservée ni utilisée pour de la publicité]."),
           ("Q4", "<b>Faut-il un téléphone ou le Wi-Fi ?</b> [Le Wi-Fi sert à créer les dessins. Le réglage se fait une seule fois depuis l'application, en 3 minutes ; ensuite, votre enfant n'a besoin que du bouton.]"),
           ("Q5", "<b>À partir de quel âge ?</b> Dès [4 ans] : un seul bouton, aucune lecture nécessaire. Les plus grands (jusqu'à 10-11 ans) s'amusent à inventer des idées de plus en plus folles."),
           ("Q6", "<b>Combien de stickers par rouleau, et où en racheter ?</b> Environ [60] stickers par rouleau. Les recharges sont sur maison-ivy.com : 5 rouleaux ([300] stickers) pour 25 €, livrés en 48-72 h."),
           ("Q7", "<b>Comprend-il bien le français ?</b> Oui. Il comprend le français et plus de 15 autres langues. Les phrases courtes d'enfant marchent très bien : « un chat astronaute » suffit."),
           ("Q8", "<b>Et si le dessin ne convient pas à un enfant ?</b> [Les demandes inadaptées aux enfants sont filtrées et remplacées par un dessin neutre.] Si un dessin vous paraît bizarre, écrivez-nous : on regarde avec vous."),
           ("Q9", "<b>Est-ce un bon cadeau de Noël ?</b> Oui : il arrive dans une boîte cadeau prête à offrir. Pour Noël, commandez avant le [18 décembre].")]),
 dict(id="S14", t="Dernier appel", shot="s14", rows=[
   ("Objectif", "Justifier la fin du défilement et proposer une dernière action."),
   ("Mise en page", "Fond crème, centré : titre, phrase, bouton principal, bouton secondaire contour encre, e-mail sélectionnable."),
   ("Interactions", "« Voir la démo (30 s) » ouvre la vidéo longue en plein écran (lecteur natif)."),
  ], copy=[("Titre H2", "Vous hésitez encore ?"), ("Texte", "Regardez 30 secondes de démo, ou posez-nous votre question : un vrai humain vous répond sous 24 h."),
           ("Boutons", "Je veux mon Bobiko → · Voir la démo (30 s)"), ("Contact", "Écrivez-nous : bonjour@maison-ivy.com (adresse à créer sur votre domaine ; éviter d'afficher l'adresse Gmail)")]),
 dict(id="S15", t="Pied de page", shot="s15", rows=[
   ("Objectif", "Confiance légale, sans fuite."),
   ("Mise en page", "Fond encre, logo crème, slogan, liens légaux, pastilles de paiement, copyright."),
  ], copy=[("Liens", "Livraison et retours · CGV · Mentions légales · Confidentialité et données vocales · Contact"),
           ("Paiements", "Visa · Mastercard · CB · Apple Pay · Google Pay · PayPal"), ("Mentions", "S'il peut le dire, ça l'imprime. · Bobiko, une marque Maison Ivy · maison-ivy.com · © 2026")]),
 dict(id="S16", t="Barre fixe (mobile et ordinateur)", shot="s16", rows=[
   ("Comportement", "Apparaît (glissement 250 ms) dès que le bouton du hero sort de l'écran par le haut ; disparaît quand la boîte d'achat de l'offre est visible à 25 %, pour éviter le doublon."),
   ("Mise en page", "Fond blanc 97 % + flou, ombre vers le haut. Vignette 48 px · prix Fredoka 20 px + nom du kit en vert · bouton 52 px à droite. Marge basse = zone de sécurité de l'iPhone."),
   ("Interactions", "Le bouton ajoute le kit affiché et ouvre le tiroir panier. Le kit suit le choix fait dans l'offre."),
  ], copy=[("Contenu", "[vignette] 99 € · Kit Créatif · [Je veux mon Bobiko]")]),
 dict(id="S17", t="Tiroir panier", shot="s17", rows=[
   ("Comportement", "Panneau latéral droit (100 % de largeur sur mobile, 420 px sur ordinateur), fond assombri ; fermeture par croix, clic à côté ou touche Échap."),
   ("Contenu", "Titre de confirmation vert, ligne du kit, une seule suggestion (recharge 5 rouleaux), total, livraison offerte, bouton de paiement, paiements express."),
   ("Shopify", "Tiroir panier du thème + appli d'upsell limitée à 1 produit (recharges)."),
  ], copy=[("Titre", "✓ Ajouté au panier"), ("Suggestion", "Ajouter 5 rouleaux ? ≈ 300 stickers de plus, pour les vacances. [+ 25 €]"),
           ("Pied", "Total · ✓ Livraison offerte · expédié sous 24 h · [Je finalise ma commande →]")]),
]

import re as _re
_START = _re.compile(r"^(\d+[.)-]|-|\(\d\)|\d+-\d+ s:|BEFORE|AFTER|RÈGLE|Prompt|Keep|Brief|PAS DE|STYLE|PRODUCT|Printed|No text)")
def reflow(t):
    out = []
    for ln in t.split("\n"):
        ln = ln.strip()
        if not ln:
            continue
        if out and not _START.match(ln):
            out[-1] += " " + ln
        else:
            out.append(ln)
    return "\n".join(out)

def build():
    b = []
    b.append(cover("Proposition finale · Landing page", "Bobiko : la landing retenue, de A à Z",
                   "Identité, structure, textes, visuels et prompts d'images, dans l'ordre de la page",
                   "Préparé le 12 octobre 2026 pour la boutique Shopify Maison Ivy.<br>Document compagnon de « Bobiko : 36 décisions pour une page qui convertit ».<br>Maquette interactive : " + MOCKUP_URL))
    toc = [("part", "La proposition", None), ("", "1. La proposition en une page", "p1"), ("", "2. Identité visuelle et verbale", "p2"), ("", "3. Structure de la page", "p3"),
           ("part", "4. La page, section par section", None)]
    toc += [("", f'{s["id"]} · {s["t"]}', s["id"]) for s in SECTIONS]
    toc += [("part", "Production", None), ("", "5. Offre et prix détaillés", "p5"), ("", "6. Images : références, méthode et prompts", "p6"),
            ("", "7. Mise en place Shopify et performance", "p7"), ("", "8. Valeurs à valider avant la mise en ligne", "p8")]
    rows = "".join(f'<tr class="part"><td colspan="2">{e(n)}</td></tr>' if k == "part" else f'<tr><td>{e(n)}</td><td class="pg">{PAGES.get(a, "")}</td></tr>' for k, n, a in toc)
    b.append(f'<section class="chapter"><h1>Sommaire</h1><table class="toc">{rows}</table></section>')

    # 1
    b.append(chap("p1", "1", "La proposition en une page", "Une landing mobile d'abord, en 16 sections, qui prolonge la promesse des pubs : <b>« S'il peut le dire, ça l'imprime. »</b> Chaque section lève une objection, dans l'ordre où le parent se la pose."))
    b.append(f'''<div class="grid2" style="grid-template-columns:62mm 1fr;align-items:start">{shot("f-fold", cap="<b>Premier écran mobile</b> (iPhone 13, 390 × 844).")}
<div>{kv([("Marque", "<b>Bobiko</b> · slogan « S'il peut le dire, ça l'imprime. »"),
 ("Cible", "Parents (surtout mamans) d'enfants de 4 à 10 ans, France, Belgique, Suisse ; trafic Meta froid."),
 ("Promesse", "L'enfant dit une idée, la machine l'imprime en sticker en 5 secondes, il le colorie et le colle."),
 ("Offre", "Kit Découverte 79 € · <b>Kit Créatif 99 € (présélectionné)</b> · Kit Fratrie 149 € · livraison offerte · 3× sans frais."),
 ("Garanties", "Livraison 48-72 h · Garantie 2 ans · 30 jours satisfait ou remboursé · Réponse sous 24 h."),
 ("Ton", "Vouvoiement chaleureux ; l'humour vient des idées des enfants ; l'IA reste en coulisse."),
 ("Look", "Fond blanc et crème, corail pour l'action, jaune crayon pour les accents, encre pour le texte ; polices rondes ; stickers en trait noir coloriés à la main."),
 ("Boutons", "« Je veux mon Bobiko → » ×6 + barre fixe ; tiroir panier avec une suggestion de recharges."),
 ("Maquette", f'<a href="{MOCKUP_URL}">{MOCKUP_URL}</a> (bouton « Afficher les annotations »)')])}</div></div>''')
    b.append('<div class="box yellow"><b>Les crochets [ ] et les chiffres soulignés dans la maquette</b> signalent des valeurs à confirmer (partie 8). Rien ne doit être publié sans vérification : la page entière repose sur la confiance.</div></section>')

    # 2 identité
    b.append(chap("p2", "2", "Identité visuelle et verbale"))
    b.append(f'''<h2>2.1 Nom et slogan</h2>
{kv([("Nom", "<b>Bobiko</b> (B-o-b-i-k-o). Dans le texte : « Bobiko », majuscule. Dans le logo : « bobiko », minuscules."),
 ("Pourquoi", "Évoque la bobine de papier ; consonnes de l'avant vers l'arrière (B→K) qui aident la mémorisation ; sons ronds et doux ; 3 syllabes ; une seule orthographe."),
 ("Domaine", "Aucun changement : la page est publiée sur votre domaine actuel <b>maison-ivy.com</b> (par exemple maison-ivy.com/products/bobiko). Bobiko est une marque produit de Maison Ivy, pas un nouveau site. Réserver seulement les comptes @bobiko sur Instagram et TikTok si disponibles."),
 ("À faire avant usage", "Recherche INPI et EUIPO (classes 9, 16, 28), puis dépôt."),
 ("Slogan", "« S'il peut le dire, ça l'imprime. » · signature secondaire pour les pubs : « Une idée dite, un sticker tout de suite. »")])}
<h2>2.2 Logo</h2>
<div class="grid3" style="align-items:stretch">
<div class="box cream" style="display:grid;place-items:center;min-height:38mm;margin:0">{logo("34pt")}</div>
<div class="box ink" style="display:grid;place-items:center;min-height:38mm;margin:0">{logo("34pt", "#FFF6EC")}</div>
<div class="box yellow" style="display:grid;place-items:center;min-height:38mm;margin:0"><span style="width:22mm;height:22mm;display:block">{logo_o()}</span></div></div>
<p class="small muted" style="margin-top:2mm">Version principale sur crème · version inversée sur encre · icône (favicon, avatar, appli).</p>
{kv([("Construction", "« bobik » en Fredoka Bold, minuscules, approche −2 %. Le dernier « o » est une bulle de parole corail #FF5A36 (cercle + petite queue en bas à gauche). Son coin haut-droit est replié comme un sticker qu'on décolle : le rabat est rose pâle #FFE1D6 avec un fin contour corail action #E8431F. Sens : la parole devient un sticker."),
 ("Tailles", "En-tête mobile 30 px de haut ; minimum 20 px ; icône minimum 16 px (favicon)."),
 ("Zone de protection", "Hauteur d'un « o » autour du logo."),
 ("Interdits", "Pas d'ombre, pas de dégradé, pas de contour, pas de rotation, pas de logo en corail sur corail, jamais plus de 5 % de la hauteur du premier écran."),
 ("Fichiers", "assets/logo/bobiko-logo.svg, bobiko-logo-inverse.svg, bobiko-icone.svg (texte à vectoriser dans un éditeur avant l'impression).")])}''')
    sw = [("Corail", "#FF5A36", "Marque : logo, accents, icônes", "#fff"), ("Corail action", "#E8431F", "Boutons d'achat uniquement · blanc 4,0:1", "#fff"),
          ("Jaune crayon", "#FFC83D", "Badges, chiffres, promesse", "#1E1B2E"), ("Encre", "#1E1B2E", "Textes, bandeau, pied de page · 15,7:1 sur crème", "#FFF6EC"),
          ("Crème", "#FFF6EC", "Fonds de sections alternées", "#1E1B2E"), ("Bleu ciel", "#2F5BEA", "Liens, information · 5,5:1", "#fff"),
          ("Vert", "#1E8A5E", "Économies, « livraison offerte », succès", "#fff"), ("Gris texte", "#5F5870", "Texte secondaire · 5,3:1 sur crème", "#fff")]
    b.append('<h2>2.3 Couleurs</h2><div class="grid3" style="grid-template-columns:repeat(4,1fr);gap:3mm">' + "".join(
        f'<div class="swatch" style="background:{h};color:{t};{"border:.3mm solid #EADFD2;" if h=="#FFF6EC" else ""}"><b>{n}</b><span>{h}</span><span>{r}</span></div>' for n, h, r, t in sw) + '</div>')
    b.append('<p class="small" style="margin-top:2mm">Règle : le corail action n\'apparaît <b>que</b> sur ce qui fait acheter. Pas de rouge pour les erreurs : bleu ciel + icône. Les stickers restent noir et blanc, coloriés à la main en jaune, corail, bleu et vert (#2FA36E).</p>')
    b.append('<h2>2.4 Typographie</h2>' + table(["Rôle", "Police", "Mobile", "Ordinateur", "Usage"], [
        ["Titre H1", "Fredoka 700", "36 px / 1,05", "60 px", "Titre du hero uniquement"], ["Titre H2", "Fredoka 700", "28-30 px / 1,08", "42 px", "Titres de section, phrases complètes"],
        ["Titre H3", "Fredoka 600", "19-20 px", "20 px", "Cartes, étapes, packs"], ["Texte", "Nunito 400", "17 px / 1,55", "17 px", "Paragraphes, 65 caractères max."],
        ["Gras / labels", "Nunito 800", "13-15 px", "13-15 px", "Badges, assurances, surtitres (majuscules + 8 % d'espacement)"],
        ["Voix d'enfant", "Caveat 700", "22-23 px", "23 px", "Phrases d'enfants seulement"], ["Bouton", "Fredoka 600", "20 px", "20 px", "« Je veux mon Bobiko → »"]], widths=["16%", "16%", "18%", "14%", "36%"]))
    b.append(f'''<h2>2.5 Formes, boutons et icônes</h2>
{kv([("Arrondis", "12 px (petits éléments), 20 px (cartes), 28 px (médias, boîte d'achat), pilule pour boutons et badges."),
 ("Bouton principal", "Pilule pleine largeur (max 420 px), 58 px de haut, fond #E8431F, texte blanc Fredoka 600 20 px, flèche qui glisse de 4 px au survol, ombre « marche » de 6 px #D23714 qui s'écrase au clic."),
 ("Bouton secondaire", "Pilule contour encre 2 px, fond transparent, 52 px."),
 ("Cartes", "Fond blanc, bordure 1,5 px #EADFD2, sans ombre ; seule la boîte d'achat a une ombre douce."),
 ("Icônes", "Trait 2 px arrondi, 24 px, couleur encre ; dans une pastille jaune 48 px pour les bénéfices. Pas d'emoji dans l'interface."),
 ("Mouvement", "Vidéo du hero, pulsation du bouton (2×), glissement de la barre fixe et du tiroir. Rien d'autre ; tout est coupé si l'utilisateur a demandé moins d'animations.")])}
<h2>2.6 Direction photo et style des stickers</h2>
<ul><li>Scènes de maison françaises réelles, lumière du jour, vue à hauteur d'enfant, couleurs saturées mais naturelles.</li>
<li>Des mains d'enfant (main droite) qui touchent le produit ; visages expressifs (surprise, rire) qui regardent le sticker ou la machine, jamais le vide.</li>
<li>Le produit est toujours identique aux photos de référence ; aucun logo d'une autre marque.</li>
<li>Ralenti autorisé seulement pour le papier qui sort, jamais pour les personnes.</li>
<li>Les stickers montrés sont de vrais tirages : trait noir simple sur blanc, certains coloriés au crayon (hachures visibles).</li></ul>
<h2>2.7 Ton et lexique</h2>
{table(["Écrire", "Éviter", "Pourquoi"], [
 ["votre enfant, il invente, il colorie", "l'utilisateur, stimule, développe", "Concret et chaleureux ; pas de promesse non prouvée."],
 ["dès seulement 79 €, soit 0,17 € le sticker", "prix choc, promo folle, GRATUIT", "Mots de petitesse, sans excès."],
 ["sans encre, sans tablette", "ne tombe jamais en panne, 100 % sûr", "Positif et vérifiable."],
 ["Je veux mon Bobiko →", "ACHETEZ MAINTENANT !!!", "Bouton à la 1re personne, sans pression."],
 ["une intelligence artificielle conçue pour les enfants", "IA révolutionnaire, technologie de pointe", "L'IA explique, elle ne vend pas."],
 ["commandé avant le 18 décembre", "plus que 3 en stock, offre limitée", "Seule l'urgence réelle est permise."]], widths=["34%", "34%", "32%"])}
<h2>2.8 Emballage</h2>
<p>Boîte carrée à coins arrondis, corail mat avec bande jaune crayon, doodles noirs (dinosaure, chat astronaute, licorne) sur les côtés, logo sur le dessus. Elle se photographie pleine et ouverte (IMG-24) et sert d'argument « idée cadeau ». Concept à générer avec IMG-26 puis à confier au fournisseur.</p></section>''')

    # 3 structure
    st = [["S0", "Bandeau d'annonce", "Identité", "—", "—"], ["S1", "En-tête", "Identité", "—", "—"], ["S2", "Hero", "C'est pour moi ?", "Oui", "IMG-01, 02, 03, 04, 15, 24"],
          ["S3", "Bande de chiffres", "Je te crois ?", "—", "—"], ["S4", "Comment ça marche", "Je te crois ?", "—", "IMG-05, 06, 07"], ["S5", "Galerie d'idées", "C'est pour moi ?", "Oui", "IMG-08 à 13"],
          ["S6", "Bénéfices + vue éclatée", "Je te crois ?", "—", "IMG-14"], ["S7", "Offre : packs + achat", "Ça vaut le prix ? · Comment j'achète ?", "Oui (ajout)", "IMG-23"],
          ["S8", "Pourquoi c'est différent", "Je te crois ?", "—", "—"], ["S9", "Émotion et moments", "C'est pour moi ?", "Oui", "IMG-16 à 19"], ["S10", "Témoignages", "Je te crois ?", "Oui", "IMG-20 à 22"],
          ["S11", "Avis", "Je te crois ?", "—", "photos clients"], ["S12", "Promesse 30 jours", "Et si ça foire ?", "—", "—"], ["S13", "FAQ", "Et si ça foire ?", "—", "—"],
          ["S14", "Dernier appel", "Indécision", "Oui", "démo 30 s"], ["S15", "Pied de page", "Identité", "—", "—"], ["S16", "Barre fixe", "Comment j'achète ?", "Toujours (ajout)", "IMG-23"], ["S17", "Tiroir panier", "Comment j'achète ?", "Paiement", "IMG-23"]]
    thumbs = ""
    if SH:
        thumbs = '<div style="display:flex;gap:2mm;align-items:flex-start;margin:3mm 0">' + "".join(
            f'<figure style="margin:0;flex:1"><img class="shot" style="border-radius:1.5mm" src="file://{SH}/s{n:02d}.png"><figcaption style="text-align:center;font-size:6.5pt">S{n}</figcaption></figure>' for n in (2, 4, 5, 6, 7, 9, 11, 13)) + '</div>'
    b.append(chap("p3", "3", "Structure de la page", "16 sections et 2 mécaniques fixes. Fond blanc et crème en alternance pour marquer le rythme ; deux bandes de couleur (chiffres en encre, promesse en jaune) servent de repères au défilement."))
    b.append(table(["#", "Section", "Objection levée", "Bouton", "Visuels"], st, widths=["7%", "26%", "28%", "14%", "25%"]))
    b.append(thumbs + '<p class="small muted">Aperçu de quelques sections mobiles, dans l\'ordre.</p></section>')

    # 4 sections
    b.append(chap("p4", "4", "La page, section par section", "Pour chaque section : la capture mobile de la maquette, puis la spécification (objectif, mise en page mobile et ordinateur, visuels, interactions, mise en œuvre) et les textes exacts."))
    for i, s in enumerate(SECTIONS):
        brk = ' style="break-before:page"' if i and s["id"] in ("S4", "S6", "S7", "S8", "S10", "S11", "S13", "S16") else ""
        b.append(f'<div{brk}><h2>{mk(s["id"])}<span class="pill i">{s["id"]}</span> {e(s["t"])}</h2><div class="sec"><div class="pic">{shot(s["shot"])}</div><div>{kv(s["rows"])}<h4>Textes exacts</h4>{copy(s["copy"])}</div></div></div>')
    b.append("</section>")

    # 5 offre
    b.append(chap("p5", "5", "Offre et prix détaillés"))
    b.append(table(["", "Kit Découverte", "Kit Créatif ★", "Kit Fratrie"], [
        ["Contenu", "1 machine, 3 rouleaux, 6 crayons, guide", "1 machine, 10 rouleaux, 12 feutres, classeur, 6 crayons, guide", "2 machines, 10 rouleaux, 2 × 6 crayons, 2 guides"],
        ["Stickers (≈ 60 / rouleau)", "≈ 180", "≈ 600", "≈ 600"], ["Prix", "<b>79 €</b>", "<b>99 €</b>", "<b>149 €</b>"],
        ["Valeur des éléments séparés", "—", "135 €", "178 €"], ["Économie affichée", "—", "Vous économisez 36 €", "Vous économisez 29 €"],
        ["Prix unitaire affiché", "0,44 € le sticker", "0,17 € le sticker", "74,50 € la machine"], ["3 fois sans frais", "3 × 26,33 €", "3 × 33 €", "3 × 49,67 €"],
        ["Rôle", "Prix d'appel, montré dans le hero", "Pack visé, présélectionné", "Ancre haute, familles de 2 enfants"]], widths=["22%", "26%", "26%", "26%"]))
    b.append(table(["Article vendu seul (sur maison-ivy.com)", "Prix", "Remarque"], [
        ["Recharge 5 rouleaux (≈ 300 stickers)", "25 €", "Proposée dans le tiroir panier ; abonnement possible plus tard"],
        ["7 rouleaux (ligne de calcul)", "35 €", "Soit 5 € le rouleau, comme la recharge"], ["12 feutres lavables", "12 €", "Doit exister en fiche produit pour justifier l'ancrage"],
        ["Classeur à stickers", "9 €", "Idem"], ["Guide « 100 idées pour commencer »", "offert", "PDF + livret imprimé dans la boîte"]], widths=["44%", "12%", "44%"]))
    b.append('''<div class="box cream"><b>Règle légale.</b> Le total barré (135 €, 178 €) est la somme des prix auxquels chaque élément est réellement vendu seul. Aucun « prix habituel » barré tant que le produit n'a pas été vendu 30 jours à ce prix (directive Omnibus).</div>
<ul><li><b>Code de bienvenue</b> : −10 % contre l'e-mail, pop-up à l'intention de sortie sur ordinateur ; sur mobile après 45 s d'inactivité ou au retour arrière ; jamais à l'arrivée.</li>
<li><b>Livraison</b> : offerte partout (France, Belgique, Suisse), 48-72 h en France.</li>
<li><b>Noël</b> : date limite réelle affichée dans l'offre et la FAQ jusqu'au jour J, puis retirée.</li></ul></section>''')

    # 6 images
    b.append(chap("p6", "6", "Images : références, méthode et prompts", "Toutes les images de la page sont listées ici, avec l'identifiant utilisé dans la maquette. Les prompts sont en anglais, langue où les générateurs d'images sont les plus fiables."))
    b.append('<h2>6.1 Les photos de référence à fournir</h2><p>Les prompts s\'appuient sur ces photos du produit réel. Elles sont à joindre à chaque génération (champ « image de référence »).</p>' + table(["Réf.", "Sujet", "Comment la prendre"], REFS, widths=["11%", "24%", "65%"]))
    b.append('''<h2>6.2 Méthode</h2><ol>
<li><b>Outils.</b> Images : un générateur qui accepte des images de référence (Gemini « Nano Banana », GPT-Image, Flux Kontext, Midjourney avec référence d'objet). Vidéo : un modèle image-vers-vidéo (Veo, Kling, Runway) à partir de IMG-01.</li>
<li><b>Ordre.</b> Générer IMG-01 en premier. Une fois l'enfant validé, joindre IMG-01 comme référence de personnage pour IMG-02, 05, 07, 16 et 28 : c'est le même enfant partout.</li>
<li><b>Prompt.</b> Coller le prompt de l'image, puis le bloc de style commun (6.3). Générer 4 variantes, garder celle où la machine est la plus fidèle.</li>
<li><b>Contrôle produit.</b> Superposer l'image et REF-01 : forme, bouton, fente, couleur. Au moindre écart, corriger par une retouche ciblée (« keep everything, fix the printer to match the reference exactly »).</li>
<li><b>Post-production.</b> Les textes, logos et légendes s'ajoutent au montage, jamais dans la génération. Export WebP, 1 600 px de large maximum sur la page.</li></ol>
<div class="box yellow"><b>Honnêteté.</b> Les scènes peuvent être générées tant que le produit est fidèle. Trois catégories ne le sont jamais : les stickers de la galerie (vrais tirages), les témoignages et les photos d'avis (vrais clients). Le client compare ce qu'il reçoit avec ce qu'il a vu.</div>''')
    b.append(f'<h2>6.3 Bloc de style commun</h2><p>À ajouter à la fin de chaque prompt photo (sauf IMG-08 à 13 et 20 à 22).</p><div class="prompt">{e(reflow(STYLE))}</div><div class="neg"><b>Négatif / à éviter :</b> {e(NEG)}</div>')
    b.append('<h2>6.4 Les prompts, image par image</h2>')
    for im in IMAGES:
        post = f'<p class="post"><b>Post-production :</b> {e(im["post"])}</p>' if im.get("post") else ""
        b.append(f'''<div class="img-card"><h3>{mk("img"+im["id"])}<span class="pill c">{e(im["id"])}</span> {e(im["t"])}</h3>
<p class="meta"><b>Où :</b> {e(im["where"])} · <b>Format :</b> {e(im["fmt"])} · <b>Références jointes :</b> {e(im["refs"])}</p>
<div class="prompt">{e(reflow(im["p"]))}</div>{post}</div>''')
    b.append("</section>")

    # 7 shopify
    b.append(chap("p7", "7", "Mise en place Shopify et performance"))
    b.append(table(["Sujet", "Réglage"], [
        ["Domaine", "Domaine actuel maison-ivy.com conservé. La landing est la page produit Bobiko (ex. maison-ivy.com/products/bobiko), sur un modèle de page dédié : sans menu, sans lien vers les vêtements, logo Bobiko dans l'en-tête. Les pubs pointent directement sur cette URL."],
        ["Marque et confiance", "Pied de page « Bobiko, une marque Maison Ivy » ; mentions légales, CGV et e-mail au nom de Maison Ivy (bonjour@maison-ivy.com à créer, plutôt que l'adresse Gmail)."],
        ["Devise", "La boutique est en USD : activer Shopify Markets avec un marché Europe en EUR (prix fixés à 79, 99 et 149 €, pas de conversion automatique qui donnerait 78,63 €)."],
        ["Thème", "Dawn ou thème « one product » rapide ; un modèle de page produit dédié avec une section par bloc (S0-S15)."],
        ["Packs", "3 variantes ou appli de bundles ; Kit Créatif par défaut ; fiches séparées pour recharges, feutres, classeur (ancrage)."],
        ["Barre fixe et tiroir", "Barre fixe personnalisée (comportement S16) ; tiroir panier natif + upsell d'un seul produit."],
        ["Paiement", "Shopify Payments, Apple Pay, Google Pay, Shop Pay, PayPal ; Alma ou Klarna pour le 3×."],
        ["Avis", "Judge.me : demande d'avis 10 jours après livraison, filtres par mots-clés, photos."],
        ["Vitesse", "Poster du hero en WebP ≤ 180 Ko et préchargé ; vidéo ≤ 1,2 Mo chargée après ; autres images en chargement différé ; 3 polices en WOFF2 ; objectif LCP < 2,5 s en 4G."],
        ["Mesure", "Pixel Meta + API de conversions, GA4 : vue, clic 1er bouton (événement), défilement jusqu'à #offre, ajout au panier, début de paiement, achat."],
        ["Pages légales", "Mentions, CGV, livraison et retours, confidentialité avec la partie « données vocales », contact."]], widths=["22%", "78%"]))
    b.append("</section>")

    # 8 valeurs
    b.append(chap("p8", "8", "Valeurs à valider avant la mise en ligne", "Chaque valeur ci-dessous apparaît dans la page. Elle doit être confirmée sur l'échantillon ou par écrit par le fournisseur."))
    b.append(table(["Valeur", "Dans la page", "Où", "Comment vérifier"], [
        ["Stickers par rouleau", "≈ 60", "S2, S3, S6, S7, S13", "Compter sur 3 rouleaux de l'échantillon"],
        ["Temps d'impression", "5 s", "S2, S3, S4", "Chronométrer 10 idées en Wi-Fi domestique"],
        ["Dimensions / poids", "9,4 × 8,1 cm · 280 g", "S6", "Mesurer et peser"], ["Autonomie", "4 h", "S6", "Test d'impression continue"],
        ["Âge minimum", "Dès 4 ans", "S6, S13", "Marquage du fournisseur, EN 71"], ["Traitement de la voix", "Effacée, jamais conservée", "S13", "Réponse écrite du fournisseur + politique de confidentialité"],
        ["Wi-Fi et appli", "Réglage unique de 3 min", "S13", "Test sur l'échantillon"], ["Filtres de l'IA", "Demandes inadaptées filtrées", "S13", "Tester 20 demandes limites"],
        ["Certificats", "CE, EN 71, radio, batterie", "S6, S13", "Rapports de test du fournisseur"], ["Date limite Noël", "18 décembre", "S7, S13", "Délai transporteur + marge"],
        ["Note et nombre d'avis", "4,7/5 · [N]", "S2, S11", "Uniquement des avis réels ; masquer sous 10"],
        ["Témoignages", "3 exemples", "S10", "Remplacer par de vrais clients ou créateurs signalés"]], widths=["22%", "22%", "18%", "38%"]))
    b.append('<div class="box ink"><b>Avant de lancer les pubs :</b> repasser la grille 10/10 et les 12 règles du plan (document 1, partie 5), tester le parcours complet sur un téléphone jusqu\'au paiement, puis lancer le test A/B n°1 (titre).</div></section>')
    return page("Proposition finale · Landing Bobiko", EXTRA_CSS + "".join(b))

if __name__ == "__main__":
    open(sys.argv[3] if len(sys.argv) > 3 else "proposition.html", "w", encoding="utf-8").write(build())
