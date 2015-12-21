import omg, random
from PIL import Image

owad = None
omap = None

def image_to_tiles(img):
    pix = img.load()
    output = [[-1 for y in range(img.size[0])] for x in range(img.size[1])]
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pix[i,j] == (0,0,0):
                output[i][j] = 0
    return output
    
def gentiles():
    width = 30
    height = 30
    tiles = [[-1 for y in range(width)] for x in range(height)]
    def digger(i,j):
        length = 80
        sid = random.choice([0,1,2,3])
        while length > 0:
            tiles[i][j] = 0
            tiles[i+1][j] = 0
            tiles[i][j+1] = 0
            tiles[i+1][j+1] = 0
            length -= 1
            if sid == 0: i += 1
            if sid == 1: j -= 1
            if sid == 2: i -= 1
            if sid == 3: j += 1
            if random.choice([0,0,0,1]) == 1:
                sid += random.choice([-1,1])
                if sid == 4: sid = 0
                if sid == -1: sid = 3
        return (i,j)
    last = digger(15,15)

    for i in range(1, width-1):
        for j in range(1, height-1):
            if tiles[i][j] == -1:
                if tiles[i+1][j] == 0: tiles[i][j] = 1
                if tiles[i-1][j] == 0: tiles[i][j] = 1
                if tiles[i][j+1] == 0: tiles[i][j] = 1
                if tiles[i][j-1] == 0: tiles[i][j] = 1

    return tiles

def tile2doom(tiles):
    player_placed = 0

    sectors = []
    sidedefs = []
    sidedefs.append(omg.mapedit.Sidedef(tx_mid="METAL2"))
    sidedefs.append(omg.mapedit.Sidedef(tx_mid="METAL2"))
    sectors.append(omg.mapedit.Sector(tx_ceil="F_SKY1",z_ceil=136))
    sectors.append(omg.mapedit.Sector(z_floor=64,light=192))

    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            if tiles[i][j] != -1:
                if player_placed == 0:
                    player_placed = 1
                    omap.things.append(omg.mapedit.Thing(x=(i*32)+16,y=(j*32)+16,type=1))
                verts = []
                verts.append((i * 32, j * 32))
                verts.append(((i+1) * 32, j * 32))
                verts.append(((i+1) * 32, (j+1) * 32))
                verts.append((i * 32, (j+1) * 32))
                omap.draw_sector(verts,sector=sectors[tiles[i][j]],sidedef=sidedefs[tiles[i][j]])

    owad.maps["MAP01"] = omap.to_lumps()

if __name__=="__main__":
    owad = omg.WAD()
    omap = omg.mapedit.MapEditor()
    #tile2doom(image_to_tiles(Image.open("test.png")))
    tile2doom(gentiles())
    owad.to_file("test.wad")