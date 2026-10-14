"""
Builds graph.json for JainNav from the circular-campus sketch.

GEOMETRY (taken from the sketch, top-down view, north = up)
  * Every floor is a set of concentric rings around one centre.
  * The corridor is a circle (dashed line) between the inner-room ring and
    the outer-room ring.
  * Angles are bearings: 0 = top of the sketch, increasing CLOCKWISE.
  * Floors 1-4: full circular corridor.  Ground floor: only an ARC from SA
    (292.5) clockwise through SP (0) to SD (135); the amphitheatre fills the
    rest.

Coordinates are screen coordinates (x right, y down), same as v1, so the
frontend's bearing() function keeps working:  x = cx + r*sin(a),
y = cy - r*cos(a).
"""
import json, math

CX = CY = 700.0
MPP = 0.07                       # metres per pixel  (calibrate with a real measurement)
R_INNER_ROOM = 300.0
R_CORR = 450.0
R_OUTER_ROOM = 555.0
R_INNER_STAIR = 428.0            # stair mouth sits just inside the corridor line
R_OUTER_STAIR = 472.0            # ... or just outside it

FLOORS = [
    ('F0', 'Ground Floor', 0), ('F1', 'First Floor', 1), ('F2', 'Second Floor', 2),
    ('F3', 'Third Floor', 3), ('F4', 'Fourth Floor', 4),
]

# 16 outer sectors of 22.5 degrees, centre of sector k = 11.25 + 22.5*k.
# k=5 and k=13 are the hatched "fault space" sectors (no room).
def sector_angle(k):
    return 11.25 + 22.5 * k

# Staircases: (angle, side of corridor the stair opens from, floors served)
STAIRS = {
    'SP': (0.0,   'inner', [0, 1, 2, 3, 4]),
    'SQ': (67.5,  'inner', [0, 1, 2, 3, 4]),
    'SC': (112.5, 'outer', [0, 1, 2, 3, 4]),
    'SD': (135.0, 'outer', [0, 1, 2, 3, 4]),
    'SX': (180.0, 'inner', [1, 2, 3, 4]),
    'SY': (247.5, 'inner', [1, 2, 3, 4]),
    'SA': (292.5, 'outer', [0, 1, 2, 3, 4]),
    'SB': (315.0, 'outer', [0, 1, 2, 3, 4]),
}
LIFT_ANGLE = 123.75              # between SC (112.5) and SD (135)
LIFT_SIDE = 'outer'              # ASSUMPTION - sits in the same outer shaft sector as SC/SD
LIFT_IDS = {0: 'LG', 1: 'L1', 2: 'L2', 3: 'L3', 4: 'L4'}

# ---------------------------------------------------------------- rooms
# (number-or-label, name). number None => named space.  Sector index -> room.
# Inner ring: sectors 0,1,2,3,4,6,7,8,9,10,11,12,14,15 (same junction as outer k)
INNER_UPPER = {  # same positions on floors 1..4, numbered fl*100 + n
    0: 12, 1: 'HALL', 2: 1, 3: 2, 4: 3, 6: 4, 7: 5, 8: 6, 9: 'CORR',
    10: 7, 11: 8, 12: 9, 14: 10, 15: 11,
}

