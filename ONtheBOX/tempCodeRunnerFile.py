floor=[]
for i in range(0,LENGTH,BLOCKSIZE):
    jerry=Stuff(screen,i,HEIGHT-BLOCKSIZE,32,32,os.path.join(BASE_DIR, "lands", "forestland.jpeg"))
    floor.append(jerry)
