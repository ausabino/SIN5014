//header

//#include<GL/gl.h>
#include<GL/glut.h>
#include<stdio.h>
#include<unistd.h>

//globals

GLuint elephant;
float elephantrot=0;
char ch='1';
char eixo;

//.obj loader

void loadObj(char *fname)
{
  FILE *fp; // cria um ponteiro arquivo
  int read;
  GLfloat x, y, z; //#
  char ch;
  elephant=glGenLists(1);//#
  fp=fopen(fname,"r"); //Abre um arquivo para leitura.

  if(!fp)
    {
      printf("nao pode abrir o arquivo %s\n", fname);
      exit(1);
    }
  glPointSize(5.0); // Tamanho do diametro do ponto
  glNewList(elephant, GL_COMPILE); // Define a lista de exibição
  {
    glPushMatrix(); // Essas rotinas push e pop podem ser legalmente armazenadas em cache em uma lista de exibição.
    glBegin(GL_POINTS);
    //glDisable(GL_POINT_SMOOTH);
    //glEnable(GL_POINT_SMOOTH);
    while(!(feof(fp)))
      {
        read=fscanf(fp,"%c %f %f %f",&ch,&x,&y,&z);
        if(read==4&&ch=='v')
          {
            glVertex3f(x,y,z); // recebe as coordenadas e desenha o objeto na janela.
          }
      }
    glEnd();
  }
  glPopMatrix(); // Essas rotinas push e pop podem ser legalmente armazenadas em cache em uma lista de exibição.
  glEndList();
  fclose(fp); // fecha arquivo
}

//O codigo do carregador .obj termina aqui

void reshape(int w,int h)
{
	glViewport(0,0,w,h); // Define a janela de Visualização é local onde a imagem será visualizada
	glMatrixMode(GL_PROJECTION); // Aplica operações de matriz subseqüentes à pilha de matriz de projeção.
	glLoadIdentity(); //#
  gluPerspective(60, (GLfloat)w / (GLfloat)h, 0.1, 1000.0);
	glMatrixMode(GL_MODELVIEW); //#
}

void drawObject()
{
 	glPushMatrix(); // Essas rotinas push e pop podem ser legalmente armazenadas em cache em uma lista de exibição.
 	glTranslatef(0,-40.00,-105); //Desenha o objeto descolado
 	glColor3f(1.0,0.63,0.27); // Mudar a cor dos pontos do objeto
 	glScalef(0.1,0.1,0.1); // Muda o tamanho do objeto
  if (eixo == 'X')
    glRotatef(elephantrot,1,0,0); //Gira o objeto a redor do eixo X
  else if (eixo == 'Y')
    glRotatef(elephantrot,0,1,0); //Gira o objeto a redor do eixo Y
  else if (eixo == 'Z')
    glRotatef(elephantrot,0,0,1); //Gira o objeto a redor do eixo Z
  else
    {
      printf("Entrada Invalida!\n");
      exit(EXIT_FAILURE);
    }
 	glCallList(elephant);
 	glPopMatrix(); // Essas rotinas push e pop podem ser legalmente armazenadas em cache em uma lista de exibição.
 	elephantrot=elephantrot+6.0;
 	if(elephantrot>360)elephantrot=elephantrot-360; // Gira o objeto em 360 graus

}

void display(void)
{
  glClearColor (0.0,0.0,0.0,1.0); // Define a cor de fundo da janela de visualização como preta
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);//Limpa a janela de visualização com a cor de fundo especificada
  glLoadIdentity();//#
  drawObject(); // função projetada para definir a exibicao do objeto
  glutSwapBuffers(); //trocar os buffers
  usleep( 100 * 1000);            /* Atualização da imagem em milisegundos Max 10^6 */

}

int main(int argc,char **argv)
{
  printf("Digite X, Y ou Z de acordo com o eixo que deseja ver o objeto rotacionar: ");
  scanf("%c", &eixo);
	glutInit(&argc,argv); //glutInit é usado para inicializar a biblioteca GLUT.
	glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB|GLUT_DEPTH); // GLUT_DOUBLE  Este método é geralmente utilizado para produzir efeitos de animação
	glutInitWindowSize(800,600);  //Define tamanho da janela.
	glutInitWindowPosition(10,10); // Define a posicao da janela.
	glutCreateWindow("Carregar Objeto");// Cria uma janela com o nome "Nome do programa".
	glutReshapeFunc(reshape); //#
  glutDisplayFunc(display); //#
	glutIdleFunc(display); //#
  //loadObj("data/elepham.obj");// busca o arquivo tipo objeto
  loadObj("elepham.obj");// busca o arquivo tipo objeto
	glutMainLoop(); //#
	return 0;

}

// para compilar..
//gcc objloaderelephant.c -o teste -lglut -lGL -lGLU
