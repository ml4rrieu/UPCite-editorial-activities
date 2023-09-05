import java.util.Collections;
Table table ; 

ArrayList<Journal> journals = new ArrayList<Journal>();

int margin ; 
color health, hhs, st; 

void setup() {
  size(1400, 800);
  background(255);

  // __0__ parse data to object instances
  table = loadTable("data-org-sci.csv", "header");
  //int nb_journals = table.getRowCount();

  IntDict publishers = new IntDict(); 

  for (TableRow row : table.rows()) {
    journals.add(new Journal (
      row.getString("publisher_1"), 
      row.getString("model_eco"), 
      row.getString("org_type"), 
      row.getString("nb \npersonne"), 
      row.getString("main_subject") 
      ));

    // calculer nb de journaux par publisher
    String publish = row.getString("publisher_1") ; 
    if ( publishers.hasKey(publish)) {
      publishers.increment(publish) ;
    } else publishers.set(publish, 1);
  }


  // var for graphic
  margin = 100 ;
  int jitterY = 5 ; 
  int jitterX = 4 ; 
  hhs = #47B39C;
  health = #EC6B56 ; 
  st = #FFC154 ; 

  // trier la liste des publisher du plus au moins important en quantité
  publishers.sortValuesReverse();


  // ___0___ calculer xspace pour chacun des publishers
  FloatList allxSpace = new FloatList() ; 

  //println("\npublishers\n\n", publishers);


// PARAM___ répartition des publishers sur X : si des publishers manquent ou s'il reste bcp de place, changer le 170 
  // xspace met en relation nb de revue et espace sur x
  for (int i = 0; i < publishers.size(); i ++) {
    allxSpace.append(
      map(i, 0, publishers.size(), 160, 1));
  }

  // passer xspace en cumulatif
  for (int i = 1; i < allxSpace.size(); i ++ ) {
    allxSpace.set(i, allxSpace.get(i-1) + allxSpace.get(i));
  }

  println("\n\nallxSpace\n\n", allxSpace);
  //println(allxSpace.sum());

  // affecter x à tous les journaux via les publishers
  for (int i = 0; i < publishers.size(); i++) {
    // du jitter uniquement si on a plusieurs revues
    if (publishers.value(i) < 3)  jitterX = 0;

    // affectation de la posx du journal 
    for (Journal item : journals) {
      if (item.publisher.equals(publishers.key(i))) {
        item.x =  allxSpace.get( i ) + random(-jitterX, jitterX)*10;
      }
    }
  }


  // ___1___ deduire les positions verticales
  for (Journal item : journals) {

    if (item.modeleEco.equals("Diamond"))item.y = margin*2 + (height-margin) * 0 + random(-jitterY, jitterY)*10 ;  
    if (item.modeleEco.equals("Gold APC")) item.y = margin*2 + (height-margin) * 1/4 + random(-jitterY, jitterY)*10;
    if (item.modeleEco.equals("Hybride")) item.y = margin*2 + (height-margin) * 2/4 + random(-jitterY, jitterY)*10;
    if (item.modeleEco.equals("Subscription")) item.y = margin*2 + (height-margin) * 3/4 + random(-jitterY, jitterY)*10;
  }

  // legende pour l'axe y

  textAlign(LEFT, CENTER);
  textSize(14);
  fill(90);
  text("Diamond", margin/10, margin*2 + (height - margin) * 0 ) ; 
  text("Gold APC", margin/10, margin*2 + (height - margin) * 1/4 ) ;
  text("Hybride", margin/10, margin*2 + (height - margin) * 2/4) ;
  text("Subscription", margin/10, margin*2 + (height - margin) * 3/4) ;


  // ___n___ deduire les tailles des cercles
  for (Journal item : journals) {
    // si aucune personne on indique un , afin d'afficher la revue
    if(item.nbPers.isEmpty()) item.nbPers = "1";
    item.size = map(float(item.nbPers), 0, 9, 14, 20);
  }

  // ___n___ deduire les couleurs des cercles
  for (Journal item : journals) {
    if (item.field.equals("Health")) item.c = health;
    if (item.field.equals("HSS")) item.c = hhs;
    if (item.field.equals("ST")) item.c = st ;
  }

  // legende sur l'axe x : nom des publishers
  textAlign(CENTER, CENTER);
  textSize(15);
  fill(40);
  for (String me : publishers.keys()) {
    // correspondante entre nb journals et taille des publishers
    int deduceTxtSize = round( 
      map(publishers.get(me), publishers.maxValue(), publishers.minValue(), 25, 17)
      );  
    textSize(deduceTxtSize);
    float posx = allxSpace.get( publishers.index(me) ) ; //- publisherWidth/2 ;
    pushMatrix();
    translate( posx, height/2 );// - margin/2);
    rotate(-PI/2);
    text(me, 0, 0);
    popMatrix();
  }



  // titre du graphique
  textSize(30);
  text("Mapping of scientific organisations journals by publisher, open access type and domain", 
    width/2, margin/5);
  textSize(15);
  textAlign(LEFT);
  //text("*journals managed by a learned society or a research laboratory", margin*0.35, margin*3/4);

  // legend for discipines
  textSize(25);
  noStroke();

  fill(#47B39C);
  //circle((width-margin*2)*1/3, margin*3/4, 20);
  text("HSS", width - 220, margin*3/4);

  fill(#EC6B56);
  //circle((width-margin*2) * 2/3, margin*3/4, 20);
  text("Health", width - 160, margin*3/4);

  fill(#FFC154);
  text("ST", width - 70, margin*3/4);


  for (Journal item : journals) item.draw();
  save("../mapping-learned-societies.png");

  println("nb journals", journals.size());
  println("nb of publisher", publishers.size());
}

void draw() {
  noLoop();
}



class Journal {
  String publisher;
  String modeleEco ; 
  String orgType; 
  String nbPers ; 
  String field ; 
  String eic ; 
  float x, y, size, xSpace, xMin, xMax; 
  color c; 


  Journal(String _publisher, String _modele, String _orgType, String _nbPers, String _field) {
    publisher = _publisher ; 
    modeleEco = _modele ; 
    orgType = _orgType ;
    nbPers = _nbPers ; 
    field = _field ; 
  }

  void draw() {
    noStroke();

    fill(c);
    circle(x, y, size);
  }
}
