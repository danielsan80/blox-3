import blox.config as config

def mv(point, pos=(0,0,0), step = config.mv_step ):
    return (
        point[0]+pos[0]*step,
        point[1]+pos[1]*step,
        point[2]+pos[2]*step
    )