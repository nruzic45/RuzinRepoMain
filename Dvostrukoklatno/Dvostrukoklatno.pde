float m1=30;
float m2=30;
float r1=100;
float r2=100;
float a1=random(0,PI/2);
float a2=random(0,PI/2);
float a1_v=0;
float a2_v=0;
float a1_a=0;
float a2_a=0;
float g=0.981;
//boolean t=false;

float t1=-0.0001;
PGraphics canvas;

    
//int circleX, circleY;  // Position of circle button

//int circleSize = 50;   // Diameter of circle
//int circleColor, baseColor;
//color circleHighlight;
//color currentColor;

//boolean circleOver = false;












void setup()
{

size(500,560);

canvas = createGraphics(500,560);
canvas.beginDraw();
  canvas.background(255);
    canvas.endDraw(); 

 
 // circleColor = color(255);
 //circleHighlight = color(204);
 // baseColor = color(102);
 // currentColor = baseColor;
 // circleX = width-100-circleSize/2+10;
 // circleY = height-100;

//  ellipseMode(CENTER);    
    
    
   
    


}
void draw()//veliki ciklus, moze se koristiti kao vreme
{

 float del=(2*m1+m2-m2*cos(2*a1-2*a2));
 float deo1=-g*(2*m1+m2)*sin(a1);
  float deo3=-m2*g*sin(a1-2*a2);
   float deo5=-2*sin(a1-a2)*m2*((a2_v*a2_v)*r2+(a1_v*a1_v)*r1*cos(a1-a2));
   
   float deo2=2*sin(a1-a2);                
    float deo4=(a1_v*a1_v)*r1*(m1+m2)+g*(m1+m2)*cos(a1);                  
     float deo6=(a2_v*a2_v)*r2*m2*cos(a1-a2);
  
 a1_a=(deo1+deo3+deo5)/(del*r1); 
  
  a2_a=deo2*(deo4+deo6)/(del*r2);
  
   // update(mouseX, mouseY);
  //background(currentColor);
  
 
  
  //if (circleOver) {
  //  fill(circleHighlight);
 // } else {
 //   fill(circleColor);
//  }
 // stroke(0);
 // ellipse(circleX, circleY, circleSize, circleSize);
  
background(0,255,0);
 image(canvas,0,0);
 
 stroke(0);
 translate(250,150);
 float x1=sin(a1)*r1;
 float y1=cos(a1)*r1;
 line(0,0,x1,y1);
 ellipse(x1,y1,m1,m1);
 float x2=x1+sin(a2)*r2;
 float y2=y1+cos(a2)*r2;
 line(x1,y1,x2,y2);
 ellipse(x2,y2,m2,m2);
  
   
 a1_v+=a1_a;
 a2_v+=a2_a; 
 a1+=a1_v; //jedan frejm jedan unit vremena
 a2+=a2_v;
 //Trenje
if (a1_v>0)
{
 a1_v+=t1;
}
if (a2_v>0)
{
 a2_v+=t1;
}
  
 canvas.beginDraw();
  canvas.translate(250,150);
   canvas.strokeWeight(2);
canvas.stroke(0);
 canvas.point(x2,y2);
   canvas.endDraw();
 
 

}









//void update(int x, int y) {
//  if ( overCircle(circleX, circleY, circleSize) ) {
//   circleOver = true;
  
 // }  else {
 //   circleOver = false;
 // }
//}

//void mousePressed() {
  //if (circleOver) {
  //  currentColor = circleColor;
  //  boolean t=true;
//  }


//}

//boolean overCircle(int x, int y, int diameter) {
//  float disX = x - mouseX;
 // float disY = y - mouseY;
 // if (sqrt(sq(disX) + sq(disY)) < diameter/2 ) {t=true;
 //   return true;
 // } else { t=false;
 //   return false;
 // }
//}