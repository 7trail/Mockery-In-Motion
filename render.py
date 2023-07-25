from vapory import *
from moviepy.editor import VideoClip

def sceneBasic(cameraPosition,c1image,c2image,c3image,characters=2,lookAt=[0,0,0]):
  """ Returns the scene at time 't' (in seconds) """
  objects = [
    LightSource([2, 4, -3], 'color', [1.5, 1.5, 1.5]),
    Background("color", [1, 1, 1]),
    Box([1,1,1],[0,0,0],Texture( Pigment( ImageMap("jpeg",'"grass.jpg"'))),'rotate',[0,90,0],'translate',[0,-1,0],'scale',[10,10,101])
  ]

  objects.append(Box([1,1,0.01],[0,0,-0.01],Texture( Pigment( ImageMap("png",f'"{c1image}"','once'))),'rotate',[0,-30,0],'translate',[-1,0,0]))

  objects.append(Box([1,1,0.01],[0,0,-0.01],Texture( Pigment( ImageMap("png",f'"{c2image}"','once'))),'rotate',[0,30,0],'translate',[1,0,0]))
  if characters > 2:
    objects.append(Box([1,1,0.01],[0,0,-0.01],Texture( Pigment( ImageMap("png",f'"{c3image}"','once'))),'rotate',[0,0,0],'translate',[0,0,1]))
  #for i in range(5):
  #  x,y = sin(t*i), cos(t*i)
  #  objects.append(Sphere( [x*i/2,y*i/2,0] , 0.25+(i/20),  color([.5, .5, .9])))
  return Scene(Camera('location', cameraPosition, 'look_at', lookAt), objects)

def make_frame(scene,fileName):
    im= scene.render(fileName,width = 800, height=400, quality=1)
    return True

#VideoClip(make_frame, duration=1).write_gif("anim.gif",fps=4)