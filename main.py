import pygame

WIDTH = 710
HEIGHT = 610


class Wall(pygame.sprite.Sprite):
    def __init__(self, position_x, position_y, w, h, color):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([w, h])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.top = position_y
        self.rect.left = position_x


class Food(pygame.sprite.Sprite):
    def __init__(self, position_x, position_y, w, h, color, bg_color):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([w, h])
        self.image.fill(bg_color)
        self.image.set_colorkey(bg_color)

        pygame.draw.ellipse(self.image, color, [0, 0, w, h])
        self.rect = self.image.get_rect()
        self.rect.left = position_x
        self.rect.top = position_y


class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0

    def __init__(self, x, y, file_name):
        pygame.sprite.Sprite.__init__(self)

        self.role_name = file_name.split(".")[0]
        self.base_image = pygame.image.load(file_name).convert()
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()

        self.rect.left = x
        self.rect.top = y
        self.prev_x = x
        self.prev_y = y
        self.is_move = False

        self.speed = [0, 0]
        self.base_speed = [30, 30]

        self.tracks = []
        self.tracks_loc = [0, 0]

    def move(self, direction):
        if direction[0] < 0:
            self.image = pygame.transform.flip(self.base_image, True, False)
        elif direction[0] > 0:
            self.image = self.base_image.copy()
        elif direction[1] < 0:
            self.image = pygame.transform.rotate(self.base_image, 90)
        elif direction[1] > 0:
            self.image = pygame.transform.rotate(self.base_image, -90)

        self.speed = [direction[0] * self.base_speed[0], direction[1] * self.base_speed[1]]
        return self.speed

    def update(self, wall_sprites, gate_sprites):
        if not self.is_move:
            return False

        x_prev = self.rect.left
        y_prev = self.rect.top

        self.rect.left += self.speed[0]
        self.rect.top += self.speed[1]

        is_collide = pygame.sprite.spritecollide(self, wall_sprites, False)

        if gate_sprites is not None:
            if not is_collide:
                is_collide = pygame.sprite.spritecollide(self, gate_sprites, False)
        if is_collide:
            self.rect.left = x_prev
            self.rect.top = y_prev
            return False
        return True


