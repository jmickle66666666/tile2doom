import random, math, omg
from scipy.spatial import ConvexHull

width = 9000
height = 2000
num_locpoints = 200
num_points = 4000

def r8int(low,high):
    r = random.randint(low,high)
    r = int(r/8)
    r *= 8
    return r

class Locpoint(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.points = []
        self.hull = None
        #dist = math.sqrt(((width/2) - x)**2 + ((height/2) - y)**2)
        dist = abs(y - (height/2))
        self.sector = omg.mapedit.Sector(z_ceil=512,tx_ceil="F_SKY1",z_floor=r8int(int(dist / 6),int(dist/4))+8,tx_floor="RROCK03",light=256)


locpoints = []
for i in range(num_locpoints):
    locpoints.append(Locpoint(random.randint(0,width),random.randint(0,height)))

def nearest_locpoint(p):
    def distance(p0, p1):
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

    ndist = width*height
    nn = None
    for n in locpoints:
        if distance(p,(n.x,n.y)) < ndist:
            nn = n
            ndist = distance(p,(n.x,n.y))
    return nn


for i in range(num_points):
    p = (random.randint(0,width),random.randint(0,height))
    np = nearest_locpoint(p)
    np.points.append(p)

omap = omg.mapedit.MapEditor()

omap.sectors.append(omg.mapedit.Sector(z_ceil=512,tx_ceil="F_SKY1",tx_floor="LAVA1",light=256))

omap.vertexes.append(omg.mapedit.Vertex(x=-32,y=height+32))
omap.vertexes.append(omg.mapedit.Vertex(x=width+32,y=height+32))
omap.vertexes.append(omg.mapedit.Vertex(x=width+32,y=-32))
omap.vertexes.append(omg.mapedit.Vertex(x=-32,y=-32))
omap.sidedefs.append(omg.mapedit.Sidedef(tx_mid="SP_ROCK1",sector=0))
omap.linedefs.append(omg.mapedit.Linedef(front=0,vx_a=0,vx_b=1))
omap.linedefs.append(omg.mapedit.Linedef(front=0,vx_a=1,vx_b=2))
omap.linedefs.append(omg.mapedit.Linedef(front=0,vx_a=2,vx_b=3))
omap.linedefs.append(omg.mapedit.Linedef(front=0,vx_a=3,vx_b=0))

for l in locpoints:
    if len(l.points) > 2:
        l.hull = ConvexHull(l.points)
        verts = []
        for v in l.hull.vertices.tolist():
            point = l.hull.points[v].tolist()
            verts.append( (point[0],point[1]) )
        sect = l.sector
        omap.draw_sector(verts,sector=sect)

bsid = omg.mapedit.Sidedef(tx_low="SP_ROCK1",sector=0)
omap.sidedefs.append(bsid)
bsidid = len(omap.sidedefs)-1

for i in range(4,len(omap.linedefs)):
    line = omap.linedefs[i]
    line.back = bsidid
    line.impassable = False
    line.two_sided = True

#things

omap.things.append(omg.mapedit.Thing(type=1,x=int(width/2),y=int(height/2)))

decor = [47,43,41,54,79,81,31,27]

for i in range(200):
    omap.things.append(omg.mapedit.Thing(type=random.choice(decor),x=random.randint(0,width),y=random.randint(0,height)))

wad = omg.WAD()
wad.maps["MAP01"] = omap.to_lumps()
wad.to_file("test.wad")

