''' Implement an AI to play tetris '''
from random import Random
from te_settings import Direction, MAXROW, MAXCOL

class AutoPlayer():
    ''' A very simple dumb AutoPlayer controller '''
    def __init__(self, controller):
        self.controller = controller
        self.rand = Random()
        self.solved_type = None;
        self.angle = None;
        self.x = None;
        self.need_solve = True;

    def next_move(self, gamestate):
        ''' next_move() is called by the game, once per move.
            gamestate supplies access to all the state needed to autoplay the game.'''
        '''self.random_next_move(gamestate)'''
        clone = gamestate.clone(True);
        if (self.need_solve == True):
            self.need_solve = False;
            (self.x, self.angle) = self.solve_next_move(gamestate);
            #print("executing x = ", str(self.x) + " angle = " + str(self.angle) + "\n");
            self.solved_type = gamestate.get_falling_block_type();
            #print("solved_type = " + str(self.solved_type) + "\n");
        if (clone.update() == True):
            gamestate.update();
            self.need_solve = True;
        now_angle = gamestate.get_falling_block_angle();
        (now_x, now_y) = gamestate.get_falling_block_position();
        if (now_angle < self.angle):
            gamestate.rotate(Direction.RIGHT);
        elif (now_angle > self.angle):
            gamestate.rotate(Direction.LEFT);
        if (now_x < self.x):
            gamestate.move(Direction.RIGHT);
        elif (now_x > self.x):
            gamestate.move(Direction.LEFT);
        #print(gamestate.get_score());
        #gamestate.update();
        #raise Exception ("STOP!");


    def random_next_move(self, gamestate):
        ''' make a random move and a random rotation.  Not the best strategy! '''
        rnd = self.rand.randint(-1, 1)
        if rnd == -1:
            direction = Direction.LEFT
        elif rnd == 1:
            direction = Direction.RIGHT
        if rnd != 0:
            gamestate.move(direction)
        rnd = self.rand.randint(-1, 1)
        if rnd == -1:
            direction = Direction.LEFT
        elif rnd == 1:
            direction = Direction.RIGHT
        if rnd != 0:
            gamestate.rotate(direction)
        gamestate.print_block_tiles()

    def solve_next_move(self, gamestate):
        x, angle = self.iterate_all_possibilities(gamestate);
        return x, angle;
        # raise Exception("STOP!");

    def iterate_all_possibilities(self, gamestate):
        max_score = -100000000;
        tmp_type = gamestate.get_falling_block_type();
        '''optimisation for block types'''
        if (tmp_type == "I"):
            optimise = 2;
        elif (tmp_type == "O"):
            optimise = 1;
        elif (tmp_type == "S"):
            optimise = 2;
        elif (tmp_type == "Z"):
            optimise = 2;
        else:
            optimise = 4;
        for angle in range(0, optimise):
            '''some weird offset for x'''
            if (tmp_type == "O"):
                fix = -1;
            elif (angle == 1):
                if (tmp_type == "I"):
                    fix = -2;
                else:
                    fix = -1;
            else:
                fix = 0;
            # print("fix =" + str(fix) + "\n");
            width = 0;
            if (tmp_type == "I"):
                if (angle == 0):
                    width = 4;
                else:
                    width = 1;
            elif (tmp_type == "O"):
                width = 2;
            elif (tmp_type == "J"):
                if (angle == 0):
                    width = 3;
                elif (angle == 1):
                    width = 2;
                elif (angle == 2):
                    width = 3;
                else:
                    width = 2;
            elif (tmp_type == "L"):
                if (angle == 0) or (angle == 2):
                    width = 3;
                else:
                    width = 2;
            elif (tmp_type == "S"):
                if (angle == 0) or (angle == 2):
                    width = 3;
                else:
                    width = 2;
            elif (tmp_type == "T"):
                if (angle == 0) or (angle == 2):
                    width = 3;
                else:
                    width = 2;
            elif (tmp_type == "Z"):
                if (angle == 0) or (angle == 2):
                    width = 3;
                else:
                    width = 2;
            '''not a clean implementation but works for this'''
            for x in range(fix, MAXCOL - width + fix + 1):
                # print("x = " + str(x) + "\n");
                clone = gamestate.clone(True);
                #clone.print_block_tiles();
                current_angle = clone.get_falling_block_angle();
                (current_x, current_y) = clone.get_falling_block_position();
                check = False;
                while (current_angle != angle):
                    if (current_angle < angle):
                        clone.rotate(Direction.RIGHT);
                    else:
                        clone.rotate(Direction.LEFT);
                    check = clone.update();
                    if (check == True):
                        break;
                    current_angle = clone.get_falling_block_angle();
                cannot_move_here = False;
                while (current_x != x) and (check == False):
                    prev_x = current_x;
                    if (current_x > x):
                        clone.move(Direction.LEFT);
                    elif (current_x < x):
                        clone.move(Direction.RIGHT);
                    check = clone.update();
                    if (check == True):
                        break;
                    (current_x, current_y) = clone.get_falling_block_position();
                    if (prev_x == current_x):
                        cannot_move_here = True;
                        break;
                if (cannot_move_here == True):
                    continue;
                #print("gamestate_type = " + str(tmp_type) + "\n");
                tmp_type = clone.get_falling_block_type();
                #print(str(clone.get_falling_block_type()) + " " + str(clone.get_falling_block_angle()) + " " + str(clone.get_falling_block_position()));
                # done with turning and positioning
                if (x + 5 < MAXCOL):
                    x_test = x + 5;
                else:
                    x_test = x - 5;
                tile_map = clone.get_tiles();
                y = 0;
                while (y < MAXROW) and (tile_map[y][x_test] == 0):
                    y += 1;
                x_test_height = MAXROW - y;
                #print("test height is" + str(x_test_height));
                while (check == False):
                    check = clone.update();
                    if (check == True):
                        break;
                tile_map = clone.get_tiles();
                y = 0;
                while (y < MAXROW) and (tile_map[y][x_test] == 0):
                    y += 1;
                x_test_new_height = MAXROW - y;
                #print("new test height is" + str(x_test_new_height));
                complete_lines = x_test_height - x_test_new_height;
                if (complete_lines < 0):
                    complete_lines = 0;
                #clone.print_tiles();
                tile_map = clone.get_tiles();
                #print(tmp_type);
                total_complete_lines = complete_lines;
                score = self.score_tile_map(tile_map, total_complete_lines);
                # print(score);
                # print("gamesate_type = " + str(gamestate.get_falling_block_type()) +  " tmp_type " + str(tmp_type) + "\n" );
                if (score > max_score):
                    max_score = score;
                    best_x = x;
                    best_angle = angle;
                    #cclone.print_tiles();
                    #print("-----------------BEST---------------");
                    # print(max_score, best_x, best_angle);
                    # print("---------------END----------------");
        return best_x, best_angle;

    def score_tile_map(self, tiles, total_complete_lines):
        height = [];
        for x in range (0, MAXCOL):
            y = 0;
            while (y < MAXROW) and (tiles[y][x] == 0):
                y += 1;
            height.append(MAXROW - y);
        avg_height = 0;
        for i in height:
            avg_height += i;
        avg_height += total_complete_lines * MAXCOL;
        # average height
        bump = 0;
        for i in range (1, MAXCOL):
            bump += abs(height[i] - height[i - 1]);
        # calculate bumpiness
        holes = 0;
        for x in range (0, MAXCOL):
            for y in range (0, MAXROW):
                #print("y = " + str(y) + " x = " + str(x));
                if (tiles[y][x] != 0):
                    #print("Found a block!! at " + str(x) + str(y));
                    for yy in range (y + 1, MAXROW):
                        if (tiles[yy][x] == 0):
                            holes += 1;
                            #print("HOLE at " + str(yy) + " " + str(x));
                    break;
        # calculate holes
        '''complete_lines = 0;
        for y in range (0, MAXROW):
            flag = True;
            for x in range (0, MAXCOL):
                if (tiles[y][x] == 0):
                    flag = False;
                    break;
            if (flag == True):
                complete_lines += 1;
         complete lines'''
        #if (complete_lines > 0):
        #    raise Exception("FOUND!");
        a = -0.510066;
        b = 0.760666;
        c = -0.35663;
        d = -0.184483;
        # const results from Tetris.AI
        if (total_complete_lines < 0):
            total_complete_lines = 0;
        #print(avg_height, total_complete_lines, holes, bump);
        score = avg_height * a + total_complete_lines * b + holes * c + bump * d;
        #print(score);
        return score;