class Game:
    def __init__(self):
        self.wall = pygame.sprite.Group()
        self.gate = pygame.sprite.Group()

        self.food = pygame.sprite.Group()

        self.hero = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()

    def walls(self):
        wall_positions = [[0, 0, 6, 600], [0, 0, 600, 6], [0, 600, 606, 6], [600, 0, 6, 606], [300, 0, 6, 66],
                          [60, 60, 186, 6], [360, 60, 186, 6], [60, 120, 66, 6], [60, 120, 6, 126], [180, 120, 246, 6],
                          [300, 120, 6, 66], [480, 120, 66, 6], [540, 120, 6, 126], [120, 180, 126, 6],
                          [120, 180, 6, 126], [360, 180, 126, 6], [480, 180, 6, 126], [180, 240, 6, 126],
                          [180, 360, 246, 6], [420, 240, 6, 126], [240, 240, 42, 6], [324, 240, 42, 6],
                          [240, 240, 6, 66], [240, 300, 126, 6], [360, 240, 6, 66], [0, 300, 66, 6], [540, 300, 66, 6],
                          [60, 360, 66, 6], [60, 360, 6, 186], [480, 360, 66, 6], [540, 360, 6, 186],
                          [120, 420, 366, 6], [120, 420, 6, 66], [480, 420, 6, 66], [180, 480, 246, 6],
                          [300, 480, 6, 66], [120, 540, 126, 6], [360, 540, 126, 6]]

        for i in wall_positions:
            w = Wall(i[0], i[1], i[2], i[3], (0, 255, 250))
            self.wall.add(w)
        return self.wall

    def gates(self):
        self.gate.add(Wall(282, 242, 42, 2, (255, 255, 255)))
        return self.gate

    def foods(self, food_color, bg_color):
        for row in range(20):
            for col in range(20):
                if (row == 7 or row == 8) and (col == 8 or col == 9 or col == 10):
                    continue
                else:
                    food = Food(30 * col + 32, 30 * row + 32, 4, 4, food_color, bg_color)

                    is_collide = pygame.sprite.spritecollide(food, self.wall, False)
                    if is_collide:
                        continue
                    self.food.add(food)
        return self.food

    def players(self, hero_image_path, ghost_images_path):
        self.hero.add(Player(287, 439, hero_image_path))

        for each in ghost_images_path:
            role_name = each.split(".")[0]

            if role_name == 'Blinky':
                player = Player(287, 199, each)
                player.is_move = True
                player.tracks = [[0, -0.5, 4], [0.5, 0, 9], [0, 0.5, 11], [0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 11],
                                 [0, 0.5, 3], [0.5, 0, 15], [0, -0.5, 15], [0.5, 0, 3], [0, -0.5, 11], [-0.5, 0, 3],
                                 [0, -0.5, 11], [-0.5, 0, 3], [0, -0.5, 3], [-0.5, 0, 7], [0, -0.5, 3], [0.5, 0, 15],
                                 [0, 0.5, 15], [-0.5, 0, 3], [0, 0.5, 3], [-0.5, 0, 3], [0, -0.5, 7], [-0.5, 0, 3],
                                 [0, 0.5, 7], [-0.5, 0, 11], [0, -0.5, 7], [0.5, 0, 5]]
                self.ghosts.add(player)

            elif role_name == 'Clyde':
                player = Player(319, 259, each)
                player.is_move = True
                player.tracks = [[-1, 0, 2], [0, -0.5, 4], [0.5, 0, 5], [0, 0.5, 7], [-0.5, 0, 11], [0, -0.5, 7],
                                 [-0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 7], [0, 0.5, 15], [0.5, 0, 15], [0, -0.5, 3],
                                 [-0.5, 0, 11], [0, -0.5, 7], [0.5, 0, 3], [0, -0.5, 11], [0.5, 0, 9]]
                self.ghosts.add(player)

            elif role_name == 'Inky':
                player = Player(255, 259, each)
                player.is_move = True
                player.tracks = [[1, 0, 2], [0, -0.5, 4], [0.5, 0, 10], [0, 0.5, 7], [0.5, 0, 3], [0, -0.5, 3],
                                 [0.5, 0, 3], [0, -0.5, 15], [-0.5, 0, 15], [0, 0.5, 3], [0.5, 0, 15], [0, 0.5, 11],
                                 [-0.5, 0, 3], [0, -0.5, 7], [-0.5, 0, 11], [0, 0.5, 3], [-0.5, 0, 11], [0, 0.5, 7],
                                 [-0.5, 0, 3], [0, -0.5, 3], [-0.5, 0, 3], [0, -0.5, 15], [0.5, 0, 15], [0, 0.5, 3],
                                 [-0.5, 0, 15], [0, 0.5, 11], [0.5, 0, 3], [0, -0.5, 11], [0.5, 0, 11], [0, 0.5, 3],
                                 [0.5, 0, 1]]
                self.ghosts.add(player)

            elif role_name == 'Pinky':
                player = Player(287, 259, each)
                player.is_move = True
                player.tracks = [[0, -1, 4], [0.5, 0, 9], [0, 0.5, 11], [-0.5, 0, 23], [0, 0.5, 7], [0.5, 0, 3],
                                 [0, -0.5, 3], [0.5, 0, 19], [0, 0.5, 3], [0.5, 0, 3], [0, 0.5, 3], [0.5, 0, 3],
                                 [0, -0.5, 15], [-0.5, 0, 7], [0, 0.5, 3], [-0.5, 0, 19], [0, -0.5, 11], [0.5, 0, 9]]
                self.ghosts.add(player)
        return self.hero, self.ghosts