ROOMS = {
    0: {  # ---------------- ground
        'inner': {
            0: ('008', 'IQAC'),
            1: (None, 'Sofa Hall', 'SOFA HALL'),
            2: ('007', 'Vice President - JGI'),
            3: ('006', 'Office - 2'),
            4: ('005', 'Director - School of Computer Science'),
            14: ('010', 'Server Room'),
            15: ('009', 'Director - FET'),
        },
        'outer': {
            0: ('013', 'Examination Center / Office - 3'),
            1: ('001', 'Administrative Office'),
            2: ('002', 'Seminar Hall'),
            3: ('003', 'Office - 1'),
            4: ('004', 'Placement Office'),
            14: ('011', 'Chemistry Lab'),
            15: ('012', 'Physics Lab'),
        },
    },
    1: {
        'inner': {
            0: ('112', 'Lecture Hall'),
            1: (None, '1st Floor Hall', '1ST FLOOR HALL'),
            2: ('101', 'Lecture Hall'), 3: ('102', 'Lecture Hall'), 4: ('103', 'Lecture Hall'),
            6: ('104', 'Faculty Room'), 7: ('105', 'Name not listed on board'),
            8: ('106', 'Lecture Hall'),
            9: (None, '1st Floor Corridor', '1ST FLOOR CORRIDOR'),
            10: ('107', 'Lecture Hall'), 11: ('108', 'Lecture Hall'),
            12: ('109', 'Faculty Room'),
            14: ('110', 'Lecture Hall'), 15: ('111', 'Lecture Hall'),
        },
        'outer': {
            0: ('126', 'Marvin Minsky Lab / Guido van Rossum Lab'),
            1: ('127', 'Lecture Hall'), 2: ('113', 'Lecture Hall'),
            3: ('114', 'Lecture Hall'), 4: ('115', 'Lecture Hall'),
            6: ('116', 'Lecture Hall'),
            7: ('117', 'Geo Technical Lab'),
            8: ('118', 'Fluid Mechanics & Machinery Lab'),
            9: ('119+120', 'Heat & Mass Transfer Lab / FESEM-GCMS-XRD Lab / Environmental Lab'),
            10: ('121', 'Material Testing Lab'),
            11: ('122', 'Machine Shop'),
            12: ('123', 'Relay & High Voltage Lab'),
            14: ('124', 'Grace Hopper Lab / Margaret Hamilton Lab'),
            15: ('125', 'DevOps / Software Design & Testing Lab / John McCarthy Lab'),
        },
    },
    2: {
        'inner': {
            0: ('212', 'Lecture Hall'),
            1: (None, '2nd Floor Hall', '2ND FLOOR HALL'),
            2: ('201', 'Lecture Hall'), 3: ('202', 'Lecture Hall'), 4: ('203', 'Lecture Hall'),
            6: ('204', 'Lecture Hall'), 7: ('205', 'Lecture Hall'), 8: ('206', 'Lecture Hall'),
            9: (None, 'Library Corridor', 'LIBRARY CORRIDOR'),
            10: ('207', 'Lecture Hall'), 11: ('208', 'Lecture Hall'), 12: ('209', 'Lecture Hall'),
            14: ('210', 'Lecture Hall'), 15: ('211', 'Lecture Hall'),
        },
        'outer': {
            0: ('226', 'Program Head Cabins'),
            1: ('227', 'Faculty Room'),
            2: ('213', 'Lecture Hall'),
            3: ('214A/B/C', 'Lecture Hall'),
            4: ('215A/B/C', 'Lecture Hall'),
            6: ('216A/B', 'Lab'),
            7: ('217A/B', 'Research Lab / Faculty Room'),
            8: ('219A/B/C', 'NetSphere Lab / Kevin Ashton Lab / Apple iOS Lab'),
            9: (None, 'Library', 'LIBRARY (2ND FLOOR)'),
            10: ('221', 'Data Analytics & Learning Lab'),
            11: ('222', 'Workshop Practice Lab'),
            12: ('223', 'Membrane Lab / Bio-inspired Nanoplasmonics / Thermochromic Materials Lab'),
            14: ('224A/B', 'Alan Turing Lab / Sir Tim Berners-Lee Lab'),
            15: ('225A/B', 'Mobile Application Development Lab / Cloud Information Security Lab'),
        },
    },
    3: {
        'inner': {
            0: ('312', 'Lecture Hall'),
            1: (None, '3rd Floor Hall', '3RD FLOOR HALL'),
            2: ('301', 'Lecture Hall'), 3: ('302', 'Lecture Hall'), 4: ('303', 'Lecture Hall'),
            6: ('304', 'Lecture Hall'), 7: ('305', 'Lecture Hall'), 8: ('306', 'Lecture Hall'),
            9: (None, 'Library Seating Hall', 'LIB SEATING HALL'),
            10: ('307', 'Lecture Hall'), 11: ('308', 'Lecture Hall'), 12: ('309', 'Lecture Hall'),
            14: ('310', 'Lecture Hall'), 15: ('311', 'Lecture Hall'),
        },
        'outer': {
            0: ('326A/B', 'Lecture Hall'),
            1: ('327A/B', 'Lecture Hall'),
            2: ('313A/B', 'Lecture Hall'),
            3: ('314A/B', 'Lecture Hall'),
            4: ('315A/B', 'Fitness Center / Programming Lab'),
            6: ('316A/B', 'Programming Lab / Lecture Hall'),
            7: ('317A/B', 'Faculty Room'),
            8: ('318A/B', 'Store'),
            9: (None, 'Library', 'LIBRARY (3RD FLOOR)'),
            10: ('321', 'Lecture Hall'),
            11: ('322A/B/C', 'Lecture Hall'),
            12: ('323', 'Faculty Room'),
            14: ('324A/B', 'Network Database Lab / Faculty Room'),
            15: ('325', 'Faculty Room'),
        },
    },
    4: {
        'inner': {
            0: ('412', 'Lecture Hall'),
            1: (None, '4th Floor Hall', '4TH FLOOR HALL'),
            2: ('401', 'Board Room - CNMS'), 3: ('402', 'Office - CNMS'),
            4: ('403', 'Lecture Hall'),
            6: ('404', 'Director - CNMS'), 7: ('405', 'Faculty Room - CNMS'),
            8: ('406', 'Faculty Room - CNMS'),
            9: (None, '4th Floor Corridor', '4TH FLOOR CORRIDOR'),
            10: ('407', 'Name not listed'),
            11: ('408', 'Lecture Hall'),
            12: ('409', 'Faculty Room - CNMS'),
            14: ('410', 'Computational Materials and Computational Molecular Modeling Lab'),
            15: ('411', 'Lecture Hall'),
        },
        'outer': {
            0: ('435-436', 'Applied Electrochemistry Lab / 2D Quantum Materials Lab'),
            1: ('437-438', 'Fruits & Vegetables Technology Lab / Green Sustainable Catalysis Lab'),
            2: ('413-415', 'Functional Materials and Devices Lab / Dairy Technology Lab / Organometallics Lab'),
            3: ('416-418', 'Functional Particles and Surfaces Lab / Low Dimensional Material Lab / Catalysis & Organic Synthesis Lab'),
            4: ('419-420', 'Nanomedicine Lab / Cell Culture Lab'),
            6: ('421', 'Nano Catalysis and Drug Molecules Lab'),
            7: ('422', 'Nano Catalysis and Drug Molecules Lab'),
            8: ('423', 'Photo and Electro Catalysis Lab'),
            9: ('424-425', 'Photo and Electro Catalysis Lab / Reaction Networks and Soft Materials / Organoelectronics / Organic & Medicinal Chemistry'),
            10: ('426-427', 'Bioinorganic and Clinical Chemistry Lab / Organic and Inorganic Chemistry Lab'),
            11: ('428-429', 'Physical Chemistry Lab / Sustainable Energy Materials and Processes Lab'),
            12: ('430', 'Carbene Chemistry Lab'),
            14: ('431-432', 'Faculty Room - CNMS'),
            15: ('433-434', 'Faculty Room - CNMS / HoD & Faculty Room - Food Technology'),
        },
    },
}


