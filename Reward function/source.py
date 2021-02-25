import math
def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']         # flag to indicate if the agent is on the track
    x = params['x']                                             # agent's x-coordinate in meters
    y = params['y']                                             # agent's y-coordinate in meters
    closest_objects = params['closest_objects']                 # zero-based indices of the two closest objects to the agent's current position of (x y).
    closest_waypoints = params['closest_waypoints']             # indices of the two nearest waypoints.
    distance_from_center = params['distance_from_center']       # distance in meters from the track center 
    is_crashed = params['is_crashed']                           # Boolean flag to indicate whether the agent has crashed.
    is_left_of_center = params['is_left_of_center']             # Flag to indicate if the agent is on the left side to the track center or not. 
    is_offtrack = params['is_offtrack']                         # Boolean flag to indicate whether the agent has gone off track.
    is_reversed = params['is_reversed']                         # flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
    heading = params['heading']                                 # agent's yaw in degrees
    objects_distance = params['objects_distance']               # list of the objects' distances in meters between 0 and track_length in relation to the starting line.
    objects_heading = params['objects_heading']                 # list of the objects' headings in degrees between -180 and 180.
    objects_left_of_center = params['objects_left_of_center']   # list of Boolean flags indicating whether elements' objects are left of the center (True) or not (False).
    objects_locationfloat = params['objects_locationfloat']     # list of object locations [(x,y) ...].
    objects_speed = params['objects_speed']                     # list of the objects' speeds in meters per second.
    progress = params['progress']                               # percentage of track completed
    speed = params['speed']                                     # agent's speed in meters per second (m/s)
    steering_angle = params['steering_angle']                   # agent's steering angle in degrees
    steps = params['steps']                                     # number steps completed
    track_length = params['track_length']                       # track length in meters.
    track_width = params['track_width']                         # width of the track
    waypointsfloat = params['waypointsfloat']                   # list of (x,y) as milestones along the track center
    
    
    # Read all 155 track coordinates (x,y) after racing lines optimization.
    racing_lines_coords = [[0.76561164, 2.79921096],
       [0.77433204, 2.695514  ],
       [0.7899877 , 2.59241502],
       [0.81253181, 2.49023377],
       [0.84155804, 2.38920145],
       [0.87670146, 2.28950824],
       [0.91814643, 2.19146346],
       [0.96598348, 2.09538003],
       [1.02110577, 2.00190733],
       [1.08483756, 1.91208936],
       [1.15889387, 1.82757667],
       [1.24544247, 1.75117454],
       [1.33865459, 1.67987295],
       [1.43751087, 1.61316408],
       [1.54114987, 1.55049121],
       [1.64906449, 1.49148807],
       [1.76077387, 1.43573189],
       [1.87582154, 1.38275015],
       [1.99379879, 1.33205039],
       [2.11442438, 1.28318436],
       [2.23741029, 1.23565791],
       [2.36252249, 1.18900726],
       [2.4895651 , 1.14282388],
       [2.61828891, 1.09677841],
       [2.74812923, 1.05069182],
       [2.87900506, 1.00439082],
       [3.00882722, 0.95892681],
       [3.13759114, 0.91473599],
       [3.26537475, 0.87215984],
       [3.39228501, 0.83154603],
       [3.51845045, 0.79324155],
       [3.64399906, 0.75760342],
       [3.76904579, 0.72500547],
       [3.89368577, 0.69584032],
       [4.01799202, 0.67049722],
       [4.14201662, 0.64930876],
       [4.26577987, 0.63273189],
       [4.38927914, 0.62123967],
       [4.51249029, 0.61526108],
       [4.63536749, 0.61516804],
       [4.75784381, 0.62127088],
       [4.87983294, 0.63381301],
       [5.0012315 , 0.65296781],
       [5.12192174, 0.67883876],
       [5.24177453, 0.71146186],
       [5.36065244, 0.75080957],
       [5.47841292, 0.79679602],
       [5.59491126, 0.84928294],
       [5.71000341, 0.90808645],
       [5.82354846, 0.97298407],
       [5.93541068, 1.0437221 ],
       [6.0454611 , 1.12002284],
       [6.15357859, 1.20159164],
       [6.25965028, 1.2881234 ],
       [6.36357148, 1.37930854],
       [6.46524502, 1.47483823],
       [6.56457998, 1.57440865],
       [6.66149006, 1.67772453],
       [6.75589138, 1.78450162],
       [6.84770001, 1.89446831],
       [6.93682919, 2.00736635],
       [7.02318639, 2.12295071],
       [7.1066703 , 2.24098868],
       [7.18716776, 2.36125827],
       [7.26455098, 2.483546  ],
       [7.33867494, 2.60764424],
       [7.40937528, 2.73334811],
       [7.47646688, 2.86045226],
       [7.53974339, 2.98874764],
       [7.59897815, 3.11801846],
       [7.65392713, 3.24803997],
       [7.70433455, 3.37857719],
       [7.7499424 , 3.50938546],
       [7.79050461, 3.64021332],
       [7.82580692, 3.77080829],
       [7.85569184, 3.90092577],
       [7.88008701, 4.03034055],
       [7.89903768, 4.15886077],
       [7.91272164, 4.28633872],
       [7.92128781, 4.41264156],
       [7.92447728, 4.53753961],
       [7.92201458, 4.66077418],
       [7.9133979 , 4.78198389],
       [7.89812233, 4.90076287],
       [7.87505235, 5.01638528],
       [7.8426419 , 5.12776564],
       [7.7991328 , 5.23341069],
       [7.74232044, 5.33103609],
       [7.66965414, 5.41671541],
       [7.58548525, 5.49133287],
       [7.49249755, 5.55565671],
       [7.39272914, 5.61057946],
       [7.28774798, 5.65703448],
       [7.17863584, 5.69567517],
       [7.06626291, 5.72714099],
       [6.95119881, 5.75168914],
       [6.83392084, 5.76948952],
       [6.71479951, 5.7804432 ],
       [6.59428145, 5.78486017],
       [6.4727123 , 5.78280876],
       [6.35041564, 5.77438996],
       [6.22767817, 5.75942619],
       [6.10480484, 5.73778469],
       [5.98210522, 5.70948046],
       [5.8598719 , 5.67464525],
       [5.73836377, 5.63350386],
       [5.61779372, 5.58636238],
       [5.49831957, 5.53359894],
       [5.38003826, 5.47565588],
       [5.26298308, 5.41303344],
       [5.1471238 , 5.34628486],
       [5.0323693 , 5.27601209],
       [4.91857262, 5.20286181],
       [4.80553743, 5.12752246],
       [4.69302581, 5.05072246],
       [4.5807927 , 4.97315917],
       [4.47306546, 4.89888131],
       [4.36498285, 4.8253982 ],
       [4.25624758, 4.75337765],
       [4.14656401, 4.68348892],
       [4.03567359, 4.6163249 ],
       [3.92335987, 4.55239151],
       [3.80945274, 4.49209756],
       [3.69383179, 4.43574605],
       [3.57642813, 4.38352817],
       [3.45722493, 4.33552102],
       [3.33625638, 4.29168982],
       [3.21360565, 4.25189567],
       [3.08940208, 4.21590815],
       [2.96381787, 4.18342069],
       [2.83706273, 4.15406719],
       [2.70937306, 4.12743907],
       [2.58099653, 4.10308575],
       [2.45215177, 4.08057666],
       [2.32301465, 4.05949102],
       [2.19837845, 4.03803371],
       [2.07480715, 4.01517768],
       [1.95267174, 3.99042323],
       [1.83230451, 3.96331844],
       [1.71408912, 3.93334796],
       [1.59845849, 3.8999487 ],
       [1.48596082, 3.86244333],
       [1.37725893, 3.82007563],
       [1.27302755, 3.77217454],
       [1.1744859 , 3.71757033],
       [1.08316271, 3.65504353],
       [1.00170501, 3.58283771],
       [0.93490907, 3.49914189],
       [0.88109283, 3.40790169],
       [0.83879464, 3.31160766],
       [0.80687151, 3.21193203],
       [0.78431647, 3.11008729],
       [0.77046979, 3.00693713],
       [0.76440624, 2.9031572 ],
       [0.76561164, 2.79921096]]

    # Calculate the min distance from the racing lines coords
    min_distance_obj = calc_min_distance_from_closest_point(x, y, racing_lines_coords)

    # Calculate 4 markers that are at varying distances away from the closest raceing line point
    marker_1 = 0.09 
    marker_2 = 0.15 
    marker_3 = 0.25
    marker_4 = 0.5 
    
    # Give higher reward if the car is closer to raceing line point and vice versa
    if min_distance_obj["value"] <= marker_1:
        reward = 1.0
    elif min_distance_obj["value"] <= marker_2:
        reward = 0.7
    elif min_distance_obj["value"] <= marker_3:
        reward = 0.4
    elif min_distance_obj["value"] <= marker_4:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track
    
    return float(reward)

def calc_min_distance_from_closest_point(curr_x, curr_y, racing_lines_coords):
    # Calculate distance d²=(x1-x2)² + (y1-y2)²
    min_distance_from_current_coord = math.inf
    index_min_distance_from_current_coord = 0
    for index, [x,y] in enumerate(racing_lines_coords):
        distance = (((curr_x - x)**2) + ((curr_y - y)**2))**0.5
        if distance < min_distance_from_current_coord:
            min_distance_from_current_coord = distance
            index_min_distance_from_current_coord = index

    return {"index": index_min_distance_from_current_coord, "value":min_distance_from_current_coord}
         


