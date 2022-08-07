class telo
{
  double m, x, y;


  telo(double masa, double px, double py)
  {
    m = masa;
    x = px;
    y = py;
  }

  void Draw(double rcrt)
  {
    ellipse((float)(x/skala+750), (float)(y/skala+400), (float)rcrt, (float)rcrt);
  }
}

int runTime = 3000;

double vreme = 0;
double gen5 = 0;

double r = 384400000.0;
double rzem = 6700000.0;
double skala = 2600000;
double gamma = (double) -6.7e-11;

telo zemlja = new telo(5.97e24, 0, 0);
telo mesec = new telo(7.342e24, r, 0);

double kolicinaUranijuma = 0.05;
double theta = 0;
double omega = 0.26 * (double)10e-5;
double tmax = 1000000;
double t = 0;
double dt = 150;




double Cubed(double a)
{
  return a * a * a;
}

double sqr(double a)
{
  return a*a;
}

class DNK
{
  double genes[] = new double[6];


  DNK VodjenjeLjubavi(DNK svaler)
  {
    DNK deriste = new DNK();

    deriste.genes[0] = 0.5 > random(1) ? svaler.genes[0] : this.genes[0];
    deriste.genes[1] = 0.5 > random(1) ? svaler.genes[1] : this.genes[1];
    deriste.genes[2] = 0.5 > random(1) ? svaler.genes[2] : this.genes[2];
    deriste.genes[3] = 0.5 > random(1) ? svaler.genes[3] : this.genes[3];
    deriste.genes[4] = 0.5 > random(1) ? svaler.genes[4] : this.genes[4];
    deriste.genes[5] = 0.5 > random(1) ? svaler.genes[5] : this.genes[5];

    return deriste;
  }

  void chernobil()
  {
    for (int i = 0; i < 4; i++)
    {
      genes[i] = random(1) < kolicinaUranijuma ? random(-10000, 10000) : genes[i];
    }

    genes[4] = random(1) < kolicinaUranijuma ? random(0, runTime) : genes[4];
  }
}

class raketa
{
  double x = 3*rzem;
  double y = 3*rzem;
  double vx;
  double vy;
  double ax, ay;
  double tx, ty;
  double tt;
  double fitness;
  boolean trosen = false;
  boolean skrsen = false;

  raketa(double spdx, double spdy, double thrx, double thry, double tht, double Theta)
  {
    x = 2*rzem*cos((float)Theta);
    y = 2*rzem*sin((float)Theta);
    vx = spdx;
    vy = spdy;
    tx = thrx;
    ty = thry;
    tt = tht;
  }

  void Draw()
  {
    rect((float)(x/skala+750), (float)(y/skala+400), 2, 2);
  }
}

ArrayList<raketa> populus = new ArrayList<raketa>();

void setup()

{
  size(1500, 800);
  noStroke();
  rectMode(CENTER);
  ellipseMode(CENTER);

  for (int i = 0; i < 1000; i++)
  {
    populus.add(new raketa(random(-10000, 10000), random(-10000, 10000), random(-10000, 10000), random(-10000, 10000), random(0, runTime), random(2*PI)));
  }
}

int i = 0;
void draw()
{
  //if (gen5 == 0 || gen5 == 5 || gen5 == 10 || gen5 == 50)
  //{
 //   if (frameCount%2 == 0)
     // saveFrame("gen" + gen5 + "/slika-####.tif");
  //}
  background(0);
  vreme++;
  zemlja.Draw(20);
  mesec.Draw(10);
  mesec.x = (double)(r * cos((float)theta));
  mesec.y = (double)(r * sin((float)theta));

  for (raketa r : populus)
  {

    if (!r.skrsen)
    {
      if (vreme > r.tt && !r.trosen)
      {
        r.trosen = true;
        r.vx += r.tx;
        r.vy += r.ty;
      }
      r.ax = gamma * (r.x - zemlja.x) * zemlja.m / Cubed(sqrt((float)(sqr(r.x - zemlja.x) + sqr(r.y - zemlja.y))));
      r.ay = gamma * (r.y - zemlja.y) * zemlja.m / Cubed(sqrt((float)(sqr(r.x - zemlja.x) + sqr(r.y - zemlja.y))));
      r.ax += gamma * (r.x - mesec.x) * mesec.m / Cubed(sqrt((float)(sqr(r.x - mesec.x) + sqr(r.y - mesec.y))));
      r.ay += gamma * (r.y - mesec.y) * mesec.m / Cubed(sqrt((float)(sqr(r.x - mesec.x) + sqr(r.y - mesec.y))));
      r.vx += r.ax * dt;
      r.vy += r.ay * dt;
      r.x += r.vx * dt;
      r.y += r.vy * dt;
      if ((sqrt(sq((float)r.x)+sq((float)r.y)) < 6700000) || 2000000 > sqrt(sq((float)(mesec.x - r.x) + sq((float)(mesec.y - r.y)))))
      {
        r.skrsen = true;
      }
      r.Draw();
    }
  }
  theta += omega*dt;

  if (frameCount%runTime==0)
  {
    gen5++;

    println(populus.get(5).tt);
    println(populus.get(13).tt);
    vreme = 0;
    theta = 0;
    double sumaFit = 0;
    double maxFit = 0;
    for (raketa r : populus)
    {
      //r.fitness = 1/(sqr(mesec.x-r.x) + sqr(mesec.y - r.y));
      r.fitness = 1/(sqr(mesec.x-r.x) + sqr(mesec.y - r.y));
      if (r.fitness > maxFit)
      {
        maxFit = r.fitness;
      }
      sumaFit += r.fitness;
    }
    println(sumaFit);
    for (raketa r : populus)
    {
      r.fitness /= sumaFit;
      if (r.skrsen == true)
      {
        r.fitness = 0;
      }
    }


    ArrayList<DNK>BazenZaSponzoruse=new ArrayList<DNK>();


    for (raketa r : populus)
    {

      int N=(int)(r.fitness*1000);
      for (i=0; i<N; i++)
      {
        DNK geniRakete = new DNK();
        geniRakete.genes[0] = r.vx;
        geniRakete.genes[1] = r.vy;
        geniRakete.genes[2] = r.tx;
        geniRakete.genes[3] = r.ty;
        geniRakete.genes[4] = r.tt;

        BazenZaSponzoruse.add(geniRakete);
      }
    }

    populus = new ArrayList<raketa>();
    for (i = 0; i < 1000; i++)
    {
      int cale=int(random(BazenZaSponzoruse.size()));
      int keva=int(random(BazenZaSponzoruse.size()));

      DNK rodcale = BazenZaSponzoruse.get(cale);
      DNK rodkeva = BazenZaSponzoruse.get(keva);
      //cale+keva=retard(Jbg nisam savrsen)*def. 1
      //cale+keva=retard(mama mi kaze da sam poseban)*def.2
      DNK retard=rodkeva.VodjenjeLjubavi(rodcale);
      retard.chernobil();
      populus.add(new raketa(retard.genes[0], retard.genes[1], retard.genes[2], retard.genes[3], retard.genes[4], random(2*PI)));
    }
  }
}