def pt(angle, r):
    a = math.radians(angle)
    return round(CX + r * math.sin(a), 1), round(CY - r * math.cos(a), 1)


def aliases_for(number):
    """First alias is what the directions show; the rest only help search."""
    out = [number]
    import re
    m = re.fullmatch(r'(\d+)\+(\d+)', number) or re.fullmatch(r'(\d+)-(\d+)', number)
    if m:
        out += [m.group(1), m.group(2)]
    m = re.fullmatch(r'(\d+)([A-C](?:/[A-C])*)', number)
    if m:
        out.append(m.group(1))
        for letter in m.group(2).split('/'):
            out.append(m.group(1) + letter)
    return out


nodes, edges = [], []


def add_node(**kw):
    nodes.append(kw)
    return kw['id']


def add_edge(a, b, **kw):
    edges.append({'a': a, 'b': b, **kw})


for fid, fname, level in FLOORS:
    ring = []   # (angle, junction_id) for the corridor of this floor

    # ---- room junctions + rooms
    spec = ROOMS[level]
    for k in sorted(set(spec['inner']) | set(spec['outer'])):
        ang = sector_angle(k)
        jx, jy = pt(ang, R_CORR)
        jid = f'{fid}-J{k:02d}'
        add_node(id=jid, floor=fid, x=jx, y=jy, kind='junction')
        ring.append((ang, jid))
        for side, r in (('inner', R_INNER_ROOM), ('outer', R_OUTER_ROOM)):
            if k not in spec[side]:
                continue
            entry = spec[side][k]
            number, name = entry[0], entry[1]
            x, y = pt(ang, r)
            if number is not None:
                rid = f'{fid}-{number}'
                add_node(id=rid, floor=fid, x=x, y=y, kind='room', name=name,
                         aliases=aliases_for(number))
            else:
                label = entry[2]
                rid = f'{fid}-' + label.replace(' ', '_').replace('(', '').replace(')', '')
                add_node(id=rid, floor=fid, x=x, y=y, kind='landmark', name=name,
                         aliases=[label])
            add_edge(rid, jid, kind='door')

    # ---- staircases
    for sname, (ang, side, floors) in STAIRS.items():
        if level not in floors:
            continue
        jx, jy = pt(ang, R_CORR)
        jid = f'{fid}-J-{sname}'
        add_node(id=jid, floor=fid, x=jx, y=jy, kind='junction')
        ring.append((ang, jid))
        sx, sy = pt(ang, R_INNER_STAIR if side == 'inner' else R_OUTER_STAIR)
        sid = f'{fid}-{sname}'
        add_node(id=sid, floor=fid, x=sx, y=sy, kind='stair', name=f'Stairs {sname}',
                 group=sname, side=side)
        add_edge(jid, sid, kind='stairmouth')

    # ---- lift
    jx, jy = pt(LIFT_ANGLE, R_CORR)
    jid = f'{fid}-J-LIFT'
    add_node(id=jid, floor=fid, x=jx, y=jy, kind='junction')
    ring.append((LIFT_ANGLE, jid))
    lx, ly = pt(LIFT_ANGLE, R_INNER_STAIR if LIFT_SIDE == 'inner' else R_OUTER_STAIR)
    lid = LIFT_IDS[level]
    add_node(id=lid, floor=fid, x=lx, y=ly, kind='lift', name=f'Lift ({lid})',
             group='LIFT', side=LIFT_SIDE)
    add_edge(jid, lid, kind='stairmouth')

    # ---- corridor
    if level == 0:
        # Ground corridor is an OPEN ARC: SA (292.5) -> clockwise through SP (0) -> SD (135).
        # Order it starting at SA so no edge jumps across the amphitheatre.
        ring.sort(key=lambda t: (t[0] - 292.5) % 360)
    else:
        ring.sort()
    for (a1, j1), (a2, j2) in zip(ring, ring[1:]):
        add_edge(j1, j2, kind='corridor')
    if level != 0:                         # upper floors: ring closes
        add_edge(ring[-1][1], ring[0][1], kind='corridor')

# ---- vertical links (lower floor = a, upper = b)
for sname, (ang, side, floors) in STAIRS.items():
    for lo, hi in zip(floors, floors[1:]):
        add_edge(f'F{lo}-{sname}', f'F{hi}-{sname}', kind='stairs', step_free=False)
for lo in range(4):
    add_edge(LIFT_IDS[lo], LIFT_IDS[lo + 1], kind='lift', step_free=True)

graph = {
    'building': 'Jain Global Campus - Faculty of Engineering',
    'meters_per_pixel': MPP,
    'floors': [{'id': f, 'name': n, 'level': l, 'width': 1400, 'height': 1400,
                'centre': [CX, CY]} for f, n, l in FLOORS],
    'nodes': nodes,
    'edges': edges,
}
json.dump(graph, open('/home/claude/graph.json', 'w'), indent=1)
from collections import Counter
print(len(nodes), 'nodes', len(edges), 'edges', Counter(n['kind'] for n in nodes))