def start_game(game, screen, font):
    score = 0
    clock = pygame.time.Clock()
    wall = game.walls()
    gate = game.gates()
    hero_sprites, ghost_sprites = game.players("pacman.png", ["Blinky.png", "Clyde.png", "Inky.png", "Pinky.png"])
    food = game.foods((255, 255, 0), (0, 0, 0))

    is_run = True
    while is_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    for hero in hero_sprites:
                        hero.move([0, -1])
                        hero.is_move = True
                elif event.key == pygame.K_DOWN:
                    for hero in hero_sprites:
                        hero.move([0, 1])
                        hero.is_move = True
                elif event.key == pygame.K_LEFT:
                    for hero in hero_sprites:
                        hero.move([-1, 0])
                        hero.is_move = True
                elif event.key == pygame.K_RIGHT:
                    for hero in hero_sprites:
                        hero.move([1, 0])
                        hero.is_move = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    hero.is_move = False
        screen.fill((0, 0, 0))

        for hero in hero_sprites:
            hero.update(wall, gate)
        hero_sprites.draw(screen)

        for hero in hero_sprites:
            food_eat = pygame.sprite.spritecollide(hero, food, True)
        score += len(food_eat)

        wall.draw(screen)
        gate.draw(screen)
        food.draw(screen)

        for ghost in ghost_sprites:
            if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
                ghost.move(ghost.tracks[ghost.tracks_loc[0]][0: 2])
                ghost.tracks_loc[1] += 1
            else:
                if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
                    ghost.tracks_loc[0] += 1
                elif ghost.role_name == 'Clyde':
                    ghost.tracks_loc[0] = 2
                else:
                    ghost.tracks_loc[0] = 0
                ghost.move(ghost.tracks[ghost.tracks_loc[0]][0: 2])
                ghost.tracks_loc[1] = 0

            if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
                ghost.move(ghost.tracks[ghost.tracks_loc[0]][0: 2])
            else:
                if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
                    loc_1 = ghost.tracks_loc[0] + 1
                elif ghost.role_name == 'Clyde':
                    loc_1 = 2
                else:
                    loc_1 = 0
                ghost.move(ghost.tracks[loc_1][0: 2])
            ghost.update(wall, None)
        ghost_sprites.draw(screen)

        score_text = font.render("Score: %s" % score, True, (255, 0, 0))
        screen.blit(score_text, [620, 10])

        if len(food) == 0:
            is_run = True
            break
        if pygame.sprite.groupcollide(hero_sprites, ghost_sprites, False, False):
            is_run = False
            break
        pygame.display.flip()
        clock.tick(10)
    return is_run


def text(screen, font, is_clearance, flag):
    clock = pygame.time.Clock()
    msg = "Game Over!"
    positions = [[235, 233], [65, 303], [170, 333]] if not is_clearance else [[235, 233], [65, 303], [170, 333]]

    texts = [font.render(msg, True, (255, 0, 0)),
             font.render('Press ENTER to continue or play again.', True, (255, 0, 0)),
             font.render('Press ESCAPE to quit.', True, (255, 0, 0))]

    is_ran = True
    while is_ran:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_ran = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if is_clearance:
                        if flag:
                            return
                        else:
                            main()
                    else:
                        main()

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit(-1)

        for idx, (text, position) in enumerate(zip(texts, positions)):
            screen.blit(text, position)
        pygame.display.flip()
        clock.tick(10)
        pygame.display.update()


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pakman")

    #  pygame.mixer.init()
    #  pygame.mixer.music.load("pacman_sound.ogg")
    #  pygame.mixer.music.play(-1, 0.0)

    pygame.font.init()
    font_small = pygame.font.SysFont("arial", 20)
    font_big = pygame.font.SysFont("arial", 35)

    num_score = 1
    for i in range(1, num_score + 1):
        if i == 1:
            game = Game()
            is_clearance = start_game(game, screen, font_small)
            if num_score == num_score:
                text(screen, font_big, is_clearance, True)
            else:
                text(screen, font_big, is_clearance)


if __name__ == "__main__":
    main()
