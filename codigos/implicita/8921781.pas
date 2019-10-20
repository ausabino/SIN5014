{ Copyright (C) 2004 Mattias Gaertner

  Example for loading and saving jpeg images.
  
  Important:
    This example uses the JPEGForLazarusPackage (see in the directory above).
    You must first open once this package so that the IDE knows, where to find
    the lpk file.
    
  See the README.txt.


  This program is free software; you can redistribute it and/or modify it
  under the terms of the GNU General Public License as published by the Free
  Software Foundation; either version 2 of the License, or (at your option)
  any later version.

  This program is distributed in the hope that it will be useful, but WITHOUT
  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
  FITNESS FOR A PARTICULAR PURPOSE. See the GNU Library General Public License
  for more details.

  You should have received a copy of the GNU General Public License along with
  this program; if not, write to the Free Software Foundation, Inc., 59 Temple
  Place - Suite 330, Boston, MA 02111-1307, USA.
}
unit MainForm;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, LResources, Forms, Controls, Graphics, Dialogs, StdCtrls,
  ExtCtrls, Buttons, ExtDlgs,Math;

type

  { TJPEGExampleForm }

  TJPEGExampleForm = class(TForm)
    Button1: TButton;
    Button2: TButton;
    save: TButton;
    OpenPictureDialog1: TOpenPictureDialog;
    ImageGroupBox: TGroupBox;
    Image1: TImage;
    save1: TButton;
    SavePictureDialog1: TSavePictureDialog;
    procedure Button1Click(Sender: TObject);
    procedure Button2Click(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure LoadJPEGButtonClick(Sender: TObject);
    procedure LoadImageButtonClick(Sender: TObject);
    procedure saveClick(Sender: TObject);
    procedure SaveJPEGButtonClick(Sender: TObject);
    procedure SaveImageButtonClick(Sender: TObject);
  private
    procedure UpdateInfo(const Filename: string);
  end;

var
  JPEGExampleForm: TJPEGExampleForm;

implementation

{ TJPEGExampleForm }

procedure plotaEixos;
var w,h,xstep,ystep,i:integer;

begin

  h := JPEGExampleForm.Image1.Height;
  w:= JPEGExampleForm.Image1.Width;
  xstep := w div 10;
  ystep := h div 10;
  JPEGExampleForm.Image1.Canvas.Line(w div 2,0,w div 2,h);
  JPEGExampleForm.Image1.Canvas.Line(0,h div 2,w ,h div 2);
  JPEGExampleForm.Image1.Canvas.TextOut(w div 2 +3,h div 2 +3,'0');
  for i:=1 to 4 do
    begin
        JPEGExampleForm.Image1.Canvas.Line(w div 2 -5 ,(h div 2) -i*ystep,w div 2+5, (h div 2) -i*ystep);
        JPEGExampleForm.Image1.Canvas.TextOut(w div 2 +4,(h div 2) -i*ystep +1,inttostr(i));
        JPEGExampleForm.Image1.Canvas.Line(w div 2 -5 ,(h div 2) +i*ystep,w div 2+5, (h div 2) +i*ystep);
        JPEGExampleForm.Image1.Canvas.TextOut(w div 2 +4,(h div 2) +i*ystep +1,inttostr(-i));
        JPEGExampleForm.Image1.Canvas.Line((w div 2) -i*xstep ,h div 2 -5,(w div 2) -i*xstep, h div 2 +5);
        JPEGExampleForm.Image1.Canvas.TextOut((w div 2) -i*xstep +4,h div 2 +1,inttostr(-i));
        JPEGExampleForm.Image1.Canvas.Line((w div 2) +i*xstep ,h div 2 -5,(w div 2) +i*xstep, h div 2 +5);
                JPEGExampleForm.Image1.Canvas.TextOut((w div 2) +i*xstep +4,h div 2 +1,inttostr(i));
      end;

end;

function  f(x,y:real):real ;
begin
  //f:= x*x+y*y-4;
  //f:= x*x-y*y-4;
  f:=ln(1+x*x+y*y)+sin(x+y)-1;
end;
function xToInteger(x:real):integer;
var w,xstep:integer;
begin
 w:= JPEGExampleForm.Image1.Width;
  xstep := w div 10;

  xToInteger := w div 2 +round(x*xstep);
end;

function yToInteger(y:real):integer;
var h,ystep,aux:integer;
begin
 h:= JPEGExampleForm.Image1.Height;
  ystep := h div 10;
  aux:=round(y*ystep);
  yToInteger := h-(h div 2 +aux);
end;

procedure plotCruveImp;
var x, y, step, val1, val2, val3:real;
begin
  x := -5;
  step := 0.01;
  while (x < 5) do
  begin
    y := -5;
    while(y < 5) do
    begin
      val1 := f(x,y) * f(x+step,y);
      val2 := f(x+step,y) * f(x+step, y+step);
      val3 := f(x,y) * f(x+step,y+step);
      if((val1 <= 0) and (val2 <= 0)) then
      begin
        JPEGExampleForm.Image1.Canvas.Line(xToInteger((x+x+step)/2),yToInteger(y),xToInteger(x+step),yToInteger((y+y+step)/2));
      end;
      if((val2 <= 0) and (val3 <= 0)) then
      begin
        JPEGExampleForm.Image1.Canvas.Line(xToInteger(x+step),yToInteger((y+y+step)/2),xToInteger((x+x+step)/2),yToInteger((y+y+step)/2));
      end;
      if((val1 <= 0) and (val3 <= 0)) then
      begin
        JPEGExampleForm.Image1.Canvas.Line(xToInteger((x+x+step)/2),yToInteger(y),xToInteger((x+x+step)/2),yToInteger((y+y+step)/2));
      end;
      val1 := f(x,y) * f(x,y+step);
      val2 := f(x,y+step) * f(x+step, y+step);
      if ((val1 <= 0) and (val2 <= 0)) then
      begin
        JPEGExampleForm.Image1.Canvas.Line(xToInteger(x),yToInteger((y+y+step)/2),xToInteger((x+x+step)/2),yToInteger(y+step));
      end;
      if ((val2 <= 0) and (val3 <= 0)) then
      begin
        JPEGExampleForm.Image1.Canvas.Line(xToInteger((x+x+step)/2),yToInteger(y+step),xToInteger((x+x+step)/2),yToInteger((y+y+step)/2));
      end;
      if ((val1 <= 0) and (val3 <= 0)) then
      begin
        JPEGExampleForm.Image1.Canvas.Line(xToInteger(x),yToInteger((y+y+step)/2),xToInteger((x+x+step)/2),yToInteger((y+y+step)/2));
      end;
      y := y + step;
    end;
    x := x + step;
  end;
end;

procedure plotCruveExp;
var t,pi,step,x,y,xnext,ynext,r:real;
begin
 pi:= 3.14159;
t:=0.0;
step:=0.1;
r:=2.0;
JPEGExampleForm.Image1.Canvas.Pen.Color:=RGBToColor(255,0,0);
while   (t<(2*pi)) do
begin
      x:=r*cos(t);
      y:=r*sin(t);
      xnext:=r*cos(t+step);
      ynext:=r*sin(t+step);
      JPEGExampleForm.Image1.Canvas.Line(xToInteger(x),yToInteger(y),xToInteger(xnext),yToInteger(ynext));
      t:=t+step;
end;
end;

procedure TJPEGExampleForm.LoadJPEGButtonClick(Sender: TObject);
var
  JPEG: TJPEGImage;
begin
  OpenPictureDialog1.Options:=OpenPictureDialog1.Options+[ofFileMustExist];
  if not OpenPictureDialog1.Execute then exit;
  try
    //--------------------------------------------------------------------------
    // Create a TJPEGImage and load the file, then copy it to the TImage.
    // A TJPEGImage can only load jpeg images.
    JPEG:=TJPEGImage.Create;
    try
      JPEG.LoadFromFile(OpenPictureDialog1.Filename);
      // copy jpeg content to a TImage
      Image1.Picture.Assign(JPEG);
    finally
      JPEG.Free;
    end;
    //--------------------------------------------------------------------------
    UpdateInfo(OpenPictureDialog1.Filename);
  except
    on E: Exception do begin
      MessageDlg('Error','Error: '+E.Message,mtError,[mbOk],0);
    end;
  end;
end;

procedure TJPEGExampleForm.Button1Click(Sender: TObject);

begin
  Image1.Canvas.Brush.Color:=RGBToColor(255,255,255); // this will not create a new brush handle
  Image1.Canvas.FillRect(1,1,Image1.Width,Image1.Height); // this will create the brush handle with the currently active theme brush for hint windows
  Image1.Canvas.Pen.Color:=RGBToColor(0,0,0);
    plotaEixos;
    plotCruveImp;
end;

procedure TJPEGExampleForm.Button2Click(Sender: TObject);
begin
   Image1.Canvas.Brush.Color:=RGBToColor(255,255,255); // this will not create a new brush handle
   Image1.Canvas.FillRect(1,1,Image1.Width,Image1.Height); // this will create the brush handle with the currently active theme brush for hint windows
     plotaEixos;
     plotCruveExp;
end;

procedure TJPEGExampleForm.FormCreate(Sender: TObject);
begin

end;

procedure TJPEGExampleForm.LoadImageButtonClick(Sender: TObject);
begin
  OpenPictureDialog1.Options:=OpenPictureDialog1.Options+[ofFileMustExist];
  if not OpenPictureDialog1.Execute then exit;
  try
    //--------------------------------------------------------------------------
    // Loading directly into a TImage. This will load any registered image
    // format. .bmp, .xpm, .png are the standard LCL formats.
    // The jpeg units register .jpeg and .jpg.
    Image1.Picture.LoadFromFile(OpenPictureDialog1.Filename);
    //--------------------------------------------------------------------------

    UpdateInfo(OpenPictureDialog1.Filename);
  except
    on E: Exception do begin
      MessageDlg('Error','Error: '+E.Message,mtError,[mbOk],0);
    end;
  end;
end;

procedure TJPEGExampleForm.saveClick(Sender: TObject);

begin
Application.Terminate;
end;

procedure TJPEGExampleForm.SaveJPEGButtonClick(Sender: TObject);
var
  JPEG: TJPEGImage;
begin
  if Image1.Picture.Graphic=nil then begin
    MessageDlg('No image','Please open an image, before save',mtError,
      [mbOk],0);
    exit;
  end;
  
  SavePictureDialog1.Options:=SavePictureDialog1.Options+[ofPathMustExist];
  if not SavePictureDialog1.Execute then exit;
  try
    //--------------------------------------------------------------------------
    // Create a TImage1 and copy the TImage into it. Then save to file.
    // This will ignore the file extension. TImage1 will always save as jpeg.
    JPEG:=TJPEGImage.Create;
    try
      // copy content of the TImage to jpeg
      JPEG.Assign(Image1.Picture.Graphic);
      // save to file
      JPEG.SaveToFile(SavePictureDialog1.Filename);
    finally
      JPEG.Free;
    end;
    //--------------------------------------------------------------------------

    UpdateInfo(SavePictureDialog1.Filename);
  except
    on E: Exception do begin
      MessageDlg('Error','Error: '+E.Message,mtError,[mbOk],0);
    end;
  end;
end;

procedure TJPEGExampleForm.SaveImageButtonClick(Sender: TObject);
begin
  if Image1.Picture.Graphic=nil then begin
    MessageDlg('No image','Please open an image, before save',mtError,
      [mbOk],0);
    exit;
  end;

  SavePictureDialog1.Options:=SavePictureDialog1.Options+[ofPathMustExist];
  if not SavePictureDialog1.Execute then exit;
  try
    //--------------------------------------------------------------------------
    // Saving directly from a TImage to a file. This will save in any registered
    // image format. .bmp, .xpm, .png are the standard LCL formats.
    // The jpeg units register .jpeg and .jpg.
    // So, saving as file1.jpg will save as jpeg, while saving a file1.bmp will
    // save as bmp.
    Image1.Picture.SaveToFile(SavePictureDialog1.Filename);

    //--------------------------------------------------------------------------

    UpdateInfo(SavePictureDialog1.Filename);
  except
    on E: Exception do begin
      MessageDlg('Error','Error: '+E.Message,mtError,[mbOk],0);
    end;
  end;
end;

procedure TJPEGExampleForm.UpdateInfo(const Filename: string);
var
  Info: String;
begin
  if Image1.Picture.Graphic<>nil then begin
    Info:=Image1.Picture.Graphic.ClassName+':'+Filename;
  end else begin
    Info:=Filename;
  end;
  ImageGroupBox.Caption:=Info;
end;

initialization
  {$I mainform.lrs}

end.

